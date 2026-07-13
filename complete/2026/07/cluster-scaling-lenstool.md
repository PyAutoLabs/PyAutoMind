## cluster-scaling-lenstool
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/237 (closed)
- completed: 2026-07-09
- pr: autolens_workspace#238 (merged)
- notes: Cluster + group scaling relations moved to the Lenstool/community convention, closing the
  referee-comment response: b0_i = b0_ref·(L_i/L_ref)^0.5 (and einstein_radius_ref for the group
  Isothermal tier) anchored to the brightest scaling member, exponents FIXED at Faber-Jackson 0.5,
  rs_i scaled ∝ L^0.5 on the cluster dPIE tier; tier dimensionality 2→1 (cluster N=13→12).
  Bergamini+19 kinematic slopes documented as the refinement; freeing the exponent shown as a
  one-line systematics test. Cluster dataset regenerated on the new truth (b0_ref=0.12 @
  L_ref=0.40; both sources still triply imaged); group dataset untouched by construction (equal
  member luminosities → ratios 1 — check this trick when changing conventions). 10 scripts across
  scripts/cluster/ + scripts/group/features/scaling_relation/. Gotchas: (1) navigator-catalogue CI
  leg — any workspace script-prose change needs `python PyAutoBuild/autobuild/regenerate_navigator.py
  autolens` committed, or 'Catalogue staleness' fails the PR; (2) subplot_tracer on the 14-galaxy
  multi-plane tracer is pathologically slow (>29 min), so tracer.png/galaxies_images.png were
  dropped from the committed dataset (old-truth artifacts anyway) — regenerate-on-use; the slow-viz
  fix is the shipped cluster plotters (PyAutoLens#578). Follow-up filed on the issue: imaging/
  features/scaling_relation, group/slam.py, guides/advanced/multi_plane.py still show the old form.
