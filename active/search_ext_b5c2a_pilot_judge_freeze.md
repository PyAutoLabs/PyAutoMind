# `@autofit_inference` B5c-2a: pull and judge the correlated_nd pilot, calibrate, rule on the OOM cells, freeze `correlated_nd@2`

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
Issued: 2026-10-16
Issue: https://github.com/PyAutoLabs/autofit_inference/issues/17
Consequence: judge
Epic: search-extensibility
Phase: B5c-2a
Witness: every task of RAL 410866 is accounted for — `results/` pulled from the PRIVATE copy into canonical `fit/autofit_inference/`, a censored stub row for any task killed without a row, and the four OUT_OF_MEMORY tasks (263/273/304/383) carried as an `oom` attempt class distinct from `missing`/`deferred`/`failed`; every row is judged under `correlated_nd@1` and the catalogue's `correlated_nd` section groups by task and dataset and ranks nothing across families; the §7 placeholders (σ-ratio bands, ESS/R-hat bars), per-cell timeouts (`max(600 s, 10 × median pilot wall)`) and the censoring rule are calibrated from the pilot by the §7 rules (a band moves only on ≥ 20 completed rows of its task, never past the 200 000 exact draws; a cell whose every attempt hit the cap is deferred with reason); amendment A2 rules on the OOM cells (memory request from measured MaxRSS + headroom, or deferral with reason) and on d100 Nautilus affordability from the pilot walls; `correlated_nd@2` is frozen — protocol §7/§11 and `state.md` carry the freeze sha, `PROTOCOL_ID` resolves `@1` for pilot rows and `@2` for scored rows with a test — and NO scored run exists or is submitted in this phase; Cortex Log entry and Insight `correlated_nd_pilot` row closed with the pilot verdicts.
Review-minutes: 40
Unattended: needs-slicing

Authority: stage 1 record `complete/2026/10/search-ext-b5c-family.md` (Compute block: pilot manifest `hpc/batch_cpu/correlated_nd/pilot.tsv`, task N = line N+2; OOM cells all `corr_gaussian_d50` data_seed 1); protocol `wiki/project/protocol_correlated_nd.md` §4–§9, §11; B5b pull pattern (`complete/2026/10/search-ext-b5b-score.md`: parallel per-directory tar on the login node, `results/` only); `PyAutoMind/policy/hpc_ral.md` (never `HPCPullPyAuto` the shared mirror; never touch another campaign's jobs). Approved plan 2026-10-16 (this chat): two phases, 2a freeze with no compute, 2b (`search_ext_b5c2b_scored_wave_submit.md`) realisations + submit.

## Why

Stage 1 pre-registered the family and ran the pilot; nothing has been judged. The scored wave cannot be frozen honestly until the pilot rows are judged under `@1` and the operational failures are understood. Four pilot tasks died at the 8 G memory cap and would silently become `failed` legs in a scored wave.

## Inputs from stage 1 (verified 2026-10-16)

- RAL 410866_[0-929]%100, wall 4:16 (2026-10-15 23:50 → 10-16 04:06 UTC): 926 COMPLETED, 4 OUT_OF_MEMORY. Results unpulled in `/mnt/ral/jnightin/inference/autofit_inference_b5c` (pin df6d218f1, PyAutoNerves 7f3055b7).
- OOM cells, all `corr_gaussian_d50` data_seed 1: 263 nautilus n_live_100 numpy seed 3 (MaxRSS 7.6 G, 2:42); 273 nautilus n_live_100 jax_cpu seed 3 (7.7 G, 2:42); 304 nautilus n_live_400 numpy seed 4 (3.1 G at kill, 0:52); 383 blackjax_nuts_warm warmup_200_samples_500 jax_cpu seed 3 (8.4 G, 3:52). Human ruling: not rerun in stage 1; settle here in A2.
- 110 pilot runs deferred under A1 (Emcee/Zeus D≥50, DynestyStatic/NSS D=100); Nautilus exempt from the live-point floor.

## Shape

1. Pull `results/` of 410866 (per-directory tar, login node) into canonical `fit/autofit_inference/`; stub rows via `scripts/misc/tooling/cnd_cap_stub.py` for any task without a row; verify 930 expected runs resolve to row/failed/missing/deferred/oom.
2. Judge under `@1` (`scripts/misc/searches/_correlated_nd.py`, `_pilot.py`); attempt table per leg; wall-rates table for this family (`scripts/misc/wall/`); catalogue + README rebuilt (`build_catalogue.py`, `build_readme.py`), grouped by task and dataset.
3. Calibrate via `calibrate_pilot.py` extended for `correlated_nd` (bands, bars, timeouts, censoring) by the §7 rules; record the calibration file under `results/calibration/`.
4. Amendment A2 in §11 (OOM memory rule / deferrals; d100 Nautilus affordability), then freeze `correlated_nd@2` in `_protocol.py` (`FROZEN` values, `PROTOCOL_ID` per wave) and record the freeze sha in §7/§11 and `state.md`.
5. Cortex: dated Log entry with the pilot verdicts and the freeze sha (newest-first). Insight: `correlated_nd_pilot` row to done with headline numbers, campaign `next` names 2b.
6. Hand back with the inputs 2b needs: calibrated timeouts, deferred cells, memory requests per cell class, freeze sha.

Decide-and-flag: the A2 memory headroom factor; whether d100 Nautilus `n_live_200` stays in the scored menu.

## Completion

The witness holds; the `complete/` record carries the freeze sha, the deferred-cell list and the per-cell memory requests for 2b. No scored run exists.
