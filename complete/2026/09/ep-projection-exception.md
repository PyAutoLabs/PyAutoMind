## ep-projection-exception

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1653
- completed: 2026-09-30
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1655
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1655
- merged: 07f6e0b (PyAutoFit main, 2026-09-30, via /prm)

### What shipped
- `autofit.exc.ProjectionException(ValueError)` replaces the bare `assert` in `AbstractMessage.project`. It names the non-finite input (samples / nan or +inf log weights / all -inf log weights / weighted-moment overflow) and survives `python -O`.
- `Prior.project` adds the prior id and `Result.projected_model` adds the parameter path (`from e`).
- EP `factor_step` lists it in its recovery tuple. One bad projection keeps the previous message with `StatusFlag.EXCEPTION` instead of killing the graph fit.
- Tests: red witness 10 failures on unmodified source; new tests 29 passed; full suite 2946 passed, 2 skipped. Workspace smoke passes for analytic_ep_minimal and analytic_gaussian_collapse.
- Behaviour change: non-EP callers of `Result.projected_model` now get a `ValueError` subclass instead of `AssertionError`.
- Spawned from ep-checkin-cleanup (PyAutoCortex#50). Shipped in parallel with ep-moment-projection (PyAutoFit#1654 / PR#1656): the two file sets were disjoint, and this one went first.

## Original prompt

# EP message projection asserts on non-finite sufficient statistics and kills the whole EP run (ic50_workspace N=50 rung, RAL 342411)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: supervised
Priority: medium
Status: issued
Consequence: glance
Witness: a unit test in `test_autofit/graphical/` in which a factor's search returns samples containing one non-finite value (e.g. `NormalMessage.project(np.array([1.0, 2.0, np.nan]), np.zeros(3))`, which today raises a bare `AssertionError` from `autofit/messages/abstract.py:316`) and, driven through `factor_step`, the EP run records that factor step as `StatusFlag.EXCEPTION`, keeps the previous message and carries on, instead of dying. The error message names the prior id and says which input was non-finite (the samples, the log weights, or an overflow). Plus a direct `project` test: a nan sample is either dropped with a warning or rejected with a `ValueError`, and never trips an `assert`.
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-30
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1653

## Why

RAL job 342411 (the ic50_workspace EP scale ladder, sim rungs 5/10/25/50, DynestyStatic nlive 150,
max_steps 12, PyAutoFit mirror at 66f9f8d5d) passed rungs N=5/10/25. It then died at the N=50 rung
right after the 4th EP sweep's `global` factor search finished (2026-09-09 23:19:27 BST).
The traceback, from `hpc/batch_cpu/error/error.342411.err`:

```
ep_sim.py:123 run_ep_fit → util.py:712 factor_graph.optimise
autofit/graphical/declarative/abstract.py:208 optimise → opt.run
autofit/graphical/expectation_propagation/optimiser.py:586 run → self.factor_step
optimiser.py:356 factor_step → factor_step(...)
optimiser.py:135 factor_step → optimiser.optimise(factor_approx)
autofit/non_linear/search/abstract_search.py:401 optimise → result.projected_model.priors
autofit/non_linear/result.py:473 projected_model → prior.project(...)
autofit/mapper/prior/abstract.py:237 project → self.message.project(...)
autofit/messages/abstract.py:316 project → assert np.isfinite(suff_stats).all()
AssertionError
```

This bug has two parts:

1. **The projection uses `assert` for a data condition.** `AbstractMessage.project`
   (`autofit/messages/abstract.py:275-319`, unchanged on main 5cf687d84 since the mirror commit)
   calculates `w = exp(logw − max logw)`, `w /= w.mean()`, `suff_stats = mean(T(x)·w)`, then asserts
   the result is finite. Probing it on main shows the assertion fires for all of these inputs:
   a nan sample, an ±inf sample, a nan log weight, a +inf log weight, all log weights −inf (this
   case is guarded upstream in `Result.projected_model`, `result.py:492`), or `x²` overflowing.
   A single sample silently returns `sigma=0` instead. A negative-precision cavity also reaches it:
   `GaussianPrior.with_message(NormalMessage(0,1)/NormalMessage(0,0.5))` has `sigma=nan`, and every
   `value_for` on it returns nan. A bare `assert` gives no diagnostic (which prior, which input) and
   disappears under `python -O`.
2. **`factor_step` cannot recover from it.** The failure-recovery path
   (`autofit/graphical/expectation_propagation/optimiser.py:150-155` on main) catches
   `ValueError, ArithmeticError, RuntimeError, InitializerException`. That path exists so that one
   factor's bad sweep degrades to its previous message and the run continues, with
   `max_consecutive_failures` as the backstop. `AssertionError` is not in that list, so one
   non-finite projection of one factor ends a 20-minute, 51-factor EP run.

The failure is not deterministic. A local rerun at 66f9f8d5d on the same dataset (unseeded Dynesty)
converged (`Terminating optimisation`, `EPHistory(kl_tol=1.0)`) midway through sweep 3 and never
reached a 4th global projection. So the witness is the unit test above, not a rerun of the rung.
It is still unknown which of the non-finite conditions fired on RAL, because output to disk was
disabled and no samples were kept. The fix should report the condition so the next occurrence
identifies itself.

## Scope

autofit_workspace_test: no edits; graphical smoke scripts rerun at ship.

- Replace the `assert` with a `ValueError`, or a `SearchException` subclass that `factor_step`
  catches, naming the prior id and the offending condition. Or drop non-finite samples/weights with
  a warning when enough finite, positively weighted samples remain.
- Make sure `factor_step`'s `except` tuple covers it.
- Leave the moment-matching maths as it is.
