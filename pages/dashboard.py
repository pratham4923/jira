from pathlib import Path

import streamlit as st
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from streamlit_sortables import sort_items

from database import Sprint, Task, User, get_db
from utils import sidebar, ui

sidebar.render_sidebar(active_page="dashboard")
ui.inject_page_css()

st.markdown(
    """
    <style>
    .pf-board-wrap {
        margin-top: 1rem;
    }

    .pf-stage-panel {
        margin-top: 1rem;
        padding: 1.2rem;
        border: 1px solid rgba(255, 248, 238, 0.07);
        border-radius: 28px;
        background:
            radial-gradient(circle at top left, rgba(246, 179, 106, 0.08), transparent 18%),
            linear-gradient(180deg, rgba(14, 17, 25, 0.96), rgba(10, 12, 18, 0.98));
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.18);
    }

    .pf-board-toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .pf-board-note {
        color: rgba(248, 242, 232, 0.62);
        font-size: 0.93rem;
    }

    .pf-board-highlight {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.55rem 0.8rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 248, 238, 0.08);
        background: rgba(255, 248, 238, 0.03);
        color: rgba(248, 242, 232, 0.74);
        font-size: 0.84rem;
    }

    .pf-board-highlight::before {
        content: "";
        width: 0.55rem;
        height: 0.55rem;
        border-radius: 50%;
        background: linear-gradient(135deg, #f6b36a 0%, #ff8e52 100%);
        box-shadow: 0 0 18px rgba(255, 142, 82, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ui.render_topbar(
    title="Execution board",
    subtitle="A denser Jira-style board surface with drag-and-drop flow between delivery lanes.",
    kicker="Delivery Surface",
)

db = next(get_db())
tasks = (
    db.query(Task)
    .options(joinedload(Task.assignee))
    .order_by(Task.status.asc(), Task.sort_order.asc(), Task.id.asc())
    .all()
)
sprints = db.query(Sprint).order_by(Sprint.id.asc()).all()
users = db.query(User).order_by(User.username.asc()).all()
uploads_root = Path("uploads")
shared_uploads_dir = uploads_root / "shared-space"
shared_uploads_dir.mkdir(parents=True, exist_ok=True)

columns = ["To Do", "In Progress", "In Review", "Done"]
status_meta = {
    "To Do": {"tone": "Queue", "note": "Scoped and ready for pickup"},
    "In Progress": {"tone": "Execution", "note": "Actively moving through delivery"},
    "In Review": {"tone": "Review", "note": "Awaiting signoff or revision"},
    "Done": {"tone": "Complete", "note": "Closed with delivery confidence"},
}


def format_task_label(task: Task) -> str:
    assignee_name = task.assignee.username if task.assignee and task.assignee.username else "Unassigned"
    return f"#{task.id} {task.title} | {task.priority} | {assignee_name}"


def next_sort_order(status: str) -> int:
    max_value = db.query(func.max(Task.sort_order)).filter(Task.status == status).scalar()
    return (max_value or 0) + 1


def persist_board_state(sorted_containers):
    task_map = {task.id: task for task in tasks}
    changed = False

    for lane_index, container in enumerate(sorted_containers):
        target_status = columns[lane_index]
        for item_index, item_label in enumerate(container["items"], start=1):
            if not item_label.startswith("#"):
                continue
            task_id = int(item_label.split(" ", 1)[0][1:])
            task = task_map.get(task_id)
            if task is None:
                continue
            if task.status != target_status or task.sort_order != item_index:
                task.status = target_status
                task.sort_order = item_index
                changed = True

    if changed:
        db.commit()
        st.toast("Board updated", icon=":material/check_circle:")
        st.rerun()


def save_uploaded_files(uploaded_files) -> int:
    saved_count = 0
    for uploaded_file in uploaded_files:
        relative_name = Path(uploaded_file.name)
        safe_parts = [part for part in relative_name.parts if part not in ("", ".", "..")]
        if not safe_parts:
            continue
        target_path = shared_uploads_dir.joinpath(*safe_parts)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(uploaded_file.getbuffer())
        saved_count += 1
    return saved_count


def list_uploaded_files():
    return sorted([path for path in shared_uploads_dir.rglob("*") if path.is_file()], key=lambda p: str(p).lower())


total_tasks = len(tasks)
done = len([task for task in tasks if task.status == "Done"])
in_progress = len([task for task in tasks if task.status in {"In Progress", "In Review"}])
completion_rate = round(done / total_tasks * 100) if total_tasks else 0
active_sprint = sprints[-1].name if sprints else "No sprint active"
assigned_tasks = len([task for task in tasks if task.assignee_id is not None])
top_load = max((sum(1 for task in tasks if task.assignee_id == user.id) for user in users), default=0)

metric_cols = st.columns(4, gap="medium")
metrics = [
    ("Active sprint", active_sprint, f"{len(sprints)} sprint lanes configured"),
    ("Completion", f"{completion_rate}%", f"{done} tasks shipped cleanly"),
    ("Assigned", assigned_tasks, f"{len(users)} workspace members active"),
    ("Peak load", top_load, "Highest task count on one assignee"),
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

info_col, deploy_col = st.columns([2, 1], gap="medium")
with info_col:
    st.markdown(
        f"""
        <div class="pf-panel" style="margin-top:1rem;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Board posture</h3>
                <p class="pf-panel-subtitle">Drag any card between lanes to change status. Order inside a lane is also persisted.</p>
                <div class="pf-chip-row" style="margin-top:1rem;">
                    <span class="pf-chip">{len([t for t in tasks if t.status == 'To Do'])} queued</span>
                    <span class="pf-chip">{in_progress} active or under review</span>
                    <span class="pf-chip">{done} completed</span>
                    <span class="pf-chip">{len(tasks) - assigned_tasks} unassigned</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with deploy_col:
    st.link_button("Deploy on Streamlit", "https://share.streamlit.io/deploy", use_container_width=True)


@st.dialog("Create New Task")
def create_task_modal(default_status: str) -> None:
    with st.form("create_task_form"):
        title = st.text_input("Title", placeholder="What needs to be done?")
        desc = st.text_area("Description", placeholder="Add context that helps the team act.")
        c1, c2 = st.columns(2)
        task_type = c1.selectbox("Type", ["Task", "Story", "Bug", "Epic"])
        priority = c2.selectbox("Priority", ["Low", "Medium", "High", "Highest"], index=1)
        user_opts = {f"{u.username} ({u.role})": u.id for u in users}
        assignee_label = st.selectbox("Assignee", list(user_opts.keys())) if user_opts else None
        submit = st.form_submit_button("Create task", use_container_width=True)

        if submit and title:
            new_task = Task(
                title=title,
                description=desc,
                type=task_type,
                priority=priority,
                status=default_status,
                sort_order=next_sort_order(default_status),
                assignee_id=user_opts[assignee_label] if assignee_label else None,
            )
            db.add(new_task)
            db.commit()
            st.rerun()


task_lookup = {format_task_label(task): task for task in tasks}
sortable_items = []
for status in columns:
    lane_tasks = [format_task_label(task) for task in tasks if task.status == status]
    meta = status_meta[status]
    sortable_items.append(
        {
            "header": f"{status} - {meta['tone']} ({len(lane_tasks)})",
            "items": lane_tasks,
        }
    )

sortable_style = """
.sortable-component {
    display: grid;
    grid-template-columns: repeat(4, minmax(240px, 1fr));
    gap: 1rem;
    align-items: start;
}
.sortable-container {
    background: linear-gradient(180deg, rgba(255,248,238,0.035), rgba(255,248,238,0.012));
    border: 1px solid rgba(255,248,238,0.07);
    border-radius: 24px;
    min-height: 420px;
    overflow: hidden;
}
.sortable-container-header {
    padding: 0.95rem 1rem;
    background: rgba(255,248,238,0.035);
    color: #fff7ef;
    font-family: "Space Grotesk", sans-serif;
    font-size: 1rem;
    border-bottom: 1px solid rgba(255,248,238,0.06);
}
.sortable-container-body {
    padding: 0.8rem;
    min-height: 320px;
}
.sortable-item, .sortable-item:hover {
    background: linear-gradient(180deg, rgba(11,13,19,0.96), rgba(17,20,28,0.96));
    border: 1px solid rgba(255,248,238,0.06);
    border-left: 3px solid #f6b36a;
    border-radius: 18px;
    color: #fff7ef;
    padding: 0.95rem 0.9rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    font-size: 0.92rem;
    line-height: 1.35;
}
.sortable-item.dragging {
    border-color: rgba(255,142,82,0.45);
    box-shadow: 0 18px 40px rgba(255,142,82,0.18);
}
@media (max-width: 1100px) {
    .sortable-component {
        grid-template-columns: repeat(2, minmax(240px, 1fr));
    }
}
@media (max-width: 700px) {
    .sortable-component {
        grid-template-columns: 1fr;
    }
}
"""

st.markdown(
    """
    <div class="pf-stage-panel">
        <div class="pf-board-toolbar">
            <div>
                <h3 class="pf-panel-title" style="margin-bottom:0.35rem;">Drag-and-drop workflow</h3>
                <div class="pf-board-note">Move cards to the next section or reorder within a lane. The board saves lane and position.</div>
            </div>
            <div class="pf-board-highlight">Live board ordering is enabled</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

sorted_board = sort_items(
    sortable_items,
    multi_containers=True,
    direction="horizontal",
    custom_style=sortable_style,
    key="jira_board_sortable",
)
persist_board_state(sorted_board)

add_cols = st.columns(4, gap="medium")
for idx, col_name in enumerate(columns):
    with add_cols[idx]:
        if st.button(f"Add task to {col_name}", key=f"add_task_{idx}", use_container_width=True):
            create_task_modal(col_name)

latest_tasks = sorted(tasks, key=lambda task: task.updated_at or task.created_at, reverse=True)[:5]

st.markdown(
    """
    <div class="pf-panel" style="margin-top:1rem;">
        <div class="pf-panel-inner">
            <h3 class="pf-panel-title">Latest movement</h3>
            <p class="pf-panel-subtitle">Recent work changes across the board.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not latest_tasks:
    st.markdown('<div class="pf-empty">No work items yet. Create the first task to start the board.</div>', unsafe_allow_html=True)
else:
    for task in latest_tasks:
        assignee_name = task.assignee.username if task.assignee and task.assignee.username else "Unassigned"
        st.markdown(
            f"""
            <div class="pf-list-row">
                <div>
                    <span class="pf-list-title">{task.title}</span>
                    <div class="pf-list-meta">{task.type} | {task.priority} | {task.status}</div>
                </div>
                <div style="color:rgba(248,242,232,0.62);">{assignee_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

uploaded_files = list_uploaded_files()

st.markdown(
    """
    <div class="pf-panel" style="margin-top:1rem;">
        <div class="pf-panel-inner">
            <h3 class="pf-panel-title">Shared files</h3>
            <p class="pf-panel-subtitle">Upload single files or a whole folder. Folder structure is preserved when the browser provides relative paths.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

upload_col, info_col = st.columns([1.5, 1], gap="medium")

with upload_col:
    picked_files = st.file_uploader(
        "Upload files or folders",
        accept_multiple_files="directory",
        key="shared_uploads",
        help="Choose individual files or select a folder to upload everything inside it.",
    )
    if st.button("Save uploaded files", use_container_width=True, key="save_shared_uploads"):
        if not picked_files:
            st.warning("Choose at least one file or folder first.")
        else:
            saved_count = save_uploaded_files(picked_files)
            st.success(f"Saved {saved_count} file(s) to the shared workspace.")
            st.rerun()

with info_col:
    st.markdown(
        f"""
        <div class="pf-panel" style="height:100%;">
            <div class="pf-panel-inner">
                <h3 class="pf-panel-title">Storage snapshot</h3>
                <p class="pf-panel-subtitle">{len(uploaded_files)} file(s) currently available in the shared workspace.</p>
                <div class="pf-chip-row" style="margin-top:1rem;">
                    <span class="pf-chip">Directory upload enabled</span>
                    <span class="pf-chip">Download from browser</span>
                    <span class="pf-chip">Shared path: uploads/shared-space</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if not uploaded_files:
    st.markdown('<div class="pf-empty">No shared files yet. Upload a file or folder to populate this area.</div>', unsafe_allow_html=True)
else:
    for file_path in uploaded_files:
        relative_path = file_path.relative_to(shared_uploads_dir).as_posix()
        file_bytes = file_path.read_bytes()
        file_col, download_col = st.columns([2.2, 0.8], gap="medium")
        with file_col:
            st.markdown(
                f"""
                <div class="pf-list-row">
                    <div>
                        <span class="pf-list-title">{file_path.name}</span>
                        <div class="pf-list-meta">{relative_path}</div>
                    </div>
                    <div style="color:rgba(248,242,232,0.62);">{len(file_bytes):,} bytes</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with download_col:
            st.download_button(
                "Download",
                data=file_bytes,
                file_name=file_path.name,
                mime="application/octet-stream",
                key=f"download_{relative_path}",
                use_container_width=True,
            )
