#!/usr/bin/env bash
# Thin preflight until Core validators are wired. Does not replace Adaptoid-OS preflight.sh.
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "== dupe artifacts =="
if find . -name '* 2.md' -o -name '* 2.*' | grep -v node_modules | grep -v .git | grep .; then
  echo "FAIL: dupe artifacts present (FM-23)"
  exit 1
else
  echo "OK: no * 2.* dupes"
fi
echo "== pytest =="
if [ -d .venv ]; then source .venv/bin/activate; fi
pytest -q --tb=no
echo "PREFLIGHT-LITE: PASS"
