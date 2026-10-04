# Restore complete Heart dashboard health

Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/274
Issued: 2026-10-04

Type: maintenance
Priority: high
Difficulty: large
Autonomy: human-required

## Original request

Check why heart is red, fix it, and then do anything else to make whole dashboard green

## Scope and evidence

Primary: @PyAutoHeart. Coordinate @PyAutoBrain and @PyAutoMind; split independent source repairs into separate tasks/PRs once confirmed.

On 2026-10-04 a fresh Heart tick exposed five clean library mains behind origin. Fast-forwarded PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy and PyAutoLens; the authoritative release verdict returned from RED to YELLOW. Refreshed Mind from origin. Cached Mind workflow failures cleared on refresh.

Remaining dashboard findings include historic cancelled CI events, CI timing regression, generated manifest drift, dirty/orphan task worktrees, stale/missing validation and timing evidence. Cortex main is dirty with science ledger changes; preserve them. The request is complete only when Heart reports monitoring.complete=true, status=green and no unresolved findings; release readiness alone is insufficient.

## Proposed phases

1. Refresh/survey canonical checkouts and source collectors. Fast-forward only clean main checkouts. Diagnose manifest mismatches against the current repos.yaml, including newly registered organs; regenerate only confirmed stale surfaces with the owning generator after plan approval.
2. Inspect Heart CI timing event lifecycle and coverage/applicability handling against actual GitHub runs. Refresh observations first; route reproduced collector defects through separate bug tasks with regression tests. Never erase adverse evidence or waive checks to obtain green.
3. Reconcile each dirty/orphan worktree against Mind claims and merged commits, preserving every local edit. Present any required destructive cleanup, merge or release as a concrete separate decision.
4. Obtain missing deep timing/install/rehearsal evidence through the existing owning procedures, repair confirmed failures, then tick and publish verified evidence. Report blocked checks explicitly.

## Validation

Use authoritative `pyauto-brain health --scope dashboard --json assess` before/after each phase; inspect all non-green checks and source evidence. Run generator check mode for changed generated surfaces and focused collector tests for any Heart code repair. Use applicable library/workspace validation only when those sources change. Retain raw diagnostic logs outside tracked source.

## Detailed implementation footing

- Brain's FeatureDecision classifies this as large and recommends separate phases. No active Mind claims on Heart/Brain were found. Proposed first branch: `feature/heart-dashboard-repair`; create the isolated worktree only after approval, then survey each newly affected repository before writing it.
- Heart and Brain clean main checkouts were also fast-forwarded (Heart c201ad9; Brain 3275298). Read their updated instructions before implementation.
- Manifest phase: use Mind `scripts/repos_sync.py --check` and bounded `--write --only` surfaces; inspect `check_map_blocks`, `check_public_tables`, `check_hub_blurb`, and `check_checkouts`. Missing canonical checkouts are PyAutoEars and PyAutoInsight. Remaining stale generated maps include Cortex, Eyes, Pulse and Gut. Prefer syncing already-merged fixes on clean mains before generating changes. Preserve Cortex's dirty science records.
- CI phase: inspect Heart `heart/checks/ci_timing.py` (`classify_cancelled`, rollup and event evidence), existing tests and actual run/job logs before deciding whether findings are real failures or require collector repairs. `heart/monitoring.py` defines completeness; do not change scoring to hide unresolved evidence.
- Missing local script timing is explicit: tick reports no PyAutoHands/run_logs/latest. A tick cannot supply deep timing evidence; use the owning validation procedure.
- Final publication uses `pyauto-heart publish` after reviewing its dry-run and clean-main preconditions. Verify published evidence separately from the local board.

Tier: undeclared — merge mode: human /prm.

## Checkpoint

### 2026-10-04 implementation and evidence

