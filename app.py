import streamlit as st

st.set_page_config(
    page_title="ProjectFlow | Agile PM",
    page_icon="PF",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("public/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    </style>
    """,
    unsafe_allow_html=True,
)

if "user" not in st.session_state:
    st.session_state["user"] = None

pages = []

if st.session_state["user"] is None:
    pages.append(st.Page("pages/login.py", title="Login", url_path="login"))
else:
    pages.append(st.Page("pages/dashboard.py", title="Dashboard", url_path="dashboard"))
    pages.append(st.Page("pages/backlog.py", title="Backlog", url_path="backlog"))
    pages.append(st.Page("pages/reports.py", title="Reports", url_path="reports"))
    pages.append(st.Page("pages/admin.py", title="Admin", url_path="admin"))

pg = st.navigation(pages, position="hidden")
pg.run()
