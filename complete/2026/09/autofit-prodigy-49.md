## autofit-prodigy-49
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1553 (closed, completed)
- completed: 2026-09-01
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1555 (MERGED 2026-09-01T19:43:45Z, a601c3b3)
- batch: 2026-08-31-pm — member `autofit-prodigy-49`, tier `glance`, 3 review-minutes; `--auto`, effective level safe (header safe, bug @ small cap safe); `batches/reviews/2026-08-31-pm.md` records `decision: UNREVIEWED`
- shipped: **root cause reframed.** `MultiStartProdigy` cannot stop at a quick-update
  boundary at all — the multi-start step loop never reads
  `iterations_per_quick_update`, and the convergence gate (`min_steps=100`) plus the
  `n_steps` ceiling are the only stop paths (confirmed empirically: cadence=50,
  n_steps=120 runs 120/120). The reported "stops at 49 steps" was `search.summary`'s
  `Total Samples = 49` line (1 best + `n_starts=48` per-start finals) misread as a step
  count. Fix: report **Total Steps** and **Stop Reason** in the multi-start
  `search.summary` block, disambiguate the Total Samples line, and pin the
  non-termination with an end-to-end `MultiStartProdigy` regression test.
- verified: targeted suites 155 passed (`text_util` + `mle` + wiring); the full serial
  suite fails only on pre-existing env-pin breakage identical on `origin/main` (dynesty
  drift, missing optional deps). 4/4 CI checks green on head 2629933cc including nojax.
  Witness falsified-first: the cadence was shown provably inert before the fix was
  written. Adversary leg pass 1 returned 2 FINDINGS (a vacuously-green e2e test; a false
  composition label on reload paths), both fixed, pass 2 CLEAN.
- traps: a "stops at N steps" bug report against a multi-start search is far more likely
  to be a misread `Total Samples` line than a real stop condition — the summary block
  reported samples where the reader expected steps, and nothing in the output said which
  was which. Merge order mattered: this PR merged second of the PyAutoFit trio, after
  #1554 and before the multistart-iterations follow-up.
- notes: **Ledger reconciliation 2026-09-03** — merged 2026-09-01, `active.md` row never
  retired (the 2026-08-31-pm members merged one at a time via `/prm`, no batch
  close-out). Written by `mind-post-cortex` phase 1 (PyAutoMind#389).

## Original prompt

# MultiStartProdigy stops at 49 steps when iterations_per_quick_update=50 in @PyAutoFit

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: an imaging/start_here.py run using MultiStartProdigy with iterations_per_quick_update=50 runs past the first quick update (total steps well above 50) instead of terminating at 49 steps, and the interaction is covered by a PyAutoFit unit test in which a quick update mid-search does not end the search.
Review-minutes: 3
Unattended: ready
Issued: 2026-08-31

MultiStartProdigy stops at 49 steps when iterations_per_quick_update=50 in @PyAutoFit

Type: bug

Original report (verbatim): the imaging/start_here.py run I did which uses MultiStartProdigy stopped at 49 steps, which is probbably due to iterations_per_quick_update=50, meaning the result is rubbish. Is there an issue with this combination of quick updates and prodigy?

Investigate the interaction between the quick-update cycle and MultiStartProdigy: the search appears to terminate at the first quick-update boundary (49 steps with iterations_per_quick_update=50) instead of resuming sampling afterwards, so the returned result is from a barely-started search.

Witness: an imaging/start_here.py run using MultiStartProdigy with iterations_per_quick_update=50 runs past the first quick update (total steps well above 50) instead of terminating at 49 steps, and the interaction is covered by a PyAutoFit unit test in which a quick update mid-search does not end the search.

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from user-intake -->
