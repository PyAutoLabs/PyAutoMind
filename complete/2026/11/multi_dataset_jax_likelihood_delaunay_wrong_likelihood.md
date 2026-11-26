- summary: retired, not fixed — the human answered Q29 "retire" (2026-11-26). The September −72070 vs 1995 mismatch never reproduced: the script passed on workspace main 48f40953 (shift 2026-11-24-am) and again on be51efb with PyAutoArray 86623611 / PyAutoGalaxy 68dc088c / PyAutoLens 903c0814 (ACTUAL 2013.50609816 == DESIRED 2013.5060801 at rtol 1e-4, JIT round-trip PASS). The cause of the historical negative value stays unknown; the original g/r inputs and stack were not available.
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371 (closed not planned; verdict https://github.com/PyAutoLabs/autolens_workspace_test/issues/371#issuecomment-7202721864)
- findings: d215674 raised DESIRED by 18.42068074 for the two intrinsic-regularized mappers (explains 1995 → 2013.5). Heart recorded the script as skipped on 2026-09-23 after an earlier 1805 s JAX hang, so no run ever recorded the numerical failure.
- PRs: none (no code change)
- shift: 2026-11-26-pm (resumed from 2026-11-24-am park)

## Original prompt

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
Issued: 2026-11-24
Verified: 2026-11-26 be51efb0 (autolens_workspace_test)
Lane: any
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

## Answers from the human
- Q29 (2026-11-26, shift 2026-11-24-am question on autolens_workspace_test#371): retire https://github.com/PyAutoLabs/autolens_workspace_test/issues/371#issuecomment-7127116263
