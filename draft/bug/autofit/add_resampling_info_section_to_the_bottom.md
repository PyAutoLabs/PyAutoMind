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

Add Resampling Info section to the bottom of search.summary

Original request (verbatim): these should be at bottom of search.summary, with a space after the 'Visualization time' line, and a subheader saying 'Resampling Info': Resurrections = 0
Value-NaN Lane-Steps = 5540
Gradient-NaN Lane-Steps = 36
Constrained Lane-Steps = 0
Value-NaN Lane-Step Rate = 0.6520715630885122
Gradient-NaN Lane-Step Rate = 0.00423728813559322

Witness: a completed search's search.summary file ends with a blank line after the 'Visualization time' line, then a 'Resampling Info' subheader followed by the six resampling lines (Resurrections, Value-NaN Lane-Steps, Gradient-NaN Lane-Steps, Constrained Lane-Steps, Value-NaN Lane-Step Rate, Gradient-NaN Lane-Step Rate).

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from user-intake -->
