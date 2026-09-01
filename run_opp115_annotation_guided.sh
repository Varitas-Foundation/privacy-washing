#!/bin/bash
# OPP-115 Experiment with Annotation-Guided Statement Extraction
#
# Key change from previous runs: Uses OPP-115's original Does/Does Not polarity
# annotations instead of LLM inference for statement typing.
#
# Discovery: OPP-115 HAS polarity annotations (previously overlooked)
#   - 13,464 "Does" annotations (95.1%)
#   - 692 "Does Not" annotations (4.9%)
#
# This enables annotation-guided extraction matching the OPPT methodology.

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"
DATA_DIR="opp115_experiment_annotation_guided_20260203"

cd "$SCRIPTS_DIR"
[ -f "$REPO_ROOT/.venv/bin/activate" ] && source "$REPO_ROOT/.venv/bin/activate"

# Force unbuffered Python output for real-time logging
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "OPP-115 Experiment (Annotation-Guided)"
echo "Data directory: $DATA_DIR"
echo "Started at: $(date)"
echo "=========================================="

# Create experiment directory
FULL_DATA_DIR="$REPO_ROOT/$DATA_DIR"
mkdir -p "$FULL_DATA_DIR"

echo ""
echo "=== Stage 0: Extract OPP-115 Attributes ==="
echo "Extracting Does/Does Not polarity from original human annotations"
echo "Started at: $(date)"
python -u extract_opp115_attributes.py --output-dir "$DATA_DIR"
echo "Completed at: $(date)"

echo ""
echo "=== Stage 0b: Convert OPP-115 Segments ==="
echo "Converting OPP-115 to pipeline format"
echo "Started at: $(date)"
# Copy from existing conversion or run converter
if [ -f "$REPO_ROOT/opp115_experiment_20260130/all_segments.json" ]; then
    cp "$REPO_ROOT/opp115_experiment_20260130/all_segments.json" "$FULL_DATA_DIR/"
    echo "  Copied existing all_segments.json"
else
    python -u convert_opp115.py
    cp "$REPO_ROOT/opp115_experiment/all_segments.json" "$FULL_DATA_DIR/"
fi
echo "Completed at: $(date)"

echo ""
echo "=== Stage 1: Statement Extraction (3-LLM Panel, Annotation-Guided) ==="
echo "Using OPP-115 Does/Does Not annotations for PRACTICE/COMMITMENT typing"
echo "3 models: Claude Haiku 4.5, GPT-5-mini, Gemini-3-flash-preview"
echo "Started at: $(date)"
python -u extract_statements_multimodel.py --data-dir "$DATA_DIR" --concurrency 50
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
echo "OPP-115 Experiment (Annotation-Guided) Complete!"
echo "Finished at: $(date)"
echo ""
echo "Key difference from previous runs:"
echo "  - Uses OPP-115's original human annotations for Does/Does Not polarity"
echo "  - No LLM inference for statement typing"
echo "  - Matches OPPT methodology"
echo "=========================================="
