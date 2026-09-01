#!/bin/bash
# Stability Experiment: Separated Extraction and Judge Panels (August 2026)
#
# Re-runs the full pipeline on both corpora with an updated, fully separated
# model configuration. The January/February 2026 runs remain the paper's
# primary reported results; this run is the stability/robustness experiment
# proposed in the paper's Future Work section. Three design changes:
#
#   1. SEPARATED PANELS (removes the extractor-judge overlap, Limitations):
#      - Extraction (western trio, stable endpoints):
#          anthropic/claude-haiku-4.5, openai/gpt-5.6-luna, google/gemini-3.7-flash
#      - Judging (Chinese trio, zero corpus conflict of interest, Ethics):
#          deepseek/deepseek-v4-flash-0731, z-ai/glm-5.3-flash, moonshotai/kimi-k3
#        DeepSeek, Zhipu, and Moonshot do not appear in the OPPT corpus, so no
#        judge evaluates its own provider's policy.
#        (kimi-k3 replaced qwen/qwen3.8-flash after the 2026-08-30 run: Qwen
#        endpoints 404 under strict OpenRouter data-policy settings.)
#
#   2. MATCHED FILTER CONFIGURATION: --enhanced-filtering is enabled for BOTH
#      corpora (the published OPP-115 run lacked the metadata compatibility
#      filters, which the paper flags as making the cross-corpus prevalence
#      difference uninterpretable).
#
#   3. SUB-THRESHOLD JUDGING: the judge stage runs with
#      --similarity-threshold 0.0, so ALL NLI-flagged pairs are judged,
#      including those below the published 0.5 judge-submission threshold
#      (441 OPPT + 1,118 OPP-115 in the published runs). Analysis can subset
#      by similarity to recover the published protocol and to measure recall
#      below the threshold.
#
# Fresh experiment directories mean a fresh judge cache: no legacy pairs can
# be carried over from earlier pair-generation passes.
#
# Known caveat carried forward: the OPP-115 Does/Does Not annotation join
# failed silently in the published run (segment-identifier mismatch; see
# paper Section 4.2). This script reuses the same input artifacts, so the
# join behavior is unchanged unless separately fixed in
# extract_statements_multimodel.py.

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"
OUTPUT_BASE="$REPO_ROOT"

# Experiment date suffix
DATE_SUFFIX="20260830"

# Input sources
OPP115_SOURCE="opp115_experiment_annotation_guided_20260203"   # paper's final OPP-115 run
OPPT_SEGMENTS="$REPO_ROOT/data/oppt/all_segments.json"

# New experiment directories
OPP115_DIR="opp115_experiment_stability_${DATE_SUFFIX}"
OPPT_DIR="oppt_experiment_stability_${DATE_SUFFIX}"

# ---------------------------------------------------------------------------
# Model panels (exported env vars take precedence over .env via load_dotenv)
# ---------------------------------------------------------------------------
export EXTRACTION_MODEL_1="anthropic/claude-haiku-4.5"
export EXTRACTION_MODEL_2="openai/gpt-5.6-luna"
export EXTRACTION_MODEL_3="google/gemini-3.7-flash"

export JUDGE_MODEL_1="deepseek/deepseek-v4-flash-0731"
export JUDGE_MODEL_2="z-ai/glm-5.3-flash"
export JUDGE_MODEL_3="moonshotai/kimi-k3"

cd "$SCRIPTS_DIR"
[ -f "$REPO_ROOT/.venv/bin/activate" ] && source "$REPO_ROOT/.venv/bin/activate"

# Force unbuffered Python output for real-time logging
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "Stability Experiment (Separated Panels)"
echo "Date: $(date)"
echo "=========================================="
echo "Extraction panel: $EXTRACTION_MODEL_1, $EXTRACTION_MODEL_2, $EXTRACTION_MODEL_3"
echo "Judge panel:      $JUDGE_MODEL_1, $JUDGE_MODEL_2, $JUDGE_MODEL_3"
echo ""

