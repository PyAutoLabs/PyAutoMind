- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/682
- completed: 2026-10-30
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/683
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/350
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/683
- summary: Merge 9b18db7 (+ ws_test c260ca4). The `mp.Chameleon` deflections were right (div alpha = 2 kappa); the potential's MGE call used the circularised ellipticity convention against a major-axis convergence, so grad(psi) was ~1/q x alpha. A convention fix alone left ~0.35% of max|alpha|, so the potential is now Keeton's closed form for each of the two cored isothermals (log coefficient b·q·s), with psi(centre) = 0; grad(psi) = alpha to ~2e-8. Follow-ups from the human: Chameleon.axis_ratio (mass + light) uses xp.where instead of a Python if, and lp.Chameleon.image_2d_from passes xp through, so all Chameleon methods jit over traced ell_comps (match NumPy to ~3e-16). DECISION TAKEN: the docstrings now state the implemented convergence (second core = core_radius_1, 2s/(1+q) rescaling, 1/(1+q) prefactor), and the parametrisation is unchanged (the old s0+s1 claim was docstring-only). autolens_workspace_test stellar.py comment updated (42 PASS / 0 FAIL).
- tests: 9 new mass + 1 new light Chameleon tests (controls fail on main); test_autogalaxy 1461 passed; test_autolens 1015 passed (first commit); CI green on 0b62e62c (3.12, 3.13, nojax, docs) and ws_test smoke 3.12/3.13.
- follow-up (unfiled): the Gaussian block in autolens_workspace_test scripts/misc/mass/stellar.py still says "computed via MGE decomposition" plus an MGE-limitation NOTE; mp.Gaussian's potential is a direct line integral since #681, so verify the NOTE, then update. Ship-time omission: the active.md row lacked its pending-release line; it was added here.

## Original prompt

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
