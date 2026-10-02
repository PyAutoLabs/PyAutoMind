# Point-source (single-source) CPU campaign — carried leftovers and completion evidence

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Epic: point-source-cpu-speed
Filed: 2026-09-27
Parent-record: complete/2026/09/point-source-cpu-p4.md

## Status

Split out of `point-source-cpu-p4` at close-out on 2026-09-27. Phase 4a shipped in
[autolens_profiling#321](https://github.com/PyAutoLabs/autolens_profiling/pull/321), record
`complete/2026/09/point-source-cpu-p4.md`, whose `## Original prompt` holds the full campaign contract.
The phase-4 code levers have their own prompts:
- phase 4b: shipped 2026-09-27, record `complete/2026/09/pointsolver-step0-gather.md` (PyAutoArray#580, autolens_profiling#330)
- phase 4c: shipped 2026-09-27, record `complete/2026/09/pointsolver-mcs-headroom.md` (PyAutoArray#584, PyAutoLens#753, autolens_profiling#335)
- the extent warning: `complete/2026/10/pointsolver-extent-sanity-check.md`
- per-package extents: `draft/feature/autolens_workspace/pointsolver_grid_extent_per_package.md`

This prompt holds only the phase 1–3 leftovers that no other prompt carries. Pick it up after the
phase-4 levers resolve.

## Carried leftovers

- **RAL cleanup** (once the release is synced):
  - the `/mnt/ral/jnightin/autolens_profiling_wt/{PyAutoArray,PyAutoLens}_point-source-cpu-p{2,3}` clones
  - the `point-source-cpu-p3` and `point-source-cpu-p4` RAL worktrees
  - `_p2_untracked_backup_20260924`
- **Test placement:** the PyAutoLens JAX unit test `test_autolens/point/triangles/test_static_lattice_jax.py`
  (~85–100 s) departs from the no-JAX-in-unit-tests convention. Consider moving it to
  autolens_workspace_test. Phase 4b pins its tie test, so do this only after 4b ships.
- **Library candidate (PyAutoFit / PyAutoLens):** `jax.grad` of an `AnalysisPoint` likelihood is
  silently all-zero without `autofit.jax.register_model(model)`. The fix is to raise or warn. File it
  via intake if no bug prompt covers it by then.
- **CI smoke coverage** for the breakdown cells: `vertex_dedup_ab.py`, `static_lattice_ab.py`,
  `solver_config_sweep.py`.
- **Unmeasured controls:**
  - the `--xla_disable_hlo_passes=constant_folding` A/B on the post-4b code
  - repeated (median) compile timings, if compile becomes a gate. Phase 3 had one cold compile per route.
- **Phase 4b leftovers** (record `complete/2026/09/pointsolver-step0-gather.md`):
  - `nopad` is dead weight in PyAutoArray `_STEP0_CONTAINMENT`. Delete it in a later library cleanup; `structured` is the default.
  - The RAL scratch copies `/mnt/ral/jnightin/autolens_profiling_wt/pointsolver-step0-gather` and
    `/mnt/ral/jnightin/autolens_profiling_wt/PyAutoArray_pointsolver-step0-gather` were left in place. Remove them with the RAL cleanup above.
  - The quotable 8490H row (job 357321) ran on a loaded node (load ~200). Re-run it on a quiet node if absolute ms against phase 4a are ever wanted; the ratios stand.
- **Phase 4c leftovers** (record `complete/2026/09/pointsolver-mcs-headroom.md`):
  - The A100 vmap-4 cell (job 359102) read +8 % on a single cell. This is likely noise; re-run it before quoting it.
  - The draw-12 fold-line attribution was carried from 4a and not re-verified in 4c.
  - The RAL scratch worktree `/mnt/ral/jnightin/autolens_profiling_wt/pointsolver-mcs-headroom` was left in place. Remove it with the RAL cleanup above.
- **Campaign completion evidence** (campaign contract): baseline/final comparison, every candidate
  disposition, and a GPU regression check for any shared library change. Record them in
  `results/notes/point_source_cpu_campaign.md` once the phase-4 levers are resolved, then close the epic.
