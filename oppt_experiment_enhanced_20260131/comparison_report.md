# Extraction Version Comparison Report

Generated: 2026-02-01T03:10:10.956039+00:00

## Experiment Directories
- **v1 (baseline):** `/Users/tbrack/Documents/Projects/Dark Patterns Research/research/privacy_washing/oppt_experiment_20260130`
- **v2 (enhanced):** `/Users/tbrack/Documents/Projects/Dark Patterns Research/research/privacy_washing/oppt_experiment_enhanced_20260131`

## Statement Extraction

| Metric | v1 | v2 | Delta |
|--------|----|----|-------|
| Total statements | 18,446 | 6,061 | -12,385 |
| COMMITMENT | 4,861 | 2,028 | -2,833 |
| PRACTICE | 13,585 | 4,033 | -9,552 |

### v2 Enhanced Field Distributions

**Subject Distribution:**
- COMPANY: 4,409 (72.7%)
- USER: 1,141 (18.8%)
- THIRD_PARTY: 354 (5.8%)
- SERVICE_PROVIDER: 136 (2.2%)
- AFFILIATES: 21 (0.3%)

**Aspect Distribution:**
- ACCESS_CONTROL: 1,446 (23.9%)
- USE: 1,355 (22.4%)
- COLLECTION: 1,339 (22.1%)
- SHARING: 921 (15.2%)
- SECURITY: 394 (6.5%)
- RETENTION: 274 (4.5%)
- DELETION: 254 (4.2%)
- SALE: 78 (1.3%)

**Scope Distribution:**
- UNIVERSAL: 3,649 (60.2%)
- CONDITIONAL: 1,503 (24.8%)
- GEOGRAPHIC_LIMITED: 345 (5.7%)
- CONSENT_BASED: 344 (5.7%)
- LEGAL_REQUIREMENT: 220 (3.6%)

**Statements with qualifiers:** 5,430 (89.6%)

## Contradiction Detection

| Metric | v1 | v2 | Delta | % Reduction |
|--------|----|----|-------|-------------|
| Total pairs evaluated | 87,813 | 3,965 | -83,848 | 95.5% |
| Contradictions detected | 13,019 | 704 | -12,315 | 94.6% |
| Contradiction rate | 14.83% | 17.76% | +2.93% | - |

### Enhanced Filtering Impact (v2)

| Filter | Pairs Excluded |
|--------|----------------|
| Aspect Incompatible Filtered | 12,758 |
| Commitment Category Filtered | 32,188 |
| Legal Requirement Scope Filtered | 578 |
| Practice Category Filtered | 7,209 |
| Qualifier Coverage Filtered | 1,025 |
| Self Segment Filtered | 2,391 |
| Subject Incompatible Filtered | 24,324 |

### Contradiction Overlap Analysis

- **Common to both:** 94 (preserved true positives)
- **v1 only (filtered by v2):** 12,925 (potential FP reduction)
- **v2 only (new in v2):** 610

**Sample pairs removed by v2 filtering (potential FPs):**
- `23andme_006_s1_vs_23andme_002_s1`
- `23andme_006_s1_vs_23andme_005_s8`
- `23andme_006_s1_vs_23andme_007_s1`
- `23andme_006_s1_vs_23andme_007_s5`
- `23andme_006_s1_vs_23andme_007_s6`
- `23andme_006_s1_vs_23andme_007_s9`
- `23andme_011_s2_vs_23andme_002_s2`
- `23andme_011_s2_vs_23andme_003_s6`
- `23andme_011_s2_vs_23andme_003_s8`
- `23andme_011_s2_vs_23andme_005_s1`

## Summary

The enhanced v2 extraction with metadata-based filtering:
- Reduced pairs evaluated by **95.5%** (83,848 pairs)
- Reduced detected contradictions by **94.6%** (12,315 contradictions)
- Preserved **94** contradictions from v1 baseline
