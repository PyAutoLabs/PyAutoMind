A correctness bug in PyAutoFit's MCMC samples construction, found while
calibrating HowToFit tutorial 3's MCMC budget (HowToFit#59 / #60).

**The bug.** `Emcee.samples_via_internal_from` took its parameters from the chain
after burn-in discard and thinning, but its log posteriors from a contiguous tail
slice of the raw, unthinned, undiscarded array:

    samples_after_burn_in = search_internal.get_chain(discard=discard, thin=thin, flat=True)
    total_samples = len(parameter_lists)
    log_posterior_list = search_internal.get_log_prob(flat=True)[-total_samples - 1 : -1].tolist()

The two are not in correspondence, so sample `i`'s reported likelihood belonged to
a different sample. The slice also carried an unexplained one-element offset.
`Zeus` had the same defect in a different form — `get_log_prob(flat=True)` against
a possibly-thinned chain, with the following `zip()` silently truncating to the
shorter list, hiding the length mismatch entirely.

**Impact.** `result.max_log_likelihood_instance` / `samples.max_log_likelihood()`
returned the argmax of a scrambled array — effectively a random post-burn-in draw
rather than the maximum likelihood sample — and the "Maximum Log Likelihood" line
of every Emcee and Zeus `result.info` was wrong. `log_likelihood_list` was wrong
per-sample, so anything derived from it inherited the error. Nested sampling and
the MLE searches were never affected. The error scales with how much the
post-burn-in samples differ, so it is near-invisible on a well-converged chain and
large on a bad one — it hides exactly where a convergence study would look.

**The fix.** Both searches request log posteriors under the same `discard` and
`thin` as the chain. `discard`/`thin` are bound in both branches of the test-mode
conditional (test mode previously inlined `discard=5, thin=5` into its `get_chain`
call), and Zeus's empty-chain fallback resets them to `0`/`1` to match the
`get_chain(flat=True)` it falls back to. Both raise `exc.SamplesException` when the
lengths disagree, so a future mismatch fails loudly — the old Zeus `zip()` was
precisely the silent-guard pattern the repo conventions forbid. API semantics were
introspected rather than assumed: emcee 3.1.6's `get_chain` and `get_log_prob` both
delegate to the same `get_value(name, flat, thin, discard)`, and zeus 2.5.4's carry
identical explicit signatures. No `discard`/`thin` values, auto-correlation logic,
nested sampling or MLE behaviour changed.

**Verification, done by the judgment tier and not taken from the implementing
agent's report.** The diff was read; the original reproduction was re-run against
the patched library over three trials, giving a worst-case `|reported - actual|`
of exactly 0.000e+00 against 0.129 before (and 11.82 on a poorly converged chain);
and the regression tests were re-run by hand against reverted source, where they
fail. A regression test that cannot fail against the bug is worthless, so that
check mattered more than the suite count.

Regression tests assert the invariant — the reported maximum likelihood must equal
the `Analysis` likelihood recomputed from the reported instance — rather than
pinning a number. Full suite 2852 passed / 2 skipped; CI green on all 4 checks.

**Blast radius turned out to be nil.** The fix moves the reported max-likelihood
of every existing Emcee and Zeus fit, but a sweep across PyAutoFit and
`autofit_workspace` for pinned Emcee/Zeus likelihood values found none, so nothing
else moved.

Follow-ups deliberately not bundled, since both change values or behaviour rather
than correcting a misalignment: `thin = int(max(autocorr)/2.0)` is 0 whenever the
largest auto-correlation time is under 2.0, raising `ValueError: slice step cannot
be zero`; and `check_size=100` raises `IndexError` from `emcee.autocorr` on chains
shorter than 100, always true under `PYAUTO_TEST_MODE=1` — Zeus guards it, Emcee
does not. Filed as `draft/bug/autofit/mcmc_thin_zero_and_check_size_short_chain.md`,
which overlaps an independently-filed 2026-09-10 prompt
(`emcee_crashes_in_autocorrelation_when_the_chain.md`) on the `check_size` half.

Shipped as PyAutoFit#1629.

## Original prompt

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
