"""Public opinion ratings. Stars only, no free text. NOT a performance measure."""
import json, os, sqlite3, time

DB = "data/index/opinion.db"
MIN_SHOWN = 30

def connect(path=DB):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        office_id TEXT NOT NULL,
        rater TEXT NOT NULL,
        stars INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5),
        created REAL NOT NULL,
        UNIQUE (office_id, rater))""")
    con.commit()
    return con

def load_offices(path="data/officeholders.json"):
    try:
        offices = json.load(open(path))
    except Exception:
        return []
    return sorted(offices, key=lambda o: o["name"].lower())  # same order rule for everyone

def rate(con, office_id, rater, stars):
    con.execute("""INSERT INTO ratings (office_id, rater, stars, created)
                   VALUES (?,?,?,?)
                   ON CONFLICT (office_id, rater) DO UPDATE SET stars=excluded.stars,
                   created=excluded.created""",
                (office_id, rater, int(stars), time.time()))
    con.commit()

def summary(con, office_id):
    rows = con.execute("SELECT stars, COUNT(*) n FROM ratings WHERE office_id=? "
                       "GROUP BY stars", (office_id,)).fetchall()
    dist = {r["stars"]: r["n"] for r in rows}
    count = sum(dist.values())
    avg = sum(k * v for k, v in dist.items()) / count if count else None
    return {"count": count, "avg": avg, "dist": dist, "shown": count >= MIN_SHOWN}
