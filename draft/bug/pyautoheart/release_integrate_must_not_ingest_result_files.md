# release-integrate must not ingest result files that pre-exist in a workspace repo's test-results/

Type: bug
Target: PyAutoHeart
Repos:
- autolens_workspace_test
- PyAutoHeart
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-09-10

Nightly Release Integrate runs 34323573912 (2026-09-09) and 34449490363 (2026-09-10) in PyAutoLabs/PyAutoHeart failed with "3 failed: autolens_workspace_test jax_likelihood/lp.py, smbh.py, multi_dataset/jax_likelihood/mge.py" while every script actually run in CI passed. Cause: autolens_workspace_test PR #311 accidentally committed a local smoke run's `test-results/` directory (`autolens_workspace_test__scripts__script.json`, `.md`, `smoke_timings.json`, with `/home/jammy/...` paths and three pre-re-pin "JAX vmap likelihood mismatch" failures). Heart's run_scripts shards write into `workspace/test-results/` and upload the whole directory, so the committed stale file rode into every autolens_test shard artifact and the analyze stage (`heart/validate.py` rglob over all `*.json`; `heart/checks/test_run.py` / `script_timing.py` glob `*__script.json`) merged its failures into the report and set `ready=false`. The immediate fix (awt#313) deletes the files and gitignores `test-results/` (the `.gitignore` only had `test_results/` with an underscore).

Wanted, a durable guard in PyAutoHeart so a leaked file can never fail a release again — pick the cheapest robust combination:
1. In the run_scripts shard steps (release-integrate.yml, workspace-validation.yml, smoke-tests.yml), delete any pre-existing `*__script.json` / `*__script.md` / `smoke_timings.json` under `workspace/test-results/` before running (keep the `cache_state.json` sidecar), or write results to a fresh directory.
2. In the analyze/collector path, drop or flag any result entry whose `file` path is not under the runner workspace (e.g. starts with `/home/jammy` or does not start with `$GITHUB_WORKSPACE`), and log a loud warning naming the shard and the foreign path.
3. Optionally a workspace-repo lint (Heart required workflow or workspace CI) that fails when `test-results/` or `*__script.json` is tracked in git.
Add tests in PyAutoHeart/tests for the chosen guard(s) using a fixture that plants a stale `*__script.json` with a foreign path and asserts it is excluded/warned.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 -->
