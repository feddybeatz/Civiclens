"""Reusable UI pieces. All dynamic text is HTML-escaped."""
import html

import streamlit as st

STATUS = {
    "supported": ("Supported", "ok"),
    "partial": ("Partially supported", "warn"),
    "no_evidence": ("No evidence found", "none"),
    "error": ("Error", "err"),
}


def esc(text) -> str:
    return html.escape(str(text))


def _flat(markup: str) -> str:
    # Markdown treats indented lines as code blocks, so strip every line.
    return "".join(line.strip() for line in markup.strip().splitlines())


def render(markup: str) -> None:
    st.markdown(_flat(markup), unsafe_allow_html=True)


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    render(f"""
    <div class="cl-eyebrow">{esc(eyebrow)}</div>
    <h1 class="cl-title">{esc(title)}</h1>
    <p class="cl-sub">{esc(subtitle)}</p>
    """)


def banner(text: str, kind: str = "warn") -> None:
    render(f'<div class="cl-banner cl-banner-{kind}">{esc(text)}</div>')


def h2(text: str) -> None:
    render(f'<div class="cl-h2">{esc(text)}</div>')


def footer() -> None:
    render('<div class="cl-footer">Understand the numbers. Check the evidence.</div>')


def badge(status: str) -> str:
    label, kind = STATUS[status]
    return f'<span class="cl-badge cl-badge-{kind}">{esc(label)}</span>'


def stat_card(label: str, value: str, caption: str) -> None:
    render(f"""
    <div class="cl-card cl-stat">
    <div class="cl-label">{esc(label)}</div>
    <div class="cl-value">{esc(value)}</div>
    <div class="cl-caption">{esc(caption)}</div>
    </div>
    """)


def doc_card(name: str, detail: str, status: str = "supported", badge_text: str = "") -> None:
    pill = badge(status) if not badge_text else (
        f'<span class="cl-badge cl-badge-ok">{esc(badge_text)}</span>')
    render(f"""
    <div class="cl-card cl-doc">
    <div><div class="cl-label" style="margin-top:0">Current document</div>
    <div class="cl-doc-name">{esc(name)}</div>
    <div class="cl-caption" style="font-size:12px;color:#6B756F">{esc(detail)}</div></div>
    {pill}
    </div>
    """)


def evidence_html(ev: dict) -> str:
    """Evidence panel shown under every AI answer.

    ev keys: status, document, page, excerpt, limitations
    A missing page/excerpt is shown as 'Unavailable', never invented.
    """
    doc = ev.get("document") or "Unavailable, no matching source"
    page = ev.get("page") or "Unavailable"
    if ev.get("excerpt"):
        excerpt = f"“{esc(ev['excerpt'])}”"
    else:
        excerpt = "Unavailable, no relevant excerpt was found."
    return (
        '<div class="cl-evidence">'
        f'<div class="cl-ev-head"><strong>Evidence</strong>{badge(ev["status"])}</div>'
        '<div class="cl-label">Source document</div>'
        f'<div class="cl-ev-val">{esc(doc)}</div>'
        '<div class="cl-label">Page</div>'
        f'<div class="cl-ev-val">{esc(page)}</div>'
        f'<div class="cl-excerpt"><div class="cl-label" style="margin-top:0">Exact excerpt</div>{excerpt}</div>'
        f'<div class="cl-limits">Limitations: {esc(ev.get("limitations", ""))}</div>'
        '</div>'
    )


def user_message(text: str) -> None:
    render(f'<div class="cl-user"><div class="cl-who">You</div>{esc(text)}</div>')


def ai_message(answer: dict) -> None:
    render(
        '<div class="cl-who cl-who-ai">CivicLens · Document-based answer</div>'
        f'<div class="cl-answer">{esc(answer["answer"])}</div>'
        f'{evidence_html(answer)}'
    )