# Create experiment directories
mkdir -p "$OUTPUT_BASE/$OPP115_DIR"
mkdir -p "$OUTPUT_BASE/$OPPT_DIR"

# Stage inputs
cp "$OUTPUT_BASE/$OPP115_SOURCE/all_segments.json" "$OUTPUT_BASE/$OPP115_DIR/"
cp "$OUTPUT_BASE/$OPP115_SOURCE/opp115_attributes.json" "$OUTPUT_BASE/$OPP115_DIR/"
cp "$OPPT_SEGMENTS" "$OUTPUT_BASE/$OPPT_DIR/"

echo "=========================================="
echo "Part 1: OPP-115 Stability Experiment"
echo "=========================================="

echo ""
echo "=== Stage 1: 3-LLM Panel Statement Extraction (annotation-guided) ==="
echo "Started at: $(date)"
python -u extract_statements_multimodel.py --data-dir "$OPP115_DIR" --concurrency 50
echo "Completed at: $(date)"

echo ""
echo "=== Stage 2: Contradiction Detection (enhanced filtering, matched config) ==="
echo "Started at: $(date)"
python -u detect_statement_contradictions.py --data-dir "$OPP115_DIR" --enhanced-filtering
echo "Completed at: $(date)"

echo ""
echo "=== Stage 3: 3-LLM Judge Verification (Chinese panel, all NLI-flagged pairs) ==="
echo "Started at: $(date)"
python -u judge_statement_contradictions.py --data-dir "$OPP115_DIR" \
    --similarity-threshold 0.0 --concurrency 20 --rate-limit 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Stage 4: Analysis Report ==="
echo "Started at: $(date)"
python -u statement_contradiction_analysis.py --data-dir "$OPP115_DIR"
echo "Completed at: $(date)"

echo ""
echo "=========================================="
echo "Part 2: OPPT Stability Experiment"
echo "=========================================="

echo ""
echo "=== Stage 1: 3-LLM Panel Statement Extraction (with OPPT annotations) ==="
echo "Started at: $(date)"
# OPPT uses annotation-guided extraction via the default segments and
# attribute-review paths; output directly to the experiment folder.
python -u extract_statements_multimodel.py --output "$OUTPUT_BASE/$OPPT_DIR/statements.json" --concurrency 50
echo "Completed at: $(date)"

echo ""
echo "=== Stage 2: Contradiction Detection (enhanced filtering) ==="
echo "Started at: $(date)"
python -u detect_statement_contradictions.py --data-dir "$OPPT_DIR" --enhanced-filtering
echo "Completed at: $(date)"

echo ""
echo "=== Stage 3: 3-LLM Judge Verification (Chinese panel, all NLI-flagged pairs) ==="
echo "Started at: $(date)"
python -u judge_statement_contradictions.py --data-dir "$OPPT_DIR" \
    --similarity-threshold 0.0 --concurrency 20 --rate-limit 0.1
echo "Completed at: $(date)"

echo ""
echo "=== Stage 4: Analysis Report ==="
echo "Started at: $(date)"
python -u statement_contradiction_analysis.py --data-dir "$OPPT_DIR"
echo "Completed at: $(date)"

echo ""
echo "=========================================="
echo "Stability Experiment Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  OPP-115: $OUTPUT_BASE/$OPP115_DIR"
echo "  OPPT:    $OUTPUT_BASE/$OPPT_DIR"
echo ""
echo "Comparison against published runs:"
echo "  - Published OPPT:    $OUTPUT_BASE/oppt_experiment_enhanced_20260131"
echo "  - Published OPP-115: $OUTPUT_BASE/$OPP115_SOURCE"
echo ""
echo "Analysis notes:"
echo "  - Subset judged pairs at similarity >= 0.5 to recover the published protocol."
echo "  - Pairs below 0.5 measure recall in the region the published sensitivity"
echo "    analysis could not reach."
echo ""
echo "Finished at: $(date)"
