# Privacy Washing: Detecting Internal Contradictions in Privacy Policies

Artifacts for the paper **"Privacy Washing: Detecting Internal Contradictions in Privacy Policies"** (Thomas Brackin, 2026; arXiv ID pending).

This repository contains the detection pipeline, all intermediate outputs (extracted statements, NLI scores, per-judge verdicts), analysis scripts, and run logs referenced in the paper's Data and Code Availability statement. Scripts resolve every path relative to the repository root, so a clone of this repository is self-contained apart from the OPP-115 corpus, which must be fetched from its original source (see below).

## Repository layout

| Path | Contents |
|------|----------|
| `scripts/` | Pipeline stages and analysis scripts. Includes the judge prompt (`judge_statement_prompt.md`, reproduced in the paper's Appendix A) and the extraction prompt (`statement_extraction_prompt_v2.md`, Appendix B), both unmodified from the runs. |
| `run_*.sh` | Orchestration scripts for the experiment runs. |
| `data/` | Corpus inputs. OPPT input files are included; OPP-115 is fetched from its original source (see `data/README.md`). |
| `oppt_experiment_enhanced_20260131/` | Primary OPPT run (January 31, 2026): extracted statements, candidate pairs, NLI scores, per-judge verdicts (`statement_judge_results.json`), and derived reports. |
| `opp115_experiment_annotation_guided_20260203/` | Primary OPP-115 run (February 3, 2026), same file structure. |
| `oppt_experiment_stability_20260830/`, `opp115_experiment_stability_20260830/` | Stability re-run (August 30–31, 2026) with separated extraction and judge panels, described in the paper's stability section. Includes the discarded first judge pass. |
| `oppt_experiment_20260130/` | Earlier OPPT pass: the segment-level pilot artifacts (318 judged pairs in `judge_results.json`, the basis of the paper's pilot recall analysis) and the earlier statement-level pair-generation pass discussed alongside the legacy pairs in the paper's Methodology section. |
| `opp115_experiment/` | Earlier OPP-115 pass: the segment-level pilot artifacts (820 judged pairs in `judge_results.json`, from which the pilot tabulation reproduces exactly) and an early statement-level pass. |
| `audits/` | The three-class commitment reclassification audit of the primary runs (`paper1_contradiction_audit.json`) and its per-corpus classification outputs, produced by `scripts/audit_paper1_contradictions.py`. |
| `stability_*.log`, `stability_contradiction_audit.json` | Stability run logs and the stability run's reclassification audit. |
| `pipeline_comparison.md`, `judge_vs_nli_comparison.md`, `combined_evidence_excerpts.md` | Pilot-era analysis reports: the segment-level vs statement-level pipeline comparison, the judge-vs-NLI recall tabulation, and the evidence excerpts behind the pilot's manual assessment. |

## Corpus inputs

- **OPPT** (123 website privacy policies collected in 2026, with three-LLM consensus annotations, CC-BY-4.0): the exact input files used for the runs are included in `data/oppt/`. The corpus is also published on Hugging Face as [OpenPrivacyPolicyTaxonomy/oppt-privacy-policies](https://huggingface.co/datasets/OpenPrivacyPolicyTaxonomy/oppt-privacy-policies).
- **OPP-115** (115 website privacy policies collected in 2015): available from its original source at [usableprivacy.org](https://usableprivacy.org/data) (Wilson et al., 2016). It is not redistributed here; `scripts/prepare_opp115.py` converts the original distribution into the format the pipeline consumes.

## Reproducing

Set up an environment and credentials:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OpenRouter API key and model identifiers
```

Run the OPPT pipeline stage by stage against a fresh output directory:

```bash
python scripts/extract_statements_multimodel.py --data-dir my_oppt_run
python scripts/detect_statement_contradictions.py --data-dir my_oppt_run --enhanced-filtering
python scripts/judge_statement_contradictions.py --data-dir my_oppt_run
python scripts/statement_contradiction_analysis.py --data-dir my_oppt_run
```

For OPP-115, first fetch and prepare the corpus (see `data/README.md`), then run `scripts/convert_opp115.py` and the same stages. The `run_*.sh` scripts record the exact stage invocations used for each experiment, including the stability run's configuration.

Model identifiers and experiment dates for every run are listed in the paper's Data and Code Availability statement and pre-filled as comments in `.env.example`. All judges ran at temperature 0.0. Note the paper's reproducibility caveat: requests were routed through OpenRouter without pinning to a specific backend provider, so provider-side serving changes can alter model outputs. Analyses that only re-read released run outputs (for example `scripts/sensitivity_analysis.py` and the report generators) require no API key and reproduce deterministically.

## Interpreting the outputs

Two caveats from the paper govern all reported figures. First, panel verdicts have not been validated against human expert judgment, so precision is unknown; "panel-confirmed" means LLM majority agreement, not expert validation. Second, the two primary corpus runs used different filter configurations, so the difference in prevalence between them is not interpretable as a corpus or era effect. See the paper's Limitations section.

## Licensing

- Code and scripts: MIT (see `LICENSE`).
- OPPT corpus annotations (`data/oppt/`): CC-BY-4.0.
- OPP-115 data: per its original distribution terms; obtain it from the original source.

## Citation

```bibtex
@article{brackin2026privacywashing,
  title={Privacy Washing: Detecting Internal Contradictions in Privacy Policies},
  author={Brackin, Thomas},
  year={2026},
  note={arXiv preprint, ID pending}
}
```
