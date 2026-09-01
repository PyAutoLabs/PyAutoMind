- shipped: 2026-09-01 — PyAutoFit main `7c1bf4ce`, merged via
  https://github.com/PyAutoLabs/PyAutoFit/pull/1554 (closes PyAutoFit#1551).
- classification: bug (PyAutoFit) — batch 2026-08-31-pm member autofit-resampling-info.
- summary: the gradient searches' resampling diagnostics moved from mid-file to a closing
  "Resampling Info" section of search.summary (blank line after the timing lines, subheader,
  six lines), extracted into `_resampling_summary_from` and appended by
  `search_summary_to_file`; emit-nothing guards unchanged so no-counter searches write
  byte-identical files. Witness observed on a real smoke run and asserted by a new
  end-of-file ordering test. Adversary CLEAN. First of the shift's three PyAutoFit merges;
  #1555's later merge conflicted with this diff in text_util.py and was resolved on that
  branch (keep composition/steps/stop-reason inline, resampling lines stay end-of-file).
- lifecycle: dispatched 18:53Z as an unattended batch member (decide-and-flag PR under the
  supervised bug-cap); accepted in the 2026-09-01 15:13 batch review; recorded 2026-09-01.

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
