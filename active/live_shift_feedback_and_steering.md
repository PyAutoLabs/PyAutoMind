# A running shift you can watch and steer: one live status comment, a /batch watch skill, and pause / drop / edit

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-13
Issued: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: (restated 2026-11-13 to the human-approved design — comment commands, not files) (a) a fake-clock shift test creates one status comment on the brief's `issue:` and then only edits it (≤ 1 edit per tick, on state change or every 10 min, plus one closing edit), its body the `batch watch` snapshot (`render_status`); a crash or timeout never yields a second comment; (b) `/pause` holds spawns, re-dispatches and new close-outs until `/resume`; `/drop <task>` removes an unspawned pick, and a dropped task's PR is never counted as an unattended merge (a close-out already past its marker check may still merge; that race is recorded as merged outside the close-out, with no stage-2 row); `/stop` has exactly the STOP file's effect; (c) commands count only from `mention_login`, after `dispatched:`, first line only, enacted and acknowledged once by comment id; an edit after enactment does not re-trigger; (d) the full suite passes offline
Review-minutes: 25
Unattended: never
Lane: any

Original request (human, 2026-11-13): "more feedback on how the run is going live… via a Claude window but maybe also somewhere on the dashboard… I would still read this and could edit a run if I saw something terrible." Needed before M3.1, the first live shift.

**What exists.** `pyauto-brain batch watch` (`agents/conductors/batch/_watch.py:1-18`, `watch` at :186) draws the slot read-only on the laptop. The digest posts once at `review-at` (`_orchestrator.py:1084` `post_once`). The kill switch is a `STOP` file in the slot, read first each tick (`_orchestrator.py:835-837`). The brief is re-read every tick (`brief_open`, `_orchestrator.py:839`), and it already has `exclude:` (`_brief.py:118`).

**Seeing it (options):**
1. **One live status comment on the shift issue, edited each tick** (throttled), body = the `batch watch` render. + readable in the GitHub app, edits do not notify (no push noise), reuses the digest's issue. − a new network act: AUTONOMY.md:835-870 allows only listed comments and "never a second comment"; this needs a dated amendment (create once, edit only).
2. **A dashboard panel.** − the slot is laptop state; showing it means committing shift state to Mind each tick (commit noise, races with the Mind writer) or a new Pages publish; stale between refreshes.
3. **A `/batch watch` skill mode for a Claude window.** + no new surface; a Claude session can also explain what it sees. − reads the slot only on the laptop; elsewhere it falls back to option 1's comment.
**Recommend 1 + 3**; the dashboard links to the open shift's issue instead of a panel.

**Steering it (smallest set):**
- `STOP` (exists): every tick does nothing while it exists; workers already out are not killed.
- `PAUSE` file (new): no new dispatches or backlog dips; workers in flight continue and are reaped.
- Drop a pick: delete it from `tasks:` or add it to `exclude:`. Re-check: `exclude:` covers backlog dips only (`batches/AGENTS.md:215`), so make it apply to named tasks too; add a "dropped, still running" state; killing a worker stays the human's, by hand.
- Edit the brief: picked up next tick already, but only in the local Mind checkout. From a phone: (a) the watcher pulls the brief from `origin/main` each tick, or (b) it reads `/pause`, `/resume`, `/drop <path>` comments by the human's login on the shift issue. Both widen the network surface (see `draft/feature/pyautobrain/mobile_shift_operation.md` blocker 2). Recommend (b): the commands live where the human already reads the status.

Tier judge: it amends the watcher's network surface and adds human controls to a running shift.
Programme: before M3.1; folds into the M3.3 "fixed sheet per shift".

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
