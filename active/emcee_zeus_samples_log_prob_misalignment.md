# Emcee and Zeus pair thinned parameters with unthinned log-probabilities

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- mcmc
- samples
- correctness
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Issued: 2026-09-14
Filed: 2026-09-14

## The bug

`autofit/non_linear/search/mcmc/emcee/search.py`, `samples_via_internal_from`:

```python
samples_after_burn_in = search_internal.get_chain(discard=discard, thin=thin, flat=True)
parameter_lists = samples_after_burn_in.tolist()
total_samples = len(parameter_lists)
log_posterior_list = search_internal.get_log_prob(flat=True)[-total_samples - 1 : -1].tolist()
```

`parameter_lists` is the chain **after** burn-in discard and thinning.
`log_posterior_list` is a contiguous tail slice of the **raw, unthinned,
undiscarded** flat log-probability array — plus an unexplained one-element
offset (`[-total_samples - 1 : -1]` drops the last entry and shifts by one).

The two are not in correspondence. Sample `i`'s reported likelihood belongs to
some other sample.

`autofit/non_linear/search/mcmc/zeus/search.py` (~line 373) has the same defect
in a different form:

```python
log_posterior_list = search_internal.get_log_prob(flat=True).tolist()
```

against a `samples_after_burn_in` that may be thinned. The subsequent `zip()`
silently truncates to the shorter list, pairing thinned parameters with the
*first* N unthinned log-probs.

## Consequences

- `result.max_log_likelihood_instance` / `samples.max_log_likelihood()` return
  the argmax of a scrambled array — effectively a random post-burn-in draw, not
  the maximum likelihood sample.
- The "Maximum Log Likelihood" line of **every** Emcee and Zeus `result.info` is
  wrong.
- `log_likelihood_list` is wrong per-sample, so anything deriving from it
  (errors at sigma, PDF summaries computed from likelihoods, model comparison)
  inherits the error.

Nested sampling and the MLE searches are unaffected.

## Evidence (verified twice, 2026-09-14)

Independent reproduction in-session on the HowToFit tutorial 3 dataset,
`af.Emcee(nwalkers=20, nsteps=500)`:

- reported `max_log_likelihood_sample.log_likelihood` = **188.9628**
- actual `analysis.log_likelihood_function(instance=max_log_likelihood())` =
  **188.8337**

A second run during calibration showed a much larger gap: reported **188.34**
for parameters whose true likelihood is **176.52**. The size of the error scales
with how much the post-burn-in samples differ, so a poorly converged chain is
punished hardest — exactly the case where a trustworthy MLE matters most.

## Fix

Ask emcee for the log-probabilities under the *same* discard/thin as the chain:

```python
log_posterior_list = search_internal.get_log_prob(
    discard=discard, thin=thin, flat=True
).tolist()
```

`discard` / `thin` currently exist only in the non-test-mode branch, so both
branches must bind them (test mode uses `discard=5, thin=5`). Zeus needs the
equivalent treatment for whichever branch produced its `samples_after_burn_in`.

## Regression test

Assert the invariant directly rather than pinning a number: for a completed
Emcee fit, `samples.max_log_likelihood_sample.log_likelihood` must equal the
`Analysis` log likelihood recomputed from `samples.max_log_likelihood()`, to
floating-point tolerance. Assert `len(parameter_lists) == len(log_posterior_list)`
too — the current code can only be caught by the values, not the lengths.

## Blast radius

This changes the reported maximum-likelihood numbers of every existing Emcee and
Zeus fit. They were wrong before, so this is a correction, but it will move
numbers in any test or doc that pinned them — check for pinned Emcee likelihoods
across the libraries and workspaces.
