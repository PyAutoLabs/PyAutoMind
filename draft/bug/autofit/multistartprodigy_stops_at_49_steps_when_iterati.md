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

MultiStartProdigy stops at 49 steps when iterations_per_quick_update=50 in @PyAutoFit

Type: bug

Original report (verbatim): the imaging/start_here.py run I did which uses MultiStartProdigy stopped at 49 steps, which is probbably due to iterations_per_quick_update=50, meaning the result is rubbish. Is there an issue with this combination of quick updates and prodigy?

Investigate the interaction between the quick-update cycle and MultiStartProdigy: the search appears to terminate at the first quick-update boundary (49 steps with iterations_per_quick_update=50) instead of resuming sampling afterwards, so the returned result is from a barely-started search.

Witness: an imaging/start_here.py run using MultiStartProdigy with iterations_per_quick_update=50 runs past the first quick update (total steps well above 50) instead of terminating at 49 steps, and the interaction is covered by a PyAutoFit unit test in which a quick update mid-search does not end the search.

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from user-intake -->
