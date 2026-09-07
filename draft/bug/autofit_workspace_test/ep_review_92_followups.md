# Codex review of autofit_workspace_test#92: correct the "reproduces the collapse" prose and cross-check the log-sigma moments

Type: bug
Target: graphical_ep
Repos:
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: `python scripts/graphical/analytic_reference.py` asserts `log_sigma_mean` / `log_sigma_std` against `scipy.integrate.quad` (1e-6) for all four prior families and passes; `grep -rn "reproduces the .*collapse" scripts/graphical/` returns nothing; `analytic_ep_minimal.py` still passes and labels the theta = sigma Laplace run as stale
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-07

Follow-up to phase 1 of the graphical-ep epic (autofit_workspace_test#91, PR #92 merged
2026-09-02). A Codex review of the merged PR raised two P2 findings; both were re-verified on
`main` on 2026-09-07 before filing.

## Original review (verbatim)

> Reviewed phase 1 PR #92, merged September 2. Verdict: two P2 findings.
>
> 1. The claimed collapse reproduction is overstated. Lines 97–100 say minimal Laplace EP
>    reproduces scatter collapse. Fresh execution instead rejects all updates: 3,000 skips, no
>    convergence, and the internal scatter distribution remains at its initial prior. The
>    boundary-density argument is valid, but the empirical conclusion should describe failed
>    projection.
>
> 2. Reported log-scatter uncertainty is numerically inaccurate. Line 420 assigns finite
>    quadrature weight to a near-zero endpoint before taking its logarithm. For the default
>    Gaussian-prior case, reported standard deviation is 0.54114, versus 0.52147 from independent
>    adaptive integration—3.8% too high. Existing assertions check the sigma-space result and miss
>    this diagnostic error.
>
> Validation otherwise supports the benchmark: both original self-tests pass, all 15 seeded prior
> combinations converge, and independent calculations confirm the [closed form].

## Verdict on each finding

**Finding 1 — correct.** The theta = sigma Laplace run (seed 0, gaussian and truncated
hyper-priors) ends after 500 sweeps with `converged False`, `skipped 3000` (500 sweeps x 5
hierarchical sites + the hyper-prior site, whose cavity stays improper), `max |delta eta|` exactly
0. The returned sigma 10.4522 +/- 4.5080 is bit-identical to the starting hyper-prior site (closed
form 6.5886 +/- 2.8853); mu and every x_i are their initial messages. In the phase-2 taxonomy of
`analytic_gaussian_collapse.py` that is **STALE**, not PATHOLOGICAL (which needs E[sigma] < 2 and
std/mean < 0.5). The mechanism sentence (tilted density unbounded as sigma -> 0, mode on the support
edge) is right; the label "reproduces the scale collapse deterministically" is wrong.

**Finding 2 — does not reproduce.** The default gaussian-prior case prints
`log sigma = 1.7948 +/- 0.4268`; `scipy.integrate.quad`, a u = log sigma substitution and 10x /
100x denser grids agree to 8 significant figures for all four shipped prior families. The
reviewer's 0.54114 / 0.52147 appear nowhere. The `np.where(pdf > 0, log_grid, 0)` line is
load-bearing (avoids `0 * log 0 = NaN`) and the gaussian prior's grid has `pdf[0] = 0`, so no finite
weight is given to `log(0)`. The class of defect exists only when real posterior mass sits at
sigma = 0 (constructed `sigma_true = 0.05`: 1.5 % std error; half-normal prior: 0.4 %) — no shipped
case, and below every consumer tolerance (a >= 0.15). What stands is the procedural point: the
self-test never cross-checks the log-sigma moments, and the docstring's "exact for the leading
term" is only true of the first moment.

## Scope

1. `scripts/graphical/analytic_ep_minimal.py` docstring (lines 97-100): keep the mechanism,
   replace "reproduces the scale collapse deterministically" with the stale-factor outcome
   (numbers above). Add the runtime counterpart: the Laplace summary line prints
   `(stale: no site updated; scatter returned at its prior)` when `skipped == sweeps * (n + 1)`.
2. `scripts/graphical/analytic_gaussian.py` lines 74-75: "reproduces the collapse
   deterministically" -> "reproduces the stale-factor state deterministically (every site update
   rejected, sigma returned at its prior)".
3. `scripts/graphical/analytic_reference.py`: reword the docstring's "exact for the leading term"
   sentence (first moment only; second-moment error ~1e-10 for every shipped prior, at most ~1.5 %
   of the std when posterior mass sits at sigma = 0); add `quad_log_sigma_moments(...)` beside
   `quad_normaliser` and assert `log_sigma_mean` / `log_sigma_std` against it (1e-6) for the four
   prior families in self-test block (ii). Do not change the moment computation itself.
4. `PyAutoMind/complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md` evidence line 22:
   same substitution as item 2 (Mind-side edit, committed with the close-out).
5. Comment on issue #91 with the two verdicts and the PR link.

No banked number changes. Not in scope: switching the log-sigma moments to a u = log sigma
quadrature (validated in scratch, but no shipped case moves).
