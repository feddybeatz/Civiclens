import argparse, datetime, json
from ai import record

def main():
    ap = argparse.ArgumentParser(description="Import a CSV you downloaded by hand.")
    ap.add_argument("csv")
    ap.add_argument("--source", required=True)
    ap.add_argument("--date", default=str(datetime.date.today()))
    ap.add_argument("--name-col")
    ap.add_argument("--seat-col")
    a = ap.parse_args()
    offices = json.load(open("data/officeholders.json"))
    r = record.load_csv(a.csv, offices, a.source, a.date, a.name_col, a.seat_col)
    print("name column:", r["name_col"], "| constituency column:", r["seat_col"])
    print("rows:", r["rows"], "| distinct members matched:", r["members"])
    print("match methods:", r["methods"])
    print("unmatched names:", len(r["unmatched"]))
    for n in r["unmatched"][:40]:
        print("  unmatched:", n)
    print("non-exact matches to review (csv name -> official name, method):")
    for c, o, how in r["fuzzy"][:400]:
        print(f"  {c} -> {o} [{how}]")

if __name__ == "__main__":
    main()
