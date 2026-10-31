"""Scheduled job: fetch headlines from allowlisted outlets into data/news.json.
Links and headlines only. News is context, never evidence of a vote."""
import json, time, urllib.robotparser as rp
from urllib.parse import urlparse
import feedparser, requests

UA = "CivicLensBot/0.1 (+contact: you@example.com)"  # put your real contact
KEYWORDS = ["election", "elections (amendment)", "livestream", "live-stream",
            "live stream", "hansard", "national assembly", "division"]

def allowed(url):
    p = urlparse(url)
    r = rp.RobotFileParser(f"{p.scheme}://{p.netloc}/robots.txt")
    try:
        r.read()
    except Exception:
        return False
    return r.can_fetch(UA, url)

def main():
    cfg = json.load(open("data/news_allowlist.json"))
    items = []
    for src in cfg["rss"]:
        if not allowed(src["feed"]):
            print("robots.txt disallows or unreachable:", src["feed"])
            continue
        try:
            xml = requests.get(src["feed"], headers={"User-Agent": UA}, timeout=30).text
        except Exception as e:
            print("fetch failed:", src["feed"], e)
            continue
        for e in feedparser.parse(xml).entries:
            text = (e.get("title", "") + " " + e.get("summary", "")).lower()
            if any(k in text for k in KEYWORDS):
                items.append({"outlet": src["outlet"], "title": e.get("title", ""),
                              "url": e.get("link", ""), "published": e.get("published", "")})
        time.sleep(3)  # one request at a time, polite delay
    json.dump(items, open("data/news.json", "w"), indent=2)
    print(f"saved {len(items)} items")

if __name__ == "__main__":
    main()
