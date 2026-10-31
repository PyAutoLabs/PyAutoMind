# Likelihood lifecycle phase 3 step 1b: commit the 2a-2c JAX re-measure rows (jax 0.11.2 day zero)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: every 2a/2b/2c JAX row on a planned cell is current at jax/jaxlib 0.11.2 with the eigen flag on CPU legs (numba rows carried; 2b/2c RAL CPU rows via the quiet-rerun ingest, autolens_profiling#494); each superseded jax 0.10.2 row is in history/; every new witness `match`; coverage, catalogue and campaign pages regenerated; build_catalogue --check --validate-with ../PyAutoPulse valid
Review-minutes: 45
Unattended: never
Epic: likelihood-lifecycle
Phase: 3
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-31
Issued: 2026-10-31
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/495

## Request (human, 2026-10-31, verbatim)

"do all 4 steps" — (1) the 2b references, (2) the quiet-rerun ingest, (3) the phase-3 rows PR, (4) designation records — then "yes, start step 3".

## Inputs (all from autolens_profiling_p2dg at 8860c50c, private 2026.10.25.1 checkout, jax/jaxlib 0.11.2)

- 2a: RAL 413614-413617 (26 legs) + A100 413618-413621 → `output/p3_jax_rerun/` — 44 cells, 132 files, 44/44 witnesses `match`. All exit 0.
- 2b A100: 413622-413625 → `output/p2b_batch1/` — 11 cells; 5 `match`, 6 `not_assessed` (alma/alma_high/jvla `jax_gpu_sparse_fp64_wtilde`) until reference array RAL 413669 finalises them.
- 2c A100: 413626 → `output/p2c/` — 3 cells + 3 `plain_runtime` experiments, witnesses `match`.
- 2c RAL CPU breakdowns (gap found 2026-10-31: the quiet rerun redid only the runtime legs): RAL 413683 (`submit_campaign_p2c_point_source_ral_cpu_fp64 --array=0,2,4,5`: 2 breakdowns + 2 plain_runtime experiments) → `output/p2c/`.
- Stale string: rows report `autolens_version 2026.8.17.1` (source checkout `__version__`); the job logs confirm import origin + tag 2026.10.25.1.

## What to do

1. Pull the rows; copy complete cells (PR B rules: final write, fit.png, parity passing `parity_witness.py --check`, library_revisions = pinned checkout) over the jax 0.10.2 rows, moving each to `history/2026.10.25.1_<old captured_at date>/`.
2. Not touched: numba rows (carried, Q7); off-plan rows (`sdp81`, `source_pixels_784`, `local_laptop`); 2b/2c RAL CPU rows (autolens_profiling#494).
3. Regenerate catalogue / setup wiki / coverage / dashboard / READMEs; campaign-page journals with before/after per cell (load and jax/flag change together on RAL; A100 legs change jax only).
4. Re-check the designation draft (`likelihood_lifecycle_p3_designation_proposals.md`) close calls against the new numbers; record which proposals move. Designation records themselves are step 4.
