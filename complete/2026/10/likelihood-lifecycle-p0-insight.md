## likelihood-lifecycle-p0-insight
- issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/39
- completed: 2026-10-23
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/45
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/40
- epic: likelihood-lifecycle (phase 0, sub-issue 0D of 0A–0E)

- Summary: Infrastructure only — no runs, no new result rows, no judgement of results (the human: every Insight result is rerun later under Optimal setups, phases 4 and 7). autolens_inference#45 (merged 5bdae73) fixes the 0C regression that had left PyAutoInsight's `lens` receipt `invalid` since bdc8b2d: `inference_catalogue.py` now publishes prepared-problem `baseline_record_id`/artifact `record_id` translated through `catalogue/migration_2026_10.json` at export time (manifests untouched), and withholds any record `problem_id` that names an unemitted prepared problem (15 rows, `problem_id_reason` names the id); new stdlib test `scripts/misc/test/test_catalogue_references_resolve.py`; artefacts re-exported; Insight validator 0 errors (was 57 = 36 artifact + 6 baseline + 15 problem); pytest 218. PyAutoInsight#40 (merged f2b38228) adds `summary.lifecycle_errors` in the shared per-record loop of `summary.validate` (v1/v2/v3): `setup_mode` ∈ {auto, explicit} with named refusal, `setup_resolved {backend, device, operator, precision, transformer, threads}`, `host_class`, `model_variant`, `likelihood {dataset_type, variant}` — declarations only, nothing cross-checked against Pulse, nothing feeds acceptance; `setup_browser.py` renders a `Setup: <mode> · <backend>/<device>/<operator>/<precision> · <host_class> · <model_variant>` line; fixture `experiment-cold` carries `setup_mode: auto`; REFERENCE/README/CHECKIN drift fixed (live pins `lens` @2 / `fit` @3, two live producers, `walltime-validation@1` routed to Pulse `lens-walltime`); pytest 204 → 219. No `inference-summary` version bump (Insight never refused the keys).
- Witness MET: autolens_inference's `Publish inference summary` run dispatched the Insight refresh (b3e8e1d1); `receipts/lens.json` on Insight main = `outcome: ok` at 5bdae73a, 284 records, no errors.
- Gotchas: #40 `lint` (`pyauto-insight check --offline`) reads the COMMITTED `receipts/lens.json`, so it stays red on any Insight PR until the producer fix lands on main and the refresh rewrites the receipt — merge the producer PR first, then merge origin/main into the Insight branch (new head, fresh green CI). 7th `prepared/` dir (`prepared-fe6fe94…`, jax_cpu sparse light_fixed seed 0) correctly stays in `coverage.excluded`: its baseline row was never committed. Heart YELLOW at ship (workspace manifest drift; PyAutoLens release validation stale), unrelated.
- Next: 0E PyAutoBrain lifecycle template + conductor grid; 0B autolens_profiling stays queued (`planned.md likelihood-lifecycle-p0-profiling`) until the cluster-pointsolver starting-grid claim clears; `predicted_ms_per_eval`/`reference_runtime_record_id` fill only after 0B re-pins `lens` to @3.

## Original prompt

# Likelihood lifecycle phase 0D: PyAutoInsight additive lifecycle fields (`setup_mode: auto`), `setup_resolved` as provenance, doc drift after 0C, and the autolens_inference prepared-problem reference fix that returns the `lens` receipt to ok

Type: feature
Target: PyAutoInsight
Repos:
- PyAutoInsight
- autolens_inference
Themes:
- samplers
- dashboard
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `bin/pyauto-insight check` is green (`outcome: ok`) on the re-exported autolens_inference `dashboard/catalogue.json` at its post-fix main commit, with the lens snapshot carrying `setup_mode`, `setup_resolved`, `setup_id`, `host_class`, `model_variant` and `likelihood` on every record; a fixture record with `setup_mode: auto` and a `setup_resolved` block validates and renders its provenance line in the setup browser; a record with `setup_mode` outside {auto, explicit} is refused with a named error; REFERENCE.md names the live pins (`lens` @2, `fit` @3) and the `walltime-validation@1` axis as Pulse's, not Insight's
Review-minutes: 25
Unattended: never
Epic: likelihood-lifecycle
Phase: 0
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-23
Issued: 2026-10-23
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/39

