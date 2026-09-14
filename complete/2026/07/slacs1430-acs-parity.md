## slacs1430-acs-parity (SLACS1430+4105 ACS reduction vs legacy — pixel parity PASS — SHIPPED)
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/17 (STAYS OPEN for the optional model-parity fit leg)
- completed: 2026-07-10 (pixel parity verdict + scripts); active.md entry retired 2026-07-14 (/morning, human-directed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/23 — MERGED (0face12, squash).
- summary: PyAutoReduce production reduction of slacs1430+4105 reproduces the trusted legacy dataset up to fully-understood differences (astrometry: legacy is rot270 of north-up; photometry flux ratio 1.040; noise ratio ≈1.35=R, legacy family internally inconsistent on the correlated-noise correction; PSF tier-1 ePSF 0.129″ vs 0.120″). Acquire dup-product bug independently fixed on main by #18's is_direct_product. Full verdict table: issues/17 close-out comment 2026-07-10.
- residual (not blocking retirement): the optional model-level parity fits are checkpointed/OOM'd (NOT RUN) — #17 stays OPEN with that as its last checklist item (resume: `prototypes/slacs1430_parity_fit.py autoreduce`/`legacy`, serially on a quiet machine). Methodology notes seed the queued PJ011646 WFC3 follow-up.
- retired: the `active/pyautoreduce_slacs1430_acs_comparison.md` copy of this task was retired
  2026-09-14 (backlog reconciliation) and its text folded in below; PyAutoReduce#17 is
  deliberately left OPEN for the optional model-parity fit leg.

## Original prompt

# PyAutoReduce validation: slacs1430+4105 ACS reduction vs trusted legacy dataset

Type: test
Target: workspaces
Repos:
- autolens_assistant
- PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-08-08 (backfilled from parked.md `parked:`)

Validate PyAutoReduce against a trusted legacy reduction: reduce the SLACS lens slacs1430+4105 from archival HST/ACS data using PyAutoReduce, then compare the resulting modeling-ready dataset (data, noise map, PSF) to the long-used collaborator-provided dataset at /mnt/c/Users/Jammy/Science/subhalo/dataset/slacs/slacs1430+4105 (used for many years in subhalo work). Comparison is a science project driven through autolens_assistant: image/noise/PSF residuals plus lens-model parity fits on both datasets.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
