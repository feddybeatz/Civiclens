"""Votes table (SQLite). Names come only from parsed Hansard rows, never from a model."""
import os, re, sqlite3

DB_PATH = "data/index/votes.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS divisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bill TEXT NOT NULL,
  stage TEXT NOT NULL,          -- e.g. 'Third Reading', 'Amendment to delete Clause 22'
  date TEXT NOT NULL,           -- YYYY-MM-DD
  dtype TEXT NOT NULL,          -- recorded | voice | unknown
  ayes_total INTEGER,
  noes_total INTEGER,
  page INTEGER,
  hansard_file TEXT,
  source_url TEXT,
  aliases TEXT DEFAULT ''       -- plain-words keywords the owner adds, e.g. 'live streaming results'
);
CREATE TABLE IF NOT EXISTS votes (
  division_id INTEGER NOT NULL REFERENCES divisions(id),
  member TEXT NOT NULL,
  vote TEXT NOT NULL,           -- ayes | noes | abstain
  page INTEGER
);
"""

def connect(path=DB_PATH):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con

def add_division(con, bill, stage, date, dtype, ayes_total=None, noes_total=None,
                 page=None, hansard_file="", source_url="", aliases="", members=()):
    cur = con.execute(
        "INSERT INTO divisions (bill,stage,date,dtype,ayes_total,noes_total,page,"
        "hansard_file,source_url,aliases) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (bill, stage, date, dtype, ayes_total, noes_total, page, hansard_file,
         source_url, aliases))
    did = cur.lastrowid
    con.executemany("INSERT INTO votes VALUES (?,?,?,?)",
                    [(did, m, v, page) for m, v in members])
    con.commit()
    return did

def members(con, division_id, side):
    rows = con.execute("SELECT member FROM votes WHERE division_id=? AND vote=? "
                       "ORDER BY member", (division_id, side)).fetchall()
    return [r["member"] for r in rows]

STOP = {"list", "the", "mps", "mp", "members", "member", "who", "voted", "vote",
        "votes", "no", "noes", "nay", "nays", "yes", "aye", "ayes", "against", "for",
        "on", "in", "of", "a", "an", "bill", "to", "and", "how", "did", "which",
        "were", "was", "is", "that", "by", "at", "me", "show", "give", "name", "names",
        "opposed", "supported", "favour", "favor", "national", "assembly"}

def _tokens(s):
    s = s.lower().replace("live streaming", "livestreaming").replace("live-streaming", "livestreaming")
    return {t for t in re.findall(r"[a-z0-9]+", s) if t not in STOP}

def search_divisions(con, question):
    q = _tokens(question)
    years = set(re.findall(r"\b(20\d\d)\b", question))
    q = {t for t in q if t not in years}
    if not q:
        return []
    scored = []
    for r in con.execute("SELECT * FROM divisions"):
        if years and r["date"][:4] not in years:
            continue
        hay = _tokens(" ".join([r["bill"], r["stage"], r["aliases"] or ""]))
        hit = len(q & hay)
        if hit and hit / len(q) >= 0.5:
            scored.append((hit, r))
    if not scored:
        return []
    best = max(s for s, _ in scored)
    return [r for s, r in scored if s == best]
