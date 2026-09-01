## cortex-schema-skeleton
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/379 (closed completed 2026-09-01)
- completed: 2026-09-01
- library-pr: PyAutoCortex https://github.com/PyAutoLabs/PyAutoCortex/pull/1 (`c24bf52b`, the repo's first PR, on top of birth commit `d38e88b`) → PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/329 (`4f02d4f0`), merged in that order
- classification: feature (pyautocortex) — epic `cortex-birth`, phase 1 of 7. Gate: phase 0
  (SHIPPED #377). Gates phases 2 and 3.
- summary: the phase that decides what the Cortex *is* as files — a run-and-ruling registry
  (project → phase → runs → rulings), not a second Mind. Shipped in PyAutoCortex:
  `AGENTS.md` / `README.md` / `REFERENCE.md` (phase header keys, the ten-state model and its
  transition table, run lines in SLURM notation `342091_[0-8,10]` with `pulled_to:` /
  `after:` / `resumes:` / `where:` continuation lines, ruling ids `R-YYYYMMDD-nn`, the one
  review vocabulary `accept | rerun | drop | leave-to-finish`, the laptop-lane closures
  quoted verbatim); `projects.yaml` (schema + worked example in a documented restricted
  YAML subset, stdlib-parsed with PyYAML parity tested; live map empty, rows are phase 3);
  `epics.md`; `rulings/AGENTS.md` ("a verdict recorded only outside the Cortex does not
  exist"; append-only, supersede never edit); `batches/AGENTS.md` + `packets/AGENTS.md` +
  `reviews/AGENTS.md` + `packets/TEMPLATE.md` (rolling board: members join when `pulled`,
  `refreshed:` lines record each pull); `docs/schema_decisions.md` (37 dated entries);
  `policy/never_rewrite_history.md` + `policy/remote_sessions.md` copies; two workflows
  (`cortex_check.yml` — check + pytest on push/PR; `ledger_merge.yml` — auto-merge of
  ledger-only `claude/**` branches with `cortex.py check` on the trial-merge tree);
  `scripts/cortex.py` (1613 lines: `check`, `gates [--grade [--write]]`, `rule`, `move`,
  `new`; injectable date and fetch) and `scripts/ledger_merge.py` (221 lines: the Mind's
  classifier with `phases/ rulings/ batches/` + `epics.md` as ledger, plus append-only
  enforcement under `rulings/**`); 123 tests over `tests/fixtures/skeleton` (ten phases, one
  per state; five rulings incl. a chain and a leave-to-finish; a batch record and review)
  and `tests/fixtures/empty`; the generated `CLAUDE.md`, `.claude/hooks/session-start.sh`
  and `.claude/settings.json` from `repos_sync.py --write`. Shipped in PyAutoBrain:
  `config/policy.yaml` gains the `test_witness` row `pyautocortex: PyAutoCortex/tests`;
  `tests/test_policy_seams.py` drops the phase-0 `WITNESS_EXEMPT` entry.
- witness: `python3 scripts/cortex.py check` → OK on `tests/fixtures/skeleton`,
  `tests/fixtures/empty` and the live tree; `python3 -m pytest tests -q` → 123 passed
  (`Cortex Check` green on the PR — one `pull_request` run; the `push` trigger is
  `main`-only, and `ledger_merge.yml` correctly did not fire on a `feature/**` branch);
  PyAutoBrain `tests/test_policy_seams.py` → 18 passed (`Brain Tests` py3.12 + py3.13
  green; `Docs` path-filtered out, nothing under `docs/` changed);
  `python3 PyAutoMind/scripts/repos_sync.py --check` → 15 legs OK.
- heart: readiness YELLOW (score 80) acknowledged by the human's `/prm` — PyAutoArray open
  PR 9d old; release validation incomplete (no rehearsal for current source). Neither
  touches PyAutoCortex or the Brain policy config.
- decisions of note (all dated in `docs/schema_decisions.md`): ten phase states with
  `legacy` / `legacy_wrong` as run-state quarantine, never a phase state; one ruling file
  per phase plus a `Batch:` header; rulings chain (`Supersedes:` one id), never tree;
  `accepted` superseded is not terminal; PR gates clear on merge only (closed-unmerged stays
  open; closed-not-planned issues are dead gates); the trial-merge `check` in
  `ledger_merge.yml` closes the ruling-id race between two branches; `projects.yaml` is
  code-not-ledger (like `repos.yaml`); the restricted YAML subset is stdlib-parsed with a
  PyYAML-parity test.
- spec extensions made in slice B (recorded, not silent): a `Reset:` header; `move pulled
  --pulled-to`; stricter `check` guards; extra optional flags; `rule --also` auto-supersedes
  on accepted phases; `gates --grade` exits 1 on an unreadable ref (fails closed).
- deviations from the prompt: `projects.yaml` is code not ledger; no PyAutoMind PR (the
  session-hook propagation already fans out to every body-map row, so the Cortex needed no
  fan-out edit); no `skills/`, so no `bin/install.sh` change.
- follow-ups found, NOT filed (for the human): `rulings/AGENTS.md` and `batches/**/AGENTS.md`
  are ledger-by-path, so a `claude/**` branch could auto-merge prose edits to them — decide
  in phase 2 whether to carve them out of the ledger classifier; `ledger_merge.py` reads
  stdin when not a TTY, so non-TTY callers need `</dev/null`; the transition table has no
  explicit `awaiting-ruling` re-pull row.
- epic: `cortex-birth` phase 1 SHIPPED; phase 2
  (`draft/feature/pyautocortex/cortex_conductor_and_dashboard.md`) is unblocked, and so is
  phase 3 (it gates on 1).
- session: claude-code-cli, Fable architect; two delegated Fable slices (A schemas / docs /
  fixtures, B `cortex.py` / `ledger_merge` / tests); close-out via `/prm` 2026-09-01.

## Original prompt

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
