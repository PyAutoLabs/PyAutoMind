## example-analysis-xp-sum
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1774
- completed: 2026-11-15
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1775
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1775
- merge: 5f580d533996026938ff4a454a2a5fc33970c1c9 (head 0dcdce8)
- tier: glance — human /prm on the approved plan

`af.ex.Analysis.log_likelihood_function` (`autofit/example/analysis.py`) now reduces the chi-squared map with `self._xp.sum(chi_squared_map)` instead of the Python builtin `sum`, so under JAX it no longer iterates the traced array element by element, and the example tutorials copy from shows the array-API pattern. The unused `xp=np` parameter was left in place (signature change out of scope).

Validation: Witness passed (`self._xp.sum(` present, no bare `sum(`). Full `test_autofit` locally on Python 3.13 / jax 0.12 with `.[optional]`: 4288 passed, 2 skipped, 1 xfailed (without the optional extras, 20–21 Zeus/Nautilus/lazy-read failures reproduce identically on unmodified main — environment, not this change). CI: unittest 3.12, 3.13, nojax, docs-build, generated-search-docs all green. Heart at ship: published board YELLOW (only blocker an aged PyAutoArray PR). No workspace impact (no API change). Conflict override: PyAutoFit shared with three-autos-public-framing and ep-projected-model-shared-prior, non-overlapping file, human-approved.

## Original prompt

# Example Analysis should reduce with xp.sum not builtin sum

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-11-15
Consequence: glance
Witness: autofit/example/analysis.py log_likelihood_function contains self._xp.sum( and no bare sum( call; the example test suite passes under both NumPy and JAX.
Review-minutes: 3
Unattended: ready
Lane: any

Example Analysis should reduce with xp.sum not builtin sum
Type: refactor
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Witness: autofit/example/analysis.py log_likelihood_function contains self._xp.sum( and no bare sum( call; the example test suite passes under both NumPy and JAX.

af.ex.Analysis.log_likelihood_function (autofit/example/analysis.py:147) reduces the chi-squared map with the Python builtin sum(chi_squared_map) instead of self._xp.sum. It works under JAX only by iterating the traced array element by element, and it is the wrong pattern for the example analysis that tutorials and workspace scripts copy from. Replace it with self._xp.sum(...). Found 2026-09-10.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
