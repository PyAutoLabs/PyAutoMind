## search-ext-b5c2a-freeze
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/17
- completed: 2026-10-16
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/18
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/71
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/34
- summary: B5c-2a of search-extensibility. Pulled the 930 `correlated_nd` pilot rows of RAL 410866 (`results/` only, per-dataset tar) from the private copy and reconciled every one of the 1040 expected runs: 749 completed rows + 177 failed + 4 oom + 0 missing + 110 deferred; all 930 rows admitted, sacct agrees with every row (`results/accounting/correlated_nd_pilot.json`). Judged under `correlated_nd@1`: 307 accepted, 623 rejected; catalogue and README group by task and dataset in menu order, nothing ranked across families. Failure anatomy: 80 Emcee/Zeus d20+banana rows = a harness bug in this repo (chain diagnostics relabelled by `g0.centre`; fixed here, cells provisionally probe-first pending the clean re-pilot `search_ext_b5c2a_rerun`); 60 d100 Nautilus rows = nautilus needs n_live > n_dim (n_live_100) and its HDF5 checkpoint cannot store a D=100 bound (n_live_200/400; fixed in PyAutoFit#1698); 10 d100 warm NUTS = provider failed; 27 at the 4 h cap. The 4 OUT_OF_MEMORY tasks had been mis-stubbed as cap kills (both exit 137 under `timeout`) and were rewritten from sacct as a new `oom` attempt class; `cnd_cap_stub.py --elapsed-s` prevents a repeat. Calibrated per §7 and froze `correlated_nd@2` at autofit_inference commit `44c5e77f1fb0779f675a8f51247d812183e93b48` (merge 6d26b5571): evidence σ band [0.85, 1.1] on 79 rows, posterior kept [0.5, 2.0] (1 row); 75 cells with timeouts (max 36 875 s), 8 probe-first, 21 deferred with reasons; memory rule `max(8 G, ceil(2 × peak))` → d50 Nautilus n_live_400 16 G, d100 cold NUTS 17 G; an OOM run in the scored wave is rerun once at 2× memory. Human rulings 2026-10-16 recorded in A2 (§11): per-task bands upheld; the post-hoc ln Z filter on the evidence calibration set upheld and declared as post-hoc (without it the band would be [0.0, 1.1]); pilot verdicts stay `@1`. Cortex Log entry + Now→2b (PyAutoCortex#71, 9e8b3d431); Insight pilot row done + campaign next (PyAutoInsight#34, aaad78b52). Nothing submitted.
- decision-taken: A2 memory headroom 2x (--mem = max(8 G, ceil(2 x peak)), peak = 8 G for an OOM class): d50 Nautilus n_live_400 16 G, d100 cold NUTS 17 G — revert: change MEMORY_HEADROOM in calibrate_correlated_nd.py and regenerate
- decision-taken: d100 Nautilus n_live_200 (and n_live_100/400, d100 warm NUTS) deferred from the scored menu — 40/40 n_live_200/400 attempts failed at the pin before sampling (nautilus HDF5 checkpoint, D = 100), affordability unmeasured — revert: drop from _correlated_nd.A2_DEFERRED by a later amendment after a fix
- decision-taken: OOM cells d50 Nautilus n_live_100 and d50 warm NUTS deferred by the cap rule read as "no attempt ended on its own" (9 at cap + 1 oom each) — revert: cap rule = every attempt Terminated at the cap (cells become probe-first)
- decision-taken: σ-ratio bands per task under @2 (evidence [0.85, 1.1] on 79 rows; posterior kept [0.5, 2.0], 1 row < 20) — revert: one band for both tasks (would flip 34 accepted pilot NUTS rows) — human-ruled upheld 2026-10-16
- decision-taken: evidence calibration set also requires §4(c) (excludes 6 collapsed banana Nautilus rows that would drag the band to 0) — revert: drop the (c) filter in calibrate_correlated_nd.calibrate — human-ruled upheld 2026-10-16
- decision-taken: new oom attempt class; the 4 OOM cap stubs rewritten from sacct; @2 reruns an oom run once at 2x memory — revert: git revert the reconcile commit 31ba4a6
- decision-taken: harness fix in 2a — chain diagnostics no longer relabel correlated_nd (all 80 Emcee/Zeus pilot rows had failed on 'g0.centre'); those 8 cells probe-first — revert: revert the _posterior/_runner hunks of b3845e8
- follow-up: `draft/research/autofit_inference/search_ext_b5c2a_rerun.md` (clean re-pilot of the 8 Emcee/Zeus cells, priority high, now unblocked) → then `draft/research/autofit_inference/search_ext_b5c2b_scored_wave_submit.md` (realisations 2–3, manifest, submit 83 cells × 50 seeds × 3 realisations ≈ 12 450 runs / ~1 430 task-hours; the runner still refuses wave-2 `correlated_nd` runs and 2b must open it); d100 Nautilus re-admission needs a later amendment after a PyAutoFit release carries #1698 (and may still fail on cost: nautilus rejection sampling at D=100 with ~100 live points is extremely slow).

### Compute (for 2b)

- compute: nothing submitted in B5c-2a; RAL 410866 results/ pulled (930 rows, per-dataset tar) from the private copy /mnt/ral/jnightin/inference/autofit_inference_b5c into the worktree autofit_inference results/searches/ (committed on feature/search-ext-b5c2a-freeze, autofit_inference#18), sacct extract at results/accounting/correlated_nd_pilot_sacct.tsv; private copy left as is; B5c-2b inputs in results/calibration/correlated_nd_wave1.json (timeouts, probe_first, scored_deferred, memory_raised_gb)
- inputs for 2b: `results/calibration/correlated_nd_wave1.json` (keys `timeouts`, `probe_first`, `scored_deferred`, `memory_raised_gb`), `_correlated_nd.A2_DEFERRED`, `wall/rates.py` `CORRELATED_ND_STEP_RATE`; pin unchanged df6d218f10cd / PyAutoNerves 7f3055b7f3d1; freeze sha 44c5e77f1fb0

## Original prompt

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
