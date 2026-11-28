## adapt-mesh-weighting-library
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/716
- completed: 2026-11-26
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/717
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/717
- Phase 1 of making the adapt-mesh-weighting result (PyAutoArray#714) the default everywhere. Added `image_mesh.HilbertSNR` (Hilbert draw with a point budget in absolute S/N: 25% even, 5% by (s/max)^8, 70% by (x/(x+3))^2 with x = max(S/N - 2, 0); `HilbertSNR(pixels=...)` is the default the human approved at gate 2), `image_mesh.soft_snr_from` and `image_mesh.adapt_image_soft_from` (the AdaptSplit adapt image). `Hilbert` and the regularizations unchanged (backward compatible, as the human asked).
- Evidence: 8 new tests, full test_autoarray 2622 passed; library mesh and adapt image equal the science project's unified arm exactly (a test-mode SLaM fit, and the mesh on 15 real lenses). Science project: `Science/development/adapt_snr_cap` (`wiki/project/state.md`, `results/snr_range/`).
- Scope merged is phase 1 only. Remainder filed as fresh prompts: phase 2 `draft/feature/autogalaxy/adapt_mesh_weighting_galaxy_adapt_images.md` (public unfloored S/N map + one-call soft AdaptSplit image), phase 3 `draft/feature/autolens_workspace/adapt_mesh_weighting_workspace_default.md` (all workspaces switch to HilbertSNR, drop weight_power / weight_floor and the S/N 3 cap).
- Trap: the input must be the S/N map before PyAutoGalaxy's 1% adapt floor; above peak S/N 200 the floor lifts sky over S/N 2 (2.5 at peak 250) and it is weighted as source.

## Original prompt

# Adapt mesh weighting: S/N-budget Hilbert mesh and soft adapt image in the library

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Difficulty: large
Autonomy: supervised
Priority: high
Consequence: judge
Parent: active/make_the_source_adapt_image_hilbert_image.md (PyAutoArray#714, task adapt-mesh-weighting)
Filed: 2026-11-26
Issued: 2026-11-26
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/716

Library phase of PyAutoArray#714. Research phases 1-2 ran in the science project
`~/Science/Science/development/adapt_snr_cap/` (read its `AGENTS.md` and
`wiki/project/state.md`). The human approved the result at gate 2 on 2026-11-26 ("looks good, I
approve proceed", on `results/snr_range/index.html`), after the unified arm was fitted on the
10 HST and 10 COWLS datasets (RAL 416941, 416981) and checked offline from peak S/N 5 to 1000.
The workspace phase (autolens_workspace scripts drop the S/N 3 cap of autolens_workspace #522
and use this default) and the docs are separate prompts, after this one ships.

## Scope, as the human set it (2026-11-26)

> I approve, can you make this the default everywhere (but keep BC via `Hilbert` great idea,
> ensure `AdaptSplit` retians BC too), so all workspaces use the new one and a user doesnt need
> to supply weight_power=3.5 and weight_floor=0.01 the default always gives this great adaption

- `image_mesh.HilbertSNR(pixels=...)` with no other arguments gives the approved weighting.
- `image_mesh.Hilbert` and `reg.AdaptSplit` keep their current behaviour and signatures (backward
  compatibility); the new behaviour reaches AdaptSplit only through the adapt image it is given.
- Every workspace (autolens_workspace, autogalaxy_workspace, HowToLens / HowToGalaxy, the
  `_test` workspaces where they model with Hilbert) switches to the new default and stops
  passing `weight_power` / `weight_floor` and the S/N 3 cap.

Phases: (1) PyAutoArray: `HilbertSNR` + the soft S/N transform; (2) PyAutoGalaxy: one call
giving the unfloored S/N map and the soft AdaptSplit image; (3) workspaces switch (own
prompts); then the science project's `slam.py` uses the library calls.

## What the human approved (the `peak_share_unified` arm)

Reference implementation: the project's `scripts/mesh_weighting.py` (`peak_share`,
`soft_term`, `above_noise`, `regularization_image_from`, `image_plane_mesh_grid_from`) and
`scripts/slam.py` (`unfloored_source_snr_from`, `galaxy_name_image_dict_from`, `source_pix_2`).

1. **Hilbert image-mesh weighting** (in place of `w = (|a| / max a) ** 3.5`, floored at 0.01),
   per Hilbert cell with S/N `s` and `x = max(s - 2, 0)`:
   `p = 0.25 / n + 0.05 * (s / max s) ** 8 / sum(...) + 0.70 * (x / (x + 3)) ** 2 / sum(...)`:
   25% of the points spread evenly over the mask, 5% on cells within about 25% of the peak
   S/N, 70% by a soft S/N saturation in absolute S/N (not normalised by the peak). Points are
   then drawn by the existing deterministic Hilbert inverse-transform sampling.
2. **AdaptSplit adapt image**: the same soft transform pixel by pixel, `(x / (x + 3)) ** 2`,
   floored at 1% of its maximum, in place of the S/N map (or the S/N map capped at 3).
   AdaptSplit itself is unchanged (it still divides by the maximum and raises to its free
   `signal_scale`).
3. **Both from the S/N map before the adapt floor**: `galaxy_name_image_dict_via_result_from`
   floors every adapt image at `adapt_minimum_percent` (1%) of its maximum; above a peak S/N of
   200 that lifts empty sky over the S/N 2 threshold (sky reads 2.5 at peak 250, 10 at 1000) and
   breaks both. The S/N map before the floor (it is already cached raw, as
   `files/galaxy_images_snr.fits`), negatives set to 0, is the input. Evidence:
   `scripts/snr_range.py`, `results/snr_range/summary.txt`.

## Open design questions for the plan

- New image-mesh class (e.g. `image_mesh.HilbertSNR`, with the six numbers as keyword
  arguments) or a new weighting mode on `Hilbert`? A new class keeps every existing pinned
  workspace_test value unchanged and old fits reproducible.
- Where the soft transform and the unfloored map live in PyAutoGalaxy so a workspace script
  needs one call to get both the mesh input and the AdaptSplit image (an option on
  `galaxy_name_image_dict_via_result_from`, or a small helper next to it). Other users of the
  floored adapt image (other regularizations, model-image adapt images) keep the floor.
- Order against `draft/bug/autoarray/hilbert_image_mesh_frame_independent.md`, which changes
  the same Hilbert interpolation and re-pins workspace_test values.

## Known limits (measured, accepted by the human)

- At peak S/N ~5 most points sit on the few pixels above S/N 2 (median 36 per image pixel over
  19 lenses) and the AdaptSplit image has no source/sky contrast.
- When the whole source is very bright (peak 250-1000) the mesh spreads evenly over all
  detected emission, arcs and faint wings alike (the saturation at S/N ~3).

## Done when

- Unit tests: the weighting reproduces the project's `peak_share` probabilities and meshes on a
  test adapt image (to rounding); the soft transform matches `regularization_image_from`; the
  unfloored input is used; a peak-250 compact-source test keeps the sky share near 0.25.
- Existing Hilbert behaviour and pinned values unchanged.
- The project's `slam.py` unified arm can be rewritten to the library calls and gives the same
  mesh (0.0 arcsec) on a test-mode lens.
