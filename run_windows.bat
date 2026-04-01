@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv312\Scripts\python.exe" (
  py -3.12 -m venv .venv312
)

call ".venv312\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
streamlit run streamlit_app.py
