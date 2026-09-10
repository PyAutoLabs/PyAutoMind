# Instrument the pixelized reconstruction row: NNLS-vs-Cholesky split, log-det emission, rectangular runtime pin re-measure

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gpu
- performance
- hpc
- pixelization
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the three dense breakdown JSONs on A100 fp64 carry a `steps_reconstruction_sub_rows` block (Cholesky of F+λH, Cholesky solve, NNLS PDIP with its iteration count and ms/iteration, both log-det Choleskys — overlapping rows, not a partition of the reconstruction row), an `nnls` block whose cell-driven reconstruction matches the library's to 1e-8, non-null `log_evidence_terms`; the baseline note gains a "Reconstruction split" section stating per row how many PDIP iterations the 37 ms is and what one Cholesky / Cholesky-solve of the same system costs; the rectangular runtime pin equals the breakdown pin; lint + `build_readme.py --check` green.
Review-minutes: 20
Unattended: ready
Parent: complete/2026/09/a100-pixelized-baseline.md
Filed: 2026-09-10
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/243

## Why

The 2026-09-10 A100 fp64 baseline (`autolens_profiling/results/notes/a100_pixelized_baseline_2026_09.md`, issue #241 / PR #242) found that the "Regularized reconstruction" step — NNLS + Cholesky on the reduced (F + λH) system — is 36.7–37.9 ms on every one of the six rows, 61–71 % of the per-call cost, identical dense vs sparse. It is the target any matrix-free CG + SLQ formulation has to attack, but the baseline cannot say how that 37 ms splits between (a) the NNLS active-set iterations (each a solve), (b) the two Cholesky factorizations (F + λH and the reduced H), (c) the log-det reads, and (d) the reconstruction / model-image assembly. Sizing a matrix-free scheme requires that split. The same cells also emit no per-term log-det values, which the SLQ-vs-exact comparison needs as ground truth. Both need the same three breakdown cells edited, so they are one task.

## What to build

1. In `scripts/imaging/likelihood_breakdown/{pixelization,delaunay,delaunay_nn}.py` (shared helpers in `scripts/misc/likelihood_breakdown/`), add independently-jitted sub-rows that overlap the "Regularized reconstruction" step (`steps_reconstruction_sub_rows`, same overlap rule as `steps_sparse_sub_rows`): a cell-driven `solve_nnls` call exposing the PDIP iteration count and ms/iteration, a one-iteration row, a single Cholesky of F + λH and a Cholesky solve on the same system, and the two log-det Choleskys of step 13. The step-12 row itself stays the library call, unchanged.
2. Emit the exact log-det values per row into the JSON (`log_det_curvature_reg`, `log_det_regularization`, plus the NNLS iteration count and the final log_evidence terms) so they can be checked against an SLQ estimate later.
3. Re-measure the rectangular `likelihood_runtime/pixelization.py` pin: it still carries the pre-#235 `28622.397322591198` while every 2026-09 leg measures `28621.128714095972`; update the constant and its comment so the pin describes what the cell computes today.
4. Re-run the three dense breakdown legs on RAL (same node, fresh cache, per the baseline launcher pattern — `hpc/batch_gpu/submit_baseline_grid.sh` is the template) plus the rectangular runtime leg to validate the re-measured pin; dense and sparse share the reconstruction code byte-for-byte, so no sparse leg is re-run. Append a "Reconstruction split" section to the baseline note with the sub-row table and log-det values; regenerate the READMEs.


Follow-on: the matrix-free CG + SLQ prompt is filed blocked on this task.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5d8bb12c-d0c2-46fc-b5a1-544c43387c68/scratchpad/intake_a.md -->
