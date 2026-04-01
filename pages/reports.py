import pandas as pd
import streamlit as st
from sqlalchemy.orm import joinedload

from database import Task, get_db
from utils import sidebar, ui

sidebar.render_sidebar(active_page="reports")
ui.inject_page_css()
ui.render_topbar(
    title="Reports",
    subtitle="Read workload, completion, and distribution trends from a cleaner operating dashboard.",
    kicker="Insights Surface",
)

db = next(get_db())
tasks = db.query(Task).options(joinedload(Task.assignee)).all()

total_tasks = len(tasks)
completed_tasks = len([t for t in tasks if t.status == "Done"])
completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks else 0)
review_tasks = len([t for t in tasks if t.status == "In Review"])

metric_cols = st.columns(4, gap="medium")
metrics = [
    ("Total tasks", total_tasks, "All tracked work"),
    ("Done", completed_tasks, "Closed items"),
    ("Completion", f"{completion_rate}%", "Across the full board"),
    ("In review", review_tasks, "Awaiting final signoff"),
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

types_dict = {}
priorities_dict = {}
assignees_dict = {}
status_dict = {}

for task in tasks:
    types_dict[task.type] = types_dict.get(task.type, 0) + 1
    priorities_dict[task.priority] = priorities_dict.get(task.priority, 0) + 1
    status_dict[task.status] = status_dict.get(task.status, 0) + 1
    assignee_name = task.assignee.username if task.assignee else "Unassigned"
    assignees_dict[assignee_name] = assignees_dict.get(assignee_name, 0) + 1

insight_col, note_col = st.columns([2, 1], gap="medium")
with insight_col:
    st.markdown(
        f"""
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Decision notes</h3>
                <p class="pf-panel-subtitle">A fast read before drilling into charts.</p>
                <div class="pf-chip-row" style="margin-top:1rem;">
                    <span class="pf-chip">{max(status_dict, key=status_dict.get) if status_dict else "No status data"} is the largest lane</span>
                    <span class="pf-chip">{max(priorities_dict, key=priorities_dict.get) if priorities_dict else "No priority data"} appears most often</span>
                    <span class="pf-chip">{max(assignees_dict, key=assignees_dict.get) if assignees_dict else "No assignee data"} carries the highest load</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with note_col:
    st.markdown(
        """
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Reporting posture</h3>
                <p class="pf-panel-subtitle">Charts stay simple so operators can read them fast.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

row1 = st.columns(2, gap="medium")
row2 = st.columns(2, gap="medium")

with row1[0]:
    st.markdown(
        """
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Tasks by type</h3>
                <p class="pf-panel-subtitle">Distribution across work categories.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if types_dict:
        df_type = pd.DataFrame(list(types_dict.items()), columns=["Type", "Count"]).set_index("Type")
        st.bar_chart(df_type, color="#f6b36a", height=280)

with row1[1]:
    st.markdown(
        """
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Tasks by priority</h3>
                <p class="pf-panel-subtitle">Where urgency is concentrated.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if priorities_dict:
        df_pri = pd.DataFrame(list(priorities_dict.items()), columns=["Priority", "Count"]).set_index("Priority")
        st.bar_chart(df_pri, color="#ff8e52", height=280)

with row2[0]:
    st.markdown(
        """
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Assignee distribution</h3>
                <p class="pf-panel-subtitle">How work is spread across the team.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if assignees_dict:
        df_ans = pd.DataFrame(list(assignees_dict.items()), columns=["Assignee", "Count"]).set_index("Assignee")
        st.bar_chart(df_ans, color="#ffd29e", height=280)

with row2[1]:
    st.markdown(
        """
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Status distribution</h3>
                <p class="pf-panel-subtitle">Board health by lane.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if status_dict:
        df_stat = pd.DataFrame(list(status_dict.items()), columns=["Status", "Count"]).set_index("Status")
        st.bar_chart(df_stat, color="#ffc892", height=280)
