# gNFWMCRLudlow normalises kappa_s with the NFW mass function whatever the inner slope…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: the 3D mass inside r200 of a `gNFWMCRLudlow` halo equals `mass_at_200` to 1e-3 for inner_slope 0.5, 1.0 and 1.5
Review-minutes: 3
Unattended: ready
Lane: any

Found 2026-11-16 in the science project stars_dm_slope by reading the code. `gNFWMCRLudlow` (`autogalaxy/profiles/mass/dark/gnfw_mcr.py`) gets kappa_s and scale_radius from `mcr_util.kappa_s_and_scale_radius_for_ludlow`, which uses the NFW characteristic overdensity 200/3 c^3 / (ln(1 + c) - c/(1 + c)) and never sees `inner_slope`. For inner_slope != 1 the halo built from `mass_at_200` therefore does not contain that mass inside r200 (at fixed inner mass, log M200 moves about 0.9 dex per unit of slope, so the error is large), and a prior on `mass_at_200` is not a prior on M200.
Fix: use the gNFW normalisation (3 - gamma) c^gamma / 2F1(3 - gamma, 3 - gamma; 4 - gamma; -c) as `gnfw_virial_mass_conc.py` does (with the z < -1 hyp2f1 fix filed separately), decide and document which concentration the Ludlow relation supplies (r200/r_s or r200/r_-2 = r200/((2 - gamma) r_s)), and add a test that the 3D mass inside r200 equals mass_at_200 for inner_slope 0.5, 1 and 1.5. Check the cored and truncated MCR variants for the same assumption.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/5_gnfw_mcr_ludlow_normalisation.md -->
