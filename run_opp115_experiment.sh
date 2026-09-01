#!/bin/bash
# OPP-115 Experiment Replication
# Run all 4 stages of the contradiction detection pipeline

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"
DATA_DIR="opp115_experiment_20260130"

cd "$SCRIPTS_DIR"
[ -f "$REPO_ROOT/.venv/bin/activate" ] && source "$REPO_ROOT/.venv/bin/activate"

# Force unbuffered Python output for real-time logging
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "OPP-115 Experiment Replication"
echo "Data directory: $DATA_DIR"
echo "Started at: $(date)"
echo "=========================================="

echo ""
echo "=== Stage 1: Statement Extraction ==="
echo "Started at: $(date)"
python -u extract_statements.py --data-dir "$DATA_DIR" --delay 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Stage 2: NLI Contradiction Detection ==="
echo "Started at: $(date)"
python -u detect_statement_contradictions.py --data-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Stage 3: 3-LLM Judge Verification ==="
echo "Started at: $(date)"
python -u judge_statement_contradictions.py --data-dir "$DATA_DIR" --concurrency 20 --rate-limit 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Stage 4: Analysis Report ==="
echo "Started at: $(date)"
python -u statement_contradiction_analysis.py --data-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=========================================="
echo "OPP-115 Experiment Complete!"
echo "Finished at: $(date)"
echo "=========================================="
