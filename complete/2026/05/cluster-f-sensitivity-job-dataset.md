## cluster-f-sensitivity-job-dataset
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1259
- repos: PyAutoFit
- notes: |
    Surfaced in a release-prep triage report as Cluster F: a single
    failing script (autofit_workspace_test/scripts/database/scrape/
    sensitivity.py) raising AttributeError: 'NoneType' object has no
    attribute 'data' at line 241 (Analysis.__init__ unpacking
    dataset.data). The user proposed two hypotheses: simulate_function
    returning None under test mode (workspace bug), or job dataset
    wiring broken by a recent PyAutoFit refactor (library bug). Both
    were wrong — the actual cause is a partial library optimization.
    PyAutoFit commit 41095a0 ("skip simulation if job is complete",
    Oct 2024) added `if self.is_complete: dataset = None` in
    Job.perform() but didn't also skip the downstream
    base_fit_cls / perturb_fit_cls calls, so they receive None.

    The library's own test_perform_twice masked the contract issue
    because the test conftest's Analysis.__init__(dataset) just
    stashes dataset without unpacking — real workspace Analysis code
    (autofit_workspace/scripts/features/sensitivity_mapping.py:246
    and the failing test-workspace script) eagerly unpacks
    dataset.data and dataset.noise_map. Fix per
    feedback_no_silent_guards.md: stop the producer of None, not
    add a consumer-side tolerance. Collapsed the if/else to always
    call simulate_cls. Re-runs still skip the expensive non-linear
    search via Search.fit's load-from-zip path
    (paths.restore() + paths.is_complete in abstract_search.py).
    Only the typically-cheap simulator cost is no longer optimized
    away.

    Verification: bug reproduced exactly on clean main (matched
    user's stack trace), fix applied, clean two-run cycle passes
    (first run completes, second hits is_complete=True via zip
    presence, restore() unzips, load path returns).
    Full PyAutoFit suite 1241/0/1 (skipped pre-existing). All 9
    autofit_workspace_test smoke scripts pass.

    Known limitation flagged in PR body but out of scope: if a
    previous run was killed mid-fit (e.g. [perturb].zip present but
    [base].zip missing), re-runs hit a different failure on that
    cell — Search.fit.restore() finds nothing to restore for the
    missing side, paths.is_complete=False, resume kicks in,
    Fitness.check_log_likelihood raises SearchException because the
    new (non-deterministic) simulator FoM doesn't match the
    persisted partial-fit FoM. Separate bug, separate fix.

    Verify-triage-clusters habit paid off again: the user's two
    hypotheses framed the search but were both wrong; the third
    answer (deliberate library design + workspace pattern conflict)
    was reachable only by tracing Job.perform() history.
