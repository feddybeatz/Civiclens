import streamlit as st

from ui import components as c
from ui import sample_data as d


def _go(key: str) -> None:
    pages = st.session_state.get("_pages", {})
    if key in pages:
        st.switch_page(pages[key])


def render() -> None:
    c.page_header("Your public money, explained", "Welcome to CivicLens",
                  "Turn a county budget into clear answers, with evidence you can check.")
    c.banner(d.NOTE)

    with st.container(border=True):
        c.render('<div class="cl-h3">Start with a budget document</div>')
        upload = st.file_uploader("Budget PDF", type=["pdf"], label_visibility="collapsed")
        st.caption("PDF up to 25 MB. Text-based PDFs work best. Review scanned pages carefully.")

    if upload is not None:
        # TODO (Phase 3): hand `upload` to documents/document_processor.py
        size_mb = upload.size / (1024 * 1024)
        c.doc_card(upload.name, f"{size_mb:.1f} MB · text extraction not connected yet",
                   badge_text="Uploaded")
    else:
        doc = d.DOCUMENT
        c.doc_card(doc["name"], f'{doc["pages"]} pages · {doc["year"]} · illustrative sample',
                   badge_text="Ready to explore")

    c.h2("At a glance")
    cols = st.columns(4)
    stats = [
        ("Total budget", "KSh 12.0B", "All sectors · p. 18"),
        ("Health allocation", "KSh 3.6B", "30% of total · p. 18"),
        ("Development", "KSh 4.8B", "40% of total · p. 12"),
        ("Document coverage", "64 pages", "Text extracted and indexed"),
    ]
    for col, (label, value, caption) in zip(cols, stats):
        with col:
            c.stat_card(label, value, caption)

    st.write("")
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            c.render('<div class="cl-h3">Ask a question, not a spreadsheet</div>'
                     '<div class="cl-muted">Start with “How much was allocated to health?” '
                     'Every answer includes its source and limitations.</div>')
            if st.button("Open Budget Assistant", type="primary", key="go_assistant"):
                _go("assistant")
    with right:
        with st.container(border=True):
            c.render('<div class="cl-h3">Bring better questions to the meeting</div>'
                     '<div class="cl-muted">Review information gaps and prepare neutral, '
                     'evidence-based questions for public participation.</div>')
            if st.button("Prepare for a public meeting", key="go_participation"):
                _go("participation")
    c.footer()
