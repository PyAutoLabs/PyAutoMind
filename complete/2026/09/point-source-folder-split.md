- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/316 (closed completed 2026-09-26)
- completed: 2026-09-26
- epic: point-source-cpu-speed
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/318 (merged `a5e3cdd7147bc59c5e3cd7348ddbebf19142b029`)
- session: Claude Code CLI (Opus 5.5 subagents), task worktree `~/Code/PyAutoLabs-wt/point-source-folder-split`, branch `feature/point-source-folder-split`; start_dev → start_workspace → ship_workspace → prm on 2026-09-26.
- summary: |
    Move-only refactor of autolens_profiling: `scripts/point_source/` held two
    different likelihood functions, so it is split into
    `scripts/point_source_image/` (image-plane χ²: `likelihood_breakdown/
    {image_plane,static_lattice_ab,vertex_dedup_ab}.py`, `likelihood_runtime/
    {image_plane,image_plane_solved}.py`, `quick_update/point_source.py`) and
    `scripts/point_source_source/` (source-plane χ²: `likelihood_runtime/
    {source_plane,source_plane_solved}.py`). Results moved to
    `results/breakdown/point_source_image/`,
    `results/runtime/point_source_image/image_plane_solved/` and
    `results/runtime/point_source_source/source_plane_solved/`; the five HPC
    submit scripts renamed `submit_breakdown_point_source_image_*` with WALL-BASIS
    cells updated; `profile.yml` runtime loop covers both folders; README (regen),
    AGENTS.md and campaign notes repointed. All moves are `git mv`; no numbers or
    behaviour changed.
- notes: |
    - Output dirs are hard-coded per cell (nothing infers the folder from the
      script path), so every path was fixed by hand and confirmed by real runs.
    - `quick_update/point_source.py` went to the image folder because
      `AnalysisPoint`'s default `fit_positions_cls` is `FitPositionsImagePairAllSolved`.
    - Deliberately unchanged: the `point_source` dataset type name/strings,
      `scripts/misc/vram/config.py` keys (they name the dataset), `scripts/cluster/`,
      dated RAL logs and historical prose.
    - Pre-existing, not regressions: `quick_update/point_source.py` ImportError on
      `subplot_fit_quick` (library API change); `test_hazards_prior_exit.py::
      test__records_the_clipper_as_what_blocks_it` fails the same on main.
    - Merge order: this merged first; #315 (point-source-source-plane-breakdown)
      and #314 (point-source-cpu-p4) rebase onto it, and #315's source-plane
      breakdown lands under `scripts/point_source_source/likelihood_breakdown/`.

## Original prompt

# Split scripts/point_source into point_source_image / point_source_source

Type: refactor
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Epic: point-source-cpu-speed
Consequence: judge
Review-minutes: 10
Unattended: ready
Filed: 2026-09-26
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/316

## User request (verbatim, 2026-09-26)

I think we need separate scripts/point_source_image and point_source_source folders they are different likelihood functions

## Scope

Move-only refactor in autolens_profiling, one folder per likelihood function:

- `scripts/point_source_image/`: image-plane chi-squared cells:
  `likelihood_breakdown/{image_plane,static_lattice_ab,vertex_dedup_ab}.py`,
  `likelihood_runtime/{image_plane,image_plane_solved}.py`, and
  `quick_update/point_source.py` if it fits the image-plane likelihood.
- `scripts/point_source_source/`: source-plane chi-squared cells:
  `likelihood_runtime/{source_plane,source_plane_solved}.py`.
- Results move the same way (`results/{breakdown,runtime,likelihood}/point_source/...`
  into `point_source_image/` or `point_source_source/` according to the likelihood).
- Every reference to the old paths is updated: hpc submit scripts (renamed
  `submit_breakdown_point_source_image_*`), `.github/workflows/profile.yml` + README,
  `scripts/misc/vram/config.py` (only if the key is the folder), README/AGENTS/skills,
  in-script output paths, and link targets in results/notes (dated narrative wording kept).
- NOT renamed: the `point_source` dataset type (`dataset/point_source*`, the simulator,
  dataset_type strings) and `scripts/cluster/`.
- Pure moves plus path fixes via `git mv`; no numbers or behaviour change.

## Merge order

This split merges FIRST; point-source-source-plane-breakdown (#315) and
point-source-cpu-p4 (#314) rebase onto it. Human-approved in-session 2026-09-26.

## Witness

`python scripts/misc/tooling/build_readme.py --check`, `check_submits.py --check` and ruff pass;
`git diff -M --stat origin/main` shows renames; one moved cell per folder runs in its
cheapest mode; a grep for `scripts/point_source/`, `breakdown/point_source/`,
`runtime/point_source/` leaves only dated-history wording.
