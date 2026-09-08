- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1577 (closed completed 2026-09-07)
- completed: 2026-09-07
- library-pr: PyAutoFit https://github.com/PyAutoLabs/PyAutoFit/pull/1578 (head `154c87dd`, merge `6331b80031b1dedae3ce277a8c2b116b52ddd261`)
- workspace-pr: autofit_workspace_test https://github.com/PyAutoLabs/autofit_workspace_test/pull/99 (head `94b72b20`, merge `9321910765f77d4f7f092e455bce33127d154610`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1578
- pending-release: autofit_workspace_test@https://github.com/PyAutoLabs/autofit_workspace_test/pull/99
- classification: bug (PyAutoFit + autofit_workspace_test) — epic `graphical-ep`; finding D6 of the phase-1 analytic Gaussian benchmark (autofit_workspace_test#91), the last open phase-1 finding.
- ci: PyAutoFit `Tests [pull_request]` 3.12 / 3.13 / nojax + `Docs` green; autofit_workspace_test `Smoke Tests [pull_request]` changes / 3.12 / 3.13 green; both CLEAN; library merged first.
- heart-ack: YELLOW "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" + stale "release validation incomplete: no rehearsal for current source" (organism-scope); nothing in either diff is in the release chain.

- summary: `Model.instance_for_arguments` constructed a Prior from the `(lower, upper)` bounds pairs that `Samples.errors_at_sigma` / `values_at_sigma` (`as_instance=True`) hand it whenever the global model holds a `Model(af.GaussianPrior)` component (every `HierarchicalFactor` graph), so `NormalMessage`'s `broadcast_arrays` raised `TypeError`. Now an explicit typed branch: a Prior-class model whose constructor arguments contain a tuple returns `ModelInstance(constructor_arguments)` (`.mean == (lo, hi)`, `.sigma == (lo, hi)`); scalar vectors (`median_pdf`, `max_log_likelihood`) still build the real prior. Workspace: the `analytic_autofit.py` docstring no longer claims the instance path is unusable; the raw `as_instance=False` read stays because the weighted-moment comparison indexes columns positionally through `prior_tuples_ordered_by_id`.
- decision: the prompt's option 1 (return a pair of instances) was rejected — it would break the public tuple-attribute instance contract used by `ep_parity.py`, `simultaneous.py` and the workspace result tutorials.
- verdict: 3 new tests in `test_autofit/graphical/global/test_errors_at_sigma_instance.py`, the two tuple-valued ones fail without the fix; full suite 2472 passed 2 skipped (baseline 2469 + 3); graphical 278 / messages 95; referee `analytic_gaussian_collapse.py` RECOVER 5/5, STALE 0/5; smoke gate 14/14; every deterministic `analytic_gaussian.py` cell byte-identical before/after (PARITY FAIL 38/41 both sides, the same three autofit-EP cells = the Laplace-on-scatter caveat).
- finding: `analytic_gaussian.py`'s graphical column is an unseeded DynestyStatic run — its PARITY count and `[info]` lines drift run to run (37 vs 38 of 41 on an identical tree); filed `draft/bug/graphical_ep/analytic_gaussian_unseeded_graphical_column.md`.
- remaining: the phase-1 findings table is complete (D1–D6 shipped). `analytic_gaussian.py` / `analytic_gaussian_priors.py` stay parked NEEDS_FIX for the moment-matching cure (`draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md`, a human decision).
- worktree: `~/Code/PyAutoLabs-wt/samples-errors-at-sigma-instance` removed at close-out.

## Original prompt

# `Samples.errors_at_sigma(as_instance=True)` crashes on a model whose component class is a Prior

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: `errors_at_sigma(1.0, as_instance=True)` on a `FactorGraphModel` global model containing `Model(af.GaussianPrior)` returns without raising, and its values equal the `as_instance=False` tuples read back through `prior_tuples_ordered_by_id`
Review-minutes: 3
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-02
Issued: 2026-09-07

D6 of the analytic Gaussian benchmark findings (autofit_workspace_test#91).
Minor, but it forced `analytic_autofit.py` to read errors with
`as_instance=False` and re-map them by hand (see its module docstring, lines
52-54).

## Why

On the hierarchical graph's global model (a `HierarchicalFactor` contributes a
`Model(af.GaussianPrior)` component), `samples.errors_at_sigma(1.0)` — the
`as_instance=True` default — raises:

```
TypeError: broadcast_arrays requires ndarray or scalar arguments, got <class 'tuple'> at position 0
```

Plain dataclass models tolerate the tuples; a `Prior` used as a `Model` class does
not, because constructing it constructs a message.

## Root cause (deepest frame last)

- `errors_at_sigma` (`autofit/non_linear/samples/pdf.py:236-255`) returns a list
  of `(lower, upper)` tuples per parameter.
- The `to_instance` wrapper (`autofit/non_linear/samples/interface.py:56`) calls
  `model.instance_from_vector(vector)` on that tuple list.
- `prior_model.py:541` — `self.cls(**constructor_arguments)` for
  `Model(af.GaussianPrior)`.
- `autofit/mapper/prior/gaussian.py:52` — `NormalMessage(mean=(lo, hi), ...)`.
- `autofit/messages/abstract.py:63` — `broadcast_arrays` on the tuple -> TypeError.

## Minimal repro

```python
import autofit as af
class Level:
    def __init__(self, x): self.x = x
class A(af.Analysis):
    def log_likelihood_function(self, i): return -0.5 * (51.0 - i.x) ** 2
m = af.Model(Level); m.x = af.GaussianPrior(50, 20)
hf = af.HierarchicalFactor(af.GaussianPrior, mean=af.GaussianPrior(50, 10), sigma=af.GaussianPrior(10, 5))
hf.add_drawn_variable(m.x)
fg = af.FactorGraphModel(af.AnalysisFactor(m, A()), hf)
samples = ...  # the EP result's Samples over fg.global_prior_model, as analytic_autofit.py builds them
samples.errors_at_sigma(1.0, as_instance=False)   # fine: list of (lo, hi)
samples.errors_at_sigma(1.0)                       # TypeError from broadcast_arrays
```

## Fix sketch

Either build two instances — `instance_from_vector(lower)` and
`instance_from_vector(upper)` — and return them as a pair (mirrors how
`values_at_sigma` style callers already split the bounds), or fall back to the
tuple list when the model contains prior-valued components. The first is the
cleaner contract; pick it unless it breaks an existing caller.

## Acceptance

- Unit test: a `Samples` over a model with a `Model(af.GaussianPrior)` component;
  `errors_at_sigma(1.0, as_instance=True)` does not raise and its bounds equal
  the `as_instance=False` tuples.
- `autofit_workspace_test/scripts/graphical/analytic_autofit.py`: the
  `as_instance=False` workaround and the docstring note at lines 52-54 can be
  removed; `analytic_gaussian.py`'s `median_pdf +/- errors_at_sigma(1.0)`
  information line is produced through the instance path with identical numbers
  on every row (this line is informational, not a PASS/FAIL cell).

## Links

- autofit_workspace_test#91 — https://github.com/PyAutoLabs/autofit_workspace_test/issues/91
  - evidence comments: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5512686880 and https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5513518379
- PyAutoFit#1405 (umbrella for the EP findings; this one is adjacent, not a cause) — https://github.com/PyAutoLabs/PyAutoFit/issues/1405
- Campaign ledger: `draft/research/graphical_ep/ep_campaign.md` (phase 1)
- Siblings: `complete/2026/09/ep-prior-id-zero.md` (D1 shipped 2026-09-02, PyAutoFit#1558),
  `complete/2026/09/ep-laplace-hessian.md` (D2/D3 shipped 2026-09-02, PyAutoFit#1562),
  `complete/2026/09/ep-message-support.md` (D4/D5 shipped 2026-09-02, PyAutoFit#1560)
- Scripts: `autofit_workspace_test/scripts/graphical/analytic_{reference,ep_minimal,autofit,gaussian,gaussian_priors,gaussian_collapse}.py`
  on branch `feature/analytic-gaussian-benchmark`
