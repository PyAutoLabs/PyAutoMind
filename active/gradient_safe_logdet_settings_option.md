# Gradient-safe log-det as a non-default Settings option (for comparison)

Type: feature
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

Supersedes the earlier `draft/bug/autoarray/reg_matrix_logdet_nonfinite_fix.md`
(which proposed changing the DEFAULT log-det and is now WITHDRAWN — see the
verdict below).

## Decision (human verdict, 2026-07-17)

An independent adversarial review
(`draft/bug/autoarray/PROBE_reg_logdet_justification.md`) confirmed the analysis
and set the scope. Its load-bearing findings:

- **C4 holds to machine precision.** `d log det(H) / d log lam` measured 1798.00,
  1797.9999, 1797.9894 at lam = 1/10/100/1000 vs the theoretical `2(S-1) = 1798`.
  The `1e-8` lift contributes only a **constant** offset, so the current
  evidence's lam-dependence — the thing that drives inference of the
  regularization coefficient — is **already correct**. The existing code is
  scientifically sound and merely numerically fragile at extreme coefficients.
- Therefore the **relative lift is a regression** (changes the lam-dependence by
  a power) and the **pseudo-determinant breaks archived comparability** (shifts
  every stored/published absolute evidence by +18.4). Both are OFF the table.
- **Doing nothing is defensible**: the Cholesky failure at high coefficient
  truncates ~17% of the Adapt prior, but that region is over-smoothed /
  low-likelihood, so the evidence bias is ~0.2 nats and largely cancels in
  same-scheme model comparison.
- The decisive open empirical fact (probe section 4): **where do production
  adaptive fits actually converge?** If real posteriors sit at c ~ 1-10, the
  whole issue lives in the exploration regime.

**The only endorsed change: an OPT-IN, NON-DEFAULT gradient-safe log-det, kept
for comparison against the Cholesky default.** The default evidence path does not
change; no published value moves; the new path exists so gradient-based searches
(which the Cholesky-NaN currently blocks) have a finite alternative we can
measure against the truth.

## Task

Add a `log_det_method` option to `autoarray/settings.py` (`Settings`), following
the EXACT existing pattern (`Optional[...] = None` field →
`conf.instance["general"]["inversion"][...]` fallback, as `use_positive_only_solver`
does). Default config value = `"cholesky"` (current behaviour, byte-identical).

- `Settings.log_det_method` property: default `"cholesky"`; opt-in `"slogdet"`.
- In `AbstractInversion.log_det_regularization_matrix_term`
  (`abstract.py:734-764`) and, for coherence, `log_det_curvature_reg_matrix_term`
  (`abstract.py:706-731`), branch on the setting:
  - `"cholesky"` → the current `2*sum(log(diag(cholesky(H))))` — unchanged.
  - `"slogdet"` → `logabsdet` from `xp.linalg.slogdet(H)`. This is **identical to
    the Cholesky value wherever H is positive-definite** (sign = +1), and returns
    a finite, differentiable value where the Cholesky NaNs — so it never blocks a
    gradient search. It is general (works for Constant AND the adaptive schemes,
    unlike an analytic precomputed-eigenvalue route, which cannot serve Adapt's
    per-pixel weights).
- Mirror the config default into the packaged
  `autoarray/config/general.yaml` inversion section AND the workspace configs
  (workspace configs override packaged defaults — a new key must be added in both
  or downstream fits break; see the CLAUDE.md note about mirroring new keys).

## Validation (the whole point is that DEFAULT moves nothing)

- **Byte-identical default:** a fit with `log_det_method="cholesky"` (and one with
  the setting absent) must produce the SAME `figure_of_merit` as current main, to
  the last bit, on the MGE and pixelization fiducials. This is the release-safety
  gate.
- **Equivalence where PD:** on a well-conditioned fixture, `slogdet` and
  `cholesky` log-dets must agree to ~1e-10.
- **Finite where Cholesky fails:** at a known-fragile point (the #104 seed-0
  reject, draw 12/35 — reproduce with the 30s LOCAL spectrum script, NOT the A100;
  the 10.9 GiB figure was value_and_grad, the forward matrix is cheap), `slogdet`
  returns finite; `cholesky` NaNs. Assert both.
- Unit tests numpy-only per repo policy; the JAX gradient-finiteness assertion
  goes in a workspace_test jax_assertions script (mirror
  `autofit_workspace_test/scripts/jax_assertions/fitness_nan_gradient_contract.py`).

## Explicitly out of scope / deferred

- **Do not change the default.** Ever, in this task.
- **Analytic precomputed-eigenvalue log-det** (exact, rectangular-mesh-only): a
  possible SECOND method the same toggle could select later, if slogdet's
  fragile-regime divergence proves problematic in comparison runs. Not now —
  it cannot serve Adapt (per-pixel weights ⇒ eigenvalues not precomputable).
- The two independent bugs this investigation surfaced, filed separately:
  `draft/bug/autoarray/constant_zeroth_broken_dead_code.md` and
  `draft/bug/autoarray/PROBE_adapt_double_square_coefficient.md`.
- The empirical "where do production fits converge" question — worth a cheap
  aggregator check, and it gates whether ANY of this matters; but it is a
  separate analysis, not a blocker for shipping an opt-in, default-preserving
  Settings option.
