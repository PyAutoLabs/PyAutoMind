`gNFW` MGE deflections were biased low for steep inner slopes (0.8% at inner_slope 2, 6% at 2.4, 10% at 2.5) because the 30-Gaussian MGE of the 3D density starts at scale_radius / 20000 and missed the mass inside that cut-off. The fix adds it back as a central term (exact 3D mass inside 10 sigma_min minus the Gaussians' mass there, as a uniform disc of radius sigma_min), with the matching potential term. Deflections now match direct numerical integration to <= 5.3e-5 over inner_slope 0–2.8 for scale_radius 5–40.

Built by shift 2026-11-19-am (worker f6597b74). The human ended the shift early to skip the worker's full serial smoke sweep ("lets just say its ok and end it early … but try make sure a few key tests ran"); the PR was opened from the cockpit chat after a targeted smoke on the branch (two gNFW integral checks, misc/mass/dark.py, autolens group_halo modeling — all passed). Shipped in PyAutoGalaxy#730, merged 2026-11-19 by human /prm.


## Original prompt

# gNFW MGE deflections lose accuracy for inner_slope above 2…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: gNFW deflections agree with direct numerical integration to 1e-3 over inner_slope 0 to 2.5 at radii 0.2 to 3 arcsec, or the profile documents and enforces a validated inner_slope range
Review-minutes: 3
Unattended: ready
Verified: 2026-11-19 b9232172 (PyAutoGalaxy)
Lane: any

Found 2026-11-16 in the science project stars_dm_slope. `gNFW.deflections_2d_via_mge_from` (`autogalaxy/profiles/mass/dark/gnfw.py`) expands the 3D density in 30 Gaussians between scale_radius/20000 and 200 x scale_radius. Compared with direct numerical integration of the convergence at radii 0.2 to 3 arcsec and scale_radius 5 to 40 arcsec, the worst relative deflection error is below 5.3e-4 for inner_slope <= 1.5, 0.8% at 2.0, 2.3% at 2.2 and 6% at 2.4: the mass inside the inner cut-off is no longer negligible for steep cusps. Script and numbers: `/home/jammy/Science/Science/development/stars_dm_slope/scripts/scratch/gnfw_mge_accuracy.py`, `/home/jammy/Science/Science/development/stars_dm_slope/results/mocks_v1/phase1/logs/gnfw_mge_accuracy.json`. Fits that let inner_slope approach or exceed 2 (some published models use priors up to 3) get a biased likelihood with no warning.
Fix: either add the analytic mass inside the inner cut-off as a point-like term, extend the Gaussian range adaptively with inner_slope, or document and enforce a validated range (and set the default prior to it); add an accuracy test against numerical integration over inner_slope 0 to 2.5.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/7_gnfw_mge_accuracy_steep_slope.md -->
