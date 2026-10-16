# `@autofit_inference` B5c-2: pull and judge the correlated_nd pilot, settle the OOM cells, freeze `correlated_nd@2`, submit the scored wave

Type: research
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-10-16
Consequence: judge
Epic: search-extensibility
Phase: B5c-2
Blocked-by: none (stage 1 record `complete/2026/10/search-ext-b5c-family.md`)
Witness: every COMPLETED task of RAL 410866 is pulled (`results/` only, per-directory tar pattern from B5b) from the PRIVATE copy and judged under `correlated_nd@1` with attempt accounting that distinguishes `missing` from `deferred` from `failed` from `oom`; the four OOM cells have an explicit ruling in the protocol (memory request raised, or cell excluded with reason) before the freeze; `correlated_nd@2` is frozen from the pilot rows and its sha recorded in `state.md` and protocol §11 BEFORE any scored run exists; the scored-wave manifest key carries the protocol id and library sha and a test refuses a row from a different pin; the scored arrays are submitted on `--partition=ral` only from a private pinned checkout, job ids on the Cortex `## Runs` lines and in `state.md`; Insight gains the `correlated_nd_scored_wave` task row and campaign `next`; the catalogue still ranks nothing across families; nothing from the scored wave is pulled or scored in this stage.
Review-minutes: 45
Unattended: needs-slicing

Authority: epic report "#### B5" and the B5c stage-1 prompt (`complete/2026/10/search-ext-b5c-family.md` "Original prompt", Size: scored wave 50 seeds × 3 realisations, about 6–8k runs, 1–2k core-hours on `ral`); protocol `wiki/project/protocol_correlated_nd.md` §6–§11; `state.md` Next; `PyAutoMind/policy/hpc_ral.md` (CPU arrays `--partition=ral` ONLY; never `HPCPullPyAuto` the shared mirror; never touch another campaign's jobs).

## Why

Stage 1 pre-registered the family and ran the pilot; nothing has been judged. The scored wave cannot be frozen honestly until the pilot rows are judged under `@1` and the operational failures are understood. Four pilot tasks died at the 8 G memory cap and would silently become `failed` legs in a scored wave.

## Inputs from stage 1 (verified 2026-10-16)

- RAL 410866_[0-929]%100, wall 4:16 (2026-10-15 23:50 → 10-16 04:06 UTC): 926 COMPLETED, 4 OUT_OF_MEMORY. Results unpulled in `/mnt/ral/jnightin/inference/autofit_inference_b5c` (pin df6d218f1). Pilot manifest `hpc/batch_cpu/correlated_nd/pilot.tsv`, task N = line N+2.
- OOM cells, all `corr_gaussian_d50` data_seed 1: 263 nautilus n_live_100 numpy seed 3 (MaxRSS 7.6 G, 2:42); 273 nautilus n_live_100 jax_cpu seed 3 (7.7 G, 2:42); 304 nautilus n_live_400 numpy seed 4 (3.1 G at kill, 0:52); 383 blackjax_nuts_warm warmup_200_samples_500 jax_cpu seed 3 (8.4 G, 3:52). Human ruling: not rerun in stage 1; settle here.
- 110 pilot runs were deferred under A1 (Emcee/Zeus D≥50, DynestyStatic/NSS D=100); Nautilus is exempt from the live-point floor.

## Shape

Mirror B5a/B5b in order:
1. Pull `results/` of 410866 into canonical `fit/autofit_inference/` (never the shared RAL mirror), judge every row under `@1`, build the per-leg attempt table and the wall-rates table for this family. Record the pilot verdicts in `state.md` and the catalogue (grouped by task, nothing ranked across families).
2. Rule on the OOM cells in a protocol amendment (A2) with reasons: raise `--mem` for d50/d100 Nautilus and NUTS-warm cells (measure from MaxRSS, add headroom), or defer them per dimension. Decide whether d100 Nautilus is affordable at all from the pilot walls.
3. Freeze `correlated_nd@2` from the pilot rows (freeze sha reachable from main before any scored run), the scored-wave manifest key, attempt accounting, submit scripts passing `check_submits.py --check`.
4. Submit the scored wave on `--partition=ral` only from a private pinned checkout (≥ df6d218f1, state the pin); job ids to Cortex `## Runs` and `state.md`; Insight task row + campaign `next`.
5. Hand back with a Compute block for B5c-3 (pull, judge under `@2`, summary records as `inference-summary@3` shards, Insight snapshot).

Decide-and-flag: realisations 3 (not 5 as in gaussian_x3) per the stage-1 Size line unless the pilot walls argue otherwise; seeds 50.

## Completion

The witness holds; `complete/` record carries a Compute block with job ids, pin, freeze sha and what B5c-3 pulls. Scoring the wave is out of scope.
