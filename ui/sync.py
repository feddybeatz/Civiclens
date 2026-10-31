"""Sync official Kenyan budget documents into data/pdfs.

    python sync.py          # download new documents (up to 8 per source)
    python sync.py 25       # allow up to 25 new documents per source
    python ingest.py        # then rebuild the search index

Safe to re-run: documents that are already downloaded are skipped.
Scanned PDFs (no text layer) are moved to data/scanned/ for later OCR.
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys
import time
from datetime import datetime
from urllib import robotparser
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import pymupdf
import requests
from bs4 import BeautifulSoup

# Put a real contact address here so site owners can reach you.
USER_AGENT = "CivicLens/0.1 (civic budget explainer; contact: CHANGE-ME@example.com)"

# --- What to sync ----------------------------------------------------------
# kind "pdf_links": the page links straight to PDF files.
# kind "links":     the page links to document pages; each is opened to find the file.
# kind "bajeti_national": the national document list, by category.
# include / exclude are case-insensitive regexes matched against the title.
SOURCES = [
    {"name": "Parliament: 2026-27 budget documents", "kind": "pdf_links",
     "url": "https://parliament.go.ke/2026-2027-budget-documents",
     "exclude": r"Hansard|Order Paper"},
    {"name": "Treasury: budget books (recent years, readable volumes)", "kind": "pdf_links",
     "url": "https://www.treasury.go.ke/budget-books",
     "include": r"2025[-/]26|2024[-/]25",
     "exclude": r"Development|Recurrent|Supplementary"},
    {"name": "CRA: revenue sharing and county budget reports", "kind": "links",
     "url": "https://cra.go.ke/downloads/",
     "link_pattern": r"cra\.go\.ke/download/[^/?#]+/?$",
     "include": r"recommendation|popular version|review report|division of revenue|allocation of revenue"},
    {"name": "Bajeti Yetu: recent uploads", "kind": "links",
     "url": "https://bajetiyetu.treasury.go.ke/",
     "link_pattern": r"document-libraries/preview\?id=\d+"},
    {"name": "Bajeti Yetu: national documents", "kind": "bajeti_national",
     "url": "https://bajetiyetu.treasury.go.ke/document-libraries/list?type=nat",
     # 1 Mwananchi guide, 2 Acts, 3 BROP, 4 Budget speech, 5 Budget summary,
     # 6 Revenue estimates, 9 Quarterly review, 11 Statistical annex, 14 Budget Policy Statement
     "categories": [1, 2, 3, 4, 5, 6, 9, 11, 14]},
]

DATA = pathlib.Path("data")
PDFS, SCANNED, DEBUG = DATA / "pdfs", DATA / "scanned", DATA / "debug"
SOURCES_JSON, CATALOG_JSON = DATA / "sources.json", DATA / "catalog.json"
LAST_SYNC = DATA / "last_sync.txt"

DELAY_SECONDS = 1.5
MAX_MB = 40
MAX_NEW_PER_SOURCE = int(sys.argv[1]) if len(sys.argv) > 1 else 8

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT
_robots: dict = {}


# --- Polite fetching -------------------------------------------------------
def allowed(url: str) -> bool:
    p = urlparse(url)
    root = f"{p.scheme}://{p.netloc}"
    if root not in _robots:
        rp = robotparser.RobotFileParser()
        try:
            r = session.get(root + "/robots.txt", timeout=20)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            rp.parse([])
        rp.modified()  # without this, can_fetch() refuses everything
        _robots[root] = rp
    return _robots[root].can_fetch(USER_AGENT, url)


def get(url: str, **kwargs):
    if not allowed(url):
        print(f"  skipped (robots.txt): {url}")
        return None
    time.sleep(DELAY_SECONDS)
    try:
        r = session.get(url, timeout=60, **kwargs)
        r.raise_for_status()
        return r
    except requests.RequestException as e:
        print(f"  request failed: {url} ({e})")
        return None


def fetch_pdf(url: str):
    r = get(url, stream=True)
    if r is None:
        return None
    size, chunks = 0, []
    for chunk in r.iter_content(1 << 16):
        size += len(chunk)
        if size > MAX_MB * 1024 * 1024:
            r.close()
            print(f"  skipped (over {MAX_MB} MB): {url}")
            return None
        chunks.append(chunk)
    return b"".join(chunks)


# --- Small helpers ---------------------------------------------------------
def norm_key(url: str) -> str:
    p = urlparse(url)
    return p.netloc.removeprefix("www.") + p.path + (("?" + p.query) if p.query else "")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:70] or "document"


def clean_title(text: str) -> str:
    text = re.sub(r"Download\s*\([^)]*\)", " ", text or "")
    text = re.sub(r"^\s*\d+\s+", "", text)
    return " ".join(text.split())


def filename(item: dict) -> str:
    h = hashlib.sha1(norm_key(item["page_url"]).encode()).hexdigest()[:6]
    return f"{slug(item['title'])}-{h}.pdf"


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


# --- Finding documents on pages -------------------------------------------
def extract_pdf_links(html: str, base: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    seen, items = set(), []
    for a in soup.find_all("a", href=True):
        url = urljoin(base, a["href"])
        if not re.search(r"\.pdf($|[?#])", url, re.I):
            continue
        key = norm_key(url)
        if key in seen:
            continue
        seen.add(key)
        row = a.find_parent("tr")  # table rows carry the description
        title = clean_title((row or a).get_text(" "))
        if len(title) < 5:
            title = unquote(pathlib.PurePosixPath(urlparse(url).path).stem)
        items.append({"title": title, "page_url": url, "file_url": url})
    return items


def extract_links(html: str, base: str, pattern: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    seen, items = set(), []
    for a in soup.find_all("a", href=True):
        url = urljoin(base, a["href"])
        if not re.search(pattern, url) or url in seen:
            continue
        title = clean_title(a.get("title") or a.get_text(" "))
        if len(title) < 5:
            continue
        seen.add(url)
        items.append({"title": title, "page_url": url, "file_url": None})
    return items


_STRONG = re.compile(r"\.pdf($|[?#])|wpdmdl=", re.I)
_WEAK = re.compile(r"download|/file", re.I)


def find_file_url(html: str, base: str):
    """Find the real file link on a document page."""
    soup = BeautifulSoup(html, "html.parser")
    cands = []
    for tag, attr in (("iframe", "src"), ("embed", "src"), ("object", "data"),
                      ("a", "href"), ("a", "data-downloadurl"),
                      ("button", "data-downloadurl")):
        for el in soup.find_all(tag):
            if el.get(attr):
                cands.append(urljoin(base, el[attr]))
    cands += [urljoin(base, m) for m in
              re.findall(r"""["']([^"'\s]+\.pdf[^"'\s]*)["']""", html, re.I)]
    resolved = []
    for url in cands:
        q = parse_qs(urlparse(url).query)
        if "file" in q:  # pdf.js style: viewer?file=<encoded url>
            url = urljoin(base, unquote(q["file"][0]))
        resolved.append(url)
    for pattern in (_STRONG, _WEAK):
        for url in resolved:
            if url != base and pattern.search(url):
                return url
    return None


