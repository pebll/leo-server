#!/usr/bin/env bash
# Start the website locally (no Docker) for quick testing.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  echo "Creating .venv…"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

cd src
echo "Serving http://127.0.0.1:8000/  (Ctrl+C to stop)"
exec uvicorn main:app --reload --host 127.0.0.1 --port 8000
