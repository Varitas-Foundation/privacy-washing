# Corpus inputs

## `oppt/` (included)

The exact OPPT input files used for all runs, released under CC-BY-4.0:

- `all_segments.json`: the 123-company OPPT corpus, segmented, with three-LLM
  consensus annotations from the companion jurisdiction study.
- `oppt_v2_attribute_review.json`: per-segment attribute annotations supplied
  to the extraction prompts as annotation blocks.

The corpus is also published as a Hugging Face dataset:
https://huggingface.co/datasets/OpenPrivacyPolicyTaxonomy/oppt-privacy-policies

## `opp115/` (fetch from original source)

OPP-115 (Wilson et al., 2016) is not redistributed here. To reproduce the
OPP-115 runs:

1. Download the corpus from https://usableprivacy.org/data and unpack it so
   this directory contains `OPP-115/sanitized_policies/` and
   `OPP-115/annotations/`.
2. Run `python scripts/prepare_opp115.py` to produce
   `opp115/opp115_prepared.json`, the file the pipeline consumes.
