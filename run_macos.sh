#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv312" ]; then
  python3 -m venv .venv312
fi

source .venv312/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
exec streamlit run streamlit_app.py
