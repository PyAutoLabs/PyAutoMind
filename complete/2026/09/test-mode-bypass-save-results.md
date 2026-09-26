- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1624 (closed completed 2026-09-14)
- completed: 2026-09-14
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1626 (merged `559699fb1531ffe2205ae3b824bd29aadb39c145`)
- session: claude CLI, task worktree `~/Code/PyAutoLabs-wt/test-mode-bypass-save-results`, branch `feature/test-mode-bypass-save-results`; intake → start_dev → start_library → ship_library → prm in one session.
- summary: |
    `AbstractSearch._fit_bypass_test_mode` — the sampler bypass behind
    `PYAUTO_TEST_MODE=2` and `=3` — wrote `samples`, `samples_summary` and the
    `.completed` marker but never called `analysis.save_results` /
    `analysis.save_results_combined`, which the normal path (`start_resume_fit`)
    calls unconditionally. Its docstring promised "all expected output files so
    that downstream code sees a complete result folder", so any script that
    writes a file in `save_results` and reads it back after the fit failed under
    smoke. The gap arrived with modes 2/3 in `d41aa53e8`; it predates the recent
    PyAutoFit commits.

    That was the whole of Heart's `autofit` workspace-smoke failure (cloud run
    34824535982): `autofit_workspace` `overview/overview_2_scientific_workflow`,
    both `.py` and `.ipynb`, ending in
    `FileNotFoundError: .../files/science_summary.json` at script line 279.

    The bypass now runs both hooks between `make_result` and `paths.completed()`,
    in the same position and with the same arguments as the normal path. They are
    deliberately **not** gated on `skip_fit_output()`: the normal path does not
    gate them either, and the smoke profile that exposed the bug sets
    `PYAUTO_SKIP_FIT_OUTPUT=1`, so gating them would reproduce the bug under
    exactly the conditions this fix targets.

    Two files, +72/-0: `autofit/non_linear/search/abstract_search.py` (+7) and
    `test_autofit/non_linear/search/test_abstract_search.py` (+65). No API
    change, no workspace edit (impact option (iii), confirmed by witness rather
    than inference).
- traps: |
    **The new test is a real falsifier, not a passing bystander.**
    `TestBypassCallsSaveResults`, parametrised over `PYAUTO_TEST_MODE` `"2"` and
    `"3"`, asserts both hooks run exactly once with the fit's own `paths` and
    `result`; with the source change stashed it fails in **both** modes. Control
    run first, then the fix.

    **The witness had to run from the canonical workspace root.** The mode-2
    command against canonical `PyAutoFit` (`main`) reproduces the
    `FileNotFoundError` at `overview_2_scientific_workflow.py:279`; the branch
    exits 0 and prints the `science_summary` it wrote under both modes 2 and 3.
    Output was cleared between runs so the `.completed` marker could not shortcut
    the bypass, and `autofit.__file__` was checked to prove the branch's `autofit`
    was on `PYTHONPATH`.

    **`overview_2` is absent from `autofit_workspace/smoke_tests.txt`**, so the
    list-driven local smoke does not cover it — only Heart's cloud run does. That
    coverage gap is a separate workspace task, not fixed here.

    **Claim conflict waived by the human.** `worktree_check_conflict` fired on
    PyAutoFit for `howtofit-mode` (one commit, `README.md` only) and
    `model-figure-prose-simplify` (no commits, three uncommitted
    `docs/cookbooks/*.md`), while this task edits only the two files above — the
    file sets are disjoint, and the task was taken in a fresh parallel worktree
    based on `origin/main`.
- readiness: |
    Heart `readiness --json` was YELLOW at ship time, the reason set the human
    acknowledged when approving this task: workspace validation not passing
    (3 failed, cloud#34824535982); manifest drift x2; profiling drift x6; release
    validation incomplete. No RED reasons. Expected effect of this merge: the two
    `autofit overview_2_scientific_workflow` smoke failures clear, leaving
    `autolens notebooks/imaging/slam.ipynb` as the third, unrelated failure.
    PyAutoFit remains **pending-release** until a build publishes it.

## Original prompt

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
