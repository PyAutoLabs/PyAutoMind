## resampling-info-summary-section
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1551 (closed, completed)
- completed: 2026-09-01
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1554 (MERGED 2026-09-01T19:34:55Z, 7c1bf4ce)
- batch: 2026-08-31-pm — member `autofit-resampling-info`, tier `glance`, 3 review-minutes; `--auto`, effective level supervised (= min(header safe, bug work-type cap)); shipped via **decide-and-flag** — one flagged decision, PR-open instead of park at ship sign-off, recorded in the PR body. `batches/reviews/2026-08-31-pm.md` records `decision: UNREVIEWED`
- shipped: `search.summary` ends with a **Resampling Info** section, so a run's
  resampling behaviour is readable from the summary file rather than reconstructed from
  the logs.
- verified: full suite PASS 2328 with 44 skipped; downstream n/a (no removed, renamed or
  re-signatured symbols). `autofit_workspace` smoke subset 8/8 PASS in-container — the
  other five workspaces were unrunnable there, no lens-stack checkouts; the mcmc script
  passed once the pinned optional samplers were installed. 4/4 CI checks green. Review
  CLEAN with one claim disposition basis-cited. Adversary leg (independent model) CLEAN:
  the witness was basis-cited by an exact-tail end-to-end run and the byte-identical
  claim by differential old-vs-new module runs.
- traps: merged **first** of the PyAutoFit trio in this slot; the other two rebase onto
  it. Heart read STALE 35 at ship (five library statuses unknown, no `report.json` in the
  web container) — acknowledged at batch dispatch, not a measured red.
- notes: **Ledger reconciliation 2026-09-03** — merged 2026-09-01, `active.md` row never
  retired. Written by `mind-post-cortex` phase 1 (PyAutoMind#389). This is one of the two
  members whose decide-and-flag branch is the evidence in
  `draft/feature/pyautobrain/batch_no_park_at_ship.md`.

## Original prompt

# Add Resampling Info section to the bottom of search.summary

Type: bug
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: a completed search's search.summary file ends with a blank line after the 'Visualization time' line, then a 'Resampling Info' subheader followed by the six resampling lines (Resurrections, Value-NaN Lane-Steps, Gradient-NaN Lane-Steps, Constrained Lane-Steps, Value-NaN Lane-Step Rate, Gradient-NaN Lane-Step Rate).
Review-minutes: 3
Unattended: ready
Issued: 2026-08-31

Add Resampling Info section to the bottom of search.summary

Original request (verbatim): these should be at bottom of search.summary, with a space after the 'Visualization time' line, and a subheader saying 'Resampling Info': Resurrections = 0
Value-NaN Lane-Steps = 5540
Gradient-NaN Lane-Steps = 36
Constrained Lane-Steps = 0
Value-NaN Lane-Step Rate = 0.6520715630885122
Gradient-NaN Lane-Step Rate = 0.00423728813559322

Witness: a completed search's search.summary file ends with a blank line after the 'Visualization time' line, then a 'Resampling Info' subheader followed by the six resampling lines (Resurrections, Value-NaN Lane-Steps, Gradient-NaN Lane-Steps, Constrained Lane-Steps, Value-NaN Lane-Step Rate, Gradient-NaN Lane-Step Rate).

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from user-intake -->
