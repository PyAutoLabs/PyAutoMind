# `@autofit_inference` B5c-2b: realisations 2–3 with exact references, the scored-wave manifest and submit scripts, submit the `correlated_nd@2` scored wave on RAL

Type: research
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-10-16
Blocked-by: draft/research/autofit_inference/search_ext_b5c2a_rerun.md (clean re-pilot of the 8 Emcee/Zeus cells must land first; 2a done — record complete/2026/10/search-ext-b5c2a-freeze.md)
Consequence: judge
Epic: search-extensibility
Phase: B5c-2b
Witness: data seeds 2 and 3 exist for all four datasets with exact references on both backends, each passing the §6 agreement test and identity-checked; the scored-wave manifest key is `(dataset, sampler, settings_name, config_id, data_seed, protocol_id, pyautofit_sha)` and a test refuses a row whose library sha differs from the wave pin; attempt accounting distinguishes `missing`/`deferred`/`failed`/`oom`; per-cell `--mem` and timeouts come from the 2a calibration and A2; every submit script passes `check_submits.py --check`; the scored arrays (50 seeds × 3 realisations × every non-deferred cell) are submitted on `--partition=ral` only, from a PRIVATE pinned checkout at the freeze-recorded pin, never the shared mirror; job ids are on the Cortex `## Runs` lines and in `state.md`; Insight gains the `correlated_nd_scored_wave` task row and campaign `next`; nothing from the scored wave is pulled or scored in this stage.
Review-minutes: 45
Unattended: needs-slicing

Authority: protocol `wiki/project/protocol_correlated_nd.md` §9 (50 seeds × 3 realisations, `ral` only, pin recorded with the freeze; each realisation judged against its own exact reference), §6; the 2a record (calibration, deferrals, memory requests, freeze sha); B5a as the template (`complete/2026/10/search-ext-b5a-wave2.md`: manifest key, attempt accounting, rates table, submit scripts, private pin under the RAL root); `PyAutoMind/policy/hpc_ral.md` (CPU arrays `--partition=ral` ONLY; never `HPCPullPyAuto` the shared mirror; never reorder/hold/cancel another campaign's jobs). Approved plan 2026-10-16 (this chat).

## Shape

1. `simulators/correlated_nd.py` + `reference/exact_correlated_nd.py` for data seeds 2–3; §10 reference table extended; tests regenerate byte for byte (structural fallback for floats as in stage 1).
2. `_wave2.py`-style wave module for `correlated_nd` (manifest key, admit, attempt accounting with `oom`), `plan_correlated_nd.py --write` for the scored manifest, submit scripts under `hpc/batch_cpu/correlated_nd/` with per-cell-class `--mem` and timeouts from 2a; `check_submits.py --check` green.
3. Private pinned checkout on RAL under the autofit_inference root (pin ≥ df6d218f1 as the freeze recorded; state it), dry-run one task per dataset, then submit on `--partition=ral` with a throttle that leaves ral usable for euclid_dr1.
4. Cortex `## Runs` lines + `state.md`; Insight row + `next`; hand back a Compute block for B5c-3 (pull, judge under `@2`, `inference-summary@3` shards, Insight snapshot).

Decide-and-flag: array throttle; whether to split arrays per backend as B5a did.

## Completion

The witness holds; record carries job ids, pin, freeze sha and what B5c-3 pulls. Scoring is out of scope.
