# Cluster likelihood scripts: image-plane manual check disagrees with the library; point_0 truth χ² is 8.5e6

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Filed: 2026-10-21
Status: formalised
Consequence: judge

@autolens_workspace @autolens_workspace_test

## Finding

These were found during positions-source-jacobian-default (PyAutoLens#791, #593, #346). Both problems existed before that change.

1. **`autolens_workspace/scripts/cluster/likelihood_function.py`:** the image-plane manual walkthrough disagrees with the library. The manual χ² is 26.2, while the library's log-likelihood is −1.5e5. The source-plane walkthrough was fixed in #593 and now prints `Match: True`.
2. **`autolens_workspace_test/scripts/cluster/likelihood_sanity.py`:** for dataset point_0, the observed images trace up to ~7″ from the truth model in the source plane. So the truth χ² is 8.5e6 under jacobian, and was 8.1e7 under the old magnification weighting. The script's old "solver precision floor × magnification" explanation was wrong. #346 made it print χ² per dataset, but the soft assertions are unchanged.

## Scope

- Find out whether point_0's dataset or its truth model is inconsistent. Possible causes: a stale simulator output, a mismatch in multi-plane redshifts, or a naming/pairing error.
- Find out why the image-plane manual check diverges. Is it the pairing class, the noise, or the normalisation?
- Fix the root cause, then restore strict assertions.
