Standalone guide `autolens_workspace/scripts/guides/units/redshifts_and_angles.py` (with figures in `images/guides/`) explaining why changing lens/source redshift does not change a PyAutoLens image in angular units, and how cluster modellers work physical-first. Distils the Slack thread previously condensed in `guides/advanced/multi_plane.py`. Pointers added from `cosmology.py`, `multi_plane.py`, the units README, and HowToLens chapter 1 tutorials 2–3 and chapter 4 tutorial 5. Adversarially reviewed before shipping.

Follow-up noticed (not filed): HowToLens `chapter_1_introduction/tutorial_2_ray_tracing.py` fails under `PYAUTO_SMALL_DATASETS=1` — `IndexError` in PyAutoArray `autoarray/plot/grid.py` `plot_grid`; pre-existing on main.

## Original prompt

# Guide: why changing redshift does not change a lensed image (angular vs physical units)

Consequence: judge
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/676

## Request (verbatim)

can you take all that lsack discusison and produce it into a separate guide (multi plane stuff is confusing in itself) and put visuals in to help, have the guide describe the problem but then go on to explain how a strong lensing cluster person often goes the opposite direction in that they have physical quantities abd angular stuff comes after (is that true?)

## Context

- Slack discussion (Jack, Andrew, Qiuhan, James) recovered from @autolens_workspace commit `1cab778c^`,
  `scripts/guides/advanced/multi_plane.py` (Slack section from line 278). It was distilled into
  multi_plane.py's "Lensing Units vs Physical Units" section (autolens_workspace#411), but multi-plane is
  confusing on its own, so this wants a separate, standalone guide.
- Draft figures + producer scripts: `C:\Users\Jammy\Workspace\Science\scratch\redshift_angles_explainer\`
  (`make_figure.py`, `make_schematic.py`, README with key quotes).
- Answer to "is that true?": yes for parametric cluster codes (Lenstool v_disp/kpc radii/z, glafic);
  caveats: free-form codes normalise kappa to a reference source redshift; everyone still fits arcsec positions.

## Approved plan (2026-11-17)

New `scripts/guides/units/redshifts_and_angles.py` in @autolens_workspace: problem → geometry sketch →
reduced-deflection / Sigma_crit degeneracy → runnable diff==0 demo → convert afterwards → cluster
"physical first" direction with flow diagram + hold-angle vs hold-mass experiment → multiple source planes
break the degeneracy (numeric demo, MSD, cosmography) → PyAutoLens supports both → links. Figures in
`images/guides/` with `.txt` descriptions; README, cross-links from cosmology.py and multi_plane.py,
llms-full.txt, notebook. Workspace-only.
