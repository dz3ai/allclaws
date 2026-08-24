#!/usr/bin/env bash
# Full-grid DRY-RUN: validates spec loading, driver wiring, ProcSpec build,
# worktree copying, result writing — for all 3 drivers x 3 tasks. NO API calls.
set -eu
cd /home/dannyz/src/github/allclaws/test_framework
rm -rf benchmark_results/longrun/*T*   # drop earlier dry-run dirs
/usr/bin/python3 -m longrun.cli run \
  --drivers aider,codex,kimi_cli \
  --tasks gh-issue-001,refactor-multi,feature-crud \
  --dry-run
echo "=== dry-run results ==="
/usr/bin/python3 - <<'PYEOF'
import json
from pathlib import Path

root = Path("benchmark_results/longrun")
runs_dir = sorted(d for d in root.iterdir() if d.name[4:5].isdigit() and "T" in d.name)[-1]
data = json.loads((runs_dir / "grid_summary.json").read_text())
print(f"run dir: {runs_dir.name} — {len(data['runs'])} runs")
for r in data["runs"]:
    print(f"  {r['platform']:8} {r['task_id']:15} {r['status']:8} argv0=...{r['argv'][0][-24:]}")
PYEOF
