- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/380 (closed completed 2026-09-01)
- completed: 2026-09-01
- library-pr: PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/330 (`4f3e498` + `e8f29af`, merge `fcfb918`) → PyAutoCortex
  https://github.com/PyAutoLabs/PyAutoCortex/pull/2 (`ba582db`, merge `7bb1703`) → PyAutoMind
  https://github.com/PyAutoLabs/PyAutoMind/pull/381 (`df2b570`, merge `3272fde`), merged in that order — the
  renderer contract: both dashboard workflows render against Brain `main`, so the Brain PR had to land first.
- classification: feature (pyautobrain) — epic `cortex-birth`, phase 2 of 7. Gate: phase 1 (SHIPPED #379).
  Gates phases 4 and 5.
- summary: the phase that gives the Cortex a **view and a driver**. Shipped in PyAutoBrain: a new conductor
  `agents/conductors/cortex/` (`AGENTS.md`, `cortex.sh`, `_cortex.py`, ~1930 lines) registered in
  `bin/pyauto-brain`, with five verbs — `census`; `dashboard --check|--apply` (a stdlib Markdown+HTML renderer:
  Awaiting ruling → Running/submitted → Ready → Gated → Recent rulings → Epics → Projects, plus the counts table
  the Brain board reads, titles and keys parametrised so no Mind literal survives); `plan` (laptop-slot
  admission: `State: ready` + witness + budget + `local-dev`, greedy by review-minutes against `--budget`, a
  cloud session reports the ready count and plans nothing, no autonomy cap consulted, the launch payload
  carries no decision); `gates --grade [--apply]` (a thin wrapper over the Cortex script's `gates_report`, so
  the daily grading job needs no Brain checkout); and `collect` (six scoring legs — `err`, `wall`, `version`,
  `checkpoint`, `resume`, `witness` — each PASS / FAIL / UNOBSERVABLE, aggregated to HEALTH = FAILED / SUSPECT /
  HEALTHY, emitting the packet member block and moving `running → pulled → awaiting-ruling`; `--pull` is opt-in
  and runs the project's own sync CLI; `--apply` is rehearsed on a temp copy and re-checked after writing; a
  `<hash>.zip` outranks a stale extracted run dir). Plus the Mind badge in `agents/conductors/intake/_intake.py`
  (probes `PYAUTO_CORTEX` / a sibling `PyAutoCortex`, badges in-flight prompts whose issue a Cortex `Gates:`
  names — render-only, no new imports, silent when absent), the board family (`config/policy.yaml`
  `cortex: PyAutoCortex`, theme palette at 6.96:1 / 8.14:1 contrast + mark, `collect_cortex()` Resume strip),
  `skills/cortex/`, the COMMANDS row and regenerated command surface, `resolve_cortex`, a `_pyauto_is_root`
  drift fix, and a third checkout (PyAutoCortex) in `tests.yml`. Shipped in PyAutoCortex: `dashboard_refresh.yml`
  (a mirror of the Mind's — Brain checkout, exit-code contract, PR errors / push+cron+dispatch self-heal, both
  Pages redispatch sites), `pages_dashboard.yml` (index = `dashboard.html`, packets under `/packets/`), and
  **`gates_grade.yml`** — the one scheduled job that mutates state: daily `cortex.py gates --grade --write`,
  commits the flips, redispatches the check and the refresh, and reddens on an unreadable ref *after* committing
  what flipped; every main-writer shares the `cortex-main-writers` concurrency group. Also the ledger carve-out,
  the first rendered `dashboard.md` + `dashboard.html` (empty registry), "Driving the Cortex" in
  `AGENTS.md`/`REFERENCE.md`, the README board link, and schema decisions 38–49. Shipped in PyAutoMind: the
  third checkout in `dashboard_refresh.yml` so the badge renders on Pages.
- witness (all four legs of the prompt's `Witness:`, re-run from the canonical checkouts after merge):
  `_cortex.py dashboard --cortex PyAutoCortex --check` → `dashboard.md + dashboard.html are current`;
  `PyAutoCortex/scripts/cortex.py check` → `cortex check: OK`; the Cortex Pages site live at
  https://pyautolabs.github.io/PyAutoCortex/ (HTTP 200, rendering every state and the rulings);
  `pyauto-brain board` shows the phase-0 family row populated —
  `Cortex: awaiting ruling 0 · running / submitted 0 · ready 0 · gated 0 · recent rulings 0`;
  `repos_sync.py --check` → 15 legs OK. Tests: PyAutoBrain **741 passed** (`Brain Tests` py3.12 + py3.13 green
  *with* the new PyAutoCortex checkout; `Docs` `docs-build` green), PyAutoCortex **127 passed** (`Cortex Check`
  green; `Dashboard Refresh` PR-mode `--check` against Brain `main` clean — the committed render is
  byte-identical to what the merged conductor produces), PyAutoMind `Spawn Drift` `privacy` green (`drift`
  skipped on PRs by design; `Dashboard Refresh` and `Lifecycle Drift` are path-filtered and correctly did not
  fire on a workflow-only diff). The gate-grading leg is witnessed by `test_cortex_conductor.py` (one phase
  flips on a mocked closed ref); the live daily job has an empty registry to grade until phase 3.
  **The Mind badge has no live instance yet** — render-only, it fires on a Mind prompt whose issue a Cortex
  `Gates:` names, and the live registry is still empty (`projects.yaml` rows are phase 3, real phases phase 4).
- heart: readiness YELLOW (score 80) acknowledged by the human's `/prm` — `! PyAutoArray: open PR 9d old`;
  `? release validation incomplete: no rehearsal for current source`. Neither touches Brain, Cortex or Mind, and
  no library release is involved.
- decisions of note:
  - the conductor is **Mind-free and stdlib-only** (an AST test pins the import set); it imports the Cortex's own
    `scripts/cortex.py` at runtime rather than re-implementing the schema, so the schema has one owner.
  - the dashboard normaliser strips the generated comment **and** the `Last updated` banner, so a no-op night
    commits nothing — the Mind renderer's daily self-heal drift is deliberately not inherited.
  - **UNOBSERVABLE is a first-class verdict** in `collect`, not a silent pass: two of the six legs are
    laptop-invisible until phase 3's pull manifest exists, and saying so beats scoring them green.
  - the **pull manifest schema** (`.cortex/pull.json`) is specified here and written in phase 3.
  - spelling: `--apply` on the Brain conductor, `--write` on the Cortex script; the wrapper translates.
  - `gates_grade.yml` is **the only scheduled mutator**, and may only ever move `gated → ready`; every
    main-writer shares the `cortex-main-writers` concurrency group.
  - **doctrine under a ledger dir is code**: any `AGENTS.md` / `TEMPLATE.md` beneath `LEDGER_DIRS` classifies as
    code so a `claude/**` branch cannot auto-merge a doctrine edit; the **dashboards stay ledger** so the
    self-heal commit auto-merges. (The Mind has the same trait and keeps it — its call, not this phase's.)
  - Brain tests now **depend on a PyAutoCortex checkout** (the fixture that IS the schema's witness); the tests
    skip cleanly when it is absent, so a local run without it still passes.
  - the rendered page's "home" link is derived from the repo's own README/AGENTS links, so a CI render and a
    laptop render are byte-identical.
- exploration corrections (things the 2026-09-01 audit had wrong, checked in this phase):
  - `agents/_pyauto_root.py` does **not** enforce an outside-path ban — the tenant firewall is the gate. The
    prompt's "one documented exception" for `projects.yaml` `local_path` rows was therefore not needed as an
    exception; the resolver is simply Cortex-scoped.
  - `agents/faculties/sizing/_sizing.py` **hard-fails without a Mind checkout** (it reads the body map at
    import), which is why `tests.yml` checks PyAutoMind out — the failure is at collection, not at test time.
  - the **Mind's** `dashboard --check` drifts daily by construction: `_intake._dashboard_body` does not strip the
    `Last updated` line, so the render differs every day even when nothing changed — 348 self-heal commits in
    the last 30 days. The Cortex renderer strips it; the Mind's fix is a follow-up worth filing.
- follow-ups found, NOT filed (for the human):
  - `_intake._dashboard_body` should strip the `Last updated` line the way the Cortex normaliser does, killing
    the Mind's daily self-heal commit (348 in 30 days).
  - `skills/prm` is over the 200-line skill cap — pre-existing, flagged by `check_skill_line_counts.sh`, not
    this phase's to fix.
  - `gh_json` is duplicated in the board and community conductors.
  - `PAT_PYAUTOLABS` needs **admin on PyAutoCortex**: `repo_settings.yml -f mode=apply` was dispatched for the
    phase-1 follow-up and failed —
    `##[warning]PyAutoLabs/PyAutoCortex — PATCH refused; the PAT needs admin on this repo`. The org enumeration
    *does* see the new repo; only the permission is missing. `delete_branch_on_merge` was set by hand (now
    `true`) and the stale merged `feature/cortex-schema-skeleton` from #379 was deleted by hand; without the PAT
    fix the next sweep will keep reddening on it. (Its other two warnings — `Jammy2211/euclid_assistant`,
    `Jammy2211/admin_jammy` — are pre-existing and unrelated.)
  - Pages needed one manual enablement (`gh api -X POST repos/PyAutoLabs/PyAutoCortex/pages -f
    build_type=workflow`) because `actions/configure-pages` cannot create a site with the default token:
    `Create Pages site failed. Error: Resource not accessible by integration`. Done once; the re-dispatched run
    succeeded and no future run needs it.
- epic: `cortex-birth` phases 0–2 SHIPPED; next is phase 3
  `draft/feature/pyautocortex/cortex_project_remotes_and_registration.md` (private project remotes +
  `projects.yaml` rows, laptop lane). Phase 4 gates on 2 **and** 3; phase 5 gates on 2 **and** the
  two-slot-batching `collect` verb.

## Original prompt

# Cortex phase 2 — the Brain conductor, the dashboard, gate grading and the Mind badge

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
- PyAutoMind
Themes:
- dashboard
- mind-workflow
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `pyauto-brain cortex dashboard --check` is clean on the phase-1 skeleton; the Cortex Pages site renders every state and the rulings; the gate workflow flips a `gated` phase whose refs are closed to `ready` in one scheduled run; the Mind dashboard shows a "gates a Cortex phase" badge on a dev prompt named in a Cortex `Gates:`
Review-minutes: 25
Unattended: needs-slicing
Epic: cortex-birth
Phase: 2
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01
Issued: 2026-09-01

Phase 2 of 7 in the PyAutoCortex birth epic. **Gate: phase 1.** Gates phases 4
and 5. **Renderer contract: the Brain PR merges BEFORE the Cortex and Mind PRs**
— both dashboard workflows check out Brain `main`.

Natural slices if plan time says so: (a) conductor + render + workflows,
(b) gate grading, (c) admission + collect scoring, (d) the Mind badge.

## Context

The Brain renders the Mind through the intake conductor
(`agents/conductors/intake/_intake.py`, `census` → `dashboard --check/--apply`),
regenerated by `PyAutoMind/.github/workflows/dashboard_refresh.yml` (checks out
`PyAutoLabs/PyAutoBrain`, self-heals `main`, then explicitly redispatches
`pages_dashboard.yml` because token pushes fire no events). The Cortex gets the
same shape with its own conductor. The nearest existing science-shaped code is
`agents/conductors/profiling/_profiling.py`: Mind-free, read-only, emits
decisions, never submits — the Cortex conductor is that, plus a renderer.

Known traps from the 2026-09-01 audit, all to be handled here rather than
worked around:

- `agents/faculties/sizing/_sizing.py:92` hardcodes the Mind body map at
  import; `agents/_pyauto_root.py:2-26` forbids absolute paths outside the
  workspace, and every science project lives at `/mnt/c/Users/Jammy/Science/`.
- `_sizing.py:934-937` caps `research`/`experiment` at `supervised`, so
  `batch plan` rejects every science run — Cortex members need their own
  admission rule, not that one.
- `registry_reconcile.yml:34` runs `lifecycle.py issues` without `--drafts`, so
  Mind gates are never auto-graded. The Cortex's grading must be the scheduled
  default, not opt-in.
- `_intake.py:918-945`: `Blocked-by:` never gates the Mind dashboard; the Mind
  badge here is render-only and must stay that way.

## Task

1. **`agents/conductors/cortex/`** registered in `bin/pyauto-brain`, with an
   `AGENTS.md` in the conductor register. Verbs: `census`, `dashboard
   --check | --apply`, `gates --grade`, `plan`, `collect`. Root resolution:
   `PYAUTO_CORTEX` → `<brain_parent>/PyAutoCortex` → `$PYAUTO_ROOT/PyAutoCortex`;
   do not extend `resolve_mind`. Project paths come from `projects.yaml`
   `local_path`, resolved through a Cortex-scoped helper that is the one
   documented exception to the outside-workspace rule (the exception is scoped
   to rows of `projects.yaml`, nothing else).
2. **Dashboard renderer** (stdlib, like `_intake.py:1657-1659` requires):
   sections *Awaiting ruling* (pulled, ordered failures → rulings-required →
   clean) → *Running / submitted* (live progress: job ids, budget vs elapsed
   from the batch record's `refreshed:` lines) → *Ready* → *Gated* (with the
   open refs and a 📋 chip) → *Recent rulings* → *Epics* (each card links its
   Mind half) → *Projects* (the where-to-look table straight from
   `projects.yaml`). Titles/keys parametrised — no Mind literals (`_intake.py`'s
   `:58, :744-746, :1631, :1988, :1997, :2294` are the pattern to avoid).
   Markdown + HTML, both with a "markdown version" link per section.
3. **Cortex workflows** (Cortex repo, Brain PR ships their text under
   `docs/organs/cortex/workflows/` for the Cortex PR to copy): `dashboard_refresh.yml`
   mirroring the Mind's including the self-heal and the explicit
   `pages_dashboard.yml` redispatch; `pages_dashboard.yml` publishing
   `dashboard.html` as index and `batches/packets/*.html`; `ledger_merge.yml`;
   **`gates_grade.yml` daily** running `cortex gates --grade --apply` (flips
   `gated → ready` and commits) — this is the one scheduled job that mutates
   state, and it may only ever move `gated → ready`.
4. **Admission rule** (`cortex plan`): a phase is plannable when `State: ready`,
   witness present, budget present, and lane is the session's (always
   `local-dev` — a cloud session reports the ready count and plans nothing,
   per the laptop-lane ruling). No autonomy cap is consulted; science members
   are `supervised` by definition and the ruling is the human's. Output: the
   proposed members with review-minutes against the slot budget, same shape as
   `batch plan`.
5. **Collect scoring** (`cortex collect`): for each `submitted`/`running`
   member, read the batch record's `refreshed:` lines and the pulled tree
   under `mirror`/`local_path`: `.err` size against the benign baseline, wall
   vs `Budget:`, version stamp in the result JSON, `checkpoint.hdf5` present
   and non-empty, no resume marker in `.out` (`Fit Already Completed` /
   `Resuming .* previous samples found`), the witness file present and scored
   against `Witness:`. Emits the packet member block
   (`PyAutoMind/batches/packets/TEMPLATE.md` member shape) and moves the phase
   `pulled → awaiting-ruling`. It **never** reads `sacct` state as health and
   never touches RAL — the pull is the human's `hpc/sync pull`, recorded as a
   `refreshed:` line.
6. **Mind badge** (`_intake.py`): when a Cortex checkout is beside the Mind (or
   `PYAUTO_CORTEX` resolves), read every Cortex phase's `Gates:`; any Mind
   prompt whose issue/PR matches gets a render-only "gates a Cortex phase →
   <phase>" badge. Absent Cortex → no badge, no error. Add the Cortex checkout
   to `PyAutoMind/.github/workflows/dashboard_refresh.yml` (Mind PR).
7. **Tests**: `tests/test_cortex_conductor.py` against the phase-1 skeleton
   fixture (every state renders; grading flips exactly one phase on a mocked
   closed ref; collect scores a fixture tree with one healthy and one
   resumed-run member; a cloud-lane session plans nothing and reports the
   count). `tests.yml` checks out PyAutoCortex beside PyAutoMind.

8. **Ledger carve-out (phase-1 follow-up, ruled in 2026-09-01).** In the
   Cortex's `scripts/ledger_merge.py`, prose that merely *lives under* a ledger
   dir is code: `rulings/AGENTS.md`, `batches/AGENTS.md`,
   `batches/packets/AGENTS.md`, `batches/packets/TEMPLATE.md`,
   `batches/reviews/AGENTS.md` (pattern: any `AGENTS.md` or `TEMPLATE.md`
   under `LEDGER_DIRS`) must classify as `code` so a `claude/**` branch cannot
   auto-merge doctrine edits. Test it; record it in `docs/schema_decisions.md`.
   The Mind has the same trait and keeps it — its call, not this phase's.
9. **Repo settings (phase-1 follow-up, ruled in 2026-09-01).** PyAutoCortex was
   born after the last `PyAutoBrain/.github/workflows/repo_settings.yml` sweep
   (org enumeration covers it; `delete_branch_on_merge=false` today, and the
   merged `feature/cortex-schema-skeleton` survived on the remote). Dispatch
   the sweep once (`gh workflow run repo_settings.yml`), confirm the setting
   flips and the stale remote branch is collected (or delete it by hand and
   say so), and add PyAutoCortex to whatever per-repo config the sweep reads
   if it is not purely org-enumerated.

## Acceptance

- The witness above; Brain tests green; `pyauto-brain board` shows the Cortex
  board family row from phase 0 populated (counts only — the strip is phase 6).
- PR order: PyAutoBrain → PyAutoCortex (workflows) → PyAutoMind (badge
  workflow checkout).

## Out of scope

- The batch conductor's second member kind and separate `review-at:` (phase 5)
  — `cortex plan`/`collect` here are standalone verbs the human runs in a
  laptop slot; phase 5 folds them into `batch`.
- Migrating any real phase or ruling (phase 4).
- Any dispatch. The conductor never submits.
