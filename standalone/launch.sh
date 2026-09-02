#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
mkdir -p out work
echo "AZbot Local — 127.0.0.1:7747"
echo "Slingshot Prep only. No upload."
if command -v xdg-open >/dev/null 2>&1; then
  (sleep 1; xdg-open "http://127.0.0.1:7747") >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then
  (sleep 1; open "http://127.0.0.1:7747") >/dev/null 2>&1 &
fi
exec python3 "$DIR/app/server.py"
