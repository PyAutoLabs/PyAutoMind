# Phase 14.1 Maintenance finding adapters with stable keys

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Issued: 2026-11-27
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: `pyauto-brain batch maintain --dry-run` over live board data lists at least 5 findings, each with key, source, repo, witness and tier floor; two reads 10 minutes apart give identical keys; tests (fixture boards) fail on the base commit
Review-minutes: 10
Lane: local-dev
Unattended: never

Slice 14.1 of `draft/feature/pyautobrain/maintenance_orchestrator.md` (plan approved 2026-11-27; the survey and the plan are in
`Science/scratch/phase14_maintenance_plan_2026-11-27/PLAN.md`). Buildable before the M3 gate (human decision 1, 2026-11-27): it is read-only tooling.

## What

One `Finding{key, source, repo, paths, summary, witness, tier_floor, lane}` type and per-source adapters:

- **No-run census** (`board.json performance.no_run`, or Heart's `no_run_census.json`): key `no_run:<repo>/<entry>`. Witness: the entry is gone from `no_run.yaml` and the script passes under the smoke cap. Tier floor: glance.
- **Heart monitoring inventory** (`board.json monitoring.findings`): key = the finding `id` with any `run_id` discriminator dropped (smoke_timings changes it every run). Leave out `worktree_drift` (human decision 4: local checkout state belongs to Gut and `/repo_cleanup`). Witness: the key is absent, or its status is green, on a fresh board read. Tier floor: glance for an organ's own workflow red; judge for a workflow file, dependency cap or public name.
- **Heart release verdict**, i.e. `_green.py`'s classifier as an adapter (human decision 3: one filing path), including the organ CI-red lines `_green` misses today (`<Organ>/workflows/<name>: failure`).

`batch maintain --dry-run [--sources …] [--json]` prints them. The tick never reads Heart, so this runs only at brief and collect time.

## Out of scope

Writing prompts (14.2), hygiene and CI-timing sources (14.5).
