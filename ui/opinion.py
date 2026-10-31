import json, uuid
import streamlit as st
from ai import opinion, record

LABEL = ("Public opinion is unverified and informal. It is not a measure of performance. "
         "Official records of votes and budgets are on the Budget Assistant page.")
PER_PAGE = 10

def _meta():
    try:
        return json.load(open("data/officeholders_meta.json"))
    except Exception:
        return {}

def _match(o, q):
    q = q.lower().strip()
    return not q or q in " ".join([o["name"], o.get("seat", ""), o.get("role", "")]).lower()

def render() -> None:
    st.session_state.setdefault("rater", uuid.uuid4().hex)
    st.title("Public Opinion")
    st.info(LABEL)
    offices = opinion.load_offices()
    if not offices:
        st.warning("No office holders loaded yet. Run: python officeholders_sync.py")
        return
    meta = _meta()
    if meta.get("as_at"):
        st.caption(f"National Assembly list from parliament.go.ke, as at {meta['as_at']}. "
                   "Everyone is listed alphabetically in the same format.")
    q = st.text_input("Search by name, role or constituency")
    found = [o for o in offices if _match(o, q)]
    pages = max(1, -(-len(found) // PER_PAGE))
    page = st.number_input("Page", 1, pages, 1) if pages > 1 else 1
    st.caption(f"{len(found)} people. Page {page} of {pages}.")
    con = opinion.connect()
    rcon = record.connect()
    for o in found[(page - 1) * PER_PAGE: page * PER_PAGE]:
        with st.container(border=True):
            st.subheader(o["name"])
            line = o["role"] + (" - " + o["seat"] if o.get("seat") else "")
            st.caption(line)
            if o.get("source_url"):
                st.caption("Source: " + o["source_url"])
            rec = record.get(rcon, o["id"])
            if rec:
                with st.expander("Recorded activity (facts, not a score)"):
                    for r in rec:
                        st.write(f"{r['metric']}: {r['value']}")
                    st.caption(f"Source: {rec[0]['source']}, file dated {rec[0]['file_date']}. "
                               "Counts show how much a member recorded in Parliament, "
                               "not how well they did.")
            stars = st.radio("Your rating (1 = low, 5 = high)", [1, 2, 3, 4, 5], index=2,
                             horizontal=True, key="s_" + o["id"])
            if st.button("Submit rating", key="b_" + o["id"]):
                opinion.rate(con, o["id"], st.session_state["rater"], stars)
                st.success("Recorded. You can change it by submitting again.")
            s = opinion.summary(con, o["id"])
            if s["shown"]:
                st.write(f"{s['count']} ratings, average {s['avg']:.1f} out of 5 (unverified).")
            else:
                st.caption(f"Results show after {opinion.MIN_SHOWN} ratings ({s['count']} so far).")
    st.caption(LABEL)
