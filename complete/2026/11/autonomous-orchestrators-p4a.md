- epic: autonomous-orchestrators (phase 4a of 4a–4c; epic draft/feature/pyautobrain/autonomous_orchestrators_epic.md)
- summary: shadow shifts + the pilot ledger. PyAutoBrain#571: `shadow: yes` (`_brief.is_shadow`, checked yes|no) makes `_tick_locked` run the plan and `_propose` record proposals (prompt, tier, pick reason, `proposed: true`) up to max-sessions — no lease, no worker, no session counted; the digest marks them `proposed (shadow)` and asks no packet; `finish_shift` appends one `batches/pilot/pilot.md` row (`_digest.pilot_row`; human cells `?`) in the digest's Mind commit, and now returns at once when `digest.posted` exists (a second call used to re-append the digest). PyAutoMind#532: `batches/pilot/pilot.md` (header + who writes what) and the `shadow:` key in batches/AGENTS.md.
- decision: ledger at batches/pilot/pilot.md, not batches/pilot.md — every batches/*.md is read as a record (human, 2026-11-04).
- witness: tests/test_orchestrator_shadow.py 9 passed (control: shadow branch off → 6 fail), incl. real-git exactly-one pilot row on Mind main; 3d digest tests 23 unchanged; Brain 1521 (+2 pre-existing test_prompt_budget failures, same on main); Mind 712; tenant firewall OK.
- merge: Mind#532 by /prm; Brain#571 by the human in the GitHub UI 2026-11-04T10:04Z after the API merge path returned repeated GitHub server errors (GraphQL "Something went wrong", 502, REST "merge already in progress").
- next: 4b unattended glance close-out + stage-2 Shadow rows.
- heart: YELLOW (autofit_test MultiStartResumeNaNCounters.py timeout; no release rehearsal) acknowledged by the human at ship; judge tier.

## Original prompt

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
