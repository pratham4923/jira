import streamlit as st


def render_sidebar(active_page="dashboard"):
    user = st.session_state.get("user") or {}
    username = user.get("username", "User")
    role = user.get("role", "Workspace member")
    initial = username[:1].upper() if username else "U"

    nav_items = [
        ("dashboard", "Dashboard"),
        ("backlog", "Backlog"),
        ("reports", "Reports"),
        ("admin", "Admin"),
    ]

    st.sidebar.markdown(
        f"""
        <div style="padding:0.25rem 0 1rem;">
            <div style="display:inline-flex; align-items:center; gap:0.8rem; margin-bottom:1rem;">
                <div style="width:2.8rem; height:2.8rem; border-radius:0.95rem; display:grid; place-items:center; background:linear-gradient(135deg, #f6b36a 0%, #ff8e52 100%); color:#22150d; font-weight:900;">PF</div>
                <div>
                    <div style="color:#fff7ef; font-family:'Space Grotesk', sans-serif; font-size:1.1rem;">ProjectFlow</div>
                    <div style="color:rgba(248,242,232,0.52); font-size:0.78rem; text-transform:uppercase; letter-spacing:0.12em;">Control Surface</div>
                </div>
            </div>
            <div style="padding:0.9rem; border-radius:1.2rem; border:1px solid rgba(255,248,238,0.08); background:rgba(255,248,238,0.03);">
                <div style="display:flex; align-items:center; gap:0.8rem;">
                    <div style="width:2.4rem; height:2.4rem; border-radius:50%; display:grid; place-items:center; background:rgba(246,179,106,0.14); color:#f6b36a; font-weight:800;">{initial}</div>
                    <div>
                        <div style="color:#fff7ef; font-weight:700;">{username}</div>
                        <div style="color:rgba(248,242,232,0.52); font-size:0.78rem;">{role}</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        "<div style='color:rgba(248,242,232,0.42); font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; margin:0.8rem 0 0.5rem;'>Workspace</div>",
        unsafe_allow_html=True,
    )

    for key, label in nav_items:
        button_type = "primary" if active_page == key else "secondary"
        if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True, type=button_type):
            st.switch_page(f"pages/{key}.py")

    st.sidebar.markdown(
        """
        <div style="margin-top:1rem; padding:0.9rem; border-radius:1.15rem; border:1px solid rgba(255,248,238,0.06); background:rgba(255,248,238,0.025);">
            <div style="color:#fff7ef; font-weight:700; margin-bottom:0.35rem;">Deploy Ready</div>
            <div style="color:rgba(248,242,232,0.56); font-size:0.86rem; line-height:1.45;">Ship this workspace to Streamlit Community Cloud from the login screen when you're ready to publish.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.divider()
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state["user"] = None
        st.rerun()
