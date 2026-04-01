import streamlit as st

from database import Task, User, get_db
from utils import sidebar, ui

sidebar.render_sidebar(active_page="admin")
ui.inject_page_css()
ui.render_topbar(
    title="Admin control",
    subtitle="Manage team access, rebalance roles, and keep governance operations inside the same visual system.",
    kicker="Operations Surface",
)

db = next(get_db())
users = db.query(User).all()
tasks = db.query(Task).all()

role_options = [
    "Admin",
    "Data Collection and Preprocessing",
    "Architecture Design",
    "Coding",
    "Testing",
    "Deployment",
]

metric_cols = st.columns(4, gap="medium")
metrics = [
    ("Users", len(users), "Active workspace identities"),
    ("Admins", len([u for u in users if u.role == "Admin"]), "Accounts with broad access"),
    ("Assigned tasks", len([t for t in tasks if t.assignee_id]), "Work tied to a user"),
    ("Open tasks", len([t for t in tasks if t.status != "Done"]), "Still in execution"),
]

for col, (label, value, note) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="pf-metric">
                <span class="pf-metric-label">{label}</span>
                <span class="pf-metric-value">{value}</span>
                <span class="pf-metric-note">{note}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="pf-panel" style="margin-top:1rem;">
        <div class="pf-panel-inner">
            <h3 class="pf-panel-title">Team management</h3>
            <p class="pf-panel-subtitle">Adjust access without leaving the workspace context.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not users:
    st.markdown('<div class="pf-empty">No users found in this workspace.</div>', unsafe_allow_html=True)
else:
    for user in users:
        cols = st.columns([1.8, 1.3, 0.9], gap="medium")
        is_current_user = str(user.id) == st.session_state["user"]["id"]

        with cols[0]:
            user_task_count = len([t for t in tasks if t.assignee_id == user.id])
            st.markdown(
                f"""
                <div class="pf-list-row">
                    <div>
                        <span class="pf-list-title">{user.username}</span>
                        <div class="pf-list-meta">{user.role} • {user_task_count} assigned tasks</div>
                    </div>
                    <div style="color:rgba(248,242,232,0.56);">{'Current session user' if is_current_user else 'Managed account'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with cols[1]:
            idx = role_options.index(user.role) if user.role in role_options else 0
            new_role = st.selectbox(
                f"Role {user.id}",
                role_options,
                index=idx,
                key=f"role_{user.id}",
                disabled=is_current_user,
                label_visibility="collapsed",
            )
            if new_role != user.role and not is_current_user:
                user.role = new_role
                db.commit()
                st.rerun()

        with cols[2]:
            if is_current_user:
                st.button("Current admin", disabled=True, key=f"cur_{user.id}", use_container_width=True)
            else:
                if st.button("Delete user", key=f"del_{user.id}", use_container_width=True):
                    db.query(Task).filter(Task.assignee_id == user.id).update({"assignee_id": None})
                    db.delete(user)
                    db.commit()
                    st.rerun()
