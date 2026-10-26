# Likelihood lifecycle phase 2b: profiling campaign — interferometer/{mge, rectangular, delaunay} (84 planned cells), including the sparse W~ (`_wtilde`) and dense routes

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/469
Consequence: judge
Witness: the coverage matrix shows zero missing and zero stale cells for class ∈ {optimal, secondary} × measurement ∈ {runtime, breakdown} for this campaign's likelihoods; every new current cell carries fit.png, provenance and parity.json; `build_catalogue --check --validate-with ../PyAutoPulse` valid at @3; the campaign wiki page records the pre-registered rule and verdict
Review-minutes: 45
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-24

Phase 2 sub-issue 2b of the `likelihood-lifecycle` epic (report §4 "Phase 2"; ledger "Phase 2" card). Depends on phase 0 (complete) and phase 1B (merged, autolens_profiling#453); start after autolens_profiling#455 (follow-ups) merges. Scope: interferometer/{mge, rectangular, delaunay} (84 planned cells), including the sparse W~ (`_wtilde`) and dense routes.

Sparse and dense, NUFFT and DFT, as in the §3.3 table.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).

## Human rulings (2026-10-25/26) and approved plan
- R1(a) dense pixelized NUFFT planned only at sma (84 → 60 cells); R2 no DFT cells; R3 hst source_pix[2] presets at the standard size (Delaunay 1250 + 30 edge AdaptSplit; rect 35² RectangularBilinearAdaptImage + Adapt; truth lensed-source adapt image, no S/N cap; MGE-20 unchanged); R4 numba headline = packaged cost-model route, forced routes as sub-rows, --n-instances 20/20/10/5 (sma/alma/alma_high/jvla); R6 visibility-chunked eager dense parity reference, one RAL task per mesh above sma; R7 parity tolerance 1e-8·|ref| fp64 (1e-3 mp); R8 batch-0 bounding cells (RAL 14 + A100 10 + optional jvla reference tasks); R9 registry instruments.
- R5 CHANGED by human 2026-10-26: pin **2026.10.25.1** (private RAL checkout /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1).
- Human 2026-10-26: "install finufft on RAL" (the 10.25.1 NumPy NUFFT path uses finufft).
- Human 2026-10-26: matrix-free (PyAutoArray#658, merged after 10.25.1) → `numpy_cpu_matrixfree` rectangular runtime as experiments/ rows on all 4 instruments at 35² plus a mesh scan at alma (64², 128², 192²) in scans/, from a private RAL checkout at exact main SHAs (labelled unreleased), never current; log-evidence agreement vs the dense reference recorded.
- Human 2026-10-26: "make sure we have checks all the different variants with sparse, dense, but also ... matrix free sparse".
- Heart RED override: live human 2026-10-26 "Yes, authorise for 2b" (PRs + planned RAL batches).
- Plan approved: "rest sounds good". PR A = presets, numba runtime scripts, --dense breakdown mode, resources/fit.png/parity in harnesses, chunked dense reference, campaigns/_common.py + interferometer_p2b.py (imaging_p2a --check byte-identical), matrix-free experiment harness, tests, R1 designation/coverage regen. Then batch 0 → walls PR → batch 1 → PR B (survey §4).
- Queued behind rectangular-28sq-profiling-rows (both edit _production_config.py) — start PR A from main after that merges.
