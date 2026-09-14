# HowToFit tutorial 3: the uninitialised Emcee fit does not reliably succeed

Type: bug
Target: HowToFit
Repos:
- HowToFit
Themes:
- howtofit
- mcmc
- flaky
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Filed: 2026-09-14
Parent: active/howtofit_tutorials_followups.md

## The claim the tutorial makes

`scripts/chapter_1_introduction/tutorial_3_non_linear_search.py`, after the first
(uninitialised) `af.Emcee` fit, asserts:

> The MCMC search succeeded, finding the same high-likelihood model that the MLE
> search with a good starting point identified.

It does not always. This is the observation-vs-truth failure mode: the prose states
an outcome as fact that the run does not reliably produce.

## Evidence (measured 2026-09-14, during HowToFit#59)

Six runs under the pre-#59 config priors: **2 clear failures out of 6**
(log likelihood -1306.6 and -108.2). Six runs under #59's restated priors:
**1 failure out of 6** (log likelihood 89.0). Statistically indistinguishable — so
this is **pre-existing on `main`, not a regression** from #58 or #59, and if anything
#59 marginally improved it.

One observed bad run: MLL 51.706 / 23.234 / 9.199 at logL 165.8, with the median PDF
at normalization 17.39 and sigma 6.37 against a truth of 25.0 and 10.0.

## Cause

The search is `af.Emcee(nwalkers=10, nsteps=200)` (check the current values). Ten
walkers over 200 steps is too few to converge reliably from a cold start on this
likelihood surface.

## Why it was not fixed in #59

The fix is to raise `nsteps` (and possibly `nwalkers`), which directly lengthens the
tutorial's runtime and its CI smoke time. That is a teaching-pace judgment call — how
long a reader should wait on this cell — not a mechanical correction, so it needs a
human decision rather than an autonomous one.

## Options to weigh

1. Raise `nsteps` until the fit succeeds ~10/10, and measure the added wall-clock in
   both the normal and the `PYAUTO_TEST_MODE` paths.
2. Keep the current budget and soften the prose to describe what actually happens —
   MCMC explores broadly but needs enough steps, which is itself a teachable point and
   sets up the tutorial's later discussion of trial-and-error step counts.
3. Give the first MCMC fit a deliberately under-resourced budget *as* the lesson, then
   show the converged version — closest to how the MLE section is already structured.

Option 2 or 3 likely beats 1 on tutorial pace; confirm with a measurement of what
`nsteps` actually buys.
