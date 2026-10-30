import streamlit as st

from ui import components as c
from ui import sample_data as d


def _gap_card(g: dict) -> None:
    c.render(f"""
    <div class="cl-card">
    <span class="cl-badge cl-badge-warn">{c.esc(g["kind"])}</span>
    <div class="cl-h3" style="margin-top:10px">{c.esc(g["title"])}</div>
    <div class="cl-muted">{c.esc(g["text"])}</div>
    <div class="cl-excerpt"><div class="cl-label" style="margin-top:0">Exact excerpt</div>“{c.esc(g["excerpt"])}”</div>
    <div class="cl-limits">{c.esc(g["meta"])}</div>
    <div class="cl-limits">{c.esc(g["note"])}</div>
    </div>
    """)


def render() -> None:
    c.page_header("From understanding to participation", "Make your next question count",
                  "Use what the budget says, and what it leaves open, to prepare for a public meeting.")
    c.banner(d.NOTE)
    st.caption(f'{d.DOCUMENT["name"]} · {d.DOCUMENT["year"]}')

    c.h2("Information gaps worth clarifying")
    cols = st.columns(2)
    for col, gap in zip(cols, d.GAPS):
        with col:
            _gap_card(gap)

    c.h2("Questions to ask at your public meeting")
    st.caption("Specific, neutral questions you can copy and take with you. "
               "Use the copy icon on each box.")
    for q in d.QUESTIONS:
        c.render(f'<div class="cl-label">{c.esc(q["tag"])} · {c.esc(q["meta"])}</div>')
        st.code(q["text"], language=None, wrap_lines=True)

    with st.expander("Copy all questions"):
        st.code("\n\n".join(q["text"] for q in d.QUESTIONS), language=None, wrap_lines=True)

    c.banner("Take the source, not just the summary. Bring the cited pages, ask where additional "
             "records can be accessed, and note the response and agreed follow-up dates.",
             kind="info")
    c.footer()
