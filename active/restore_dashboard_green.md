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
