import streamlit as st

from ui import about, chat, dashboard, insights, participation, styles

st.set_page_config(page_title="CivicLens", page_icon=":material/account_balance:", layout="wide")
styles.inject()

PAGES = {
    "dashboard": st.Page(dashboard.render, title="Dashboard", icon=":material/dashboard:",
                         url_path="dashboard", default=True),
    "assistant": st.Page(chat.render, title="Budget Assistant", icon=":material/chat:",
                         url_path="assistant"),
    "insights": st.Page(insights.render, title="Budget Insights", icon=":material/bar_chart:",
                        url_path="insights"),
    "participation": st.Page(participation.render, title="Public Participation",
                             icon=":material/groups:", url_path="participation"),
    "about": st.Page(about.render, title="About CivicLens", icon=":material/info:",
                     url_path="about"),
}
st.session_state["_pages"] = PAGES

with st.sidebar:
    st.markdown('<div class="cl-logo">CivicLens</div>'
                '<div class="cl-tagline">Where Did Our Money Go?</div>', unsafe_allow_html=True)
    for page in PAGES.values():
        st.page_link(page)
    st.markdown('<div class="cl-side-note">AI explanations are not official government '
                'statements.</div>', unsafe_allow_html=True)

st.navigation(list(PAGES.values()), position="hidden").run()
