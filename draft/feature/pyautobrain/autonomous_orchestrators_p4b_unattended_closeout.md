# Autonomous orchestrators phase 4b: unattended `glance` close-out + stage-2 Shadow rows

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
Epic: autonomous-orchestrators
Phase: 4
Blocked-by: draft/feature/pyautobrain/autonomous_orchestrators_p4a_shadow_shifts.md
Consequence: judge
Witness: with fake PRs and fake sessions, a declared-`glance` PR whose CI landed green and whose guards all hold gets exactly one close-out session dispatched and exactly one row in `autonomy_log.md` "Unattended `glance` sub-window (stage 2)"; each guard failing on its own (witness not run by an independent session, Heart RED, merge-cap reached, tier not `glance`, `decision-taken` label, no different-model adversary leg during the first 10) dispatches nothing and the digest names the reason; the `glance-auto-merges` counter moves only on a real merge; `pytest PyAutoBrain/tests -q` and PyAutoMind tests green
Review-minutes: 25
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md, phase 4; slice 4b of 4a–4c. Doctrine: `PyAutoBrain/AUTONOMY.md` "Unattended `glance` merges" (2026-11-03) and "The `glance` Shadow-window ruling — 2026-11-04" (record `complete/2026/11/glance-tier-ruling.md`).

Until this lands, no shift may merge unattended: the ruling's stage-2 sub-window table exists, but nothing writes to it.

- **When CI lands** on a PR a worker named in its `.done`, using the one read the watcher is allowed (`gh pr checks`), the watcher checks every guard in "Unattended `glance` merges" plus the stage-2 rule. If all hold, it starts **one** close-out session running the `/prm` procedure. That is a dispatch, under the brief's grant, not a merge by the watcher, so the watcher's network surface is unchanged. If any guard fails, nothing is dispatched and the digest names the reason.
- **Stage-2 rule:** each of the first 10 unattended merges needs the different-model adversary leg actually run. Count the rows in the stage-2 table to know where the sub-window stands.
- **`lifecycle.py shadow-row` gains an unattended mode** that appends to the stage-2 table (columns: date, task, brief, gate with the adversary leg, human action) and never to the stage-1 table.
- **Counters:** `glance_auto_merges` (and `pushes` if a push is sent) increment in `counters.json`, so the digest's zeros from 3d start moving.
- Revisit `merge-cap:` counting: one merge past the cap retires the sub-rule (AUTONOMY revert condition).

Tier: judge — merge mode: human `/prm`.

<!-- filed by hand 2026-11-04 when phase 4 was sliced 4a–4c (agent proposal, human approved filing); headers mirror intake's -->
