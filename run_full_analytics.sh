#!/bin/bash
# Run full analytics pipeline for an experiment
# Usage: ./run_full_analytics.sh <data_dir>

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"
DATA_DIR_REL="$1"

if [ -z "$DATA_DIR_REL" ]; then
    echo "Usage: $0 <data_dir>"
    exit 1
fi

# Convert to absolute path
DATA_DIR="$REPO_ROOT/$DATA_DIR_REL"

cd "$SCRIPTS_DIR"
[ -f "$REPO_ROOT/.venv/bin/activate" ] && source "$REPO_ROOT/.venv/bin/activate"
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "Full Analytics Pipeline"
echo "Data directory: $DATA_DIR"
echo "Started at: $(date)"
echo "=========================================="

echo ""
echo "=== Step 1: Linguistic Features Extraction ==="
echo "Started at: $(date)"
python -u linguistic_features.py --data-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Step 2: Segment-Level Contradiction Detection ==="
echo "Started at: $(date)"
python -u detect_contradictions.py --data-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Step 3: Segment-Level Judge Verification ==="
echo "Started at: $(date)"
python -u judge_contradictions.py --data-dir "$DATA_DIR" --rate-limit 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Step 4: Privacy Washing Index Computation ==="
echo "Started at: $(date)"
python -u privacy_washing_index.py --data-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Step 5: Contradiction Report Generation ==="
echo "Started at: $(date)"
python -u contradiction_report.py --data-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=========================================="
echo "Full Analytics Complete!"
echo "Finished at: $(date)"
echo "=========================================="
