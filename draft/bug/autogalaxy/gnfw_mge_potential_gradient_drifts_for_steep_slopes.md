# gNFW MGE potential gradient drifts from the deflections for steep inner slopes

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: for an elliptical gNFW with inner_slope 0 to 2.5, the finite-difference gradient of potential_2d_from matches deflections_yx_2d_from to 1e-4 relative at radii 0.2 to 3 arcsec

Found 2026-11-19 while fixing PyAutoGalaxy#729 (gNFW MGE inner-mass deficit). `MGEDecomposer.potential_2d_via_mge_from` (`autogalaxy/profiles/mass/abstract/mge.py`) gets psi by integrating the MGE deflection along the ray from the origin with a fixed 20-node Gauss-Legendre rule. For a steep cusp the integrand is sharply peaked near t = 0, so the rule loses accuracy. On main b9232172 (MGE-only, no #729 term), elliptical gNFW (ell_comps (0.1, 0.05), scale_radius 10), max relative |grad psi - alpha| at (0.3,0.4), (-1,1.5), (2,-0.5) is 2.3e-6 at inner_slope 1, 8.7e-4 at 2.0 and 6.3e-3 at 2.4. The #729 inner-mass term is exactly consistent (|grad - alpha| <= 4e-10), so this is the MGE potential's own quadrature. It matters for time delays and anything that uses the potential with steep cusps.
reproduce before fixing: the finite-difference check above on main; the n_quad argument cannot be raised from outside (IndexError at n_quad=200), so the nodes appear fixed at 20.
Fix: a cusp-aware substitution in the radial integral (e.g. t = s^k), or more nodes, or a closed-form per-Gaussian potential for the circular case; add the gradient-consistency test over inner_slope 0 to 2.5.
