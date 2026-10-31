"""PROVISIONAL parser for Ayes/Noes lists in Hansard text.
The real layout of a Kenyan Hansard division list has NOT been seen yet.
Check output by hand against the PDF, then adapt HEAD/END/split rules."""
import argparse, re

HEAD = re.compile(r"^\s*(AYES|NOES|NAYS|ABSTENTIONS?)\b\s*[:\-]?\s*\(?(\d+)?\)?\s*$", re.I)
END = re.compile(r"^\s*(the speaker|mr\.? speaker|result|the (ayes|noes) have it|\(?question put)", re.I)
TOT = re.compile(r"\b(ayes|noes)\b\s*[:=\-]?\s*(\d+)", re.I)

def _side(word):
    w = word.lower()
    if w.startswith("aye"):
        return "ayes"
    if w.startswith("abst"):
        return "abstain"
    return "noes"

def _names(line):
    line = re.sub(r"^\s*\d+[\.\)]\s*", "", line)
    parts = re.split(r"\s{2,}|;|\t", line.strip())
    out = []
    for p in parts:
        p = re.sub(r"^\d+[\.\)]\s*", "", p.strip())
        if p and not p.isdigit():
            out.append(p)
    return out

def parse_division(text):
    res = {"ayes": [], "noes": [], "abstain": [], "totals": {}}
    side = None
    for line in text.splitlines():
        m = HEAD.match(line)
        if m:
            side = _side(m.group(1))
            if m.group(2) and side in ("ayes", "noes"):
                res["totals"][side] = int(m.group(2))
            continue
        if END.match(line):
            side = None
            continue
        if side and line.strip():
            res[side].extend(_names(line))
    if not res["totals"]:
        for m in TOT.finditer(text):
            res["totals"][_side(m.group(1))] = int(m.group(2))
    return res

def names_found_in_text(names, source_text):
    """Each name must appear word for word in the source text (same idea as the excerpt check)."""
    norm = re.sub(r"\s+", " ", source_text)
    return [n for n in names if re.sub(r"\s+", " ", n) not in norm]  # returns MISSING names

if __name__ == "__main__":
    from ai import votes
    ap = argparse.ArgumentParser(description="Add one division from a text file you have checked.")
    ap.add_argument("--text-file", help="text of the division list (omit for --voice)")
    ap.add_argument("--voice", action="store_true", help="voice vote: no names recorded")
    ap.add_argument("--bill", required=True)
    ap.add_argument("--stage", required=True)
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--page", type=int)
    ap.add_argument("--file", default="", help="Hansard PDF filename")
    ap.add_argument("--url", default="")
    ap.add_argument("--aliases", default="")
    a = ap.parse_args()
    con = votes.connect()
    if a.voice:
        did = votes.add_division(con, a.bill, a.stage, a.date, "voice", page=a.page,
                                 hansard_file=a.file, source_url=a.url, aliases=a.aliases)
        print("added voice division", did)
    else:
        txt = open(a.text_file).read()
        r = parse_division(txt)
        missing = names_found_in_text(r["ayes"] + r["noes"] + r["abstain"], txt)
        mem = [(n, "ayes") for n in r["ayes"]] + [(n, "noes") for n in r["noes"]] \
            + [(n, "abstain") for n in r["abstain"]]
        print(f"ayes={len(r['ayes'])} noes={len(r['noes'])} abstain={len(r['abstain'])} totals={r['totals']}")
        if missing:
            raise SystemExit(f"Names not found in source text: {missing}")
        dtype = "recorded" if mem else "unknown"
        did = votes.add_division(con, a.bill, a.stage, a.date, dtype,
                                 r["totals"].get("ayes"), r["totals"].get("noes"),
                                 a.page, a.file, a.url, a.aliases, mem)
        print("added division", did, "type", dtype, "- CHECK AGAINST THE PDF BY HAND")
