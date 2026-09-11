## reconstruction-row-split
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/243
- completed: 2026-09-11
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/244 (merge 2a4216a)
- pending-release: none — workspace-category task, no library PR, so the `active.md` row carried no `pending-release:` line.
- summary: |
    Instrumented the pixelized reconstruction row the 2026-09-10 A100 baseline could only
    measure as one 37 ms block, and answered what it is made of. Five commits on
    `feature/reconstruction-row-split`: 410fe9e (overlapping `steps_reconstruction_sub_rows`
    in the three dense breakdown cells, new shared helper
    `scripts/misc/likelihood_breakdown/reconstruction_steps.py`, READMEs regenerated),
    e6b61f9 (rectangular runtime log-evidence pin re-measured to `28621.128714095972` from
    the pre-#235 `28622.397322591198`), 353b9cf (four `_recon_split` A100 submit variants),
    9938181 (the four result legs), 044dccd (the note section). Four jobs 342643-342646 ran
    on `euclid-ral-gpu-2` (A100 80GB PCIe) fp64 in one ~7-minute window, each with a fresh
    per-job `JAX_COMPILATION_CACHE_DIR`, `autotune_cache_entries_at_start: 0`,
    `cache_fresh: true`. Results written under the `_recon_split` tag so the 2026-09-10
    baseline JSONs stay canonical. Note section:
    `results/notes/a100_pixelized_baseline_2026_09.md` → "## Reconstruction split (2026-09-11)".
- witness: |
    Every clause of the prompt's Witness header, MET:
    - *the three dense breakdown JSONs on A100 fp64 carry a `steps_reconstruction_sub_rows`
      block (Cholesky of F+λH, Cholesky solve, NNLS PDIP with iteration count and
      ms/iteration, both log-det Choleskys — overlapping rows, not a partition)* — **MET**.
      All three `*_hpc_a100_fp64_recon_split.json` carry seven sub-rows: `Cholesky (F+λH)`,
      `Cholesky solve (unconstrained)`, `NNLS PDIP (cell-driven, max_iter 50)`, `NNLS PDIP
      one iteration`, `NNLS PDIP @vmap 16 (identical lanes)`, `Log det Cholesky (F+λH
      reduced)`, `Log det Cholesky (H reduced)`, plus a
      `steps_reconstruction_vmap_note` stating the overlap rule.
    - *an `nnls` block whose cell-driven reconstruction matches the library's to 1e-8* —
      **MET**: `reconstruction_max_abs_diff_vs_library` 4.69e-10 (rect) / 7.59e-10
      (Delaunay) / 1.17e-09 (DelaunayNN) against `reconstruction_tolerance` 1e-8, with
      `iterations`, `converged: true`, `ms_per_iteration`, `max_iter`, `solver_tol`,
      `jacobi_preconditioning` all emitted.
    - *non-null `log_evidence_terms`* — **MET**: six terms per leg, including the two
      Cholesky log-dets.
    - *the baseline note gains a "Reconstruction split" section stating per row how many
      PDIP iterations the 37 ms is and what one Cholesky / Cholesky-solve of the same system
      costs* — **MET**: 139 lines at `## Reconstruction split (2026-09-11)`, with the
      sub-row table, the log-det table, provenance/gate, and a "What this says to the
      matrix-free work" subsection that supersedes item 1 of the baseline's own.
    - *the rectangular runtime pin equals the breakdown pin* — **MET**: the runtime leg
      (job 342646) carries `pinned_expected: 28621.128714095972`, `pinned_drift: []`, and
      the breakdown leg's `log_evidence` is 28621.128714096816 (2.9e-14 relative).
    - *lint + `build_readme.py --check` green* — **MET**: the `lint` workflow is
      `completed/success` on head sha 044dccd (it is the job that runs
      `build_readme.py --check`); `scripts/misc/likelihood_breakdown/README.md` was
      regenerated in 410fe9e.
- findings: |
    - **The 37 ms is not a linear solve — it is 21 / 22 / 22 PDIP iterations at 1.77 / 1.70 /
      1.70 ms each** (rectangular / Delaunay / DelaunayNN), and every iteration is a fresh
      dense KKT Cholesky inside `jaxnnls`.
    - **Positivity costs ~24x the exact solve it replaces.** One Cholesky of the same F+λH is
      1.19-1.26 ms; the full exact unconstrained solve (that factorisation + two triangular
      solves) is 1.52-1.58 ms.
    - **This resizes the matrix-free CG + SLQ target to ~1.6 ms, not 37 ms**, plus the ~2.4 ms
      of the two log-det Choleskys (1.15-1.27 ms each) that SLQ actually attacks. A free CG
      solve would take ~4 ms off a 50-65 ms call and leave the 37 ms untouched. The lever is
      the NNLS **iteration count** — warm starts, looser `solver_tol`, lower `max_iter`, or a
      different treatment of positivity altogether — not the cost of a factorisation.
    - **Batching does not rescue it.** At `vmap` 16 with *identical* lanes (the best case: no
      straggler in the `lax.while_loop`) the NNLS amortises only **1.70x** — 37.1 → 21.9 ms
      per call — against 12x for the batched sparse inversion setup.
    - **The "one iteration" row is an upper bound, not the marginal cost.**
      `solve_nnls(..., max_iter=1)` pays the whole solver entry (Jacobi scaling, initial
      interior point, first KKT factorisation) which the loop amortises: 3.17-3.32 ms, ~1.9x
      the amortised per-iteration cost.
    - **The exact log-det ground truth is now recorded**: log det F+λH = 3888.258090 /
      8360.401763 / 7224.568778, log det H = 1692.786817 / 7756.614959 / 6690.183752. Compare
      terms within a mesh, never across: the rectangular values are ~2x smaller only because
      its regularization is `Constant(1.0)` while the Delaunay family uses `adapt_split`.
    - **The instrumentation is nearly free**: ~1.1 s of extra compile (0.07-0.10 s per
      Cholesky row, 0.43-0.46 s per NNLS row, the same order as step 12's 0.45 s
      `reconstruction_jit`) and no per-call cost to the timed steps.
    - The shared RAL library install was refreshed between the 2026-09-10 baseline and this
      re-run (PyAutoFit e354dbb6, PyAutoArray 667deed3, PyAutoGalaxy 6640a749, PyAutoLens
      0da06de6; PyAutoNerves unchanged at 0e7163bc). Every step row still lands within 0.7 %
      of the 2026-09-10 dense numbers, so the split is directly comparable to the baseline.
- follow-ups: |
    Not filed as prompts here — a later `/intake` owns them:
    1. **Profile the positivity lever**, the finding this task turned up: a `solver_tol` sweep
       on A100, a batched-PDIP profile at `vmap` 16 to explain why identical lanes buy only
       1.7x, and a JAX warm-started active-set prototype measured against the 1.7 ms per
       PDIP iteration. Offered to the human at close-out; not yet filed.
    2. **A library change threading `pdip_iter` / `converged` out of `solve_nnls_primal` as
       aux**, so profiling cells need not replicate the Jacobi scaling to read them.
    3. The `delaunay` / `delaunay_nn` breakdown cells still write no `pinned_expected` /
       `pinned_drift`; their eager pins were audited from stdout for this run.
    4. **Pin the RAL install revisions per grid.** The shared install moved between the
       2026-09-10 and 2026-09-11 runs (rows within 0.7 %, so harmless here) — future grids
       should record and pin the revisions rather than discover them afterwards.
- trap: |
    The RAL bridge is pull-only: commit inside the RAL worktree, fetch it over ssh from the
    laptop, push from local. There is no push path from RAL to origin.
- notes: |
    Parent: `complete/2026/09/a100-pixelized-baseline.md` (issue #241 / PR #242). This task
    discharges follow-ups 1-3 of that record. The remaining one — filing the matrix-free
    CG + SLQ PyAutoArray prompt — is filed and was blocked on this task;
    `draft/research/autoarray/matrix_free_pixelized_imaging_likelihood_cg_solv.md` had its
    `Blocked-by:` repointed at `autolens_profiling#243` (now closed) at this close-out, so it
    reads as ready to start — and its sizing must start from ~1.6 ms + 2.4 ms, not 37 ms.

## Original prompt

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
