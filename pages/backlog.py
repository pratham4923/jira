import streamlit as st
from sqlalchemy.orm import joinedload

from database import Sprint, Task, get_db
from utils import sidebar, ui

sidebar.render_sidebar(active_page="backlog")
ui.inject_page_css()
ui.render_topbar(
    title="Backlog and planning",
    subtitle="Shape the next sprint, distribute unfinished work, and keep planning decisions visible.",
    kicker="Planning Surface",
)

db = next(get_db())
sprints = db.query(Sprint).all()
tasks = db.query(Task).options(joinedload(Task.assignee)).filter(Task.sprint_id == None).all()


@st.dialog("Create New Sprint")
def create_sprint_modal() -> None:
    with st.form("create_sprint_form"):
        name = st.text_input("Sprint name", placeholder="ProjectFlow Sprint 1")
        c1, c2 = st.columns(2)
        start_date = c1.date_input("Start date")
        end_date = c2.date_input("End date")
        goal = st.text_input("Sprint goal", placeholder="What outcome should this sprint deliver?")
        submit = st.form_submit_button("Start sprint", use_container_width=True)
        if submit and name:
            new_sprint = Sprint(name=name, start_date=start_date, end_date=end_date, goal=goal, status="Planning")
            db.add(new_sprint)
            db.commit()
            st.rerun()


summary_cols = st.columns(4, gap="medium")
summary_items = [
    ("Sprints", len(sprints), "Planning lanes available"),
    ("Backlog tasks", len(tasks), "Items waiting for assignment"),
    ("With goals", len([s for s in sprints if s.goal]), "Sprints carrying a clear mission"),
    ("Ready now", len([t for t in tasks if t.priority in {"High", "Highest"}]), "High-priority backlog work"),
]

for col, (label, value, note) in zip(summary_cols, summary_items):
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

action_col = st.columns([1, 3])[0]
with action_col:
    if st.button("Create sprint", use_container_width=True):
        create_sprint_modal()

st.markdown(
    """
    <div class="pf-panel" style="margin-top:1rem;">
        <div class="pf-panel-inner">
            <h3 class="pf-panel-title">Sprint runway</h3>
            <p class="pf-panel-subtitle">Every sprint holds dates, intent, and a visible planning state.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not sprints:
    st.markdown('<div class="pf-empty">No sprints yet. Create one to start structuring the backlog.</div>', unsafe_allow_html=True)
else:
    for sprint in sprints:
        date_range = f"{sprint.start_date.strftime('%b %d, %Y') if sprint.start_date else 'No start'} to {sprint.end_date.strftime('%b %d, %Y') if sprint.end_date else 'No end'}"
        goal = sprint.goal if sprint.goal else "No goal set yet."
        st.markdown(
            f"""
            <div class="pf-list-row">
                <div>
                    <span class="pf-list-title">{sprint.name}</span>
                    <div class="pf-list-meta">{date_range}</div>
                </div>
                <div style="max-width:24rem; color:rgba(248,242,232,0.74);">{goal}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="pf-panel" style="margin-top:1rem;">
        <div class="pf-panel-inner">
            <h3 class="pf-panel-title">Backlog intake</h3>
            <p class="pf-panel-subtitle">Assign work to a sprint without losing the task context.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not tasks:
    st.markdown('<div class="pf-empty">The backlog is clear. Everything is already assigned.</div>', unsafe_allow_html=True)
else:
    sprint_opts = {"Move to sprint...": None}
    sprint_opts.update({s.name: s.id for s in sprints})

    for task in tasks:
        left, right = st.columns([2.5, 1], gap="medium")
        with left:
            assignee_name = task.assignee.username if task.assignee and task.assignee.username else "Unassigned"
            st.markdown(
                f"""
                <div class="pf-list-row">
                    <div>
                        <span class="pf-list-title">{task.title}</span>
                        <div class="pf-list-meta">{task.type} • {task.priority} • {assignee_name}</div>
                    </div>
                    <div style="max-width:26rem; color:rgba(248,242,232,0.62);">{(task.description or "No description yet.")[:120]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            selected_sprint_name = st.selectbox(
                f"Sprint assign {task.id}",
                list(sprint_opts.keys()),
                key=f"sprint_select_{task.id}",
                label_visibility="collapsed",
            )
            if sprint_opts[selected_sprint_name] is not None:
                task.sprint_id = sprint_opts[selected_sprint_name]
                db.commit()
                st.rerun()