- Synced 28 additional clean canonical mains plus .github/profile from already-merged origin changes. All 46 manifest repos present; Insight/Ears cloned and Pulse updated in the preceding turn. Dirty canonical mains were preserved.
- Collector PR https://github.com/PyAutoLabs/PyAutoHeart/pull/275, commit 1c9b924: manifest parser accepts coverage suffixes and keeps unknown headings adverse; worktree scan observes standalone linked worktrees and correctly identifies symlink-only bundles. Existing parser bug prompt remains linked context, not claimed as whole-dashboard completion.
- Validation: before repair 4 regression failures/16 passes; after repair 20 focused passes; 1181 full Heart passes in 70.72s. Independent review CLEAN; Python 3.12/3.13 CI passed. Merge approval requested separately under undeclared-tier human /prm policy.
- Refreshed URL hygiene (12 clean repos), PyPI floors (7 satisfiable), unit/import and workspace smoke timing artifacts (300 tracked tests, 12 imports, 536 script timings; no slowdown in the fresh collector summaries). New unit observations lack baseline comparisons and remain unknown, not passing.
- Fresh skipped-script census: 12 SLOW, of which 5 unmeasured; 15 NEEDS_FIX; 50 permanent entries across 9 workspaces. These require separate measured repairs; exclusions were not removed to change score.
- Release validation preflight passed without warnings. Dispatched TestPyPI-only rehearsal https://github.com/PyAutoLabs/PyAutoHands/actions/runs/37198725621 (still running at last check) and smoke https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/37198914051 (queued). No production release. Continue with rehearsal artifact download and `release validate --stage3-plan`, followed by integration and canonical ingest; don't dispatch duplicate runs.
- Published refreshed privacy-checked dev-box evidence via Heart publish (commit 60c8df9). Snapshot monitoring RED 31/100, incomplete, 105 findings; release YELLOW 75/100 while new smoke report pending. Local complete findings: /tmp/heart-remaining-findings.md and /tmp/heart-dashboard-handoff.json.
- Remaining manifest drift: Cortex/Eyes generated maps and seven generated hooks in dirty canonical repos. Upstream changes exist; clean-main-only sync deliberately preserved local science/work.
- Read-only worktree audit: sparse-operator-oversampling-cache has 11 staged source/test files (+44/-1157) explicitly retained for human inspection; cortex-may-submit holds patch-unique unmerged Brain/Cortex commits; bootstrap-stage-b holds three unmerged benchmark/docs commits. mass-field-profiling-live holds untracked scientific witnesses; point-source-search-nautilus-leaf has explicit KEEP worktree/data instruction; vis-lp-inspection-bundle is active with unmerged commit and dataset/output symlinks. None removed or reclassified as passing.
- Dirty canonical repos contain science records/results (Cortex, Eyes, inference/profiling), untracked user scripts (Fit/Lens assistants), and one formatting-only developer patch. These need owner decisions/preservation before checkout cleanup, not automatic deletion.

Follow-up 2026-10-04: user explicitly requested getting new repos such as PyAutoInsight and PyAutoPulse. Cloned PyAutoInsight and PyAutoEars into their canonical organs/ paths; fast-forwarded clean PyAutoPulse main by ten commits to f180151. All three checkouts are clean and match origin/main. Broader source-repair plan approval is still pending.

Human approved the phased implementation plan on 2026-10-04: "I approve of the plan". Proceed with bounded repairs and validation; preserve unfinished work. Tier remains undeclared, with human /prm for merges. Register the issue and worktree before source repairs.

### 2026-10-04 generated drift cleared

- Continued on explicit user request: "Do dashboard repair and continue heart work".
- Fast-forwarded Eyes, both assistants, both profiling/inference projects and the Lens developer workspace after checking upstream changes did not overlap any local files. Verified all 128 local files byte-for-byte unchanged; receipt `/tmp/heart-preserving-sync.json`.
- Cortex upstream overlapped only generated dashboard.md/dashboard.html/state.json. Backed up every local changed file with SHA256 receipt in `/tmp/heart-cortex-before-sync`, restored only those three generated files, fast-forwarded main, and regenerated the dashboard using `pyauto-brain cortex dashboard --apply`. Science records, projects.yaml and checkin.yaml stayed byte-identical. Local science remains uncommitted intentionally.
- `repos_sync.py --check` now passes all 20 checks: all 46 declared checkouts present, all generated hooks and organism maps current. No new source implementation or PR was required.
- Heart after manifest sync: monitoring RED 46/100; release readiness STALE 85, sole release reason "release validation incomplete: no rehearsal for current source". Integration run 37199991757 still running at checkpoint; do not dispatch another.
- PyAutoGalaxy CI was showing an old September observation despite passing current main tests. Exact live API payload and collector replay confirm current main success; refreshed CI via its owning collector without changing policy or injecting evidence.
- Asked human to restore Anthropic OAuth credential/organization access for Mind digest's oauth_not_allowed_for_organization failure. No messaging workflow rerun authorized.

