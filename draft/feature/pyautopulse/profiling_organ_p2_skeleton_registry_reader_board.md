# Profiling organ phase 2 — the organ skeleton: registry, reader, board, workflows

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoPulse
- PyAutoBrain
Themes:
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `bin/pyauto-pulse check` prints `check: OK` against the lens registry row (summary resolves at one commit, validates, receipt written); hermetic pytest green over the acceptance cases; `bin/pyauto-pulse board` writes `dashboard.md/.html` + `state.json` (validated by `PyAutoBrain/board/_state.py`) with one `autolens_profiling` row linking to its Pages page; lint/pages/refresh workflows green
Review-minutes: 20
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Phase: 2

Blocked on: phase 0 shipped (the repo exists and is named) and phase 1 shipped (the `profiling-summary` v1 file it reads is published).

Phase 2 of the `profiling-organ-birth` epic. Human decision 2026-10-02: the
organ is **PyAutoPulse** (organ key `pulse`); the repo is created in phase 0. Modelled on the Eyes skeleton
(`complete/2026/09/eyes-organ-skeleton.md`, PyAutoEyes#2): the organ reads,
validates and links; it renders no measurement, judges nothing and copies no
result trees.

## Task

1. **`registry.yaml`** — version + one row per instance, fields per the spec
   ("Proposed project registry"): `instance: lens`, `repo: autolens_profiling`
   (a Mind body-map identity — location and GitHub come from `repos.yaml`, no
   second catalogue), `summary_path: dashboard/summary.json`,
   `supported_schema: profiling-summary@1`, `dashboard_url`, `library_refs:
   [PyAutoLens, PyAutoGalaxy, PyAutoArray, PyAutoFit]`, `cortex_project` when
   one exists. Lens row only.
2. **Reader** (`<pkg>/registry.py`, `<pkg>/summary.py`, `<pkg>/ingest.py`;
   PyYAML + stdlib, no scientific imports): resolve the instance's branch to
   **one commit**, read `summary_path` at that commit (raw GitHub URL at the
   SHA), validate the exchange contract (known schema/version, required
   fields, unique ids, finite numerics, dates, safe evidence paths), and write
   a **receipt** (`receipts/<instance>.json`: resolved commit, fetch time,
   outcome, error). Unsupported version / invalid feed → the instance is
   reported failed and the last good snapshot is kept, labelled **cached** with
   its original evidence time and the new fetch error (never re-aged by a
   render). A local `--path` read reports checkout revision + dirty state and
   is labelled as such.
3. **Board** (`<pkg>/board.py` → `dashboard.md`, `dashboard.html`,
   `state.json`): one row per registered project with scope, evidence time,
   last fetch, coverage, status and links; a detail section per instance
   showing the producer's own `comparisons[]` (drift candidates with their
   provenance and the `/profiling triage …` prompt as a manual-handoff
   action descriptor) and `limitations[]`. Keep the three notions separate on
   the page: transport/schema integrity, evidence freshness (`valid_until`
   missing → "freshness policy unspecified", shown with the age), scientific
   qualification. A valid empty feed reads "no measurements". No league table
   across cells; no recomputed ratio; no Heart verdict. `state.json` is the
   organ's own cockpit feed (`organ: pulse`, `repo: PyAutoPulse`), status summarising
   the organ's monitoring scope only.
4. **`bin/pyauto-pulse`** dispatcher (Heart/Eyes pattern): `check`, `board`,
   `census`, `fetch [--instance K]`.
5. **Tests** (hermetic, fixtures under `tests/fixtures/`): the spec's acceptance
   cases that belong to the reader — valid empty producer; one project
   unavailable (cached snapshot + error shown); unsupported schema; duplicate
   record id; stale cached snapshot keeps its evidence time; unknown
   provenance; compile/runtime axis mismatch refused; changed hardware shown
   as a separate group, never merged. Plus a **second-producer fixture** with
   a different cell grammar behind the same contract, proving the reader has
   no project-specific branching (a fixture, not a manufactured repo).
6. **Workflows**: `lint.yml` (ruff + pytest + `check`), `pages_dashboard.yml`
   (publish `dashboard.html` as index with `state.json` beside it, validated by
   `PyAutoBrain/board/_state.py`), `dashboard_refresh.yml` (push to main, PR,
   nightly, `repository_dispatch` from `autolens_profiling`'s
   `pages_dashboard.yml` — the Eyes/Cortex pattern; the sender side is a
   one-line follow-up in the project repo, filed separately), shared
   `concurrency` group for the main-writers.
7. **Prose**: `AGENTS.md` (organ boundaries, the growth-rule state it owns, the
   "never" list from the spec's "Profiling domain contract"), `REFERENCE.md`
   (registry schema, the `profiling-summary` v1 contract as the organ reads it,
   receipt format), `README.md`. Brain: `config/policy.yaml` `test_witness`
   row for the new repo (as Brain#428 did for Eyes).

## Out of scope

The Brain board card and the cockpit identity transition (phase 3); any change
to `autolens_profiling` beyond the dispatch sender follow-up; a second real
producer (phase 4); the inference organ.

## Ship policy

Supervised: plan on the issue, end at PR-open, merge human (`/prm`). Human
enables GitHub Pages (source: GitHub Actions) on the new repo — the first
Pages run fails until then, as PyAutoEyes#2 did.
