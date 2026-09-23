# multi_dataset/jax_likelihood/delaunay.py asserts the wrong likelihood on main (−72070 vs 1995)

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: The script's own parity assertion passes on main (ACTUAL == DESIRED at rtol 1e-4) and the cause is named — a stale DESIRED constant, a changed dataset/simulator, or a library regression — with the fixing commit or the corrected constant justified from an independent NumPy evaluation.
Review-minutes: 10
Unattended: safe
Filed: 2026-09-23

## Observed

While validating PyAutoArray#566 (2026-09-23) against the canonical stack (PyAutoArray main
22e6d608, autolens_workspace_test main), `scripts/multi_dataset/jax_likelihood/delaunay.py`
fails its own assertion identically under BOTH positive-only solvers (library PDIP and the new
certified solver), so the solver is not the cause:

    ACTUAL [-72070.621739 x3] vs DESIRED 1995.085399, rtol 1e-4

Every sibling JAX parity script (imaging/jax_likelihood/{lp,rectangular_mge,potential_correction,
delaunay}.py, weak/jax_grad.py) passes on the same stack. Not filed by the PyAutoArray#566 PR —
the failure predates that branch.

## Do

Reproduce on main; evaluate the multi-dataset Delaunay likelihood eagerly in NumPy for the same
instance; decide whether DESIRED is stale (then fix the constant with its derivation in a comment),
the dataset/simulator changed (then re-simulate and re-pin), or a library regression exists (then
route to the library via start_dev). Check the Heart workspace-validation run history for when it
first went red.
