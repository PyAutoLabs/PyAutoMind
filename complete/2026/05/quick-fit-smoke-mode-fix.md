## quick-fit-smoke-mode-fix
- completed: 2026-05-07
- workspace-prs:
    - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/60
    - https://github.com/PyAutoLabs/autolens_workspace/pull/129
- repos: autogalaxy_workspace, autolens_workspace
- notes: |
    Cluster A of the recent release-prep triage. Four aggregator tutorials
    (scripts/guides/results/aggregator/{data_fitting,models}.py × 2 workspaces)
    crashed with `TypeError: 'NoneType' object is not subscriptable` at
    PyAutoGalaxy/autogalaxy/aggregator/agg_util.py:101 in fast smoke mode
    (PYAUTO_TEST_MODE=2 + PYAUTO_SKIP_VISUALIZATION=1). Root cause: the
    _quick_fit.py helper invoked via subprocess inherited those env vars,
    suppressing the visualizer that writes image/dataset.fits, so
    fit.value("dataset") returned None. Fix: helper now pops
    PYAUTO_SKIP_VISUALIZATION / PYAUTO_SKIP_FIT_OUTPUT and downgrades
    PYAUTO_TEST_MODE>=2 to 1 before importing autofit. Idempotent early-exit
    means cost is paid once per workspace per smoke run. Standalone fix —
    no library change. The PR #55/#118 refactor that split start_here.py
    into _quick_fit.py + un-skipped these scripts in no_run.yaml exposed
    the latent bug (the old start_here.py had a partial PYAUTO_TEST_MODE=1
    pop, but it never handled modes 2/3 + SKIP_VISUALIZATION).
