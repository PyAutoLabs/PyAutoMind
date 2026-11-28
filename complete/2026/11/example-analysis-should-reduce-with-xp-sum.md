- summary: superseded — PyAutoFit#1775 ("refactor: example Analysis reduces chi-squared with xp.sum", merged 2026-11-15) already made the change: `af.ex.Analysis.log_likelihood_function` reduces with `self._xp.sum`. Found when the shift 2026-11-26-pm2 worker picked it up (prompt premise refuted); nothing left to do.
- found by: shift worker 2026-11-26-pm2; retirement approved by the human at the 2026-11-27 review.

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
