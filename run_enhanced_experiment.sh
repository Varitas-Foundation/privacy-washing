#!/bin/bash
# Enhanced Extraction Experiment with 3-LLM Panel
# Uses 3-LLM consensus extraction (v2 prompt with subject/aspect/scope/qualifiers)
# and enhanced filtering for both OPP-115 and OPPT corpora

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"
OUTPUT_BASE="$REPO_ROOT"

# Experiment date suffix
DATE_SUFFIX="20260131"

# Baseline directories for comparison
OPP115_BASELINE="opp115_experiment_20260130"
OPPT_BASELINE="oppt_experiment_20260130"

# New experiment directories
OPP115_DIR="opp115_experiment_enhanced_${DATE_SUFFIX}"
OPPT_DIR="oppt_experiment_enhanced_${DATE_SUFFIX}"

cd "$SCRIPTS_DIR"
[ -f "$REPO_ROOT/.venv/bin/activate" ] && source "$REPO_ROOT/.venv/bin/activate"

# Force unbuffered Python output for real-time logging
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "Enhanced Extraction Experiment (3-LLM Panel)"
echo "Date: $(date)"
echo "=========================================="

# Create experiment directories
mkdir -p "$OUTPUT_BASE/$OPP115_DIR"
mkdir -p "$OUTPUT_BASE/$OPPT_DIR"

# Copy segment files from baseline experiments
cp "$OUTPUT_BASE/$OPP115_BASELINE/all_segments.json" "$OUTPUT_BASE/$OPP115_DIR/"
cp "$OUTPUT_BASE/$OPPT_BASELINE/all_segments.json" "$OUTPUT_BASE/$OPPT_DIR/"

echo ""
echo "=========================================="
echo "Part 1: OPP-115 Enhanced Experiment"
echo "=========================================="

echo ""
echo "=== Stage 1: 3-LLM Panel Statement Extraction ==="
echo "Started at: $(date)"
python -u extract_statements_multimodel.py --data-dir "$OPP115_DIR" --concurrency 50
echo "Completed at: $(date)"

echo ""
echo "=== Stage 2: Enhanced Contradiction Detection ==="
echo "Started at: $(date)"
python -u detect_statement_contradictions.py --data-dir "$OPP115_DIR" --enhanced-filtering
echo "Completed at: $(date)"

echo ""
echo "=== Stage 3: 3-LLM Judge Verification ==="
echo "Started at: $(date)"
python -u judge_statement_contradictions.py --data-dir "$OPP115_DIR" --concurrency 20 --rate-limit 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Stage 4: Analysis Report ==="
echo "Started at: $(date)"
python -u statement_contradiction_analysis.py --data-dir "$OPP115_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Stage 5: Version Comparison ==="
echo "Started at: $(date)"
python -u compare_extraction_versions.py --v1-dir "$OPP115_BASELINE" --v2-dir "$OPP115_DIR"
echo "Completed at: $(date)"

echo ""
echo "=========================================="
echo "Part 2: OPPT Enhanced Experiment"
echo "=========================================="

echo ""
echo "=== Stage 1: 3-LLM Panel Statement Extraction (with annotations) ==="
echo "Started at: $(date)"
# OPPT uses annotation-guided extraction, output directly to experiment folder
python -u extract_statements_multimodel.py --output "$OUTPUT_BASE/$OPPT_DIR/statements.json" --concurrency 50
echo "Completed at: $(date)"

echo ""
echo "=== Stage 2: Enhanced Contradiction Detection ==="
echo "Started at: $(date)"
python -u detect_statement_contradictions.py --data-dir "$OPPT_DIR" --enhanced-filtering
echo "Completed at: $(date)"

echo ""
echo "=== Stage 3: 3-LLM Judge Verification ==="
echo "Started at: $(date)"
python -u judge_statement_contradictions.py --data-dir "$OPPT_DIR" --concurrency 20 --rate-limit 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Stage 4: Analysis Report ==="
echo "Started at: $(date)"
python -u statement_contradiction_analysis.py --data-dir "$OPPT_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Stage 5: Version Comparison ==="
echo "Started at: $(date)"
python -u compare_extraction_versions.py --v1-dir "$OPPT_BASELINE" --v2-dir "$OPPT_DIR"
echo "Completed at: $(date)"

echo ""
echo "=========================================="
echo "Enhanced Experiment Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  OPP-115: $OUTPUT_BASE/$OPP115_DIR"
echo "  OPPT:    $OUTPUT_BASE/$OPPT_DIR"
echo ""
echo "Comparison reports:"
echo "  - $OUTPUT_BASE/$OPP115_DIR/comparison_report.md"
echo "  - $OUTPUT_BASE/$OPPT_DIR/comparison_report.md"
echo ""
echo "Finished at: $(date)"
