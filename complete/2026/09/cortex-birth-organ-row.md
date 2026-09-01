- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/377 (closed completed 2026-09-01)
- shipped: 2026-09-01 — seven PRs on `feature/cortex-birth-organ-row`, merged in this order:
  PyAutoMind https://github.com/PyAutoLabs/PyAutoMind/pull/378 (`d8734225`) →
  PyAutoGut https://github.com/PyAutoLabs/PyAutoGut/pull/5 (`29907c15`) →
  .github https://github.com/PyAutoLabs/.github/pull/8 (`eeb0b45c`) →
  PyAutoScientist https://github.com/PyAutoLabs/PyAutoScientist/pull/26 (`71024628`) →
  pyautolabs.github.io https://github.com/PyAutoLabs/pyautolabs.github.io/pull/6 (`e2fe7466`) →
  PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/328 (`3ea67da7`) →
  PyAutoNerves https://github.com/PyAutoLabs/PyAutoNerves/pull/158 (`026644df`).
- classification: feature (pyautocortex) — epic `cortex-birth`, phase 0 of 7. Human-gated:
  `PyAutoLabs/PyAutoCortex` was created by hand on github.com 2026-09-01 (public, empty,
  not cloned locally in phase 0).
- summary: the Cortex becomes an organ of record. `repos.yaml` gains the `category: organ`,
  `organ: Cortex` row ("where the organism learns what is true: the science body map
  (`projects.yaml`) and the rulings of record for every science run; the science mirror of
  the Mind — runs and rulings, not prompts and PRs"); `repos_sync.py --write` regenerated
  the organism map blocks (PyAutoBrain, PyAutoGut, PyAutoNerves `AGENTS.md`), the public
  organ tables (`.github` profile README, PyAutoScientist README) and the root routing
  table. `ORGANISM.md` carries the boundary prose — *the Mind decides what to build, the
  Brain routes the work and executes nothing, the Cortex learns what is true* — the
  science-mirror sentence beside Gut's storage-mirror one, the ruling-of-record rule ("a
  verdict recorded only outside the Cortex does not exist") and the growth rule naming the
  Cortex as the second organ to earn organ status. Brain also gains `docs/organs/cortex.md`
  (+ toctree, RTD organism summary), the README organ count, `SIBLING_ORGANS` in
  `agents/_pyauto_root.py`, and a `WITNESS_EXEMPT` entry in `tests/test_policy_seams.py`
  for the empty repo (phase 1 replaces it with a real witness). The hub blurb in
  `pyautolabs.github.io/index.html` names the Cortex. The human's organ ordering rule —
  **Brain, Mind, Cortex, Memory, Heart, Hands, Nerves, Gut** — is applied everywhere organs
  are listed (`repos.yaml`, `ORGANISM.md`, `policy.yaml`, `_theme.py`, `install.sh`,
  `SIBLING_ORGANS`, every regenerated block and table, the blurb) and ordinal prose
  ("the seventh organ") is dropped.
- witness: `python3 PyAutoMind/scripts/repos_sync.py --check` — 15 legs OK, exit 0.
  Tests: PyAutoBrain 691 passed (CI py3.12 + py3.13 + docs build green); PyAutoMind 307
  passed (`lifecycle_drift`, `dashboard_refresh`, `spawn_drift` privacy green; spawn
  `drift` job skipped by design on PRs); PyAutoNerves unittest 3.12 / 3.13 / nojax green.
  PyAutoGut, .github, PyAutoScientist and pyautolabs.github.io have no PR checks
  configured — merged `MERGEABLE/CLEAN` under the human's `/prm`.
- heart: readiness YELLOW (score 80, 20:52Z) acknowledged by the human's `/prm` —
  PyAutoArray open PR 9d old; release validation incomplete (no rehearsal for current
  source). Neither touches the seven doc/manifest repos shipped here.
- deviations (approved on #377): no `board/_theme.py` ORGANS palette / MARKS entry and no
  `config/policy.yaml` boards-family row — deferred to phase 2 with the board and a logo
  (Gut/Nerves precedent; a `boards:` key without a palette fails `test_board_theme`); no
  `bin/install.sh` Cortex organ-array entry — deferred to phase 1 with the skeleton;
  `dashboard.md` / `dashboard.html` dropped from the Mind PR because the boards footer
  renders from PyAutoBrain `main`'s `policy.yaml` (regenerated at this close-out from the
  merged Brain).
- follow-ups found, NOT filed (for the human): `PyAutoBrain/docs/concepts/organism.md`
  already lacked a Nerves row before this change; `spawn.py` offline generate flags the
  PyAutoMemory template's `.claude/hooks/session-start.sh` + `.claude/settings.json` as
  UNMATCHED (`MEMORY_RULES` has no `.claude/*` DROP — pre-existing); `PyAutoBrain/bin/install.sh:64`
  comment "a fork keeps the five organs" is stale; three stale `active.md` claims
  (`organ-board-github-link`, `silence-colab-cli-message`, plus any other merged-but-not-closed
  entry) await their own `/prm`.
- epic: `cortex-birth` phase 0 SHIPPED; phase 1 (`draft/feature/pyautocortex/cortex_schema_and_skeleton.md`)
  is unblocked — the skeleton now has a repo to land in.
- session: claude-code-cli, Fable architect; execution delegated to a Fable subagent at the
  human's direction; close-out via `/prm` 2026-09-01.

## Original prompt

# Cortex phase 0 — birth: the repo, the body-map row, the boundary prose

Type: feature
Target: pyautocortex
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoScientist
- pyautolabs.github.io
Themes:
- mind-workflow
- docs-hub
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check` exits 0 with a Cortex row; every organ's AGENTS.md map block lists PyAutoCortex; `pyautolabs.github.io` hub blurb check passes
Review-minutes: 15
Unattended: never
Epic: cortex-birth
Phase: 0
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01
Issued: 2026-09-01

Phase 0 of 7 in the PyAutoCortex birth epic. **Gates nothing external; gated by
nothing.** Gates phase 1 (the skeleton needs a repo to land in).

**The repo is created by the human.** Nothing in the organism creates PyAutoLabs
org repos (checked 2026-08-26: the only `gh repo create` calls make a visiting
scientist's own repo; `spawn.py` force-syncs into templates that already exist).
So the first act is a human one on github.com, and everything else in this phase
is the wiring that makes a repo an organ.

## Context

`PyAutoBrain/ORGANISM.md:63-72`: "A new organ costs an `AGENTS.md`, a
`CLAUDE.md` stub, install wiring, a body-map row and boundary prose — it must
earn that by owning state or effects no existing organ can." The Cortex earns
it by owning the science body map and the rulings ledger (epic ledger, "The
decision"). The mechanical consequences of a `category: organ` row are known:
`repos_sync.py:227-249` writes the system map into every organ's AGENTS.md
block, `:265-303` regenerates `.github/profile/README.md` and
`PyAutoScientist/README.md`, `:702-712` requires the name in
`pyautolabs.github.io/index.html`.

## Task

**Ordering rule (human, 2026-09-01):** wherever organs are listed, the order
is Brain, Mind, Cortex, Memory, Heart, Hands, Nerves, Gut.

1. **Human step, first:** create `PyAutoLabs/PyAutoCortex` on github.com
   (public — the Mind is public and the Cortex holds rulings, not data; the
   science *projects* it points at are the private ones). Default branch
   `main`, empty. Record the creation date in this prompt.
   Repo created: 2026-09-01 — https://github.com/PyAutoLabs/PyAutoCortex (public, empty; not cloned locally in phase 0)
2. `PyAutoMind/repos.yaml`: add the row — `category: organ`, `organ: Cortex`,
   role prose "The Cortex — where the organism learns what is true: the science
   body map (`projects.yaml`) and the rulings of record for every science run;
   the science mirror of the Mind (runs and rulings, not prompts and PRs)".
   Run `python3 scripts/repos_sync.py --write`; commit the regenerated
   AGENTS.md routing table and every organ's map block it touches.
3. `PyAutoBrain/ORGANISM.md`: the organ row (`:13-21`) and the boundary prose,
   verbatim from the epic ledger: *the Mind decides what to build, the Brain
   routes the work and executes nothing, the Cortex learns what is true.* Add
   the sibling sentence beside Gut's ("the storage mirror of Memory"): the
   Cortex is the science mirror of the Mind. State the ruling-of-record rule in
   one sentence.
4. `PyAutoBrain/docs/organs/cortex.md` beside the six existing organ pages —
   short, same register, linking the epic ledger.
5. **Deferred (approved deviation, PyAutoMind#377):** the `board/_theme.py`
   ORGANS palette + MARKS entry and the `config/policy.yaml` board-family row
   move to phase 2 (with the board itself), and the `bin/install.sh` organ
   arrays move to phase 1 (with the skeleton) — Gut and Nerves have none of
   these either, a board key without a palette fails `test_board_theme.py`,
   and a mark needs a logo. Phase 0 only applies the ordering rule above to
   the existing entries.
6. `pyautolabs.github.io/index.html` hub blurb so `check_hub_blurb` passes;
   `PyAutoScientist/README.md` is regenerated by step 2 — verify, do not hand-edit.
7. `PyAutoBrain/AGENTS.md` / `CLAUDE.md`: the one-line pointer the other organs
   have. Nothing else in Brain changes in this phase.

## Acceptance

- The witness above, plus: `pyauto-brain board` renders without a KeyError on
  the new organ key; the Cortex repo contains only what step 1 created (the
  skeleton is phase 1 — do not pre-empt it here).
- PRs: PyAutoMind (body map + regenerated maps), PyAutoBrain (ORGANISM, docs,
  theme, policy, install), pyautolabs.github.io (blurb). PyAutoScientist only
  if `repos_sync` touched it.

## Out of scope

- Any file in the Cortex repo beyond GitHub's own initial state (phase 1).
- The Brain conductor and Cortex dashboard (phase 2).
- A Cortex template / `spawn.py` rule (deferred, epic ledger).
