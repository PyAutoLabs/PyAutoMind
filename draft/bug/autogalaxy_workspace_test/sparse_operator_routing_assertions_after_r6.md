# autogalaxy_workspace_test sparse-operator routing assertions still expect the pre-R6 mapping route

Type: bug
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: likelihood-lifecycle
Filed: 2026-11-26

## Finding

Release-integrate rehearsal PyAutoHeart run 45805219063, with the R6 library mains (PyAutoArray#715 e261e6d6 `lazy_sparse_operator` defaults to auto):
- `scripts/misc/jax_assertions/fit_imaging_sparse_operator.py`: `AssertionError: expected the un-operated dataset to route to InversionImagingMapping, got InversionImagingSparseNumba`
- `scripts/misc/jax_assertions/fit_interferometer_sparse_operator.py`: `AssertionError: linear light + one mapper: expected the un-operated dataset to route to InversionInterferometerMapping, got InversionInterferometerSparse...`

R6 deliberately routes an un-operated dataset to the sparse inversion. The scripts assert the old behaviour. The R6b workspace sweep (`likelihood-lifecycle-r6b-use-jax-sweep`) does not include autogalaxy_workspace_test.

## Ask

First confirm that the new route is the intended R6 behaviour, not a library regression. Then update the assertions to the R6 route, or opt the "un-operated" case out explicitly if the script is meant to pin the mapping route. Check whether autolens_workspace_test has sibling assertions.

Witness: both scripts pass on the integrate profile.
