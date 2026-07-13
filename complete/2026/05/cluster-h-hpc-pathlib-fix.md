## cluster-h-hpc-pathlib-fix
- issue: N/A (Cluster H from triage report 2026-05-07T15-42-17Z)
- completed: 2026-05-08
- workspace-prs: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/62, https://github.com/PyAutoLabs/autolens_workspace/pull/136
- repos: autogalaxy_workspace, autolens_workspace
- notes: |
    Two classes of leftover typos from the `os.path` → `pathlib` blanket
    refactor PRs (autogalaxy #59, autolens #128) in the HPC tutorial
    scripts. The triage report only flagged the autogalaxy `path.sep`
    crash at line 64 — running the script after that one-line fix
    surfaced a second bug at line 207 (`dataset_Path()` corrupted from
    `dataset_path` by the same case-insensitive `path → Path`
    substitution). Expanded scope to fix both classes in the same PR
    after exhaustive grep confirmed only 4 case-corrupted identifiers
    across the two files (`Path.cwd()` and prose-text "Path" in section
    headers were unaffected). Final tally: autogalaxy 6 sites (3 ×
    `Path(path.sep)` + 3 × `dataset_Path()`), autolens 4 sites (3 + 1).
    autolens twin file (`example_cpu.py`, different name from autogalaxy's
    `example_cpu_and_gpu.py`) does not show in the failure list because
    it is pre-emptively listed in `no_run.yaml` ("HPC paths dont exist
    locally."). Verified post-fix that the autolens script no longer
    raises `NameError` and instead reaches the expected pre-existing
    `ConfigException` at line 110 — exactly the failure mode the
    `no_run.yaml` skip documents — so the skip stays.
