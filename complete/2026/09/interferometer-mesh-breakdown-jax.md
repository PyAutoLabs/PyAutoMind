# interferometer-mesh-breakdown-jax

- Repo: autolens_profiling (workspace-only)
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/348 (closed with a Shipped comment)
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/352 (MERGED, merge commit `15131f91`, head `3459e25`, 2026-09-28; lint green, the only check; origin/main merged into the branch to resolve a `wiki/index.md` row conflict with #351)
- Epic: interferometer-likelihood-campaign, phase 3 of `draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md`
- Heart: the human acknowledged YELLOW at ship (2026-09-28). The reasons were a workspace validation timeout (autolens_test multi_dataset/rectangular.py), manifest drift ×1, a PyAutoMemory PR 8 days old and incomplete release validation. None of them touch autolens_profiling.

## What shipped

Phase 3 of the campaign, the A100 mask-radius sweep. 12 RAL A100 fp64 jobs ran: Delaunay-1500 and rectangular 39² at sma / alma / alma_high, radius r2.0 / r5.0, on the sparse (W~) path.
- **Jobs:** 366895 / 366896 (tasks 2-5) and 366907 / 366908 (sma, tasks 0-1).
- **Libraries** (the mirror, refreshed by HPCPullPyAuto): Nerves bf104102, Fit 404b3e5f, Array 9428eca2, Galaxy c9609825, Lens 21b520be. nufftax 0.6.1.
- **Submits:** `hpc/batch_gpu/submit_breakdown_interferometer_{delaunay,pixelization}_a100_radius_sweep_fp64`, each a 6-task array.
- **Witness met:** every JSON has non-null steps and the requested `mask_radius_arcsec`. The inversion path is `sparse`, step sum ÷ full JIT is 1.002–1.051, and no sparse leg ran out of memory, including alma_high r5.0.
- **Headline:** only F grows with the radius, 4.9–7.8× from r2.0 to r5.0, at about 0.8–1.2 µs per FFT-extent pixel whatever N_vis. The solve stays flat at 17.6–26.6 ms.
  - Full JIT, alma Delaunay: 39.1 / 49.5 / 70.2 ms at r2.0 / r3.5 / r5.0.
  - Full JIT, alma_high Delaunay: 54.1 / 101.5 / 190.9 ms.
  - vmap gains only 6 % at alma_high r5.0.
- **Ledger:** `results/notes/interferometer_mesh_a100_breakdown_2026_09.md` § "Mask-radius sweep — A100 fp64 (phase 3, #348)". The wiki campaign page and index row are updated.
- **Caveats:** the r3.5 column reuses the #324 rows, which ran on older library revisions. The A100 JSONs don't record peak VRAM. For Delaunay, the A100 nnz/col is taken from the triplet count and overstates the in-situ value.

## For phase 4

CPU radius rows exist only at alma (r2.0 / 4.25 / 5.0 / 6.0). sma and alma_high CPU rows at r2.0 / r5.0 must be added before the CPU-vs-A100 decision-matrix witness can be met. The RAL worktree `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-breakdown-jax` is left in place on RAL; this close-out does not clean it.

## Original prompt

# Interferometer likelihood campaign 3/3 — phase 3: A100 mask-radius sweep (Delaunay-1500 + rect 39², fp64)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- likelihood-profiling
- gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: all 12 `results/breakdown/interferometer/[<inst>/]{delaunay,pixelization}_hpc_a100_fp64_r{2.0,5.0}.json` files exist with non-null steps. Each has `mask_radius_arcsec` equal to the requested radius and inversion path `InversionInterferometerSparse`, with the step sum within 10 % of the full JIT. Any out-of-memory row is recorded and marked blocked.
Review-minutes: 8
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-28
Issued: 2026-09-28
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/348
Campaign: draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md

Phase 3 of the campaign prompt above (retained in `draft/` as the campaign intent; its
campaign contract governs). Plan approved by the human in-session 2026-09-28.

## Overview
Phase 3 of interferometer likelihood campaign 3/3. Every committed A100 interferometer mesh row is at the preset mask radius r3.5. The phase-4 decision matrix needs A100 rows at r2.0 and r5.0 next to the CPU rows. This phase runs 12 RAL A100 jobs: Delaunay-1500 and rectangular 39², at sma / alma / alma_high, radii r2.0 / r5.0, fp64. It then writes them up in the A100 mesh ledger and the profiling wiki. No harness code changes: `interferometer_pixelized.py` already takes `--mask-radius` and adds an `_r<radius>` output suffix.

## Plan
- Two new GPU submit scripts (Delaunay, rectangular), each running sma / alma / alma_high at r2.0 and r5.0 in fp64.
- Pre-flight on RAL: the shared mirror matches the library mains and nufftax is at or above the 0.6.1 floor. Submit from a RAL worktree of the branch, then pull the rows back.
- New "Mask-radius sweep — A100 fp64" section in `results/notes/interferometer_mesh_a100_breakdown_2026_09.md`.
- Update the wiki campaign page and index row (the #338 rule), regenerate the README dashboards, keep lint green.




### Affected Repositories
- autolens_profiling (primary, workspace-only)

### Branch Survey
| Repository | Current Branch | Dirty? |
|-----------|---------------|--------|
| lens/autolens_profiling | main (level with origin) | clean (untracked `dataset/abell_1201/`, untouched) |

**Suggested branch:** `feature/interferometer-mesh-breakdown-jax`

### Implementation Steps
1. `hpc/batch_gpu/submit_breakdown_interferometer_{delaunay,pixelization}_a100_radius_sweep_fp64`, cloned from `submit_breakdown_interferometer_delaunay_a100_alma_fp64_n_sweep`. Keep its env block, source-revision echo, nufftax floor assert and x64. Each leg runs `scripts/interferometer/likelihood_breakdown/{delaunay,pixelization}.py --instrument <inst> --mask-radius {2.0,5.0} --config-name hpc_a100_fp64 --vmap-batch 16,4`. The lever sub-rows are off.
2. Outputs keep the existing layout: alma rows go in the `results/breakdown/interferometer/` root, and sma / alma_high rows go in `<inst>/`. Files are named `{delaunay,pixelization}_hpc_a100_fp64_r{2.0,5.0}.{json,png}`. The run-time dashboard (`CONFIG_TAGGED_RE`) does not ingest them, by design.
3. alma_high r5.0 risks running out of memory, since its FFT extent is about (5/3.5)² × 560². An out-of-memory error is recorded in the JSON and marked blocked in the ledger; it does not fail the phase.
4. Ledger section with one row per instrument × radius × mesh. Columns: masked pixels, nnz/col, full-JIT ms, F share, step sum ÷ full JIT, source revisions, RAL job ids. It also carries a flag for phase 4: phase-2 CPU radius rows exist only at alma, so sma / alma_high CPU rows at r2.0 / r5.0 are still missing.
5. Wiki: add a journal entry to `wiki/campaigns/interferometer_likelihood.md` and update its Headline / Profiling PRs / Next lines. Update the `wiki/index.md` row. Then run `check_wiki.py --check`, `build_readme.py` (then `--check`) and `check_results_layout.py`.

### Key Files
- `scripts/misc/likelihood_breakdown/interferometer_pixelized.py`: harness (`--mask-radius` :137, `mask_radius_suffix` :306)
- `hpc/batch_gpu/submit_breakdown_interferometer_*_a100_*`: submit templates
- `results/notes/interferometer_mesh_a100_breakdown_2026_09.md`: ledger
- `wiki/campaigns/interferometer_likelihood.md`, `wiki/index.md`


**Witness:** all 12 `results/breakdown/interferometer/[<inst>/]{delaunay,pixelization}_hpc_a100_fp64_r{2.0,5.0}.json` files exist with non-null steps. Each has `mask_radius_arcsec` equal to the requested radius and inversion path `InversionInterferometerSparse`, with the step sum within 10 % of the full JIT. Any out-of-memory row is recorded and marked blocked.

## Survey finding (for phase 4)

Phase-2 CPU radius rows exist only at alma (r2.0 / 4.25 / 5.0 / 6.0). sma and alma_high CPU
rows at r2.0 / r5.0 are missing — phase 4 must add them before the decision matrix can be filled.
