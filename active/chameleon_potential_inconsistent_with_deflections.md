# `mp.Chameleon.potential_2d_from` is inconsistent with its deflections (~60%)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: for an elliptical and a circular `ag.mp.Chameleon`, the central finite-difference gradient of `potential_2d_from` matches `deflections_yx_2d_from` to < 1e-4 of max|alpha| at off-centre points, and lap(psi) = 2 kappa; tests pin it
Filed: 2026-10-29
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/682

Found while fixing PyAutoGalaxy#680/#681 (the `lmp.Gaussian` potential was wrong: its gradient did not reproduce its deflections). Same check on main 2026-10-29: `Sersic` (MGE potential) agrees to ~1e-3 of |alpha| (MGE accuracy, fine); `Chameleon(ell_comps=(0.2,-0.1), intensity=1.0)` gives max|grad psi - alpha| = 6.4e-3 with max|alpha| = 1.0e-2 at (0.7,0.3), (-0.5,0.9), (1.2,-1.0). Determine whether the potential (MGE route in `autogalaxy/profiles/mass/stellar/chameleon.py`) or the deflections are wrong (check div(alpha) = 2 kappa first), then fix the wrong one. A Chameleon is a difference of two cored isothermals, so an analytic potential may exist.
