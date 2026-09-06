# jax_delaunay returns more than the five values imaging/jax_likelihood/delaunay.py unpacks

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Filed: 2026-09-06

Pre-existing on `autolens_workspace_test` `main` (reproduced on a detached
`origin/main` worktree during phase 6 of the ci-timing-fast-tests epic, so it
is not that phase's doing):

```
ValueError: too many values to unpack (expected 5)
  File ".../scripts/imaging/jax_likelihood/delaunay.py", line 384, in interpolated_sum
    _, _, mappings, split_points, split_mappings = jax_delaunay(
```

`jax_delaunay`'s return signature grew and this consumer was not updated. The
script is already disabled on the PR gate for a different reason (the jax-0.7
`pytype_aval_mappings` removal note in `smoke_tests.txt`), so it fails silently
on the weekly channel. Everything before line 384 passes on the phase-6 branch
(vmap literal, poisoned-lane isolation, `jit(fit_from)` round-trip, invalid-mesh
NaN check).

Ask: (1) find the commit that changed `jax_delaunay`'s return tuple and every
in-repo caller of it; (2) update `interpolated_sum` in the workspace script (and
any sibling) to the current signature; (3) re-check whether the gate disable
reason still holds under the installed jax and, if not, re-enable the entry.
