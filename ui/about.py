import streamlit as st

from ui import components as c

STEPS = [
    ("Upload", "Add a government or county budget PDF. Text-based documents give the clearest results."),
    ("Find evidence", "CivicLens locates relevant passages and keeps the document name and page number attached."),
    ("Gemma 4 explains", "Ask in everyday language. Get a clear explanation grounded in the retrieved passages."),
    ("Verify", "Read the exact excerpt, open the cited page, and check the limitations before drawing conclusions."),
]


def _go(key: str) -> None:
    pages = st.session_state.get("_pages", {})
    if key in pages:
        st.switch_page(pages[key])


def render() -> None:
    c.page_header("Public money. Public questions.", "Where Did Our Money Go?",
                  "CivicLens helps Kenyan citizens read public budgets with more confidence.")
    c.render("""
    <div class="cl-mission">
    <h2>A budget should be a starting point for participation, not a barrier to it.</h2>
    <p>We turn dense budget documents into plain-language explanations, while keeping the evidence
    visible, so you can understand priorities, spot unanswered questions and participate in the
    decisions that affect your community.</p>
    </div>
    """)

    c.h2("From PDF to a verifiable answer")
    for i, (col, (title, text)) in enumerate(zip(st.columns(4), STEPS), start=1):
        with col:
            c.render(f'<div class="cl-card"><span class="cl-step-n">0{i}</span>'
                     f'<div class="cl-h3">{c.esc(title)}</div>'
                     f'<div class="cl-muted">{c.esc(text)}</div></div>')

    st.write("")
    left, right = st.columns(2)
    with left:
        c.render('<div class="cl-card"><div class="cl-h3">Evidence before certainty</div>'
                 '<div class="cl-muted">CivicLens distinguishes supported answers, partial evidence and '
                 'questions the document cannot answer. Missing evidence is never treated as proof of '
                 'wrongdoing. An allocation is not an expenditure. A summary is not an audit.</div></div>')
    with right:
        c.render('<div class="cl-card"><div class="cl-h3">Open technology, public purpose</div>'
                 '<div class="cl-muted">Powered by Gemma 4, open source. AI helps explain the text; the '
                 'uploaded document remains the source of truth. The model can make mistakes or miss '
                 'context.</div></div>')

    st.write("")
    if st.button("Go to Dashboard", type="primary"):
        _go("dashboard")
    c.footer()
