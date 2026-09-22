## euclid-single-rgb-vis-lp
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/98
- issued: 2026-09-20
- prompt: active/single_rgb_dr1_vis_lp_pilot.md
- session: Codex (session ID unavailable)
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/99
- heart-red-override: User authorized issue #98 development override in this session: "Authorize issue #98 development override" in response to commit, push, pending-release PR, and RAL deployment for this branch. Heart RED: `release validation FAILED (stage integrate)`. Final branch gates: 223 fast tests passed (10 deselected); 37 focused tests passed; Euclid smoke 9/9 passed; Ruff check/format and diff check passed; real DR1 JPG rendered to two-panel `rgb.png`; review faculty surface at f28e3cf judged CLEAN. Development shipping only; no merge or release.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/euclid-single-rgb-vis-lp
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-single-rgb-vis-lp

- completed: 2026-09-21
- merge: 1c67027fa1cda094ba614ef795b924f00eb7271d
- reconciliation: PR #99 verified MERGED through GitHub; clear stale awaiting-merge claim only. Existing worktree and local science data remain untouched.

## Original prompt

# Single RGB visualisation for the Euclid DR1 VIS-LP pilot

Work type: feature
Target: euclid_strong_lens_modeling_pipeline
Repo: @euclid_strong_lens_modeling_pipeline
Issued: 2026-09-20

## Original request

ok thefile i just added images.zip has the rgb images dfor all 14000 objects. It looks like its one rgb per lens (not rgb_0 and rgb_1) like before. Can you find the 10 lenses we submitted and cancelled, upload their rgbs to RAL so they are loaded and vis_lp outputs them in their image folder via the util.py route and then submit the run?

## Context

`images.zip` is in the `euclid_dr1` science project. The first ten tiles in the full 15,032-tile tile-ID ordering have one unique JPG each in the archive. The first tile already has a completed top-1000 VIS-LP fit; the cancelled pilot 345242 covered the next nine (`dr1_sep1_rest` batch 01 indices 0–8). The current `util.VisualizerImaging` requires both `rgb_0` and `rgb_1`, so a single `rgb.jpg` is skipped. Preserve the existing two-image route while supporting a single RGB and its masked view in `image/rgb.png`.

## Proposed plan

1. In `euclid_strong_lens_modeling_pipeline/util.py`, keep the existing `rgb_0`/`rgb_1` four-panel path. When that pair is unavailable, load a single `rgb` PNG/JPG/JPEG and write `image/rgb.png` with the original and mask-applied views.
2. Add a focused visualizer test that exercises the one-image route and the existing two-image route, including the output filename and panel count. Run that test and the relevant fast suite.
3. Ship the workspace change, port only the reviewed visualizer change to the private `euclid_dr1` science clone, and sync its `util.py` to RAL after checking the currently running jobs. Do not refresh shared PyAuto libraries.
4. The ten selected JPGs from `images.zip` are staged as `rgb.jpg` in their corresponding local dataset directories and checksum-verified on RAL. The first tile already has a completed top-1000 `vis_lp` result and `image/rgb.png`; resubmit the nine cancelled `dr1_sep1_rest` tasks as array indices `0-8`, then record the new job ID in Cortex.

Branch: `feature/euclid-single-rgb-vis-lp` in a dedicated workspace worktree.
