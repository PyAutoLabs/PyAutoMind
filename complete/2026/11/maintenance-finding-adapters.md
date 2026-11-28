Merged PyAutoBrain#732 (human /prm, 2026-11-27). Phase 14.1 of the maintenance orchestrator.

`pyauto-brain batch maintain --dry-run [--sources census,monitoring,release] [--json]` (`agents/conductors/batch/_maintain.py`). It is read-only and never called from the tick. Its findings have stable keys, a witness and a tier floor.

**Sources:**
- **No-run census:** one whole source, whichever is fresher; never merged.
- **Heart monitoring inventory:** keys without `run_id`. Excludes worktree_drift, repo_state, open_prs and release rows. Timing families are deferred to 14.5.
- **`_green.classify`:** the release adapter, plus organ CI-red lines.

**One key per defect.** A repo-level `ci:` key gives way to workflow-level keys.

**Tier floors** (judge when unsure):
- **Census:** glance only from structured passed/seconds/cap. NEEDS_FIX and kill or timeout wording force judge.
- **Organ CI red:** glance only on the head commit, outside release workflows, and for an organ that ships no package and is neither the Brain nor the Heart oracle. Those exclusions are derived from the body map and the policy; if they can't be read, nothing is glance.

**Reads report ok, stale and partial.** An unread source exits 3. Slice 14.2 must never file from, or clear keys for, an unread, stale or partial read.

Live: 23 findings with stable keys (20 census judge; monitoring 2 glance organ dashboard reds and 1 judge release workflow; release stale). Tests: 36, each round red on the previous head. Full suite 2641 passed. Independent Opus review: 4 rounds, the last CLEAN after a fail-safe minor fixed in 5319f6d. Heart dev-ship GREEN.

Follow-up, not filed: before any census row can be glance, Heart's census must publish structured passed/seconds/cap_s fields.

## Original prompt

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
