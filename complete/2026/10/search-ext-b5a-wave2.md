## search-ext-b5a-wave2
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/8
- completed: 2026-10-15
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/9
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/63
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/29
- summary: B5a of search-extensibility. Froze `gaussian_x3@2` at autofit_inference 72d6faaf before any scored run existed (freeze sha reachable from main; PR merge commit 3463aa190), and built the scored-wave infrastructure: per-wave protocol id, the extended manifest key, attempt accounting, the NSS wave-2 settings, the wall-rates table and the submit scripts (autofit_inference#9). Submitted scored wave 2 on RAL with `--partition=ral` only, against a private PyAutoFit pin df6d218f1 and PyAutoNerves 7f3055b7. ALL 1,629 array tasks had COMPLETED by the morning of 2026-10-15; nothing has been pulled or scored yet. Ledger Now/Runs lines with job ids went in through PyAutoCortex#63 (b9197c372). The Insight `gaussian_x3_search_wave2` task row and the campaign `next` line went in through PyAutoInsight#29 (c99fb9261).
- decisions: the 13 decide-and-flag items are listed in the PR body of autofit_inference#9.
- follow-up: pull, judge and publish continue as task B5b (search-ext-b5b), which starts from the compute and next lines below.

### Compute (for B5b)

- compute: RAL `ral` jobs 408244/408245 (references), 408246 (probe), 408346/408347 (reference builds), 408348/408365/408366/408367 (scored arrays, 11,750 runs, %60 throttle); all 1,629 array tasks COMPLETED by 2026-10-15 morning, nothing pulled yet; freeze sha 72d6faaf, PyAutoFit pin df6d218f1 (A4 merge, unreleased) + PyAutoNerves 7f3055b7 in /mnt/ral/jnightin/autofit_inference/.pyauto_pin/ (zeus-mcmc 2.5.4 in .pyauto_pin/site); RAL clone at f0b3eef (f9605cf state.md-only commit not pulled there); dry-run copy /mnt/ral/jnightin/autofit_inference_b5a_dryrun/ can be deleted
- next: B5b: pull all RAL rows, build the JAX blend realisation-1 reference locally (pilot seeds 0+2 plus RAL seed 1), set probe-first timeouts from probe 408246 and submit the remaining 980 runs of those cells, judge under @2, catalogue, export the wave-2 summary, refresh the Insight snapshot and run `cortex done` on the run lines; carried to B5b: re-judging the pilot's @1 JAX blend rows against the new reference is a reassessment needing an explicit decision; LBFGS on blend numpy still returns +inf at the pin; PRs autofit_inference#9 (merge commit 3463aa190, freeze 72d6faaf reachable from main), PyAutoCortex#63, PyAutoInsight#29 merged 2026-10-15

## Original prompt

# `@autofit_inference` B5a: freeze `gaussian_x3@2`, build the scored-wave infrastructure, submit scored wave 2 on RAL

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
Phase: B5a
Witness: `scripts/misc/searches/_protocol.py` carries `FROZEN_V2` with the six values from `results/calibration/gaussian_x3_wave1.json` and `PROTOCOL_ID` resolves per wave (`@1` for the 223 pilot rows, `@2` for scored rows) — a test judges one pilot row under `@1` and one synthetic scored row under `@2` and the verdict strings carry the id; protocol §7/§11 and `state.md` record the freeze commit sha BEFORE any scored run exists; the scored-wave manifest key is `(dataset, sampler, settings_name, config_id, data_seed, protocol_id, pyautofit_sha)` and a test refuses a row whose library sha differs from the wave pin; references exist (or are scheduled, with job ids) for every data realisation 1–5 on both backends, each identity-checked by `REFERENCE_IDENTITY`; attempt accounting distinguishes `missing` from `deferred` from `failed` per leg; NSS wave-2 settings entry uses ≥50 MCMC steps (retires `draft/feature/autofit_inference/nss_settings_for_wave2.md`); `scripts/misc/wall/` has a rates table derived from the pilot walls and `check_submits.py --check` passes for every submit script; the scored-wave arrays are submitted on `--partition=ral` only, against a PRIVATE PyAutoFit checkout pinned at a sha ≥ df6d218f1 (A4 merge) under the autofit_inference RAL root, never the shared `/mnt/ral/jnightin/PyAuto` mirror, and the job ids are on the Cortex ledger `## Runs` lines and in `state.md`; Insight gains the `gaussian_x3_search_wave2` task row and the campaign `next` line names the submission; nothing is pulled or scored in this stage.
Review-minutes: 45
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-14

Authority: epic report "#### B5" (scored wave 2: 50 seeds × 5 data realisations on `--partition=ral`, library revision frozen after A2+A4, D16 vii); protocol `wiki/project/protocol_gaussian_x3.md` §7 (freeze from the 17 existing calibration rows, pilot NOT restarted, the 297 deferred runs move to wave 2 and are judged under `@2`), §9, §10 (JAX blend Nautilus reference seed 1 deferred); `state.md:29-38,72-75`; review 06 item 7 (`search_extensibility_epic_reviews/06_codex_astra_b3_postmerge.md:178`); the epic ledger lines ~203–211; `PyAutoMind/policy/hpc_ral.md` (read it first: CPU arrays `--partition=ral` ONLY; never `HPCPullPyAuto` the shared mirror — euclid_dr1 depends on it — use a private pinned checkout; never reorder/hold/cancel another campaign's jobs).

Facts from the survey (do not re-derive): `FROZEN_V2` exists only in `calibrate_pilot.py:9`'s docstring; `calibration_set.n = 17` (target 20; §7 lines 175–182 explain why 17 suffice); proposed frozen values sigma_ratio_band [0.5, 2.0], ppc_chi2_tolerance 10.0, mode_radius_px 5.5, nested_min_ess 500, chain_max_rhat 1.01, chain_min_ess 400, timeout_rule max(600 s, 10 × median pilot total wall). Manifest keys today are `(dataset, sampler, settings_name, config_id)` (`_pilot.py:120,163-170`); rows already carry `data_seed` (`_runner.py:31,303-345`, only `data_seed1` exists); references exist only for data_seed 1 under `results/reference/<dataset>/{numpy,jax_cpu}`; `REFERENCE_IDENTITY` at `_protocol.py:57-75`; deferred legs: nautilus ×3 settings × 2 backends, dynesty_static/dynamic × 2, emcee × 2, zeus numpy 16 + jax 18, blackjax_nuts jax 16, blackjax_nuts_warm jax 18 (blend fails deterministically, TracerBoolConversionError — keep deferred with reason unless fixed upstream), smc jax 17, nss jax 20. `hpc/batch_cpu/template` (ral, 8 cpus, 16 gb, 24 h, `--config-name ral_numpy_fp64`, WALL-BASIS header required); `hpc/sync` has submit/pull/status but no push (code reaches RAL by `git pull` on the login node); rates table empty. Cortex row on origin/main `projects.yaml:278-290` (`ral_root /mnt/ral/jnightin/autofit_inference`); the Cortex page "Now" is stale (misses the A4 gate), `## Runs` empty. The local canonical PyAutoCortex is 12 commits behind with uncommitted files — work only in the task worktree, fast-forward it there.

**Decisions to flag (decide-and-flag):** (1) the RAL library pin is a private clone of PyAutoFit (and its PyAuto deps per `activate.sh`) at the A4 merge sha df6d218f1, or the first release that contains it if one exists at submission, under `/mnt/ral/jnightin/autofit_inference/.pyauto_pin/`, PYTHONPATH-prefixed in the batch template — never the shared mirror; (2) wave size: 50 seeds × 5 realisations × every non-deferred leg × 2 backends; submit references first (data_seed 2–5, both backends, plus the deferred JAX blend seed 1), then the scored arrays in batches sized from the rates table so the `ral` partition is shared fairly (throttle `%N` and say what N); (3) `blackjax_nuts_warm` on the blend stays deferred with its reason unless the TracerBoolConversionError is fixed in PyAutoFit main at the pin; (4) the second model family is NOT in this stage — file it as `draft/research/autofit_inference/search_ext_b5c_second_model_family.md` with the candidate list (multimodal, high-D correlated, funnel) and a recommendation.

Shape: PR 1 autofit_inference (freeze + manifest/judging/accounting + NSS settings + wall rates + submit scripts; lint green; no results) → submit on RAL via `hpc/sync submit --cpu` from the login node after `git pull` there → PR 2 PyAutoCortex (ledger: Now/Runs with job ids, log entry newest-first) → PR 3 PyAutoInsight (wave-2 task row, campaign `next`, no snapshot change). Stage 2 (pull, catalogue, `@2` verdicts, Insight snapshot, consumers) is a later task `search-ext-b5b`, opened when the arrays finish; this task's `active.md` row stays open with `status: compute-running` after the PRs merge.
