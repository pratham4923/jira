# ProjectFlow

ProjectFlow is a Streamlit-based Jira-style workspace for task execution, sprint planning, reporting, and team administration.

## Features

- Login and account creation
- Admin user management
- Drag-and-drop task board
- Backlog and sprint planning
- Reports dashboard
- Streamlit Community Cloud deploy button
- Windows and macOS launcher scripts

## Stack

- Python
- Streamlit
- SQLAlchemy
- SQLite

## Run locally

### Windows

Double-click `run_windows.bat`

### macOS

Double-click `run_macos.command`

Or run:

```bash
bash run_macos.sh
```

### Manual

```bash
python -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv312
.venv312\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Default local admin

The repository does not ship with a database file.

Create the first account from the UI, or seed your own local database if you want a preset admin user.

## Project structure

```text
.
|- app.py
|- streamlit_app.py
|- database.py
|- requirements.txt
|- pages/
|- public/
|- utils/
|- run_windows.bat
|- run_macos.sh
|- run_macos.command
```

## Deployment

This app is ready for Streamlit deployment.

- Main entrypoint: `streamlit_app.py`
- Dependencies: `requirements.txt`

You can also deploy from the in-app Streamlit deploy button.
