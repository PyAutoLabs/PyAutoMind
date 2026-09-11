## release-integrate-discard-stale-result-files
- issue: none (direct wiring change; the prompt was picked from draft/ and never issued)
- completed: 2026-09-11
- organ-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/225 (merge 412daaa2)
- closed-out: 2026-09-11 from a web session (`/prm` on the MCP surface; no task worktree — session clones only)

**Summary.** One workflow step, *Discard result files the workspace checkout carries*, placed between the workspace checkout and the runner in both shard jobs of `workspace-validation.yml` (`run_scripts` unconditional; `run_notebooks` gated like its checkout) and before *Mark scripts start* in `smoke-tests.yml`. It removes `*__script.json`, `*__script.md`, `smoke_timings.json` and `report.json` under `test-results/`, plus any `smoke_timings.json` elsewhere in the checkout (`.git` pruned), keeps `cache_state.json` (this run's sidecar, not a result), and prints one `::warning::` per discarded file so a leaking repo is visible in the run log rather than silently laundered. The shell carries no `${{ }}` so the wiring tests execute it verbatim against a planted stale tree. Four tests in `tests/test_workflow_wiring.py`; Heart suite 971 passed on both Python legs.

**Scope shipped vs filed.** The prompt offered three guards and asked for the cheapest robust combination. Option 1 (delete pre-existing result files before the runner) is what shipped. Options 2 (analyze-side path filter with a loud warning naming the shard and the foreign path) and 3 (a workspace-repo lint that fails when `test-results/` or `*__script.json` is tracked) are re-filed as `draft/bug/pyautoheart/release_integrate_analyze_path_filter_and_workspace_lint.md`, pointing back here.

**The release.** Nightly Release Integrate runs 34323573912 (2026-09-09) and 34449490363 (2026-09-10) stopped at Stage 3 on the stale `test-results/` that autolens_workspace_test#311 committed, while every script that ran passed. awt#313 removed the files on the workspace side; run 34573908023 (2026-09-11 07:20 UTC, on Heart main *before* #225) then went green end to end: every shard, analyze and emit_release_report succeeded, notebook legs skipped as usual, 43 minutes. #225 is the durable guard, not what fixed last night.

**Traps / notes.**
- **The tenant firewall reads test modules.** The first push failed Heart Tests not on pytest (971 passed) but on the `repos_sync.py --check --only "tenant firewall (organ code)"` step that follows it: a comment in `tests/test_workflow_wiring.py` named `autolens_workspace_test`, and a workspace repo's name in organ code outside a declared config surface is an instance fact. The workflow files may carry the name; the test module may not. Reworded the comment (commit 65d1015). Run the firewall locally before pushing Heart test changes: symlink Heart, Mind and Brain under one root and run the check with `--root` pointing at it.
- The discard step runs *after* checkout and *before* the runner, so this run's own results are never touched; `cache_state.json` is kept because it is the JAX-cache sidecar, not a report.
- A shallow web-session clone cannot prove a merge with `merge-base --is-ancestor` until `origin/main` is fetched into `refs/remotes/origin/main` explicitly; a plain `fetch origin main` in a clone made with `--branch` leaves only `FETCH_HEAD`.

**Follow-ups.** The re-filed prompt above (options 2 and 3). `complete/2026/09/einstein-radius-jit-seed-finder.md` cited this prompt's draft path for the Stage 3 failures; repointed to this record in the same close-out commit.

## Original prompt

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
