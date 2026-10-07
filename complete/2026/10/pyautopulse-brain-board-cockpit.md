## pyautopulse-brain-board-cockpit
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/450
- completed: 2026-10-02
- epic: profiling-organ-birth
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/451
- library-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/24
- summary: Phase 3 of `profiling-organ-birth`, NARROWED by the human 2026-10-02 to the organ → Brain board interface: `collect_pulse()` strip on the Brain board (head counts of `PyAutoPulse/dashboard.md`, composed like Cortex/Eyes, display-only), mirrored test, board AGENTS line, profiling conductor + skill prose (Pulse board = where cross-project drift candidates are read; `autolens_profiling` owns semantics; `/profiling triage <comparison_key>` names a Pulse row — the `triage` verb takes no target), `docs/organs/pulse.md` state/cockpit paragraph; hub cockpit Pulse card after Hands fed from `PyAutoPulse/state.json`. Brain full pytest 1142 passed. Hub has no CI; human approved the merge. Supersedes `draft/feature/pyautobrain/register_profiling_dashboard_on_brain_board.md` (never shipped; the Brain never consumed the project feed, so no source transition was needed) — retired with this record.
- deviations: autolens_profiling `build_state()` identity change split to `draft/feature/autolens_profiling/cockpit_feed_project_identity.md` (blocked on task evaluation-grid-cap-field's claim); hub README bullet added; no `sw.js` cache bump (caching unchanged).
- traps: the Brain tenant-firewall CI step rejects a real instance name (`autolens_profiling`) in a test fixture — organ tests must use neutral names (`alpha_profiling`), as the Eyes fixture does; fixed on the branch (54a8008) before merge.
- follow-ups: hub `index.html` link to the Pulse board (Eyes has one); autolens_profiling cockpit-feed identity (filed, blocked); `pulse-refresh` dispatch sender in autolens_profiling; `.github` org-profile Pulse row (human); phase 4 waits for a real second `_profiling` producer.

## Original prompt

# Profiling organ phase 3 — Brain board card and cockpit transition

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoBrain
- pyautolabs.github.io
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Consequence: judge
Witness: the Brain board (`board/_board.py`) renders one organ strip for the profiling organ beside Cortex/Eyes, reading the organ's `state.json`; the `autolens_profiling` project page stays reachable from it; `board/_state.py` validates both feeds; no duplicate card for the same scope; Brain pytest green
Review-minutes: 10
Unattended: ready
Filed: 2026-10-02
Issued: 2026-10-02
Epic: profiling-organ-birth
Phase: 3

Blocked on: phase 2 shipped (the organ's `state.json` exists and is published).

Phase 3 of the `profiling-organ-birth` epic — the **organ → Brain board**
interface. Human decision 2026-10-02: the organ is **PyAutoPulse** (organ key
`pulse`).

## Scope note (human, 2026-10-02)

Narrowed at issue time: PyAutoBrain + pyautolabs.github.io only. The `autolens_profiling`
`build_state()` identity change (task item 3) is split into
`draft/feature/autolens_profiling/cockpit_feed_project_identity.md`, blocked on task
`evaluation-grid-cap-field`'s claim of that repo; the Brain never consumed the project feed, so
there is no source transition to keep in lockstep. PyAutoPulse itself is untouched.

## Context

`autolens_profiling/dashboard/state.json` emits `organ: profiling` today, a
legacy wire label from before the organ existed. The spec (Brain #444, "Two
interfaces") says: keep the project page/feed working during transition; when
a real organ is registered, update the Brain board's **source and identity in
the same rollout step**, keep a clear link to the project page, and avoid
duplicate cards for the same scope. Do not silently repoint a feed before the
new consumer contract is tested — which is what phase 2's tests and this
phase's witness establish.

This phase **supersedes**
`draft/feature/pyautobrain/register_profiling_dashboard_on_brain_board.md`
(register the *project* feed on the Brain board) if that task has not shipped
first; if it has, this phase moves the card from the project feed to the
organ feed and retires nothing the project publishes.

## Task

1. **PyAutoBrain** `board/_board.py`: a `collect_pulse()` strip composed like
   `collect_eyes()` (the organ's renderer decides the numbers, the Brain board
   shows them), fed from the organ's `state.json`/board head; the `boards`
   family already lists the organ from phase 0. `board/_theme.py` ORGANS key
   and footer; `board/AGENTS.md` one line among the sibling boards. The strip
   links the organ board and, through it, the project page.
2. **Prompt wiring**: the organ's drift items carry the producer's
   `/profiling triage …` prompt as a `prompt`-kind action; confirm the
   profiling conductor's `triage` verb accepts that argument shape (read-only
   check, fix the prompt text in the organ if not).
3. **autolens_profiling** `build_dashboard.py` `build_state()`: once the organ
   strip is live, the project's own cockpit feed stops claiming
   `organ: profiling` — either `organ: autolens_profiling` as a project feed
   if `board/_state.py` admits project keys, or the project keeps `state.json`
   for its own Pages badge only and the Brain reads the organ. Decide on the
   issue from what `_state.py` and `_theme.py` actually accept; record the
   choice in the organ's `REFERENCE.md`.
4. **Profiling conductor prose**: `agents/conductors/profiling/AGENTS.md` and
   `skills/profiling/profiling.md` name the organ board as where drift
   candidates are read from, and `autolens_profiling` as where the measurement
   semantics live.

## Out of scope

Any new judgment in the Brain board (the organ displays, the conductor judges);
Heart readiness (the cockpit status is the organ's own monitoring scope, never
release readiness); the inference organ.

## Ship policy

Supervised: plan on the issue, end at PR-open, merge human (`/prm`). Brain
merges after the organ's `state.json` is published and validated.
