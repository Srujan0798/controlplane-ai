#!/usr/bin/env bash
# Human runs AFTER: gh auth login -h github.com
set -euo pipefail
cd "$(dirname "$0")/.."
gh auth status
# Create public repo if missing, else ensure public
if ! gh repo view srujansai/controlplane-ai >/dev/null 2>&1; then
  gh repo create controlplane-ai --public --source=. --remote=origin --push || true
fi
gh repo edit srujansai/controlplane-ai --visibility public || true
git push -u origin feature/round2-elevation
git push origin --tags || true
# optional: also push main if desired
echo "Public URL: https://github.com/Srujan0798/controlplane-ai"
gh repo view Srujan0798/controlplane-ai --json url,visibility,isPrivate
