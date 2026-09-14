Retired by proof, not by separate development.

This prompt recorded that HowToFit tutorial 3's uninitialised Emcee fit did not
reliably succeed despite the prose asserting it did — measured at 2 failures in 6
runs, pre-existing on `main` and not caused by HowToFit#58 or #59. It was filed
rather than fixed because the remedy meant raising the search budget, which trades
tutorial and CI runtime and looked like a human pacing decision.

That reasoning was wrong on the facts. CI does not run the sampler at all
(`config/build/profile_smoke.yaml` sets `PYAUTO_TEST_MODE: "2"`, skip sampler, with
no tutorial 3 override), so the only cost was a reader's wall-clock, and the
baseline fit took 3.9s — abundant headroom. Measured properly the failure rate was
worse than filed: 11/20 successes, not 4/6.

Fixed in HowToFit#60 as part of the `howtofit-tutorial-followups` task: both Emcee
searches moved to `nwalkers=20, nsteps=500`, which succeeded 80/80 at a median
9.8s, with CI runtime unchanged at ~1.5s. Walkers, not steps, were the binding
constraint.

No separate PR, no separate issue — the work shipped inside HowToFit#60. Retired
here so the dashboard stops offering it as pickable backlog.
