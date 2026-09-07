# Give imaging/jax_likelihood/mge_group.py a dataset that actually contains group members

Type: test
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Witness: the script fits a `simulator/group.py` dataset with N>=2 simulated satellites of theta_E >= 0.1", its extra-galaxy `einstein_radius` priors are centred on those truths (not on 0), the source basis is non-zero at prior medians, and `|delta_ll| > 9.0` holds for the +5% mass perturbation.
Unattended: ready
Filed: 2026-09-07

autolens_workspace_test#299 (2026-09-07) fixed the zeroed-source failure of
`mge_group.py` by anchoring the model on the simulator truth — and because
`simulator/simple.py` simulates no group members, the five `IsothermalSph` satellites'
`einstein_radius` prior became `UniformPrior(0.0, 0.02)`.

The script therefore no longer exercises satellites with meaningful mass: the group's
lensing contribution is negligible, though the five deflection computations remain in the
jit graph and are perturbed by the assertion.

The honest version is a group dataset: add `scripts/imaging/simulator/group.py` (or reuse
autolens_workspace's group simulator at the 100x100 @ 0.3" smoke geometry), simulate 2-5
satellites at known positions/masses, point `mge_group.py` at it with priors anchored on
those truths, and re-pin. Keep the 9.0 floor.

Runs on the weekly/integrate channels only, so budget the pin regeneration accordingly
(see the fb6e709 lesson in #297: off-gate scripts were not re-matched by the dataset
rebuild).
