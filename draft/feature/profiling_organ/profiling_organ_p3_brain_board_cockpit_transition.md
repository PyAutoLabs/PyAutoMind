# Profiling organ phase 3 — Brain board card and cockpit transition

Type: feature
Target: profiling_organ
Repos:
- PyAutoBrain
- autolens_profiling
- profiling_organ
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: the Brain board (`board/_board.py`) renders one organ strip for the profiling organ beside Cortex/Eyes, reading the organ's `state.json`; the `autolens_profiling` project page stays reachable from it; `board/_state.py` validates both feeds; no duplicate card for the same scope; Brain pytest green
Review-minutes: 10
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Phase: 3

Blocked on: phase 2 shipped (the organ's `state.json` exists and is published).

Phase 3 of the `profiling-organ-birth` epic — the **organ → Brain board**
interface. `profiling_organ` is the phase-0 placeholder target.

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

1. **PyAutoBrain** `board/_board.py`: a `collect_<key>()` strip composed like
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
