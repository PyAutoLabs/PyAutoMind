# Profiling organ phase 0 — name the organ, register its row, write its boundaries

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
- pyautolabs.github.io
Themes:
- profiling
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check` green (hub-blurb leg aside) with the new organ row; every generated `repos_sync:map` block and organ table names the organ; `config/policy.yaml` `boards:` lists it; Brain/Heart/Hands pytest green
Review-minutes: 15
Unattended: never
Filed: 2026-10-02
Issued: 2026-10-02
Epic: profiling-organ-birth
Phase: 0

Phase 0 of the `profiling-organ-birth` epic. **Human-gated**: the `gh repo create`, and the `.github` org-profile row are human acts. Gates
phases 2 and 3 (the organ skeleton needs the repo; the cockpit transition
needs the organ identity). Phase 1 (the project-side summary contract in
`autolens_profiling`) does **not** wait on this phase.

## Request (verbatim)

> Yesterday we filed an intake about building a pyauto organ (name tbh) which
> is the dahsboard layer above the _profiling repos. Can we begin that work

## Context

The architecture is decided and recorded; this phase executes it, it does not
re-derive it:

- `PyAutoBrain/docs/research/ecosystem_levels.md` (Brain #440) — library /
  project / organ as responsibility roles, not a containment hierarchy.
- `PyAutoBrain/docs/research/profiling_inference_organs.md` (Brain #444) —
  the profiling organ's read contract: an instance registry, a versioned
  `profiling-summary` domain contract produced by each `*_profiling` project,
  a cross-project dashboard, and a cockpit feed. The organ validates the
  exchange contract; the project validates domain semantics. It never moves
  pins, combines unmatched timings, applies the compile threshold to runtime,
  computes an ecosystem-wide speed score or issues a Heart verdict.
- `complete/2026/09/pyautoeyes-organ-decision.md` + `pyautoeyes-birth-organ-row.md`
  — the precedent: Eyes is the cross-project dashboard over the
  `<lib>_visualization` project repos. The profiling organ is the same
  layering over the `<lib>_profiling` project repos.

**Growth rule** (`PyAutoBrain/ORGANISM.md` "Growth rule"): the organ earns its
repo by owning state no organ holds today — the **profiling instance
registry** (which projects publish a summary, where, under which contract
version), the **profiling-summary read contract**, the **ingest receipts**
(resolved commit per project per render) and the **cross-project board**.
The Brain's profiling conductor stays where it is and remains the only judge
(`triage`); `autolens_profiling` keeps its producers, results, drift policy
and its own Pages dashboard. A dashboard alone does not make an organ; the
cross-project registry and contract do (spec, "Decision").

**Today there is one real producer** (`autolens_profiling`). The spec is
explicit: do not manufacture empty `<lib>_profiling` siblings to satisfy the
"second adopter" milestone; a fixture tests the reader early, a real second
project is phase 4 when one exists.

## Human decisions this phase needs (answer on the issue)

1. **The organ's name — DECIDED 2026-10-02: `PyAutoPulse`, organ key `pulse`**
   (human, verbatim: "lets go with PyAutoPulse"). The pulse is a rate read
   over time, which is what the run-time-over-release board shows. The
   cockpit key is `pulse`, not the legacy wire label `profiling` that
   `autolens_profiling/dashboard/state.json` emits today (spec, "Two
   interfaces": that label is not proof the project is an organ). History
   note from the human: a `PyAutoPulse` repo existed once and was renamed to
   `PyAutoHeart`; the name is free again and the new repo is a fresh create.
   Candidates not chosen: PyAutoMuscle, PyAutoReflex, PyAutoMetabolism.
2. **Fresh repo, not a rename.** Unlike Eyes, nothing is promoted: the project
   repo stays a project. Human runs `gh repo create PyAutoLabs/PyAutoPulse --public`
   (the public-surface guard denies it to the agent).
3. **Canonical organ order.** The human ruled 2026-09-25 that organs read Brain,
   Mind, Cortex, Memory, Eyes, Heart, Hands, Nerves, Gut. Where does the new
   organ sit? Default proposal: after Eyes (both are perception/dashboard
   organs), before Heart.

## Task (phase 0)

One task worktree, PRs in the Cortex order **Mind → Brain → Heart → Hands → hub**:

1. **PyAutoMind**: `repos.yaml` organ row (`path: organs/PyAutoPulse`, `github:
   PyAutoLabs/PyAutoPulse`, `category: organ`, `organ: pulse`, `role`, `public_role`
   — role text from the spec's "Decision" and "Ownership" sections, modelled on
   the Eyes row); `ORGANS` frozenset in `scripts/repos_sync.py` (~line 141);
   `policy/session_start_hook.sh` dir chains (~lines 134–140); `ROUTING.md`;
   `epics.md` `profiling-organ-birth` notes (name chosen, ledger repointed to
   `PyAutoPulse/dashboard.md` once phase 2 lands); decision record
   `complete/2026/10/pyautopulse-organ-decision.md` (what state the organ owns,
   boundaries against the profiling conductor, the project repos, Heart and
   Mind — modelled on `pyautoeyes-organ-decision.md`); then
   `python3 scripts/repos_sync.py --write` (map blocks, organ tables, hooks).
2. **PyAutoBrain**: `SIBLING_ORGANS` (`agents/_pyauto_root.py` ~line 60 and
   `bin/_pyauto_root.sh`); `ORGANISM.md` organ-table row + boundary prose +
   growth-rule paragraph (the fourth capability to earn an organ, after Gut,
   Cortex, Eyes); `docs/concepts/organism.md`; new `docs/organs/pyautopulse.md` +
   toctree; `README.md` organ count; `organs/AGENTS.md` routing row;
   `config/policy.yaml` `boards:` family entry (so `board/_board.py` derives
   its Pages URL — no card yet, that is phase 3); profiling conductor prose
   (`agents/conductors/profiling/AGENTS.md`, `skills/profiling/profiling.md`):
   one paragraph naming the organ as where the cross-project view lives and
   the conductor as the judge. `tests/test_policy_seams.py` `WITNESS_EXEMPT`
   until phase 2 tests land.
3. **PyAutoHeart**: `_SIBLING_ORGANS` (`heart/_workspace.py`, `heart/_workspace.sh`),
   `config/repos.yaml` organism list entry.
4. **PyAutoHands**: `_SIBLING_ORGANS` (`autohands/_workspace.py`).
5. **pyautolabs.github.io** `index.html` blurb; **PyAutoScientist** README
   table (generated); **.github** profile row (human).

Local: clone the fresh empty repo at `organs/PyAutoPulse` with the standard organ
stubs (`AGENTS.md` with repos_sync markers, `CLAUDE.md` → `@AGENTS.md`,
`README.md`, LICENSE). Content arrives in phase 2.

## Out of scope

The registry, reader, dashboard and workflows (phase 2); the Brain board card
and the cockpit transition (phase 3); any change inside `autolens_profiling`
(phase 1); the inference organ (its own epic, not started).

## Ship policy

Supervised: present the plan, open the issue, end at PR-open; merge is human
(`/prm`). If Heart is RED for reasons touching none of these repos, ship only
under a contemporaneous human RED override recorded in the four sinks.
