# Cortex phase 1 — the schema and the repo skeleton

Type: feature
Target: pyautocortex
Repos:
- PyAutoCortex
- PyAutoMind
Themes:
- mind-workflow
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `python3 scripts/cortex.py check` exits 0 on a skeleton holding one example project, one phase in every state, and two rulings (one superseding the other); `ledger_merge.py --check` classifies every file
Review-minutes: 25
Unattended: needs-slicing
Epic: cortex-birth
Phase: 1
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01
Issued: 2026-09-01

Phase 1 of 7 in the PyAutoCortex birth epic. **Gate: phase 0** (the repo must
exist). Gates phases 2 and 3.

This is the phase that decides what the Cortex *is*. Everything the human ruled
on 2026-09-01 (epic ledger, "The decision") is fixed input here; the work is
turning it into files, schemas and one lifecycle script. It is a design-heavy
prompt and may need slicing at plan time — the natural seam is (a) schemas +
docs, (b) `cortex.py` + ledger-merge.

## Context

The Cortex is a run-and-ruling registry, not a prompt lifecycle. The unit is a
**phase** of a **project**, which spawns **runs** (SLURM job ids) and ends in a
**ruling**. Three science projects exist today with three ledger formats
(`autolens_profiling` PROGRAMME/DECISIONS/RESULTS; `subhalo_validation`
state.md + journal + results_summary; euclid — none yet) and three `hpc/sync`
CLIs. The schema must be able to describe all three without changing them.

The Mind's conventions to keep where they fit: a light, human-writable header
(no YAML frontmatter); ledger dirs that auto-merge (`ledger_merge.py`
default-deny classifier); `never_rewrite_history.md`; the session-start hook
propagated from Mind's `policy/session_start_hook.sh`; markdown a human edits by
hand as the source of truth for registries.

## Task

1. **`projects.yaml` — the science body map.** One row per project: `name`,
   `remote` (may be `none`), `local_path` (laptop, outside the workspace — this
   is a Cortex-only exception to the workspace-paths rule and must say so),
   `ral_root`, `mirror` (laptop pull root, may be `none`), `sync_cli` (path +
   which verbs it has), `ledger` (the project's own commentary ledger),
   `witness_file` (glob), `partition`, `status: active | dormant`. Seed rows
   are phase 3's job; here the schema plus one worked example.
2. **Phase files.** `phases/<project>/<slug>.md` with a header mirroring the
   Mind's shape: `Project:`, `Phase:` (distinct integers within a project),
   `State:` (`planned | gated | ready | submitted | running | pulled |
   awaiting-ruling | accepted | rerun | dropped`), `Gates:` (GitHub issue/PR
   refs only — `Repo#N` shorthand or URL, comma-separated; the same `GATE_REF_RE`
   grammar as `PyAutoMind/scripts/lifecycle.py:879-898`, and it clears only when
   every ref closes), `Witness:` (pre-registered, mandatory before `submitted`),
   `Budget:` (wall), `Runs:` (job ids, appended as they are submitted),
   `Lane: local-dev` (always; the field exists for the batch conductor's
   filter), `Review-minutes:`, `Epic:` (the shared slug — join key with Mind),
   `Filed:`. Body: Question / Witness / Where to look / Runs / Ruling ref.
   Quarantine: `legacy` and `legacy_wrong` are states of a **run**, recorded in
   the phase's Runs block, never of a phase.
3. **`rulings/` — the ledger of record.** `rulings/<YYYY>/<MM>/<id>.md`, id =
   `R-<YYYYMMDD>-<nn>`. Header: `Project:`, `Phase:`, `Runs:`, `Ruling:`
   (`accept | rerun | drop | leave-to-finish`), `Supersedes:` (optional ruling
   id), `Reviewed-at:`, `Review-minutes-actual:`, `Follow-ups:` (GitHub refs —
   the issue is created at filing, see epic). Body: the human's words verbatim,
   then evidence pointers. **Append-only; a wrong ruling is superseded by a new
   one, never edited.** State the rule in `rulings/AGENTS.md`: *a verdict
   recorded only outside the Cortex does not exist.*
4. **`batches/`.** `AGENTS.md`, `packets/`, `reviews/` — copy the Mind's
   record schema and change what differs: `review-at:` is per Cortex batch;
   the packet is a **rolling board** (members are added when `pulled`, nothing
   in `submitted`/`running` holds review control, `refreshed:` lines are the
   record of each pull); `delivered:` = `.err` clean + wall < budget + version
   stamp + `checkpoint.hdf5` sane; member line `<slug>: <phase path> — <runs>
   — <review-minutes> — <state>`. **One review vocabulary**: `accept | rerun |
   drop | leave-to-finish` — retire the Mind's `reviews/AGENTS.md:24` science
   line and `packets/TEMPLATE.md:64`'s longer list in favour of this (phase 4
   edits the Mind copies; here, the Cortex is authoritative). Lift the member
   block (Question · Witness · Health evidence · Readout · Ruling · Where to
   look · Est. review-minutes) from `PyAutoMind/batches/packets/TEMPLATE.md`.
5. **`scripts/cortex.py`** — one script, stdlib only: `check` (every phase file
   parses, states legal, every `submitted+` phase has a witness, every ruling id
   unique and every `Supersedes:` resolves, every project in a phase path is in
   `projects.yaml`), `gates` (offline: list open gates; `--grade` polls GitHub
   via `gh` and reports which `gated` phases are now `ready` — advisory here,
   the daily flip is phase 2's workflow), `rule` (append a ruling from a body
   file, assign the id, update the phase's `State:` and ruling ref), `move`
   (state transitions with the legal-transition table enforced).
6. **`scripts/ledger_merge.py`** adapted from the Mind's: ledger dirs
   `phases/ rulings/ batches/`, ledger files `projects.yaml`, `epics.md`.
   `policy/never_rewrite_history.md` copied; `policy/session_start_hook.sh`
   pulled in by the Mind's `session_hook_propagate.yml` (add the Cortex to its
   fan-out list — a Mind PR).
7. **`epics.md`** — same schema as the Mind's, plus `- mind-half:` linking the
   Mind entry by slug; the Mind's entries gain the reciprocal `- cortex-half:`
   in phase 4.
8. **`AGENTS.md`, `CLAUDE.md`, `README.md`, `REFERENCE.md`** — the organ's
   own docs in the Mind's register. `AGENTS.md` carries the laptop-lane closures
   verbatim from `PyAutoMind/draft/research/euclid/batch_science_lane.md`
   ("What is now out of scope, and why") so nobody re-derives them.

## Acceptance

- The witness above.
- A dated `docs/schema_decisions.md` recording every choice made here that the
  epic ledger did not already fix (id format, transition table, what a run vs
  a phase is), so phase 2's conductor reads decisions rather than guessing.
- PRs: PyAutoCortex (skeleton), PyAutoMind (hook fan-out only).

## Out of scope

- Seeding real projects (phase 3) and migrating real phases/rulings (phase 4).
- Any Brain code (phase 2). The `gates --grade` verb here is a hand tool; the
  scheduled grading lives in phase 2.
- A GitHub Pages site — phase 2 builds the renderer; do not hand-write HTML.