Phase 0 sub-issue 0D of the `likelihood-lifecycle` epic (ledger `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`; report §3.2 "`inference-summary` (Insight; additive)", §3.8 "Insight: unchanged structure; the setup page shows `setup_resolved` as provenance", §4 phase 0 "0D PyAutoInsight"). Depends on 0A (PyAutoPulse#70, merged 2026-10-21) and 0C (autolens_inference#42→#43→#44, PyAutoPulse#71, PyAutoCortex#74, merged 2026-10-21; record `complete/2026/10/likelihood-lifecycle-p0-inference.md`). 0B (autolens_profiling) is NOT a dependency and is not touched here: autolens_profiling is claimed by the cluster-pointsolver starting-grid work in another session.

## State found 2026-10-23 (read before planning; do not re-survey)

1. **The Insight `lens` receipt is `invalid` at the 0C merge commit** (`receipts/lens.json`: `resolved_commit` bdc8b2d, `outcome: invalid`, 284 records, cached from the last ok fetch at autolens_inference 71bfd57b with 148 records; `dashboard.md` shows "latest fetch invalid", 0/148). Running Insight's own validator (`insight.summary.validate` → `insight.catalogue.validate`) on the local `dashboard/catalogue.json` reproduces 57 errors of exactly two kinds, both **producer-side reference breaks introduced by 0C**, none about the new fields:
   - `prepared-<hash>: artifact source record unresolved` and `prepared-<hash>: baseline record unresolved or wrong problem` for all 6 emitted `prepared_problems`: the committed `prepared/<id>/manifest.json` files (PR #42) carry `record_id`s in the **pre-move path form** (`results/slam/imaging/hst/slam_base_light_fixed/hpc_a100_jax_cpu_dense_fp64/stages_seed1.json#stage-…`), and the move-only PR #43 rewrote record ids to the mirrored tree (`results/imaging/rectangular/hst/validation/light_fixed/jax_cpu_dense_fp64/seed_1/stages.json#stage-…`) without mapping the manifests' references. `catalogue/migration_2026_10.json` holds the old→new map.
   - `<record>#stage-03dd03936a025726: problem unresolved` on ~43 `mass_total[1]` records (current and archived): their `problem_id` names a prepared id that is not among the 6 emitted `prepared_problems` (7 `prepared/` dirs exist; the exporter emits 6 — establish whether the seventh is dropped, or whether the problem id is derived differently from the record's side).
   - The additive 0C fields (`setup_mode` = `explicit` everywhere, `setup_resolved {backend, device, operator, precision, transformer, threads}`, `setup_id`, `host_class` ∈ {hpc_a100, hpc_ral_cpu, local_laptop}, `model_variant` ∈ {default, light_fixed, delaunay_1250}, `likelihood {dataset_type, variant}`) pass the current Insight validator untouched: Insight does not refuse unknown record keys, so **no version bump** of `inference-summary` is needed (the §3.2 condition). 0D declares them in the contract instead of leaving them undocumented.
2. **Insight doc drift**: REFERENCE.md line 68 says "The live registry remains `inference-summary@1` in this phase" while `registry.yaml` pins `lens` at `inference-summary@2` and `fit` at `@3`; REFERENCE.md line 14 and README.md lines 21–22 still say autolens_inference is the "first real producer" and the second-producer fixture "is not a claim of a second adopter" although `fit` (autofit_inference) has been a live adopter since search-extensibility B3 (2026-10-08). Nothing in Insight mentions that full-fit wall-time validation (`walltime-validation@1`, produced by autolens_inference since 0C) is a **Pulse** evidence axis (PyAutoPulse registry row `lens-walltime`) and not an Insight artefact; CHECKIN.md's "what each organ reads" prose should say so in one sentence so a check-in does not look for it on the Insight board.
3. autolens_inference `README.md` line 311 documents `dashboard/catalogue.json` as inference-summary@2 (correct); `scripts/misc/tooling/export_inference_summary.py` writes `setup_mode: "explicit"` as a constant (line ~194). autolens_inference PR #30 (README pin table, branch `fix/pin-readme-peeled-commits`) is still open and touches README only.

## Rulings applied

R8 (recommended, confirmed by 0C's plan approval 2026-10-21): sampler folders `…/samplers/<model_variant>/<sampler>/{auto|explicit/<setup_id>}/seed_<n>`; Insight records assume `setup_mode: auto` for sampler campaigns from phase 7 and carry `setup_resolved` as provenance. R7: `host_class` is provenance, never identity — Insight renders it, never filters acceptance by it. Additive only: Insight never infers scientific acceptance, never selects a setup, never computes a ratio; Cortex keeps scientific authority; Mind keeps task state.

## What, as separate PRs in this order

1. **autolens_inference producer fix (one PR, content only, no moves)** — the exporter resolves every `prepared/<id>/manifest.json` `record_id` (artifacts and `baseline_record_id`) through `catalogue/migration_2026_10.json` to the mirrored-tree record ids (or the manifests are regenerated with the new ids in the same PR — choose in the plan; the map is the audit trail either way), and emits the prepared problem for every `prepared/` dir that a record's `problem_id` names (or drops the dangling `problem_id` with a `problem_id_reason`, never an unresolved reference). Re-export `dashboard/summary.json`, `dashboard/catalogue.json` and `dashboard/walltime_validation.json`; `export_inference_summary --check` current. Add a test that runs the vendored Insight-shape check the repo already uses for `--check` (or a stdlib reference-resolution test: every `problem_id`, `baseline_record_id` and artifact `record_id` resolves). Rebase after autolens_inference PR #30 if it lands first (README only).
2. **PyAutoInsight contract + render + docs (one PR)**:
   - `insight/catalogue.py` (v2 path) and the v3 shard path in `insight/summary.py`: declare the additive record fields — `setup_mode` ∈ {`auto`, `explicit`} (other values refused with a named error; absent allowed for pre-0C producers), `setup_resolved` object with text-or-null `backend`, `device`, `operator`, `precision`, `transformer` and integer-or-null `threads`, `host_class` text, `model_variant` text, `likelihood {dataset_type, variant}` texts. Validation of declarations only: no cross-check against Pulse, no inferred `auto` resolution.
   - `insight/setup_browser.py`: the record disclosure heading or first provenance line shows `setup_mode` and the `setup_resolved` tuple (e.g. `explicit · jax/gpu/dense/fp64 · hpc_a100 · light_fixed`), per report §3.8; `insight/board.py` record table unchanged in structure, drops nothing.
   - Fixtures: extend `tests/fixtures/lens_summary_v2.json` with one `setup_mode: auto` record carrying `setup_resolved`, and a negative fixture or test case for an invalid `setup_mode`; tests in `test_catalogue.py`, `test_setup_browser.py`, `test_summary.py` (v3 shard).
   - REFERENCE.md: the "Identity and ownership" table gains the additive fields with their meaning (provenance; `auto` means the library chose the setup — phase 5 — and `setup_resolved` records what it chose); line 68 rewritten to the live pins (`lens` @2, `fit` @3) with the deploy order kept as the rule; line 14 and README.md 21–22 rewritten: two live producers (autolens_inference `lens`, autofit_inference `fit`); one paragraph pointing full-fit wall-time validation at PyAutoPulse (`walltime-validation@1`, instance `lens-walltime`) and stating Insight does not host it. CHECKIN.md: one sentence on the same routing.
   - Run `ruff check .`, `ruff format --check .`, `python -m pytest tests -q`, `bin/pyauto-insight check --offline` (Insight AGENTS.md).
3. **Refetch** after both merge: `bin/pyauto-insight fetch`/the dashboard refresh workflow re-reads `lens` at the post-fix autolens_inference main; `receipts/lens.json` `outcome: ok`; `dashboard.md` lens section current. This happens on the Insight main via the scheduled refresh or a `repository_dispatch`; the receipt is the witness, committed by the refresh, not by hand.

## Out of scope

Any change to autolens_profiling or PyAutoPulse (0B re-pins `lens` to @3 and fills `predicted_ms_per_eval`); an `inference-summary` version bump (not needed: Insight accepts the keys today); re-pointing `reference_runtime_record_id` (0B); sampler campaigns under `auto` (phase 7) and the library `setup="auto"` (phase 5); any Insight-side ranking, acceptance or setup selection; the Brain lifecycle template (0E).

## Blocked-by (operational, not a header gate)

None. autolens_inference is unclaimed (0C's task closed 2026-10-21); PyAutoInsight is unclaimed. Producer fix (PR 1) lands before the Insight PR is judged complete, because the Insight witness needs a resolvable lens catalogue; the two PRs are independent to write.
