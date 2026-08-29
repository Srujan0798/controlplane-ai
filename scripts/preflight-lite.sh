#!/usr/bin/env bash
# Thin preflight until Core validators are wired. Does not replace Adaptoid-OS preflight.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== dupe artifacts (tracked trees only) =="
hits=$(find . -type f \( -name '* 2.md' -o -name '* 2.*' -o -name '* copy.*' \) \
  ! -path '*/.git/*' \
  ! -path '*/.venv/*' \
  ! -path '*/.worktrees/*' \
  ! -path '*/node_modules/*' \
  ! -path '*/__pycache__/*' \
  ! -path '*/graphify-out/*' \
  ! -path '*/.data/*' \
  ! -path '*/.superpowers/*' \
  ! -path '*/.pytest_cache/*' \
  2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "FAIL: dupe artifacts present (FM-23)"
  echo "$hits"
  exit 1
else
  echo "OK: no * 2.* dupes in project trees"
fi
echo "== pytest =="
if [ -f .venv/bin/activate ]; then source .venv/bin/activate; fi
pytest -q --tb=no
echo "PREFLIGHT-LITE: PASS"
