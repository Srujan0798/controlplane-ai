#!/usr/bin/env bash
# Freeze installed Python packages into submission/sbom-pip-freeze.txt
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/submission/sbom-pip-freeze.txt"
mkdir -p "$ROOT/submission"
if [[ -x "$ROOT/.venv/bin/pip" ]]; then
  "$ROOT/.venv/bin/pip" freeze > "$OUT"
elif command -v pip >/dev/null 2>&1; then
  pip freeze > "$OUT"
else
  python3 -m pip freeze > "$OUT"
fi
echo "wrote $OUT ($(wc -l < "$OUT" | tr -d ' ') packages)"
