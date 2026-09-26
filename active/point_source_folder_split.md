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
