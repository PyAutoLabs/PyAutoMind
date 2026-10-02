## profiling-summary-v1
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/359
- completed: 2026-10-02
- epic: profiling-organ-birth (phase 1)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/360
- head: b93db793d7ac4f85d17b38b63924346c101f7215
- merge: 4d6523f6ca56f6921d225596307007b71bb16bc2
- summary: PyAutoPulse phase 1 — `build_dashboard.py` gains a fourth output, `dashboard/summary.json`, the `profiling-summary` v1 project→organ read contract (envelope with schema/version, project/scope, generated_at, evidence_updated_at, valid_until null, producer_revision, comparison_policy, coverage {expected, observed, excluded}; one record per plotted point with a stable `<series key>@<version>` id; one comparison per series carrying the producer's own drift badge with a `qualified` flag and reasons; explicit limitations). `validate_summary()` refuses unknown schema/version, missing fields, duplicate ids, non-finite numbers, bad dates and unsafe evidence paths before anything is written; a valid empty feed is "no measurements". `series.json`, `state.json` and `index.html` are byte-identical (the summary is written with the committed render stamp; `--check` reuses the committed `producer_revision`). `pages_dashboard.yml` publishes the file beside `series.json`; `dashboard/README.md` documents the grammar; `AGENTS.md` names the folder. First render: 145 series, 159 records, 4 releases, 6 excluded rows.
- verification: local — ruff clean, 14 dashboard tests (7 existing + 7 new), `build_dashboard.py --check` current, `check_results_layout.py --check` / `build_readme.py --check` unchanged, `PyAutoBrain/board/_state.py dashboard/state.json` ok, tooling pure stdlib. CI — lint run 36982602027 attempt 2 SUCCESS on the exact head; attempt 1 failed only on lychee 504 Gateway Timeouts from github.com for eight links in the untouched top-level README (log quoted in session; re-run requested by the human). Merge state clean; `/prm` merged; head proven ancestor of `origin/main`, 0 ahead.
- heart: GREY at the door and at ship (Pages host blocked in the remote container); no readiness verdict consulted; no RED override used. Project repo only — no library change, nothing pending release.
- design-authority: `PyAutoBrain/docs/research/profiling_inference_organs.md` (Brain #444) on `ecosystem_levels.md` (Brain #440); the cockpit `state.json` still says `organ: profiling` — the identity moves in phase 3, by design.
- traps: `producer_revision` is HEAD at render, never the hash of the commit that contains the file; `--check` must reuse the committed value or every commit reads STALE. `evidence_updated_at` is the newest release DATE encoded in a library version (result rows carry no measurement wall-clock) — the newest in the tree is 2026-08-17 even though 2026.9.27.1 releases exist elsewhere. A pre-#342 row's `host` can still be set (device.hostname fallback) while `has_provenance` is false.
- next: phase 0 (`draft/feature/pyautomind/profiling_organ_p0_name_row_and_boundaries.md`, human `gh repo create PyAutoLabs/PyAutoPulse` first), then phase 2 (`draft/feature/pyautopulse/profiling_organ_p2_skeleton_registry_reader_board.md`, the reader against this file). Follow-up for the organ's refresh: a one-line `repository_dispatch` sender in this repo's `pages_dashboard.yml` once PyAutoPulse exists (phase 2 names it).
- session: Claude Code remote (web), https://claude.ai/code/session_01B5uEFSAb34aK5R6PTX7jJm; remote clone, no task worktree.

## Original prompt

# Profiling organ phase 1 — publish the `profiling-summary` v1 contract from autolens_profiling

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/359
Consequence: judge
Witness: `python scripts/misc/tooling/build_dashboard.py` also writes `dashboard/summary.json` (`schema: profiling-summary`, `version: 1`) and `--check` is idempotent on it; `pytest scripts/misc/test/test_build_dashboard.py` covers the envelope, the record grammar and every rejection case; `lint.yml` green; `series.json`, `state.json`, `index.html` and the drift badge byte-identical to before
Review-minutes: 12
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Phase: 1

Phase 1 of the `profiling-organ-birth` epic — the **project → organ**
interface. It does **not** wait on phase 0: the contract is defined by
`PyAutoBrain/docs/research/profiling_inference_organs.md` (Brain #444) and
the producer is this repo, whatever the organ ends up being called. Nothing
reads the file yet; phase 2 builds the reader against it.

## Request (verbatim)

> Yesterday we filed an intake about building a pyauto organ (name tbh) which
> is the dahsboard layer above the _profiling repos. Can we begin that work

## Context — what the producer already does

`scripts/misc/tooling/build_dashboard.py` (autolens_profiling#345, pure stdlib)
scans `results/{runtime,breakdown,simulators,lens}` and writes three files that
`pages_dashboard.yml` publishes:

- `dashboard/series.json` — `schema_version: 1`, `generated`, `reference_host`,
  `loadavg_cap`, `drift_ratio: 2.0`, `drift_floor_s: 0.001`, `series[]`
  (145 today; each `key / section / cell / config / sparse / points[] / drift`)
  and `refused[]` (6 today). A point carries `version, single_jit_s,
  vmap_per_call_s, host, backend, job, loadavg, has_provenance, source,
  qualified, reason`.
- `dashboard/state.json` — the organ cockpit feed (`board/state_schema.json`
  v1) with the legacy wire label `organ: profiling`. **Unchanged by this phase**
  (spec: "Do not silently repoint a feed before the new consumer contract is
  tested"; the identity moves in phase 3).
- `dashboard/index.html`.

The spec's rules for this interface: the summary is **generated by the project
from its own artifacts**, its path is **registered explicitly** by the organ
(no guessed conventional filename), it carries a small common **envelope** plus
domain **records**, and the organ reads it at one resolved commit. Series
semantics, qualification and the 2x / 1 ms drift policy stay here.

## Task

1. **Exporter.** In `build_dashboard.py` (or a sibling `build_summary.py` it
   calls — keep one scan), write `dashboard/summary.json` from the same
   `build_series()` output. Envelope fields per the spec ("Proposed summary
   envelope"), with the file's own grammar documented in `dashboard/README.md`:
   - `schema: "profiling-summary"`, `version: 1`
   - `project: "autolens_profiling"`, `scope: "release-runtime"` (what this
     feed covers: per-call run time per release across the four result sections)
   - `generated_at` (= the existing `generated` stamp, UTC Z),
     `evidence_updated_at` (latest `version` release date derivable from the
     included points, else `null` + `reason`), `valid_until: null` (no declared
     age policy — the organ must show "freshness policy unspecified", not invent
     a TTL), `producer_revision` (the git commit of this repo at render; `null`
     + reason when not a git checkout — never the hash of the commit that will
     contain the file)
   - `coverage`: expected cells where known (`SECTIONS` x the cells scanned),
     observed series/points/releases counts, `excluded` = the `refused[]` rows
     with their reasons
   - `records[]`: one per **point** with a stable id
     (`<series key>@<version>`), `axis: "runtime"`, `unit: "s"`, the
     measurement (`single_jit_s`, `vmap_per_call_s`), identity (`section,
     cell, config, sparse, backend, precision` parsed from the config,
     `version` as the measured library revision), provenance (`host, job,
     loadavg, has_provenance, qualified, reason`) and `evidence` (the
     repository-relative `source` path — the organ resolves it against the
     captured commit)
   - `comparisons[]`: the producer's drift verdicts — one per series with
     `comparison_key`, `policy: "runtime-drift-2x-1ms"`, `baseline` (from
     version), `candidate` (to version), `ratio`, `status`
     (`drifted | improved | flat | insufficient`), and `reasons` for a
     qualification refusal — so the organ **displays** drift candidates and
     never recomputes them
   - `limitations[]`: explicit lines (pre-#342 rows lack provenance; HPC rows
     off the reference host are unqualified; memory and compile axes are not
     in this feed)
2. **Self-validation.** A `validate_summary(payload)` the exporter runs before
   writing and `--check` runs on the committed file: known schema/version,
   unique record ids, finite numerics (a `NaN`/`inf` is refused, not written),
   ISO-8601 UTC dates, no `..`/absolute `evidence` paths, required fields
   present, optional unknowns `null` + reason — never `0` or a success default.
3. **Idempotence + publish.** `--check` covers `summary.json`; `lint.yml` already
   runs it. `pages_dashboard.yml` copies `summary.json` beside `series.json`.
4. **Tests** in `scripts/misc/test/test_build_dashboard.py` over a fabricated
   `results/` tree: a valid feed; the **valid empty producer** (no points →
   empty `records`, `coverage.observed = 0`, still a valid file — "no
   measurements", not "all passed"); duplicate id; non-finite metric; unsafe
   evidence path; unknown provenance → `null` + reason; refused rows land in
   `coverage.excluded`, never in `records`.
5. **Docs**: `dashboard/README.md` grammar section; one line in `AGENTS.md`
   "Repository Structure" naming `summary.json` as the organ read contract;
   the ecosystem spec is the authority, link it.

## Constraints

- No change to historical results, qualification, the drift ratio/floor, the
  cockpit `state.json` or `index.html` — witness is byte-identity.
- Pure stdlib, no PyAuto* imports (the file renders in CI without the stack).
- Public file: no private storage paths or credentials.
- Phase-2 fixture, not phase-1 scope: a second-producer fixture lives with the
  organ's reader, not here.

## Ship policy

Supervised: plan on the issue, end at PR-open, merge human (`/prm`). Heart RED
only under a contemporaneous human development-only override.
