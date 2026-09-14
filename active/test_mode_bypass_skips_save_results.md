# Test-mode bypass never calls `analysis.save_results`, breaking scripts that read their own result files

Type: bug
Target: autofit
Repos:
- PyAutoFit
Themes:
- test-mode
- workspace-smoke
Difficulty: easy
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `PYAUTO_TEST_MODE=2 python autofit_workspace/scripts/overview/overview_2_scientific_workflow.py` completes and prints the science_summary it wrote; a PyAutoFit unit test asserts the bypass calls save_results / save_results_combined
Review-minutes: 10
Filed: 2026-09-14
Issued: 2026-09-14
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1624

User request (verbatim, 2026-09-14):

"""
can you fix the PyAutoHeart being red
"""
(follow-up after the RED cleared to YELLOW: "yes do next step" — file the PyAutoFit
bypass fix through start_dev, which also clears both autofit smoke failures.)

## Context

Heart workspace-smoke cloud run 34824535982 (PyAutoHeart, `workspace-smoke.yml`,
`PYAUTO_TEST_MODE=2`) fails on `autofit_workspace` `overview/overview_2_scientific_workflow`
(`.py` and `.ipynb`) with

    FileNotFoundError: .../files/science_summary.json
      overview_2_scientific_workflow.py:279  print(search.paths.load_json("science_summary"))

The script defines `Analysis.save_results` to `paths.save_json("science_summary", …)`
and reads it back after the fit (autofit_workspace 424555d, 2026-09-09).

`AbstractSearch._fit_bypass_test_mode` (`autofit/non_linear/search/abstract_search.py`,
modes 2 and 3) writes samples + samples_summary, builds the result and calls
`paths.completed()`, but never calls `analysis.save_results` / `save_results_combined`,
unlike the normal path (`start_resume_fit`, ~line 829). Its docstring promises
"all expected output files so that downstream code sees a complete result folder".
Any workspace script that round-trips a custom `save_results` file therefore fails
under smoke. The gap predates the recent PyAutoFit commits (introduced with modes 2/3
in d41aa53e8).

Downstream `save_results` implementations (autogalaxy `galaxies.json`, autolens
`tracer.json`) are cheap JSON dumps already guarded against instance-build failures
(PyAutoFit #1535), so calling them from the bypass is safe in both modes.
