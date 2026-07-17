# Test-mode bypass never writes the .completed marker, so bypassed fits

Type: bug
Target: autofit
Repos:
- PyAutoFit
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Found during slam-resume-profiling (autolens_profiling#70, the test-mode epic's phase 3): in
@PyAutoFit `autofit/non_linear/search/abstract_search.py`, `_fit_bypass_test_mode` (the
`PYAUTO_TEST_MODE=2/3` path) writes samples, summary and results but returns without calling
`self.paths.completed()` — unlike `start_resume_fit`, which marks completion before returning.

Consequence: a bypass-"completed" search is never seen as complete (`paths.is_complete` false), so
re-running the same script re-bypasses every stage instead of taking `result_via_completed_fit`.
This defeats the resume-representative purpose of `PYAUTO_TEST_MODE_SAMPLES` (PyAutoFit#1378/#1381):
the docstring promises "downstream code sees a complete result folder", and `.completed` is part of
a complete result folder.

Fix is one line — call `self.paths.completed()` before the return in `_fit_bypass_test_mode`
(NullPaths/DatabasePaths already no-op safely, matching the surrounding save calls). Add a unit test
asserting `paths.is_complete` after a bypassed fit, and that a second `fit()` routes through
`result_via_completed_fit`.

The autolens_profiling harness (`pipeline_resume/slam_resume.py`, `_install_resume_timers`) carries a
runtime patch applying exactly this marker as a stopgap — remove that patch block when this ships.

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ce78c7e9-3f34-4983-bb53-8840527c1fb6/scratchpad/intake_bypass_completed.md -->