### 2026-10-04 integration result and next repair

- Release integration 37199991757 completed with 723 passes, 82 skips, one timeout. All TestPyPI installation checks passed. `autolens_workspace_test/scripts/multi_dataset/jax_likelihood/rectangular_rtu.py` timed out at 1805.04s after JAX compiled the vectorized likelihood in 3.1s and blocked waiting for materialization; stack points to JAX block_until_ready through autofit/non_linear/jax_compile.py:249, invoked at script line 206. Similar to the historical execution-stall family, not yet proven identical root cause. No timeout increase/quarantine/retry performed.
- Authoritative canonical ingest completed with RED60, exact reason `release validation FAILED (stage integrate)`. Artifacts `/tmp/heart-validation-37198725621`, failed leg JSON `/tmp/heart-failed-multidataset`, logs `/tmp/heart-integration-failure.log`. Heart published current real evidence; monitoring RED33/100.
- Issue #278 fixes retired-repo cache leakage (PyAutoConf and PyAutoBuild) through a valid current Heart roster. Task branch feature/retired-repo-sidecars has an uncommitted three-file patch; 22 focused and 1200 full tests pass, independent review CLEAN. Copied-cache replay preserves every one of 150 sidecar files and all configured/global evidence. Shipping authorization under current RED requested; no grant received yet. Do not publish or claim the patch live until authorized.
- User OAuth-access question remains pending. Existing science files and retained worktrees stay intact.

### Authorization and diagnostic continuation

Human “I authorise both need help with latter if its doable” authorized #278 development shipping despite RED and timeout work. Subsequent “Hmmm dont do thr anthropic stuff do whatever work you can without it” withdraws the Anthropic migration only; credentials and workflow remain untouched. #278 shipped as Heart PR #279 (ba9d2f3); human /prm remains required.

Started existing autolens_workspace_test retime workflow 37203338570 for multi_dataset/jax_likelihood/rectangular_rtu.py, 3 repeats per Python leg,300s cap,native stack dump after120s. This is smoke-profile/current-source diagnostic evidence, not the TestPyPI release environment and cannot clear release validation. Prior causal research record is complete/2026/08/xla-cpu-eigen-pool-deadlock.md; do not re-open its settled decision against filing upstream.

### Focused timeout evidence

- Re-time 37203338570 completed all six repetitions under the default smoke profile: Python3.12 15.9/8.2/8.3s; Python3.13 15.6/8.0/7.8s. Harness verdict NEITHER on both; no native dump triggered. This does not clear the failed TestPyPI release.
- Actual build_env_for_script resolution for rectangular_rtu.py shows only PYAUTO_TEST_MODE (2 vs0) and PYAUTO_FAST_PLOTS (1 vs0) differ; the script declaration already enables JAX/full datasets. Follow-up diagnostic 37203617994 uses exactly those two release overlays,3 repeats per leg,300s cap,native dump120s. Preceding draft dispatch37203585601 was cancelled before measurement to use the exact resolved overlay; it is not diagnostic evidence.
- PR #279 Python3.12/3.13 checks passed. Explicit human /prm requested separately under RED override; no merge grant yet.

