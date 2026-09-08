# `mge_model_from`: optional ordering of multiple bases and a configurable ell_comps limit

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-08
Consequence: review
Witness: `mge_model_from(total_gaussians=20, gaussian_per_basis=2, order_bases=True)` returns a Basis model carrying exactly one assertion `basis_0.ell_comps_1 > basis_1.ell_comps_1`; `order_bases=False` (the default) carries none and every existing test is byte-for-byte unchanged; `ell_comps_limit=0.5` sets the TruncatedGaussian ell_comps bounds to ±0.5; the Euclid pipeline composes its vis_lp lens light with `ell_comps_limit=0.5, order_bases=True` and no prior reassignment loop.
Review-minutes: 5
Unattended: ready


Human direction 2026-09-08 (verbatim): "I think that the solution should be implemented in the source as an extension to mge_model_from, I think it should be default off for now but used in the euclid pipeline with it on, and we can swap it to default on once its properly tested".

Context: `mge_model_from(gaussian_per_basis=K>1)` builds K bases with identical sigma ladders, iid ell_comps priors and a shared centre, so swapping any two bases' ell_comps is an exact label symmetry of the likelihood (euclid_strong_lens_modeling_pipeline#54, `docs/mge_label_degeneracy.md`). PyAutoFit#1583 (merged 2026-09-08) makes `add_assertion` enforceable on the JAX path, and gathers child-attached assertions, so an assertion on the returned Basis model is enforced on both backends.

Add to `autogalaxy/analysis/model_util.py::mge_model_from`:
1. `order_bases: bool = False` — when True, `gaussian_per_basis > 1` and not `use_spherical`, add to the returned `af.Model(Basis)` one assertion per consecutive pair, `ell_comps_1[j] > ell_comps_1[j+1]`, named `mge_basis_{j}_ell_comps_1_gt_basis_{j+1}`. The key is `ell_comps_1` (cos 2φ component), not the magnitude: on the Euclid phase-4 tiles the two bases often sit at the ±0.5 edge with opposite signs (equal magnitude), where a magnitude key slices both modes. Docstring: what it removes, why e1, the blind band (a small |Δe1| between bases means the ordering did not resolve on that dataset), that it changes the run identifier, that `take_attributes` refuses a target with assertions, and that the default stays off until validated.
2. `ell_comps_limit: float = 1.0` — the TruncatedGaussian ell_comps bounds become ±`ell_comps_limit` (uniform priors keep `ell_comps_uniform_width`). Needed so callers set tighter bounds without replacing the prior objects an assertion references.

Tests in `test_autogalaxy/analysis/test_model_util.py`: default off → no assertions, existing tests unchanged; order_bases with K=2 → one assertion, K=3 → two, spherical → none; an ordered vector satisfies and its swap fails via `assertions_satisfied_from_vector`; `ell_comps_limit=0.5` bounds. No JAX in unit tests.

Follow-up (workspace): euclid_strong_lens_modeling_pipeline#57 composes with `ell_comps_limit=0.5, order_bases=True`.
