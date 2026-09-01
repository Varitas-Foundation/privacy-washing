"""
Stability-Run Contradiction Audit (August 2026)

Applies the same three-class commitment reclassification audit used on the
published runs (scripts/audit_paper1_contradictions.py)
to the stability experiment's panel-confirmed contradictions: classifies every
unique commitment-side statement as COMPANY_COMMITMENT, PRACTICE, or
USER_CONTROL and counts confirmations whose commitment is not a genuine
company commitment.

Differences from the published audit script:
  - Reads the stability experiment judge results
    (*_stability_20260830/).
  - Uses the stability run's extraction panel (EXTRACTION_MODEL_1/2/3,
    falling back to MULTIMODEL_1/2/3) as the classifier panel, mirroring the
    published audit's use of the pipeline's own models.
  - Writes to stability_contradiction_audit.json so
    the published audit output (audits/paper1_contradiction_audit.json) is untouched.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# The classifier infrastructure lives alongside this script (classify_commitments.py)
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify_commitments import (  # noqa: E402
    OpenRouterClient,
    classify_statement_three_models,
    compute_agreement_metrics,
    load_prompt_template,
)

from dotenv import load_dotenv  # noqa: E402

load_dotenv(REPO_ROOT / ".env")

CLASSIFIER_MODELS = [
    os.environ.get("EXTRACTION_MODEL_1", os.environ.get("MULTIMODEL_1", "")).strip().strip('"').strip("'"),
    os.environ.get("EXTRACTION_MODEL_2", os.environ.get("MULTIMODEL_2", "")).strip().strip('"').strip("'"),
    os.environ.get("EXTRACTION_MODEL_3", os.environ.get("MULTIMODEL_3", "")).strip().strip('"').strip("'"),
]

JUDGE_RESULTS_PATHS = {
    "oppt": REPO_ROOT / "oppt_experiment_stability_20260830" / "statement_judge_results.json",
    "opp115": REPO_ROOT / "opp115_experiment_stability_20260830" / "statement_judge_results.json",
}

OUTPUT_PATH = REPO_ROOT / "stability_contradiction_audit.json"


def extract_commitment_statements(judge_results_path: Path) -> list[dict]:
    """Extract unique commitment-side statements from panel-confirmed contradictions."""
    with open(judge_results_path) as f:
        data = json.load(f)

    verified = [a for a in data["annotations"] if a.get("final_verdict") == "CONTRADICTION"]

    seen = set()
    statements = []
    for v in verified:
        sid = v["commitment_statement_id"]
        if sid not in seen:
            seen.add(sid)
            statements.append({
                "statement_id": sid,
                "company": v["company"],
                "text": v["commitment_text"],
                "category": v.get("commitment_category", ""),
                "similarity_min": min(
                    vv["semantic_similarity"] for vv in verified
                    if vv["commitment_statement_id"] == sid
                ),
                "num_contradictions_in": sum(
                    1 for vv in verified if vv["commitment_statement_id"] == sid
                ),
            })
    return statements


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key or not all(CLASSIFIER_MODELS):
        print("ERROR: Set OPENROUTER_API_KEY and EXTRACTION_MODEL_1/2/3 (or MULTIMODEL_1/2/3) in .env")
        sys.exit(1)

    print("Classifier panel:")
    for m in CLASSIFIER_MODELS:
        print(f"  {m}")

    template = load_prompt_template()
    client = OpenRouterClient(api_key)

    all_results = {}
    audit_summary = {}

    for corpus, path in JUDGE_RESULTS_PATHS.items():
        print(f"\n{'=' * 60}")
        print(f"AUDITING {corpus.upper()} STABILITY-RUN CONTRADICTIONS")
        print(f"{'=' * 60}")

        statements = extract_commitment_statements(path)
        print(f"  Unique commitment statements to classify: {len(statements)}")

        results = []
        for i, stmt in enumerate(statements):
            result = classify_statement_three_models(
                client, stmt, CLASSIFIER_MODELS, template, max_workers=3
            )
            results.append(result)

            cls = result["final_classification"] or "SPLIT"
            consensus = result["consensus_type"]
            flag = " *** MISLABELED ***" if cls != "COMPANY_COMMITMENT" else ""
            print(f"  [{i + 1}/{len(statements)}] {stmt['company']}: COMMITMENT -> {cls} ({consensus}){flag}")

            time.sleep(0.3)

        reclassified = [r for r in results if r["final_classification"] != "COMPANY_COMMITMENT"]
        user_control = [r for r in results if r["final_classification"] == "USER_CONTROL"]
        practice = [r for r in results if r["final_classification"] == "PRACTICE"]

        stmt_to_cls = {r["statement_id"]: r["final_classification"] for r in results}
        by_stmt = {s["statement_id"]: s for s in statements}
        affected = [s for s in statements if stmt_to_cls.get(s["statement_id"]) != "COMPANY_COMMITMENT"]
        affected_contradictions = sum(s["num_contradictions_in"] for s in affected)
        affected_above_05 = sum(
            s["num_contradictions_in"] for s in affected if s["similarity_min"] >= 0.5
        )
        total_contradictions = sum(s["num_contradictions_in"] for s in statements)

        corpus_summary = {
            "total_commitment_statements": len(statements),
            "correctly_labeled": len(statements) - len(reclassified),
            "reclassified_total": len(reclassified),
            "reclassified_to_user_control": len(user_control),
            "reclassified_to_practice": len(practice),
            "total_contradictions": total_contradictions,
            "affected_contradictions": affected_contradictions,
            "unaffected_contradictions": total_contradictions - affected_contradictions,
            "affected_rate": round(affected_contradictions / max(total_contradictions, 1), 4),
        }

        print(f"\n  SUMMARY for {corpus.upper()}:")
        print(f"    Correctly labeled COMPANY_COMMITMENT: {corpus_summary['correctly_labeled']}/{len(statements)}")
        print(f"    Reclassified to USER_CONTROL: {len(user_control)}")
        print(f"    Reclassified to PRACTICE: {len(practice)}")
        print(f"    Affected contradictions: {affected_contradictions}/{total_contradictions} ({corpus_summary['affected_rate']:.1%})")

        if reclassified:
            print("\n  RECLASSIFIED STATEMENTS:")
            for r in reclassified:
                s = by_stmt[r["statement_id"]]
                print(f"    [{r['company']}] {r['final_classification']} (was COMMITMENT) x{s['num_contradictions_in']}:")
                text = r["text"]
                print(f'      "{text[:150]}..."' if len(text) > 150 else f'      "{text}"')

        all_results[corpus] = results
        audit_summary[corpus] = corpus_summary

    output = {
        "metadata": {
            "purpose": "Audit stability-run panel-confirmed contradictions for commitment label accuracy",
            "methodology": "three_llm_judge_reclassification",
            "models": CLASSIFIER_MODELS,
            "judge_results": {k: str(v) for k, v in JUDGE_RESULTS_PATHS.items()},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "summary": audit_summary,
        "agreement": {k: compute_agreement_metrics(v) for k, v in all_results.items()},
        "results": all_results,
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved audit to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
