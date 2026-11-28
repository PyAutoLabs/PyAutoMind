The autogalaxy_workspace_test jax_assertions sparse-operator scripts give their mapping leg `lazy_sparse_operator="off"`, so it stays on the dense mapping route under R6's lazy sparse default. The sparse leg and all assertions are unchanged. Corrective PR under Heart RED ("✗ release validation FAILED (stage integrate)"), authorized live 2026-11-26.

- PR: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/141 (merged 91b4f4eb9)
- Validation: on library main the unmodified scripts fail with the CI assertions; the branch passes all assertions incl. parity; PR smoke CI green on 3.12 and 3.13.

## Original prompt

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
