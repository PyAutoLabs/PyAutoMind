# Autonomous orchestrators phase 4a: shadow shifts + the pilot ledger (`batches/pilot.md`)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Filed: 2026-11-04
Issued: 2026-11-04
Epic: autonomous-orchestrators
Phase: 4
Consequence: judge
Witness: a fake shadow shift (`shadow: yes`) spawns zero workers while its counters record what it would have dispatched with each pick reason; its digest lists those proposals; `finish_shift` appends exactly one well-formed row to a new `PyAutoMind/batches/pilot.md` table through the one Mind writer; `batch brief --check` accepts `shadow: yes|no` and refuses any other value; `pytest PyAutoBrain/tests -q` green
Review-minutes: 20
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md, phase 4 ("Dev orchestrator pilot", "What the pilot measures", "Success measures (pilot)"); slice 4a of 4a–4c. Builds on phase 3 (`complete/2026/11/autonomous-orchestrators-p3a.md` … `-p3d.md`).

The pilot opens with two **shadow shifts**: the orchestrator proposes and digests, the human works as today, and the minutes are logged as the baseline. This slice builds that mode and the ledger the whole pilot is measured in.

- **`shadow: yes`** (brief key, `batches/AGENTS.md`): the watcher runs the same plan inside the brief and records each proposal (prompt, tier, pick reason) in `counters.json`, but spawns nothing and takes no lease.
- **Digest:** a shadow shift's digest lists the proposals under brief work and backlog picks (marked as proposals, not work), with every counter.
- **`batches/pilot.md`:** one row per shift, appended by `finish_shift` through the one Mind writer. Columns are the epic's pilot measures: slot, shadow or live, `review-minutes-planned`, `review-minutes-actual`, verified merges, `glance` auto-merges, reverts, overrules, pushes, drafts filed, tokens, workers crashed. The human fills `review-minutes-actual` and overrules at check-in, so the row lands with those cells blank and a check-in step names them.
- Docs: `batches/AGENTS.md`, the batch conductor `AGENTS.md`.

Tier: judge — merge mode: human `/prm`.

<!-- filed by hand 2026-11-04 when phase 4 was sliced 4a–4c (agent proposal, human approved filing); headers mirror intake's -->
