"""Global CSS that turns Streamlit into the CivicLens design.

Colours come from the Figma file:
  primary #0F5C4D, highlight #E0A126, text #1A1F1C, canvas #F7F8F5
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"], button, input, textarea {
  font-family: 'Inter', sans-serif;
}
.stApp { background: #F7F8F5; color: #1A1F1C; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1080px; padding-top: 2rem; padding-bottom: 3rem; }

/* sidebar */
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E4E8E2; }
.cl-logo { font-size: 20px; font-weight: 700; color: #0F5C4D; margin-bottom: 2px; }
.cl-tagline { font-size: 12px; color: #6B756F; margin-bottom: 18px; }
.cl-side-note { font-size: 12px; color: #6B756F; line-height: 1.5; margin-top: 24px; }

/* page header */
.cl-eyebrow { font-size: 12px; font-weight: 600; color: #0F5C4D; margin-bottom: 4px; }
.cl-title { font-size: 32px; font-weight: 600; margin: 0 0 6px 0; padding: 0; letter-spacing: -0.01em; }
.cl-sub { font-size: 16px; color: #4A544E; margin: 0 0 16px 0; max-width: 70ch; }
.cl-h2 { font-size: 20px; font-weight: 600; margin: 28px 0 12px 0; }
.cl-h3 { font-size: 17px; font-weight: 600; margin: 0 0 6px 0; }
.cl-muted { font-size: 14px; color: #5B665F; line-height: 1.55; }
.cl-footer { font-size: 12px; color: #6B756F; margin-top: 40px; }

/* banners */
.cl-banner { border-radius: 8px; padding: 10px 14px; font-size: 13px; margin-bottom: 16px; }
.cl-banner-warn { background: #FBF1DA; border: 1px solid #EBD39A; color: #6B4E0D; }
.cl-banner-info { background: #E7F1EC; border: 1px solid #C5DCD1; color: #0F5C4D; }
.cl-banner-err { background: #FBE9E7; border: 1px solid #EDBDB6; color: #8A2A1E; }

/* cards */
.cl-card { background: #FFFFFF; border: 1px solid #E4E8E2; border-radius: 12px; padding: 16px 18px; }
.cl-stat .cl-label { font-size: 12px; color: #6B756F; }
.cl-stat .cl-value { font-size: 28px; font-weight: 600; color: #0F5C4D; margin: 4px 0; }
.cl-stat .cl-caption { font-size: 12px; color: #6B756F; }
.cl-label { font-size: 12px; color: #6B756F; margin-top: 8px; }
.cl-doc { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.cl-doc-name { font-weight: 600; font-size: 16px; }

/* badges */
.cl-badge { display: inline-block; border-radius: 999px; padding: 2px 10px; font-size: 12px; font-weight: 500; }
.cl-badge-ok { background: #E1F0E8; color: #0F5C4D; }
.cl-badge-warn { background: #FBF1DA; color: #7A5A10; }
.cl-badge-none { background: #ECEEEB; color: #5B665F; }
.cl-badge-err { background: #FBE9E7; color: #8A2A1E; }

/* chat */
.cl-who { font-size: 11px; font-weight: 600; color: #5B665F; margin-bottom: 4px; }
.cl-who-ai { margin-top: 18px; color: #0F5C4D; }
.cl-user { background: #E7F1EC; border-radius: 10px; padding: 10px 14px; margin: 14px 0 0 auto; width: fit-content; max-width: 80%; font-size: 15px; }
.cl-answer { background: #FFFFFF; border: 1px solid #E4E8E2; border-radius: 10px; padding: 14px 16px; font-size: 15px; line-height: 1.6; }
.cl-evidence { background: #FFFFFF; border: 1px solid #E4E8E2; border-radius: 10px; padding: 14px 16px; margin-top: 8px; font-size: 13px; }
.cl-ev-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.cl-ev-val { font-size: 14px; font-weight: 500; }
.cl-excerpt { background: #F3F5F1; border-left: 3px solid #0F5C4D; border-radius: 6px; padding: 8px 12px; margin-top: 10px; font-size: 14px; }
.cl-limits { font-size: 12px; color: #6B756F; margin-top: 10px; }

/* about page */
.cl-mission { background: #0F5C4D; color: #FFFFFF; border-radius: 14px; padding: 28px 30px; }
.cl-mission h2 { color: #FFFFFF; font-size: 26px; font-weight: 600; margin: 0 0 10px 0; }
.cl-mission p { color: #D6E9E1; margin: 0; max-width: 70ch; font-size: 15px; }
.cl-step-n { font-size: 12px; color: #6B756F; float: right; }

/* streamlit widgets */
div[data-testid="stFileUploaderDropzone"] {
  background: #FFFFFF; border: 1.5px dashed #8DB5A9; border-radius: 12px; padding: 28px;
}
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 12px; }
.stButton > button { border-radius: 8px; font-weight: 500; }
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
