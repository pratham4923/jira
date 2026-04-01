import streamlit as st


def inject_page_css() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {
            max-width: none;
            padding-left: 20rem;
            padding-right: 2rem;
            padding-top: 1rem;
        }

        div[data-testid="stMarkdownContainer"] p {
            margin-bottom: 0;
        }

        .pf-topbar {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            padding: 1.5rem 1.6rem;
            border: 1px solid rgba(255, 248, 238, 0.07);
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(255, 153, 92, 0.12), transparent 28%),
                rgba(12, 14, 20, 0.78);
            box-shadow: 0 20px 70px rgba(0, 0, 0, 0.24);
            backdrop-filter: blur(16px);
        }

        .pf-kicker {
            font-size: 0.72rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: rgba(248, 242, 232, 0.52);
            margin-bottom: 0.7rem;
            display: block;
        }

        .pf-title {
            margin: 0;
            font-size: clamp(2rem, 3vw, 3.8rem);
            line-height: 0.96;
            color: #fff7ef;
        }

        .pf-subtitle {
            margin-top: 0.8rem;
            max-width: 48rem;
            color: rgba(248, 242, 232, 0.7);
            font-size: 1rem;
            line-height: 1.5;
        }

        .pf-userpill {
            display: inline-flex;
            align-items: center;
            gap: 0.85rem;
            padding: 0.75rem 0.95rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 248, 238, 0.08);
            background: rgba(255, 248, 238, 0.03);
        }

        .pf-userbadge {
            width: 2.4rem;
            height: 2.4rem;
            border-radius: 50%;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, #f6b36a 0%, #ff8e52 100%);
            color: #27170d;
            font-weight: 800;
        }

        .pf-usercopy strong {
            display: block;
            color: #fff7ef;
            font-size: 0.98rem;
        }

        .pf-usercopy span {
            color: rgba(248, 242, 232, 0.55);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .pf-metric {
            padding: 1.15rem 1.2rem;
            border-radius: 22px;
            border: 1px solid rgba(255, 248, 238, 0.07);
            background: rgba(14, 17, 25, 0.82);
            backdrop-filter: blur(14px);
            min-height: 100%;
        }

        .pf-metric-label {
            display: block;
            color: rgba(248, 242, 232, 0.56);
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .pf-metric-value {
            display: block;
            color: #fff7ef;
            font-family: "Space Grotesk", sans-serif;
            font-size: clamp(1.8rem, 2.4vw, 2.6rem);
            line-height: 1;
        }

        .pf-metric-note {
            display: block;
            margin-top: 0.55rem;
            color: rgba(248, 242, 232, 0.62);
            font-size: 0.92rem;
        }

        .pf-panel {
            border: 1px solid rgba(255, 248, 238, 0.07);
            border-radius: 26px;
            background: rgba(14, 17, 25, 0.82);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.22);
            overflow: hidden;
        }

        .pf-panel-inner {
            padding: 1.35rem;
        }

        .pf-panel-title {
            margin: 0;
            color: #fff7ef;
            font-size: 1.12rem;
            letter-spacing: -0.03em;
        }

        .pf-panel-subtitle {
            margin-top: 0.35rem;
            color: rgba(248, 242, 232, 0.56);
            font-size: 0.92rem;
        }

        .pf-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }

        .pf-chip {
            padding: 0.5rem 0.75rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 248, 238, 0.07);
            background: rgba(255, 248, 238, 0.03);
            color: rgba(248, 242, 232, 0.76);
            font-size: 0.82rem;
        }

        .pf-column-shell {
            padding: 0.95rem;
            border: 1px solid rgba(255, 248, 238, 0.06);
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(255, 248, 238, 0.03), rgba(255, 248, 238, 0.01));
        }

        .pf-column-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.9rem;
        }

        .pf-column-top strong {
            color: #fff7ef;
            font-size: 1rem;
        }

        .pf-column-top span {
            min-width: 2rem;
            text-align: center;
            padding: 0.35rem 0.55rem;
            border-radius: 999px;
            background: rgba(255, 248, 238, 0.06);
            color: rgba(248, 242, 232, 0.76);
            font-size: 0.78rem;
        }

        .pf-task {
            padding: 1rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 248, 238, 0.06);
            background: rgba(8, 10, 15, 0.8);
            margin-bottom: 0.7rem;
        }

        .pf-task-type {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: rgba(248, 242, 232, 0.58);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
        }

        .pf-task-type::before {
            content: "";
            width: 0.5rem;
            height: 0.5rem;
            border-radius: 50%;
            background: #f6b36a;
            box-shadow: 0 0 18px rgba(246, 179, 106, 0.55);
        }

        .pf-task-title {
            display: block;
            margin-top: 0.55rem;
            color: #fff7ef;
            font-weight: 700;
            font-size: 1rem;
        }

        .pf-task-desc {
            display: block;
            margin-top: 0.45rem;
            color: rgba(248, 242, 232, 0.58);
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .pf-task-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
            margin-top: 0.8rem;
        }

        .pf-priority {
            display: inline-flex;
            padding: 0.35rem 0.62rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            background: rgba(255, 177, 102, 0.12);
            color: #ffd6b0;
        }

        .pf-assignee {
            color: rgba(248, 242, 232, 0.78);
            font-size: 0.82rem;
        }

        .pf-list-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.1rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 248, 238, 0.06);
            background: rgba(255, 248, 238, 0.025);
            margin-bottom: 0.8rem;
        }

        .pf-list-title {
            color: #fff7ef;
            font-weight: 700;
            display: block;
        }

        .pf-list-meta {
            color: rgba(248, 242, 232, 0.56);
            font-size: 0.88rem;
            margin-top: 0.3rem;
        }

        .pf-empty {
            padding: 2rem 1.4rem;
            text-align: center;
            color: rgba(248, 242, 232, 0.62);
        }

        @media (max-width: 1100px) {
            .main .block-container {
                padding-left: 2rem;
            }
        }

        @media (max-width: 780px) {
            .pf-topbar,
            .pf-list-row {
                flex-direction: column;
            }

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(title: str, subtitle: str, kicker: str = "ProjectFlow") -> None:
    user = st.session_state.get("user") or {}
    username = user.get("username", "User")
    role = user.get("role", "Workspace member")
    initial = username[:1].upper() if username else "U"
    st.markdown(
        f"""
        <div class="pf-topbar">
            <div>
                <span class="pf-kicker">{kicker}</span>
                <h1 class="pf-title">{title}</h1>
                <p class="pf-subtitle">{subtitle}</p>
            </div>
            <div class="pf-userpill">
                <div class="pf-userbadge">{initial}</div>
                <div class="pf-usercopy">
                    <strong>{username}</strong>
                    <span>{role}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
