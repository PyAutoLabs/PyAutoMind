# Likelihood lifecycle phase 0B: autolens_profiling mirrored tree, day-zero migration map, `profiling-summary@3` catalogue builder, misc grouping, coverage matrix, parity convention

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
Themes:
- profiling
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `tests/test_results_mirror_scripts.py` passes (every `results/<dataset_type>/<variant>/` has a `scripts/<dataset_type>/<variant>/` and vice versa, `archive/` excluded); `build_catalogue --check` is current and emits `profiling-summary@3` with every record carrying `class`/`status` and exactly one `current` per key; `pyauto-pulse check` accepts the re-pinned `lens` instance at @3 and its receipt refetches; the coverage matrix tool lists current / superseded / missing / stale cells per likelihood × class × measurement
Review-minutes: 40
Unattended: never
Epic: likelihood-lifecycle
Phase: 0
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-21
Issued: 2026-10-23
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/442

Phase 0 sub-issue 0B of the `likelihood-lifecycle` epic (ledger `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`; report §3.1, §3.6, §3.7, §4 phase 0; survey `likelihood_lifecycle_epic_surveys/01_profiling_inference_layout.md`). 0A (PyAutoPulse#70, merged 2026-10-21) defined the contract this issue emits: v3 records carry `likelihood`, `instrument`, `regime`, per-record `setup` + `setup_id`, `host_class`, `model_variant`, `measurement`, `metric`/`unit`/`values`, `class`, `status`, `superseded_by`, `day_zero`, `figures[]`, `decision_id`, `release_pin`, `measured_at`; there are no `setups[]`/`selections[]` — `planned_cells` (with `class`) replace selections; `archive_record_count` is required (PyAutoPulse REFERENCE.md "`profiling-summary` v3").

## Rulings applied (confirmed 2026-10-21)

R1 `setup_id` = `<backend>_<device>_<operator>_<precision>[_<transformer>]`, host/tier moves to `host_class`; R2 label-only history cut — nothing deleted, nothing re-run; R3 the provisional designations of report §3.3 are the phase-0 class labels (provisional, confirmed by phases 2–3; no `decision_id` exists yet, so every provisional Optimal row is emitted `class: optimal` only once a designation decision exists — until then `class: secondary` with a `provisional_optimal: true` note in `limitations`, or the builder refuses; decide in the plan); R7 `local_*` rows are never `current`.

## What, as separate PRs in this order (data guard: moves and content never in one PR)

1. **Commit nothing new first; migration map** — `catalogue/migration_day_zero.json`: old path → new path (+ sha256) for every tracked file under `results/` (1,456 files, 326 MB, `results/lens/solver/corpus` 165 MB) and `results/notes/` ledgers → `wiki/campaigns/<dataset_type>/<variant>/`; dead experiments (dated suffixes, `_lever`, `_probe`, pre-2026-09 series, `baselines/PreOptimizationTimes`, frozen packs) → `archive/YYYY/MM/<slug>/`. Legacy model names retired in paths (`pixelization` → `rectangular`, `*_numba` → the `setup_id`). The map is reviewed by the human before any move.
2. **Move-only PR** (git mv only, reviewed as renames): the §3.7 layout `results/<dataset_type>/<variant>/<instrument>/<setup_id>/<host_class>/{runtime,breakdown,gradient,fit,parity,provenance}.*` with `history/<release_pin>_<date>/` for superseded files; `results/lens/<component>/`, `results/misc/<group>/`; `wiki/campaigns/<dataset_type>/<variant>/`; `archive/YYYY/MM/<slug>/` with a README pointer at each old parent; `results/README.md` redirect table. Never under a live RAL job on a RAL checkout of this repo.
3. **Catalogue builder** (`scripts/misc/tooling/build_catalogue.py`, `catalogue/registry.json`, `_script_routes.py`): reads the mirrored tree, emits `profiling-summary@3`, converts the config grammar, assigns `class`/`status` by the §3.6 rule (the 29 `planned_baseline` + 3 `reference_candidate` → `current` provisional where the host rule holds; other records on mirrored keys → `superseded` with `superseded_by`; archived → counted), `planned_cells` with `class`, `figures[]` where `fit.png` exists; `build_catalogue --check`; `dashboard/catalogue.json` regenerated; Pulse `registry.yaml` `lens` pin → `profiling-summary@3` (one-line PyAutoPulse PR after the builder merges) and the Pulse receipt refetched.
4. **`scripts/misc/` grouping polish**: `misc/test/` split by group, `misc/searches/` orphan removed, one-off scripts to `archive/`, a README per group.
5. **Coverage matrix tool** (extend the profiling conductor's `campaign` grid diff or add `scripts/misc/tooling/coverage_matrix.py`): likelihood × class × measurement → current / superseded / missing / stale, reading the v3 catalogue and the §3.3 provisional table.
6. **Parity witness convention**: `parity.json` per cell (reference log-likelihood, tolerance, status ∈ match / diverged / not_assessed) documented in `results/README.md` and read by the builder into `measurement: parity` records.

## Out of scope

Re-measuring anything (phase 3); designation decisions (phase 3); `fit.png` rendering in `_profile_cli.py` (phase 1B); `runtime_estimates.yaml` (phase 5E); autolens_inference (0C); Brain conductor grid (0E).

## Blocked-by (operational, not a header gate)

(Resolved 2026-10-22: that task merged as autolens_profiling#438 and the claim is released.) autolens_profiling was claimed by `cluster-pointsolver-robust-settings` (issue #436, branch `feature/cluster-pointsolver-robust-settings`, 5 unmerged commits, RAL sweeps live on 2026-10-21). The move-only PR cannot land under that branch or under live RAL jobs on a RAL checkout; start after that task ships (or the human releases the claim) — `/start_dev` registers this in `planned.md` until then.
