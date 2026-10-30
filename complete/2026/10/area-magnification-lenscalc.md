# LEGGOS area magnification on LensCalc (arc phase 6a)

- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/685

Issue PyAutoGalaxy#684 → PR PyAutoGalaxy#685 merged 2026-10-30. Epic `cluster-strong-lensing`, phase 6a (parent
`draft/feature/autolens/area_magnification_leggos.md`).

Added `LensCalc.source_plane_area_from(mask, sub_size=4)` (A_src = Σ A_pix,i/|μ_i|, LEGGOS Eq. 7, links to source
size), `area_magnification_from(mask, sub_size=4)` (μ_area = A_img/A_src, Eq. 6, one image per mask),
`image_masks_from(mask)` (split by parity + connected regions; touching same-parity images not separated) and
`area_magnification_list_from(mask, sub_size=4)`. Hessian μ at sub-pixel centres; NumPy only.

Tests: analytic SIS annulus μ_area −4.7e-4, A_src −1.5e-4; sub_size convergence second order (3.9e-4 → 5.7e-6);
parity split across the Einstein ring (outer ring −6e-4 vs analytic); double-counting trap. PyAutoGalaxy 1466 passed,
PyAutoLens 1015 passed / 1 xfailed; CI docs + 3.12/3.13/nojax green. Heart STALE (release validation) acknowledged;
human authorized ship + merge.

Next slices: 6b autolens_workspace_test validation vs simulated truth (uniform-disk source, resolution + segmentation
controls), 6c source_science docs, 6d autolens_assistant LEGGOS II ingest.

## Original prompt

# Area magnification on LensCalc (LEGGOS Eq. 6-7): per-pixel inversion over an image-plane mask

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
Epic: cluster-strong-lensing
Phase: 6a
Parent: draft/feature/autolens/area_magnification_leggos.md
Arc: draft/feature/autolens/source_cluster_arc.md
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Filed: 2026-10-30
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/684
Witness: `LensCalc.area_magnification_from(mask)` reproduces the analytic SIS annulus-segment area magnification to <0.5% at sub_size 4 with error falling as sub_size grows; `area_magnification_list_from(mask)` splits a mask covering several images into same-parity connected segments and returns one value per image; works for a Tracer via `LensCalc.from_tracer(..., plane_j=)`; full PyAutoGalaxy + PyAutoLens suites pass.

## Original request (human, 2026-10-30)

> ship it when the tests pass, do all steps and then do phase 6

Phase-6 parent (verbatim user request, 2026-08-19): "Ability to get areas only Magnification as extension to
source science scripts. Look at LEGGOS paper for description of equations but basically area extension to the
above, seems like standard calculation in cluster lensing. [...] Remember also that area can link to source size."

## Slice

Phase 6 is split: **6a** library API (this prompt, PyAutoGalaxy `LensCalc`, which PyAutoLens reaches through
`LensCalc.from_tracer`); **6b** autolens_workspace_test validation against simulated truth (uniform-disk source of
known area, resolution and segmentation controls, CI smoke); **6c** workspace docs (source_science scripts:
area magnification + source size); **6d** autolens_assistant LEGGOS II wiki/literature ingest. Forward ShapeSolver
stays out of scope (transferred to cluster-pointsolver-speed).

## Work

1. `LensCalc.source_plane_area_from(mask, sub_size=4, xp=np)`: A_src = sum over the mask's sub-pixels of
   (sub-pixel area / |mu|), mu from `magnification_2d_via_hessian_from` (LEGGOS Eq. 7). This is the source-plane
   area the image region maps from — the link to source size.
2. `LensCalc.area_magnification_from(mask, sub_size=4, xp=np)`: mu_area = A_img / A_src (LEGGOS Eq. 6), for a
   mask covering ONE image. Document that a mask spanning several images of the same source double-counts A_src.
3. `LensCalc.area_magnification_list_from(mask, sub_size=4)`: split the mask into images — connected regions of
   the same parity (sign of mu; the critical curve is the boundary) — and return one mu_area per segment
   (plus the segment masks), so a whole-arc mask gives per-image values.
4. Unit tests: analytic SIS annulus segment (outer image, theta in [r1, r2] maps to beta = theta - theta_E);
   sub_size convergence; parity split of a mask straddling the tangential critical curve; multi-plane via a
   mocked/Tracer-like deflection callable; NumPy path (JAX optional, importorskip).
