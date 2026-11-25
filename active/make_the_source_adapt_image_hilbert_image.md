# Make the source adapt image / Hilbert image mesh adapt well…

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Lane: ral
Issued: 2026-11-25

## Background (read these first)
- Evidence and audit that motivated this:
  `~/Science/Science/development/adapt_snr_cap/` — read `AGENTS.md`,
  `wiki/project/state.md`, `scripts/slam.py`, `scripts/compare.py`, and the comparison page
  `results/compare/index.html`. Results are in `output/<sample>/<lens>/{shared,cap3,uncapped}/`.
  It runs the autolens_workspace Delaunay SLaM
  (`autolens_workspace/scripts/imaging/features/pixelization/delaunay.py`, Hilbert 1250 points,
  `weight_power=3.5, weight_floor=0.01`, AdaptSplit) on 5 SLACS, 5 BELLS GALLERY and 4 Euclid
  DR1 lenses, in two arms that differ only in the source adapt image:
  `cap3` (S/N map capped at 3.0, the workspace rule since autolens_workspace #522,
  Mind `complete/2026/09/adapt-image-snr-cap.md`) and `uncapped` (raw S/N map).
  The Euclid arm was RAL job 416418; pull it first if `output/euclid/` is incomplete.
- Origin of the cap: `~/Science/Science/archive/subhalo_validation/wiki/project/results_summary.md`
  (`pl_eff_1_outer`: outer images got 1–3% of the core's mesh weight).
- Library: `PyAutoArray/autoarray/inversion/mesh/image_mesh/hilbert.py` and the weighted-mesh
  base (`weight_map_from`: `w = (|adapt| / max(adapt)) ** weight_power`, floored at
  `weight_floor`, then points drawn ∝ w), plus the existing but rejection-only guards
  `check_mesh_pixels_per_image_pixels` and `check_adapt_background_pixels`. Also the AdaptSplit
  regularization's signal weighting (also peak-normalised), and
  `PyAutoGalaxy/.../adapt_images.py` `galaxy_name_image_dict_via_result_from` (S/N map default).
  Look through PyAutoArray / autolens_workspace git history (from 2023-12 on) for earlier Hilbert
  variants that resampled to protect background coverage.

## The problem, in the human's words
Neither arm is right on every lens. Uncapped covers more of the source when it is extended
and less compact (slacs0216, slacs0252, slacs1627). Capped gives the compact parts the
resolution they need where uncapped is too coarse (slacs1430, slacs1250, BELLS J1110+3649).
BELLS GALLERY needs a very high effective source resolution to reconstruct its compact
Lyman-alpha blobs. The cause is that the weight is normalised by the peak: with peak S/N 250,
everything below S/N ~67 sits on the floor, so the mesh barely adapts; capping at 3 flattens
everything above S/N 3 to the same weight, so all the source structure is treated as equal.
`weight_power=3.5, weight_floor=0.01` on an S/N map "works for many lenses", but it is
heuristic. Constraints:
- Bayesian evidence cannot pick the adaptation by itself: in the past, meshes that pile nearly
  all pixels on the source and leave the background with almost none were often favoured.
- Hilbert parameters move every mesh point, so sampling them inside a search
  (`source_pix[2]`) gives a discontinuous likelihood; that route has never worked well.

## Goal
A source adapt-image → image-mesh weighting that gives good adaptation by default across
Euclid (0.1"/px, low S/N), HST (SLACS 0.05", BELLS 0.04", compact high-S/N clumps) and higher
resolution data, without per-lens tuning most of the time, and with a clear, documented knob a
human can turn after `source_pix[1]` (inspect the adapt image and mesh, then adjust) before
`source_pix[2]`. Working in S/N is probably right, since it normalises across instruments, but
it is open; a source-gradient / structure term may help.

## What to do
1. Measure before proposing. On the 14 lenses' `source_pix[1]` adapt images (both arms),
   quantify the coverage each weighting gives: points per unit S/N band, background share,
   points on compact clumps vs extended arcs, effective source-plane resolution. Make plots.
2. Propose 2–4 candidate weightings, built offline from the saved `source_pix[1]` adapt images
   (no fits needed to compare meshes). Ideas, not requirements:
   - an S/N transform that is not peak-normalised (e.g. log / asinh / rank- or
     quantile-based weights, or a soft cap that compresses rather than clips);
   - a fixed point budget: a guaranteed share for the background, the rest for the source,
     split by S/N and/or a gradient or curvature estimate;
   - a gradient / structure term so compact, sharply varying regions get resolution even when
     not the brightest;
   - the same treatment of the AdaptSplit signal weighting, so mesh and regularization agree.
3. Pick quantitative, non-evidence checks of "good adaptation" (e.g. residual structure in the
   compact regions, background coverage floor, source-plane pixel size vs PSF-deconvolved
   feature size), and use the evidence only as a secondary check, aware of the bias above.
4. Fit the winning 1–2 candidates on the same 14 lenses (a new arm in `adapt_snr_cap`, or a
   successor project), RAL GPU, and compare with `cap3` / `uncapped` using `compare.py`.
5. Deliver: a library default (PyAutoArray / PyAutoGalaxy) through the dev workflow,
   workspace scripts and docs updated so every SLaM uses it, one human-facing tuning knob
   documented, and a short note on how to tune it after `source_pix[1]`.

## Rules
- Plan first and wait for approval before editing library or workspace code.
- Library changes go through PyAutoLabs dev worktrees, not the science project.
- Ask before RAL submissions and record runs in the Cortex.
- Do not record verdicts on which arm is "better" in your own words; show the evidence and let
  the human judge.

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/tmp/claude-1000/-home-jammy-Science/8bf66d7b-2128-41e7-86f0-68d09386bd8e/scratchpad/brief.md -->
