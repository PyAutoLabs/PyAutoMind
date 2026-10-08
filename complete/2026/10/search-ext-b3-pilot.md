## search-ext-b3-pilot
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/4
- completed: 2026-10-08
- epic: search-extensibility (phase B3)
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/5
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/23
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/61

**Shipped (all merged 2026-10-08, human `/prm`, in this order):** autofit_inference#5 (19:53:50Z), PyAutoInsight#23 (19:53:55Z), PyAutoCortex#61 (19:54:01Z). Launched `--auto`, effective supervised (feature@large), tier judge.
- **Wave-1 pilot of protocol `gaussian_x3@1`, stopped by the human wrap-up ruling (2026-10-08):** no more pilot compute. The PRs commit what exists: **223 of 520** pilot rows (203 from batch 1 plus 20 from batch 2), each flagged `pilot: true` and stamped with PyAutoFit `0dbf258c4f5e` (pre-A2). The pilot ranks nothing (protocol §9).
- The 297 runs without a row are `deferred` with a reason. **Wave 2 runs on RAL `--partition=ral`.** NSS waits for A3b, plus the per-cell reasons (Zeus-JAX wall cap, BlackJAXNUTS-warm blend trace failure). The JAX blend Nautilus reference stays `pending` (2 of 3 seeds).
- `catalogue/search_catalogue.json` covers every A1-registry search: 13 measured, NSS deferred, Drawer unsupported; nothing ranked. `results/calibration/gaussian_x3_wave1.json` has 17 calibration rows (fewer than 20), so the σ-ratio band and the ppc tolerance stay at `@1`. `dashboard/summary.json` publishes `inference-summary@1` with all 223 records.
- **The `gaussian_x3@2` freeze is deferred.** It must land before any wave-2 row. The BFGS/LBFGS non-finite rows predate A2 (exact JAX gradients) and are expected to change.
- Organs: PyAutoInsight registers `autofit_inference` as instance `fit` with the gaussian_x3 campaign and the wave-1 task. PyAutoCortex flips `projects.yaml` `autofit_inference` from planned to **active** and opens its ledger.
- **Human ruling:** the campaign page stays in autofit_inference `wiki/project/state.md`. There is **no autofit_assistant PR**, because its dated `wiki/project/` entries are gitignored per-clone memory. The claimed `autofit_assistant` branch carried no commits.

## Original prompt

# Wave-1 pilot, Insight registration and the search catalogue (epic search-extensibility, phase B3)

Type: feature
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
- autofit_assistant
Themes:
- searches
- inference
- benchmark
Difficulty: large
Autonomy: supervised
Consequence: judge
Witness: the Insight board (`pyauto-insight board` + `check --offline`) shows the `fit` instance with pilot records; `catalogue/search_catalogue.json` lists every registered search (from `python -m autofit search-manifest --json`) with a status in {measured, unsupported, deferred, failed} and no cross-task ranking; the frozen thresholds are committed in protocol §7 before any wave-2 row; `cortex.py check` passes with the autofit_inference row `active`
Unattended: ready
Priority: high
Epic: search-extensibility
Status: active
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autofit_inference/issues/4
Filed: 2026-10-08

Human launch 2026-10-08: `--auto` for A2, A3, A3b and B3. Plan `draft/research/autofit/search_extensibility_epic_report.md` §4 (phase text quoted verbatim below), architecture §3.3–§3.5, decisions in §8. A0, A0c, A1 and B2 are merged (A1: capability attributes, `Analysis.is_jax`, REQUIRED gate, registry/manifest, `docs/design/run_ctx.md` frozen). Golden identifiers (A0a(i)) are frozen by human ruling: any identifier change stops the item and is flagged. The nine A0 strict xfails are witnesses: flip only the ones a phase names, never add silent ones. Depends on B2 (merged: harness, protocol `gaussian_x3@1`, numpy Nautilus reference). B3 first completes the pending references (protocol §10: JAX Nautilus ×3 and the `gaussian_x3_separated` references on both backends), then runs the pilot.

## Original request (verbatim from the epic plan)

"B3 — Wave-1 pilot, Insight registration, catalogue (depends on B2; wants A1, not blocked). Repos: autofit_inference, PyAutoInsight, PyAutoCortex, autofit_assistant (wiki campaign page). Scope: Insight campaign and task `gaussian_x3_search_wave1`: the exploratory pilot, 10 seeds × the wave-1 menu × both models, local CPU, numpy+JAX, on current main flagged `pilot`; NSS on the blend is recorded `deferred` until A3b. Inference campaign intent lives in PyAutoInsight `campaigns.yaml`/`tasks/`; commit the rows; Insight fixture and `registry.yaml` row `fit`; `catalogue/search_catalogue.json`, keyed by search class and grouped by requested task (point/MAP, posterior, evidence), every registered search marked measured, unsupported, deferred or failed; freeze the thresholds, timeouts and censoring rules in the protocol; a research-wiki campaign page, one row per (model × task) verdict. Risk: low. Verify: `pyauto-insight board` and `check --offline`; `cortex.py check`; no cross-task ranking in the generated tables. Witness: the Insight board shows the `fit` instance with pilot records, the catalogue lists every registered search with a status, and the frozen thresholds are committed before any wave-2 row."

## Pins

Wave-1 menu (report §3.7): evidence/posterior Nautilus (`n_live` 100/200/400), DynestyStatic, DynestyDynamic, SMC (NSS deferred until A3b); posterior Emcee, Zeus (numpy and JAX legs), BlackJAXNUTS cold and warm-from-short-Nautilus; point/MAP LBFGS, BFGS, MultiStartAdam/Prodigy/ADABelief/Lion; Drawer not benchmarked. 10 seeds, local CPU, `local_numpy_fp64` and `local_jax_cpu_fp64` where JAX-native, both datasets. The pilot ranks nothing; it calibrates the σ-ratio band and freezes thresholds/timeouts/censoring (D16 iii) in protocol §7 via a §11 amendment. Rows carry the PyAutoFit commit (post-A1 main). Compute budget: run in background batches; if the full menu cannot finish, commit what ran with honest coverage (every un-run cell marked `deferred` with the reason) — never fabricate rows, never run on RAL `gpu`; wave 2 is RAL `--partition=ral` later. Organ edits: Insight `registry.yaml` row `fit` (`inference-summary@1`, `cortex_project: autofit_inference`) + campaign + task; Cortex `projects.yaml` row `autofit_inference` → `active` with the ledger pointing at the project state page (`cortex.py check`); autofit_assistant `wiki/project/` campaign page with provenance stamps. Follow B1's deviation rule: organ rows land only once a published summary exists (commit the autofit_inference summary first).

## Verification

Harness tests + gates (ruff, README/summary/WALL checks, witness); Insight `check --offline` with the real registry row and `board`; `cortex.py check`; assistant provenance check; no table ranks tasks against each other (unit test on the catalogue builder).

## Shape

PRs: autofit_inference (rows, references, catalogue, protocol amendment, summary) first; then PyAutoInsight (registry + campaign + task), PyAutoCortex (row), autofit_assistant (wiki page). Feature cap at large → effective supervised: decide-and-flag at ship, one flagged decision at most; tier judge.
