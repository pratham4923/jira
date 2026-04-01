import streamlit as st

st.set_page_config(
    page_title="ProjectFlow | Agile PM",
    page_icon="PF",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    header, footer, [data-testid="stHeaderActionElements"] {
        display: none !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 14% 12%, rgba(255, 145, 77, 0.22), transparent 18%),
            radial-gradient(circle at 86% 16%, rgba(255, 209, 102, 0.10), transparent 18%),
            radial-gradient(circle at 50% 100%, rgba(255, 110, 64, 0.09), transparent 22%),
            linear-gradient(180deg, #06070c 0%, #0b0d14 38%, #121621 100%);
        color: #f8f2e8;
    }

    html, body, [class*="css"] {
        font-family: "IBM Plex Sans", sans-serif;
    }

    .block-container {
        max-width: 100%;
        padding-top: 1.3rem;
        padding-bottom: 2rem;
        animation: appFadeUp 0.55s cubic-bezier(0.22, 1, 0.36, 1);
    }

    @keyframes appFadeUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    h1, h2, h3, h4 {
        font-family: "Space Grotesk", sans-serif;
        letter-spacing: -0.04em;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea,
    .stDateInput input {
        background: rgba(255, 248, 238, 0.04) !important;
        color: #f8f2e8 !important;
        border: 1px solid rgba(255, 245, 233, 0.08) !important;
        border-radius: 16px !important;
    }

    div[data-baseweb="input"] input:focus,
    .stTextArea textarea:focus,
    .stDateInput input:focus {
        border-color: rgba(255, 166, 102, 0.65) !important;
        box-shadow: 0 0 0 1px rgba(255, 166, 102, 0.18), 0 0 0 5px rgba(255, 166, 102, 0.08) !important;
    }

    div.stButton > button,
    div.stLinkButton > a {
        min-height: 48px;
        border-radius: 999px;
        border: 1px solid rgba(255, 177, 102, 0.24);
        background: linear-gradient(135deg, #f6b36a 0%, #ff8e52 100%);
        color: #23160c !important;
        font-weight: 700;
        box-shadow: 0 20px 60px rgba(255, 122, 70, 0.18);
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        text-decoration: none !important;
    }

    div.stButton > button:hover,
    div.stLinkButton > a:hover {
        transform: translateY(-2px);
        filter: brightness(1.03);
        box-shadow: 0 24px 72px rgba(255, 122, 70, 0.24);
    }

    div.stButton > button[kind="secondary"] {
        background: rgba(255, 248, 238, 0.05);
        color: #f8f2e8 !important;
        border: 1px solid rgba(255, 248, 238, 0.08);
        box-shadow: none;
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(255, 248, 238, 0.06);
        background: rgba(15, 17, 24, 0.78);
        backdrop-filter: blur(18px);
        border-radius: 24px;
        padding: 1.2rem 1.15rem 1rem;
    }

    div[data-testid="stTabs"] button {
        color: rgba(248, 242, 232, 0.72);
        font-weight: 600;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f8f2e8;
    }

    div[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top, rgba(255, 149, 91, 0.16), transparent 22%),
            linear-gradient(180deg, rgba(14, 16, 22, 0.98) 0%, rgba(8, 9, 13, 0.98) 100%);
        border-right: 1px solid rgba(255, 248, 238, 0.06);
    }

    div[data-testid="stSidebar"] .block-container {
        padding: 1rem 1rem 1.25rem;
    }
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
