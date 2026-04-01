import bcrypt
import streamlit as st

from database import User, get_db

for session_key, default_value in {
    "login_username": "",
    "login_password": "",
    "signup_username": "",
    "signup_password": "",
    "signup_role": "Admin",
}.items():
    if session_key not in st.session_state:
        st.session_state[session_key] = default_value

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1280px;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .pf-login-shell {
        border: 1px solid rgba(255, 248, 238, 0.07);
        border-radius: 30px;
        background:
            radial-gradient(circle at top left, rgba(246, 179, 106, 0.10), transparent 22%),
            linear-gradient(180deg, rgba(14, 17, 25, 0.96), rgba(10, 12, 18, 0.98));
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.24);
        overflow: hidden;
    }

    .pf-login-left {
        padding: 2.25rem 2.25rem 2rem 2.25rem;
    }

    .pf-login-right {
        padding: 2.25rem 2.25rem 2rem 1.25rem;
    }

    .pf-mark {
        display: inline-flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.7rem 0.95rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 248, 238, 0.08);
        background: rgba(255, 248, 238, 0.03);
        color: rgba(248, 242, 232, 0.72);
        font-size: 0.8rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .pf-mark-badge {
        width: 2.35rem;
        height: 2.35rem;
        display: grid;
        place-items: center;
        border-radius: 0.85rem;
        background: linear-gradient(135deg, #f6b36a 0%, #ff8e52 100%);
        color: #24170f;
        font-weight: 900;
    }

    .pf-headline {
        margin: 1.4rem 0 0 0;
        font-size: clamp(2.4rem, 4vw, 4.6rem);
        line-height: 0.94;
        color: #fff7ef;
    }

    .pf-subhead {
        margin-top: 1rem;
        max-width: 34rem;
        color: rgba(248, 242, 232, 0.68);
        font-size: 1rem;
        line-height: 1.6;
    }

    .pf-proof-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin-top: 1.6rem;
    }

    .pf-proof {
        padding: 1rem;
        border-radius: 18px;
        border: 1px solid rgba(255, 248, 238, 0.07);
        background: rgba(255, 248, 238, 0.03);
    }

    .pf-proof strong {
        display: block;
        color: #fff7ef;
        margin-bottom: 0.35rem;
        font-size: 0.98rem;
    }

    .pf-proof span {
        color: rgba(248, 242, 232, 0.6);
        font-size: 0.88rem;
        line-height: 1.45;
    }

    .pf-utility {
        margin-top: 1.25rem;
        display: grid;
        gap: 0.7rem;
    }

    .pf-utility-row {
        display: flex;
        gap: 0.7rem;
        color: rgba(248, 242, 232, 0.7);
        font-size: 0.94rem;
        line-height: 1.45;
    }

    .pf-utility-row::before {
        content: "";
        width: 0.55rem;
        height: 0.55rem;
        margin-top: 0.42rem;
        border-radius: 50%;
        background: linear-gradient(135deg, #f6b36a 0%, #ff8e52 100%);
        box-shadow: 0 0 18px rgba(255, 142, 82, 0.35);
        flex: 0 0 auto;
    }

    .pf-side-card {
        padding: 1.15rem;
        border-radius: 22px;
        border: 1px solid rgba(255, 248, 238, 0.07);
        background: rgba(255, 248, 238, 0.028);
        margin-bottom: 1rem;
    }

    .pf-side-card h3 {
        margin: 0;
        color: #fff7ef;
        font-size: 1.15rem;
    }

    .pf-side-card p {
        margin: 0.5rem 0 0 0;
        color: rgba(248, 242, 232, 0.62);
        font-size: 0.92rem;
        line-height: 1.5;
    }

    .pf-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.9rem;
    }

    .pf-chip {
        padding: 0.42rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 248, 238, 0.07);
        background: rgba(255, 248, 238, 0.03);
        color: rgba(248, 242, 232, 0.76);
        font-size: 0.8rem;
    }

    div[data-testid="stForm"] {
        margin-top: 0.75rem;
    }

    @media (max-width: 900px) {
        .pf-proof-grid {
            grid-template-columns: 1fr;
        }

        .pf-login-left,
        .pf-login-right {
            padding: 1.35rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

outer_left, outer_right = st.columns([1.2, 0.88], gap="large")

with outer_left:
    st.markdown(
        """
        <div class="pf-login-left">
            <div class="pf-mark">
                <div class="pf-mark-badge">PF</div>
                ProjectFlow
            </div>
            <h1 class="pf-headline">Ship work with the clarity of a real operating system.</h1>
            <p class="pf-subhead">ProjectFlow gives you a clean delivery workspace for backlog planning, execution tracking, reporting, and admin control without the visual noise that usually slows teams down.</p>
            <div class="pf-proof-grid">
                <div class="pf-proof">
                    <strong>Board control</strong>
                    <span>Move work across delivery states with a denser, product-first board surface.</span>
                </div>
                <div class="pf-proof">
                    <strong>Sprint planning</strong>
                    <span>Shape the next sprint from backlog without losing context.</span>
                </div>
                <div class="pf-proof">
                    <strong>Deploy ready</strong>
                    <span>Push the same workspace to Streamlit Community Cloud when needed.</span>
                </div>
            </div>
            <div class="pf-utility">
                <div class="pf-utility-row">Built to feel closer to a real Jira-style workspace than a demo landing page.</div>
                <div class="pf-utility-row">No sample users, no fake files, and no placeholder task clutter on first launch.</div>
                <div class="pf-utility-row">Windows and macOS runners are included so the app starts like a real product.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with outer_right:
    st.markdown(
        """
        <div class="pf-login-right">
            <div class="pf-side-card">
                <h3>Enter the workspace</h3>
                <p>Sign in to continue or create the first account for this workspace.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Log In", "Create Account"])

    with tab1:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Log in", use_container_width=True)

            if submit:
                db = next(get_db())
                user = db.query(User).filter(User.username == username).first()
                if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                    st.error("Invalid username or password")
                else:
                    st.session_state["user"] = {
                        "id": str(user.id),
                        "username": user.username,
                        "role": user.role,
                        "progress": user.progress,
                    }
                    st.rerun()

    with tab2:
        with st.form("signup_form", clear_on_submit=True):
            new_username = st.text_input("Choose username", key="signup_username")
            new_password = st.text_input("Create password", type="password", key="signup_password")
            role = st.selectbox(
                "Role",
                [
                    "Admin",
                    "Data Collection and Preprocessing",
                    "Architecture Design",
                    "Coding",
                    "Testing",
                    "Deployment",
                ],
                key="signup_role",
            )
            signup_submit = st.form_submit_button("Create account", use_container_width=True)

            if signup_submit:
                if not new_username or not new_password:
                    st.error("Please fill out all fields.")
                else:
                    db = next(get_db())
                    existing_user = db.query(User).filter(User.username == new_username).first()
                    if existing_user:
                        st.error("Username already exists.")
                    else:
                        hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        new_user = User(username=new_username, password=hashed_pw, role=role, progress=0)
                        db.add(new_user)
                        db.commit()
                        st.success("Account created. Log in from the first tab.")
