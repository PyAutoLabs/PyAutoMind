## gradient-safe-logdet
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/391
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/392 (MERGED)
- verdict: SHIPPED — the one endorsed source change from the reg-logdet adversarial review
- summary: |
    The only source change endorsed by the independent adversarial review of the
    reg-logdet non-finite investigation (autolens_workspace_developer#104).

    Added Settings.log_det_method: default "cholesky" (byte-identical to prior
    behaviour), opt-in "slogdet" (logabsdet of xp.linalg.slogdet(M)) = identical
    where M is positive-definite, finite+differentiable where the Cholesky would
    NaN, general (serves the adaptive schemes too). Applies to BOTH evidence
    log-det terms (log_det_curvature_reg_matrix_term and
    log_det_regularization_matrix_term) via a shared _log_det_symmetric_from
    helper whose default branch is the identical Cholesky expression. Config key
    log_det_method:cholesky in packaged general.yaml, Optional->conf fallback
    mirroring use_positive_only_solver.

    WHY NON-DEFAULT: the review proved (C4) the current evidence's
    coefficient-dependence is correct to machine precision (d log det/d log lam =
    1798), so changing the default would be a regression (relative lift) or break
    archived-evidence comparability (pseudo-determinant). This adds an opt-in
    alternative only; the default evidence path is unchanged.

    VALIDATION: full test_autoarray suite 926 passed — every existing log_evidence
    test (imaging/interferometer/fit_dataset) unchanged = the byte-identical-default
    gate. New tests: default==cholesky==numpy log det; slogdet==cholesky on PD;
    slogdet finite where cholesky fails on non-PD.

    TWO THINGS VERIFIED NOT ASSUMED:
      1. NO workspace config mirroring needed. A single-path Config test KeyErrored
         on a workspace missing the key, but production LAYERS packaged defaults
         under the workspace config (Config(*paths), first overrides later), so a
         packaged-only key resolves — confirmed against the existing packaged-only
         nnls_target_kappa (in ZERO workspaces). The prompt's "mirror into
         workspaces" instruction was wrong.
      2. slogdet is MORE accurate than cholesky on ill-conditioned PD matrices
         (matches numpy log det exactly; cholesky ~2.5e-7 off on a 25-pixel Constant
         reg matrix). So even in the PD regime it is not bit-identical to the
         current evidence — another reason it is non-default / for comparison.

    THE ADVERSARIAL REVIEW's OTHER FINDINGS (filed, not acted on here):
      - draft/bug/autoarray/constant_zeroth_broken_dead_code.md — ConstantZeroth is
        dead code (eye(P) shape bug + missing neighbors_sizes arg).
      - draft/bug/autoarray/PROBE_adapt_double_square_coefficient.md — C9: Adapt's
        4th-power coefficient (double square at adapt.py:47 then :84).
      - The decisive open empirical question: where do production ADAPTIVE fits
        converge? If c~1-10 the whole conditioning issue lives in exploration only.
      - Verdict of record on draft/bug/autoarray/PROBE_reg_logdet_justification.md.

    FOLLOW-UP AT SHIP (option i, new coverage): JAX gradient-finiteness assertion
    -> autogalaxy_workspace_test (mirror
    autofit_workspace_test/scripts/jax_assertions/fitness_nan_gradient_contract.py);
    autolens_workspace_test was claimed by dpie-lenstool-default. NOT YET DONE.

    Heart RED acked contemporaneously (5 pre-existing unrelated reasons).

## Original prompt

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
