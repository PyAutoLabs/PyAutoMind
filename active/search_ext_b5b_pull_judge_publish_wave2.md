# `@autofit_inference` B5b: pull scored wave 2, judge it under `gaussian_x3@2`, publish the catalogue and summary

Type: research
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: B5b
Witness: every pulled wave-2 row is admitted or refused by `_wave2.admit` with the per-leg `accounting()` sums equal to the expected counts (11,750 scored + 20 probe, 250 deferred with reasons); `catalogue/search_catalogue.json` carries a `gaussian_x3@2` section whose per-cell success rates and expected-wall-per-right-answer are computed only from `@2` rows at the pinned PyAutoFit revision df6d218f1; `dashboard/summary.json` validates against the Insight read contract and `bin/pyauto-insight check --offline` passes with the `fit` snapshot refreshed; the JAX blend realisation-1 reference reaches `status: complete` from three Nautilus seeds and passes the §6 agreement test; the probe-first cells get `@2` timeouts written from the probe medians by the frozen rule and their remaining runs are submitted on RAL `--partition=ral`; `cortex.py done` has moved jobs 408244–408367 into the log; the lint gate (`export_inference_summary.py --check`, `plan_wave2.py --check`, `check_submits.py --check`, `build_catalogue.py --check`) is green.
Review-minutes: 40
Unattended: needs-slicing
Filed: 2026-10-15
Issued: 2026-10-15

## Request

Human 2026-10-15: "ok do the next batch of tasks in auto" after the B5a /prm. B5a's `complete/2026/10/search-ext-b5a-wave2.md` and `wiki/project/state.md` name this task: "Pull, catalogue and `@2` verdicts are the next task (B5b)."

## Facts from the B5a hand-back and the 2026-10-15 survey (do not re-derive)

- Compute is finished: RAL jobs 408244/408245 (references), 408246 (probe), 408346/408347 (reference builds), 408348/408365/408366/408367 (scored arrays) — all 1,629 array tasks COMPLETED by 2026-10-15 morning; queue empty; nothing pulled. Freeze sha 72d6faaf (in main via merge commit 3463aa190). Pin PyAutoFit df6d218f1 + PyAutoNerves 7f3055b7 under `/mnt/ral/jnightin/autofit_inference/.pyauto_pin/` (zeus 2.5.4 in `.pyauto_pin/site`). RAL clone at f0b3eef. Dry-run copy `/mnt/ral/jnightin/autofit_inference_b5a_dryrun/` may be deleted. The RAL login node filesystem is very slow (git pull 10–20 min; plan long rsyncs, never a `HPCPullPyAuto` of the shared mirror).
- `hpc/sync pull` (or `pyauto-brain cortex pull --project autofit_inference`) pulls `output/`, `results/` and logs 1:1 with no wave filter; `search_internal/` excluded. Rows land in `results/searches/<dataset>/data_seed<d>/<sampler>/<settings>/ral_*_fp64/search_seed*.json`; new references in `results/reference/<dataset>/<backend>/data_seed{2..5}/`. `results/` is committed (small rows only); `output/` is gitignored. AGENTS.md: commit results/exporter changes first, regenerate `dashboard/summary.json` and commit it separately.
- JAX blend realisation-1 reference: `python scripts/misc/reference/build_reference.py --dataset gaussian_x3_blend --backend jax_cpu` reads `output/reference/.../nautilus_seed{0,1,2}/<hash>/files/samples.csv`; seeds 0 and 2 are local pilot runs (rows committed), seed 1 comes from RAL task `run nautilus 1 1 ral_jax_cpu_fp64` (reference_gaussian_x3_blend.tsv:50). A stray local `nautilus_seed1/a7506fab…` output directory exists with no committed row — decide which seed-1 run the reference uses and say so. The NSS `ln 3!` constant-likelihood offset (task `constant nss 0 1`) must be merged into `results/reference/constant_likelihood.json` (check how `run_constant_likelihood.py` output is merged).
- GAPS the task must close (all in `scripts/misc/searches/` and `scripts/misc/tooling/`): (1) no probe-median timeout writer and no generator for the remaining probe-first submits — `TIMEOUT_RULE_V2` = max(600 s, 10× probe median) (`_protocol.py:89-97`); `cells()` reads timeouts from `results/calibration/gaussian_x3_wave1.json["timeouts"]` and a missing entry makes a cell `probe_first`; `plan_wave2.py --check` is a lint gate so new submit files must come out of the planner; the Insight task file says 980 remaining runs; (2) no `@2` judge/accounting CLI — `_wave2.admit`, `operational_kill`, `accounting` exist with no caller outside tests; (3) `build_catalogue.py` (:99-104) and `export_inference_summary.py` (:323-325) filter to wave 1 by design, deferring `@2` to this stage; (4) Insight `registry.yaml` pins `supported_schema: inference-summary@1` for instance `fit`.
- Carried decisions: (a) re-judging the pilot's `@1` JAX blend rows (today `not_assessed`) against the new reference is a reassessment (review 06 item 8); (b) `@2` timeouts are 10× laptop medians and RAL is 4–7× faster, so censoring is lenient — a recorded limitation; (c) LBFGS on blend numpy still returns +inf at the pin.

## Rulings for the plan (settled here, flag in the PR body)

1. **Pilot rows are not re-judged.** The 223 `@1` pilot rows keep their `@1` verdicts; the JAX blend pilot rows stay `not_assessed` with the reason "reference completed after the pilot (B5b)". The pilot ranks nothing, so nothing is lost; a reassessment would be a separate, human-chosen task.
2. **Schema stays `inference-summary@1`.** Wave-2 rows are exported in the same schema with `protocol_id: gaussian_x3@2` per record and a top-level `protocols` list; the Insight registry is not bumped. If the @1 schema cannot carry a per-record protocol id without a contract change, stop with a batched issue question rather than forking the contract.
3. **The catalogue gets a `gaussian_x3@2` section** beside the wave-1 pilot section; the wave-1 section is byte-identical apart from the producer revision. `@2` ranks (the pilot does not); the ranking fields are success rate and expected wall per right answer under the frozen rules.
4. **Probe-first cells**: write `results/calibration/gaussian_x3_wave2_probe.json` (timeouts from the probe medians by `TIMEOUT_RULE_V2`, with the 20 probe rows cited), teach `cells()` to read it after the wave-1 timeouts, regenerate the submits with `plan_wave2.py`, and submit the remaining runs on RAL `--partition=ral` with the same exclusions, throttle and pin checks as B5a. Those runs are pulled by a small follow-up (B5b-2); this row stays open as compute-running after PR-open, exactly as B5a did.
5. **Commits**: rows first (`results/`), then tooling, then the regenerated catalogue and `dashboard/summary.json` as their own commits. Never commit `output/`.

## Shape

PR 1 autofit_inference (pulled rows + reference + constant offset + probe timeouts + submits + @2 judge CLI + catalogue + exporter + summary; `wiki/project/state.md` "Now" and journal entry; lint green) → PR 2 PyAutoCortex (run lines done, ledger) → PR 3 PyAutoInsight (`fit` snapshot refreshed from PR 1's merged main or `--from fit=<path>` flagged as a local read; task file next-line; campaign next). Human /prm in that order. Nothing on RAL beyond the probe-first remainder; never touch other campaigns' jobs; CPU arrays on `--partition=ral` only.