Follow-up37203617994 completed 6/6 passes with exact resolved release environment overlay: Python3.12 7.8/4.9/4.9s; Python3.13 9.2/8.0/7.7s; both NEITHER. Together with the smoke-profile diagnostic this is12/12 passing focused executions. No stall/native dump was captured, and no claim of a fix or release clearance follows; these used current source rather than the exact TestPyPI integration installation. Saved logs `/tmp/heart-rectangular-retime.log` and `/tmp/heart-rectangular-release-retime.log`. No further jobs/watchers left by this session. PR279 CI green; human /prm still required. Anthropic workflow and credentials remain untouched.

### PR279 merged — 2026-10-04

Human /prm merged PR279 at 3d86fd8; issue278 closed and phase recorded in [complete/2026/10/retired-repo-sidecars.md](../complete/2026/10/retired-repo-sidecars.md). This supersedes earlier awaiting-authorization/PR-open checkpoints. No retired-repo work remains pending; umbrella274 stays open for genuine health findings.

### 2026-10-04 resumed exact-environment investigation

- Live user authorization: “I authorize development investigation and repair despite the current RED reason above. Follow start-dev and record the task-specific authorization wherever required.” Prepare tested independently reviewed PRs; merges remain explicit human /prm. No Anthropic credentials/digest/OAuth work, production release, external messages, unattended watchers, cap increases, quarantine, evidence erasure or destructive cleanup.
- Refreshed canonical Heart tick/readiness: RED60, exact reason `release validation FAILED (stage integrate)`; monitoring RED33/incomplete. Published feed reported STALE45 and is outdated; it does not supersede canonical failed evidence.
- Saved failure artifact reviewed: Python3.12.14; 723 passes,82 skips,one1805s materialization timeout. Original workspace df35fd4553f861575af7c27ad25b5f4d8d97d09c; Hands760affdbcbf0605266e49b33a65f7bef89f9b0b3. Exact library SHAs remain in /tmp/heart-validation-37198725621/commit_shas.json.
- Discriminating new evidence: integration installed JAX/JAXlib0.11.2 then workflow explicitly downgraded both to0.10.2. Both passing focused retimes installed0.11.2. This runtime difference is not a proven cause. Historical Eigen/ducc0 research reviewed; no upstream filing.
- Isolated diagnostic reconstruction under Mind tmp/heart-timeout-20261004: archived exact workspace+Hands,115 final package pins extracted from failed log, clean venv installing exact TestPyPI wheels. No source edits or canonical science changes. Next: verify import/version provenance, bounded target repetitions with native capture, compare only discriminating runtime changes if failure reproduces.

## Bounded exact-wheel diagnostic phase (approved umbrella #274)

- Preserve the failed run's package pins, workspace/Hands SHAs, Python patch version and source URL in a diagnostic manifest.
- Add a manual Heart workflow that installs only those wheels and dependencies, checks exact workspace/Hands commits, and invokes their existing release environment resolver.
- Run only rectangular_rtu.py, at most six fresh processes, native dump after120s,300s cap. Preserve results and stop on the first failure. Never emit or ingest release-stage evidence.
- Validate manifest/provenance/error handling and process timeout behavior locally; independently review the final branch; prepare a PR, with human /prm for merge.

Tier: undeclared — merge mode: human /prm.

Detailed files: `.github/workflows/release-diagnostic.yml` (manual isolated Ubuntu runner, Python3.12.14, explicit wheels, upload diagnostic artifacts even on failure); `.github/scripts/release_diagnostic.py` (manifest validation, package/import/environment receipt, existing Hands env resolver and workspace retime native-stack helpers, bounded capture); `diagnostics/release-37199991757.json` (115 observed final pins and immutable repo SHAs); `tests/test_release_diagnostic.py` (fail-closed manifest and bounded child-process regressions); `docs/release_validation.md` (diagnostic meaning/limitations and invocation).

Starting Heart main34c73d3, clean; no competing Heart Mind claim. Task branch feature/restore-dashboard-green under .worktrees/restore-dashboard-green. Existing approved umbrella plan and live user development override apply to this evidence-gathering phase. No causal fix asserted and release RED remains `release validation FAILED (stage integrate)`.
