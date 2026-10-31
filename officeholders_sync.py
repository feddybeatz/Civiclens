"""Builds data/officeholders.json from Parliament's official member list (PDF)
plus data/executive.json. Run by hand or on a schedule, never while a user waits."""
import argparse, json, os, re, subprocess, sys
import urllib.robotparser as rp
from urllib.parse import urlparse, unquote
import requests

UA = "CivicLensBot/0.1 (+contact: you@example.com)"  # put your real contact
SRC, OUT, META = "data/officeholders_source.json", "data/officeholders.json", "data/officeholders_meta.json"
PARTIES = {"ANC", "CCM", "DAP-K", "DCP", "FORD-K", "FORD-Kenya", "GDDP", "Independent", "JP",
           "KANU", "KUP", "MCCP", "MDG", "NAP-K", "NOPEU", "ODM", "PAA", "TSP", "UDA", "UDM",
           "UPA", "UPIA", "WDM", "WDM-K"}
ROW = re.compile(r"^\s*(\d{1,3})\.\s+(.*\S)\s*$")

def allowed(url):
    p = urlparse(url)
    r = rp.RobotFileParser(f"{p.scheme}://{p.netloc}/robots.txt")
    try:
        r.read()
    except Exception:
        return False
    return r.can_fetch(UA, url)

def download(url):
    os.makedirs("data/officeholders", exist_ok=True)
    path = os.path.join("data/officeholders", unquote(url.rsplit("/", 1)[-1]))
    if os.path.exists(path):
        return path
    if not allowed(url):
        sys.exit("robots.txt blocks or is unreachable. Download the PDF by hand, then run with --pdf FILE")
    r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    r.raise_for_status()
    open(path, "wb").write(r.content)
    return path

def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                              text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
        return "\n".join(p.get_text("text") for p in fitz.open(path))

def parse(text):
    members = []
    for line in text.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        body = m.group(2).strip().rstrip("`").strip()
        if body.lower().startswith("vacant"):
            continue
        party = ""
        tok = body.rsplit(None, 1)
        if len(tok) == 2 and tok[1] in PARTIES:
            party, body = tok[1], tok[0].strip()
        parts = re.split(r"\s{2,}", body)
        if len(parts) >= 2:
            name, seat, split = parts[0], " ".join(parts[1:]), True
        else:
            name, seat, split = body, "", False
        seat = seat.replace("(CWR)", "(County Woman Representative)")
        members.append({"name": name, "role": "Member of the National Assembly",
                        "seat": seat, "party": party, "split": split})
    return members

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", help="use a PDF you downloaded by hand")
    ap.add_argument("--force", action="store_true", help="write even if the count differs")
    a = ap.parse_args()
    url = json.load(open(SRC))["na_pdf"]
    path = a.pdf or download(url)
    text = pdf_text(path)
    members = parse(text)
    exp = re.search(r"TOTAL\s+(\d+)", text)
    expected = int(exp.group(1)) if exp else None
    d = re.search(r"as at (\d{2})(\d{2})(\d{4})", unquote(os.path.basename(path)))
    as_at = f"{d.group(3)}-{d.group(2)}-{d.group(1)}" if d else ""
    print(f"parsed {len(members)} members; PDF total {expected}; as at {as_at or 'unknown'}")
    print("rows without a party:", sum(1 for m in members if not m["party"]))
    print("rows where name and constituency could not be separated:", sum(1 for m in members if not m["split"]))
    for m in members[:2] + members[-2:]:
        print("  sample:", m["name"], "|", m["seat"], "|", m["party"])
    if expected and len(members) != expected and not a.force:
        sys.exit("Count does not match the PDF total. Nothing written. Check the layout, then use --force if sure.")
    for m in members:
        m["source_url"], m["as_at"] = url, as_at
    people = json.load(open("data/executive.json")) + members
    seen = {}
    for p in people:
        base = slug(p["name"] + "-" + p.get("seat", ""))
        seen[base] = seen.get(base, 0) + 1
        p["id"] = base if seen[base] == 1 else f"{base}-{seen[base]}"
    people.sort(key=lambda p: p["name"].lower())
    json.dump(people, open(OUT, "w"), indent=1, ensure_ascii=False)
    json.dump({"as_at": as_at, "count": len(people), "source_url": url}, open(META, "w"))
    print("wrote", len(people), "people to", OUT)

if __name__ == "__main__":
    main()
