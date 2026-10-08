# Linear-solver programme phase 5: a Mapper (pixelized) corpus — is raw+polish admissible and is Jacobi stable on the systems pixelized likelihoods actually produce?

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- linear-solver
- gpu
- pixelization
Difficulty: moderate
Autonomy: supervised
Priority: medium
Consequence: judge
Status: active
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/399
Depends-on: complete/2026/10/linear-solver-p3b-gpu-timing.md; autolens_profiling#398 (phase 4a: the A100 Jacobi batched/unbatched divergence is batch-shape-dependent Cholesky rounding amplified on Jacobi-unstable systems)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md

## Original request (chat 2026-10-08)

"I want a fast solution but it also needs to be stable for all likelihood functions." Options were
laid out (wrap up / one bounded evidence step / switch the Mapper default now / keep probing
Jacobi); the human chose the bounded evidence step: "Lets do option 2".

## Why

Every phase so far ran on SLaM MGE systems (n = 60). The programme's open decision is the Mapper
(pixelized) GPU default, which is Jacobi today, and no pixelized system has been through the cells.
Jacobi's known trigger is the scaling of signal-free MGE columns, which pure Mapper systems do not
have — but the production SLaM pixelized stages are *mixed* (lens light MGE + source pixelization),
where both the trigger and the Mapper default apply. Raw+polish is fast and bit-stable on MGE but
its admissibility on pixelized systems is untested.

## Scope

1. **Capture new corpus groups** with new `--source` runners in `scripts/lens/solver/capture.py`
   (same `_recording_solver` wrap of `reconstruction_positive_only_from`, post-regularisation,
   pre-Jacobi; `_corpus.add_group` computes the fnnls reference; existing groups untouched):
   - `delaunay_hst`: imaging, parametric lens mass + Delaunay source (the profiling repo's HST
     Delaunay preset), ~8 parameter vectors (near-truth + spread);
   - `rectangular_hst`: same with the default rectangular mesh, ~8 vectors;
   - `slam_mixed_hst`: lens light 2×20 MGE + Delaunay source (the SLaM source_pix configuration),
     ~8 vectors — the production case;
   - optional `interferometer_delaunay`: ~4 vectors if the interferometer harness captures cleanly.
   Record `no_regularization_index_list`, `source_column_index_list`, model, n, and confirm the
   positive-only solver setting the captured path used.
2. **Run the existing cells over the new groups**, CPU and one A100 job: `accuracy.py` (all
   candidates), `timing.py` (batch sizes scaled to n; compile separate), `batched_divergence.py`.
3. **Judge** against the phase-1 pre-registered rule, stated as *extended* to this corpus (it was
   pre-registered for MGE): is raw+polish admissible on Mapper and mixed systems; does Jacobi
   diverge or show the A100 batched/unbatched sensitivity on any of them; what does each cost.
4. **Write-up**: extend `wiki/research/jacobi_a100_batched_divergence.md` (or a sibling page) with
   the Mapper evidence and a recommendation table for the default decision; ledger rows; README
   auto-tables; campaign page Next line. No default, pin or tolerance changes here.

## Witness

New corpus groups in `results/lens/solver/corpus/`, CPU + A100 artefacts for the three cells over
them, the wiki recommendation table; `ruff`, `build_readme.py --check`, lint smoke.

## Compute

One A100 job (minutes to tens of minutes; n up to ~1600 batched fp64) from the private base
`/mnt/ral/jnightin/PyAuto_wt/linear-solver-p3` via the RAL `autolens_profiling_wt/linear-solver-p4a`
worktree. CPU on the laptop from tag worktrees. Needs separate compute authorization.
