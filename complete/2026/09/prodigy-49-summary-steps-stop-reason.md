- shipped: 2026-09-01 — PyAutoFit main `a601c3b3`, merged via
  https://github.com/PyAutoLabs/PyAutoFit/pull/1555 (closes PyAutoFit#1553).
- classification: bug (PyAutoFit) — batch 2026-08-31-pm member autofit-prodigy-49.
- summary: ROOT CAUSE REFRAMED — the reported bug does not exist: a MultiStart search
  cannot stop at a quick-update boundary (the cadence was inert for the family), and the
  "49" was `Total Samples = 49` (1 best + 48 per-start final points, fixed at
  construction) misread as a step count because the summary never reported the run's real
  length. Fix: the summary labels the sample count with its composition (only where the
  arithmetic holds — reload paths stay plain) and reports `Total Steps` and `Stop Reason`;
  a new e2e regression runs a cadence mid-budget to completion and carried a
  `quick_update_count == 0` inertness tripwire, flipped to `> 0` by the sibling wiring
  merge (#1556). Adversary found two real issues (vacuously-green e2e; composition label
  false on reload paths), both fixed pre-merge. Merged second of the shift's PyAutoFit
  trio after resolving a text_util.py conflict with #1554 on the branch.
- lifecycle: dispatched 18:53Z as an unattended batch member; accepted in the 2026-09-01
  15:13 batch review; recorded 2026-09-01.

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
