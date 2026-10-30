import streamlit as st

from ui import components as c
from ui import sample_data as d


def answer_question(question: str) -> dict:
    """PLACEHOLDER. Phase 5/6 replaces this with the real pipeline:
    retrieve evidence -> Gemma 4 -> validate citations.

    Keep the return shape: answer, status, document, page, excerpt, limitations.
    """
    if "health" in question.lower():
        return {
            "answer": ("Health services were allocated KSh 3.6 billion in FY 2025/26. "
                       "That is 30% of the KSh 12.0 billion county budget. "
                       "This tells us what was planned, not what was spent."),
            "status": "supported",
            "document": d.DOCUMENT["name"],
            "page": 18,
            "excerpt": "Health services: KSh 3,600,000,000, representing 30% of the total county budget of KSh 12,000,000,000.",
            "limitations": "This is an allocation, not evidence of actual expenditure or services delivered.",
        }
    return {
        "answer": ("I couldn’t find an answer to that in this document. "
                   "That does not mean the information does not exist; this document alone "
                   "cannot answer that question."),
        "status": "no_evidence",
        "document": None,
        "page": None,
        "excerpt": None,
        "limitations": "This document cannot confirm the requested detail. No conclusion about delivery can be drawn.",
    }


def _ask(question: str) -> None:
    st.session_state.pending_q = question


def _reset() -> None:
    st.session_state.messages = []


def render() -> None:
    st.session_state.setdefault("messages", [])

    c.page_header("Ask. Understand. Verify.", "Budget Assistant",
                  "Ask in plain language. Follow every explanation back to the document.")
    c.banner(d.NOTE)

    top_l, top_r = st.columns([4, 1])
    with top_l:
        c.doc_card(d.DOCUMENT["name"], f'{d.DOCUMENT["pages"]} pages · {d.DOCUMENT["year"]}',
                   badge_text="Ready")
    with top_r:
        st.button("New conversation", on_click=_reset, width="stretch")

    # A question can come from the input box or from a suggestion chip.
    question = st.chat_input("Ask about this budget...") or st.session_state.pop("pending_q", None)
    if question:
        st.session_state.messages.append({"role": "user", "text": question})
        st.session_state.messages.append({"role": "ai", "answer": answer_question(question)})

    for m in st.session_state.messages:
        if m["role"] == "user":
            c.user_message(m["text"])
        else:
            c.ai_message(m["answer"])

    if not st.session_state.messages:
        c.render('<div class="cl-muted" style="margin:24px 0">No questions yet. '
                 'Try one of the suggestions below.</div>')

    c.render('<div class="cl-label" style="margin-top:24px">Suggested questions</div>')
    cols = st.columns(len(d.SUGGESTED))
    for i, (col, q) in enumerate(zip(cols, d.SUGGESTED)):
        with col:
            st.button(q, key=f"chip_{i}", on_click=_ask, args=(q,), width="stretch")
    st.caption("Answers use the uploaded document. Always verify the cited page.")
