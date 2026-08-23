# The Brain board — assessment and design record

Date: 2026-08-23. The investigation write-up for
`draft/research/pyautobrain/explore_dashboardify_the_brain_s_operational_sur.md`
("dashboardify the Brain's operational surfaces"), resolved by the human's
direction: **build the PyAutoBrain dashboard, move the /wake_up routine onto
it, and make it the morning and general starting point** — with the local repo
sync run as a terminal command rather than a Claude chat. Implementation:
PyAutoBrain branch `claude/pyautobrain-dashboard-o33z4r`.

## What was decided

The sixth one-tap board, at `https://pyautolabs.github.io/PyAutoBrain/`. Same
pattern as the five live boards (Mind tasks, Heart health, Hands release,
Memory knowledge, Scientist umbrella): a generated page + one-tap 📋
copy-for-Claude payloads + `badge.json` as the cross-board headline contract.
Where the Heart board answers "is it safe to release?" and the Mind board
"what could I work on?", the Brain board answers **"what needs me this
morning?"** — the operational glance `/wake_up` used to assemble by driving
doors in sequence.

### Inventory: wake_up's legs → their new home

| /wake_up leg | On the board? | How |
|---|---|---|
| Sync (`pull_all_main.sh`) | ⌨ chip only | stays local — `bin/morning.sh` (sync + clean in one terminal command; the board's top row carries it as a copyable **terminal** chip, visually distinct from Claude chips) |
| Clean slate (`clean_slate.sh`) | ⌨ chip only | same — inside `morning.sh`; orphan-dataset calls remain terminal output |
| Overnight sweep (`overnight_status.sh`) | ✅ | rendered rows incl. the ⏸ blocked-at-a-gate refinement; each ✗ carries a `/bug … — <run url>` chip |
| Health/release verdict | ✅ | read from the **Heart board's badge.json** (compose, don't recompute) + `/health` chip; nightly-release outcome is an overnight row |
| Version drift (`version_drift.sh`) | ✅ | consensus check rendered; drift rows carry `/bug` chips |
| Community scan | ✅ | imports the Ears' `build_scan()` wholesale; awaiting-response rows carry `/community triage <ref>` chips; replies stay human-gated in `/community` |
| Issue-tracker drift | ✅ (count only) | org-wide open-issue count + `/issue_cleanup` chip; the two-evidence audit stays that skill's confirmation-gated job |
| Resume context | ✅ | the Mind's own generated dashboard counts + `active/` task files (`/start_dev` chips) + pending-release PRs (`/prm <url>` chips) |
| Hygiene | 🚪 door only | `/hygiene` chip — the sweep itself needs local timings, so it stays a door, not a board section (see "not dashboarded" below) |
| The digest card | ✅ | the whole page *is* the card; `pyauto-brain board` prints the identical markdown digest in a terminal, and badge.json carries the "N need you / clear to work" verdict |

`/wake_up` survives as a fallback door only (board stale/unreachable, or
explicit ask); its body now says so and delegates to `morning.sh` + the board
CLI. The passive morning Slack webhooks are unchanged.

### Architecture (mirrors the sibling boards)

- **`PyAutoBrain/board/_board.py`** — thin collect (read-only `gh` + the
  sibling boards' published badges) + pure render (`--md/--html/--json/--badge`,
  `--apply` writes the Pages payload). A **surface**, not an agent: it neither
  acts nor opines, so it sits outside the conductor/faculty tiers (precedent:
  the Mind renderer living with the intake conductor). `pyauto-brain board`
  dispatches to it; `/board` is the chat-side wrapper (the mobile fallback).
- **Vocabulary in `config/policy.yaml` under `board:`** (declared config
  surface): overnight job list, version-stamp list, reference release repo,
  sibling-board map. Org/owner derived from `repos.yaml` at runtime — tenant
  firewall clean (gate run green).
- **`brain_board.yml`** publishes daily at 05:30 UTC (after the Heart's 05:00
  badge refresh) + on dispatch: Pages artifact only (`index.html`,
  `badge.json`, `board.json`, `board.md`) — **nothing committed**, since the
  data is time-varying and a daily self-heal commit would be pure noise. This
  is the one deliberate divergence from the Mind board's committed-page shape,
  and matches Heart/Hands.
- The umbrella router can consume `brain | N need you / clear to work` from
  `badge.json` like the other boards' headlines (follow-up, not wired here).
- 413 Brain tests pass (8 new hermetic board tests: stub gh, fabricated Mind,
  file:// badges; read-only proof; html self-containment).

### Considered and NOT dashboarded (the research prompt allowed "none")

- **Hygiene / profiling / import-time metric dashboards** (the prompt's axis
  2): their measurements are local-machine facts the cloud render cannot
  observe honestly. The Heart's devbox-publish pattern could feed them later;
  deferred until a real morning need shows up — the board carries their doors.
- **The full issue_cleanup audit half**: needs the Mind completion records +
  per-issue evidence; too heavy and too judgment-laden for a generated page.
  Count + door is the honest surface.
- **A conductor-roster page of its own** (axis 1's "per-conductor sections"):
  folded into the board as the collapsed "All doors" section, generated from
  the dispatcher registry — no second roster copy anywhere.

### Post-merge, once (operational notes)

1. If the first `brain_board.yml` run fails at configure-pages ("Resource not
   accessible by integration" — the Hands hit this), create the site once:
   `gh api -X POST repos/PyAutoLabs/PyAutoBrain/pages -f build_type=workflow`,
   then re-dispatch.
2. Retire the muscle-memory: mornings are `bash PyAutoBrain/bin/morning.sh`
   in a terminal + the board, not `/wake_up`.
3. Candidate follow-ups to file via `/intake` if wanted: umbrella-router card
   for the Brain badge; `overnight_status.sh`/`version_drift.sh` reading the
   `board:` policy block instead of their own lists; devbox-published hygiene
   metrics on the board.