def filter_items(items: list[dict], src: dict) -> list[dict]:
    seen, out = set(), []
    for it in items:
        key = norm_key(it["page_url"])
        if key in seen:
            continue
        seen.add(key)
        if src.get("include") and not re.search(src["include"], it["title"], re.I):
            continue
        if src.get("exclude") and re.search(src["exclude"], it["title"], re.I):
            continue
        out.append(it)
    return out


def discover(src: dict) -> list[dict]:
    r = get(src["url"])
    if r is None:
        return []
    base = src["url"]
    if src["kind"] == "pdf_links":
        items = extract_pdf_links(r.text, base)
    elif src["kind"] == "links":
        items = extract_links(r.text, base, src["link_pattern"])
    elif src["kind"] == "bajeti_national":
        items = []
        for cat in extract_links(r.text, base, r"[?&]cat=\d+"):
            n = int(re.search(r"[?&]cat=(\d+)", cat["page_url"]).group(1))
            if n in src["categories"]:
                page = get(cat["page_url"])
                if page is not None:
                    items += extract_links(page.text, cat["page_url"],
                                           r"document-libraries/preview\?id=\d+")
    else:
        items = []
    items = filter_items(items, src)
    print(f"  found {len(items)} candidate documents")
    return items


# --- Downloading -----------------------------------------------------------
def has_text(path: pathlib.Path) -> bool:
    try:
        with pymupdf.open(path) as doc:
            return any(doc[i].get_text().strip() for i in range(min(5, len(doc))))
    except Exception:
        return False


def process(item: dict, fn: str, source_name: str, catalog: dict, sources: dict) -> str:
    file_url, data = item["file_url"], None
    if file_url is None:
        r = get(item["page_url"])
        if r is None:
            return "failed"
        if r.content[:5] == b"%PDF":
            data = r.content
        else:
            file_url = find_file_url(r.text, item["page_url"])
            if not file_url:
                dump = DEBUG / (slug(item["title"]) + ".html")
                dump.write_text(r.text)
                print(f"  no file link found for '{item['title'][:60]}' (page saved to {dump})")
                return "no-file-url"
    if data is None:
        data = fetch_pdf(file_url)
    if not data or data[:5] != b"%PDF":
        print(f"  not a PDF, skipped: {item['title'][:60]}")
        return "failed"

    path = PDFS / fn
    path.write_bytes(data)
    catalog[fn] = {"title": item["title"], "source": source_name,
                   "url": item["page_url"], "file_url": file_url,
                   "fetched": datetime.now().date().isoformat()}
    sources[fn] = item["page_url"]
    if not has_text(path):
        shutil.move(str(path), SCANNED / fn)
        print(f"  scanned/unreadable, moved to data/scanned: {item['title'][:60]}")
        return "scanned"
    print(f"  saved: {item['title'][:70]} ({len(data) // 1024} KB)")
    return "ok"


def main() -> None:
    for d in (PDFS, SCANNED, DEBUG):
        d.mkdir(parents=True, exist_ok=True)
    catalog, sources = load_json(CATALOG_JSON), load_json(SOURCES_JSON)
    totals = {"ok": 0, "scanned": 0, "failed": 0, "no-file-url": 0, "already have": 0}
    try:
        for src in SOURCES:
            print(f"\n== {src['name']}")
            attempted = 0
            for item in discover(src):
                fn = filename(item)
                if (PDFS / fn).exists() or (SCANNED / fn).exists():
                    totals["already have"] += 1
                    continue
                if attempted >= MAX_NEW_PER_SOURCE:
                    print(f"  limit of {MAX_NEW_PER_SOURCE} new documents reached; run again for more")
                    break
                attempted += 1
                totals[process(item, fn, src["name"], catalog, sources)] += 1
    finally:
        SOURCES_JSON.write_text(json.dumps(sources, indent=2))
        CATALOG_JSON.write_text(json.dumps(catalog, indent=2))
        LAST_SYNC.write_text(datetime.now().isoformat(timespec="minutes"))
    print("\nSummary:", ", ".join(f"{k}: {v}" for k, v in totals.items()))
    print("Next: python ingest.py   (then restart the app unless auto-reload is set up)")


if __name__ == "__main__":
    main()
