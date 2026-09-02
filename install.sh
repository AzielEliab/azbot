#!/usr/bin/env bash
# AZBot one-click install. Counted download via this project's Worker.
# Usage: curl -fsSL https://azbot-download-tracker.vibelock.workers.dev/install.sh | bash
set -euo pipefail

HOST="${AZBOT_HOME_HOST:-https://azbot-download-tracker.vibelock.workers.dev}"
ASSET="${AZBOT_HOME_ASSET:-azbot-0.2.0.tar.gz}"
WORKDIR="${AZBOT_HOME:-$HOME/azbot}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "Downloading counted tarball from ${HOST}/download (User-Agent Mozilla/5.0)…"
curl -fsSL -A 'Mozilla/5.0' "${HOST}/download?asset=${ASSET}" -o "${ASSET}"

tar -xzf "${ASSET}"
DIR="$(find . -maxdepth 1 -type d -name 'azbot-*' | head -n 1)"
if [ -n "${DIR}" ]; then
  cd "${DIR}"
fi

python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

echo
echo "Installed AZBot."
echo "Run:  azbot ui"
echo "Then open http://127.0.0.1:8870  (loopback only)"
echo "Author: Aziel Eliab."
