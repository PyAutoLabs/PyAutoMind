# NUTS warm-start driver + A100 MCMC probe (and an SMC research row)

Type: feature
Epic: inference-programme
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- inference
- jax
- hpc
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-28

## Original request (verbatim)

> get some SMC or other MCMC runs queued up on the A100s so we can probe that
> stuff too

## Context

The A100 harvest of 2026-08-26/27 closed the gradient-MAP (MultiStart*) arc.
The inference programme's remaining sampler questions are the **MCMC** ones —
PROGRAMME.md Phase 6 (warm-started NUTS) and Phase 7 (SMC, Gate D) — and
`autolens_profiling` currently has **no** MCMC leaf at all:
`scripts/misc/searches/_samplers.SAMPLER_BUILDERS` registers only `nautilus`,
`nss` and the five `multi_start_*` gradient optimizers.

PyAutoFit main now ships `af.BlackJAXNUTS`
(`autofit/non_linear/search/mcmc/blackjax/nuts/search.py`) with the PR#1522
warm-start API: `num_chains`, `initializer=result.start_point_from(...)` /
`InitializerParamStartPoints.from_result(...)`, and
`inverse_mass_matrix=None|"diagonal"|"dense"|ndarray|Result`. PROGRAMME.md's
line stating "BlackJAXNUTS is single-chain, diagonal-mass, no start-vector
injection" is therefore **stale** and must be corrected.

No SMC class exists in PyAutoFit. The only SMC material is a parked prototype
on `autolens_workspace_developer` branch `feature/blackjax-smc-gradient-kernel`
(issue wsdev#113), whose 4 arms ran as RAL job 331058 and are harvested under
`results/notes/inference/phase_00_unblocking/ral_harvest/`.

## Goal

1. `scripts/misc/searches/_samplers.py` — add `build_nuts` (env-driven like its
   siblings) registered in `SAMPLER_BUILDERS`, with a `multi_start_unique_tag`-
   style `nuts_unique_tag` so the knobs that are **not** in
   `BlackJAXNUTS.__identifier_fields__` (seed, warm-start source) cannot make an
   arm silently resume a sibling's `.completed` fit. Env knobs:
   `SEARCHES_NUTS_NUM_CHAINS` (default 4), `SEARCHES_NUTS_NUM_WARMUP`,
   `SEARCHES_NUTS_NUM_SAMPLES`, `SEARCHES_NUTS_MASS` (`diag|dense|result`),
   `SEARCHES_NUTS_WARM_FROM` (path to a completed result output dir; unset =
   cold), `SEARCHES_NUTS_JITTER`, reusing the existing `SEARCHES_SEED`.
2. `scripts/imaging/searches/nuts/mge.py` leaf mirroring
   `multi_start_prodigy/mge.py`, plus a `searches/README.md` section and
   `build_readme.py --check` idempotence.
3. `hpc/batch_gpu/submit_search_nuts_imaging_mge_a100_hst_fp64_probe` — an array
   of 2 (task 0 cold, task 1 warm from a completed Prodigy mge result on RAL),
   short (warmup 200 / samples 200 / 4 chains), `--time=0:45:00`, WALL-BASIS
   `source: unmeasured  probe-first: yes`, `gres=gpu:1`, sources
   `_gpu_preflight.sh`, sets `JAX_ENABLE_X64`.
4. Local CPU smoke of the leaf at tiny settings, proving the driver writes the
   standard results JSON.
5. SMC: establish from the Phase 0 harvest notes exactly how job 331058 was
   submitted and resubmit ONE short research-row arm if it can be done cleanly;
   otherwise record the precise blocker. No `af.` SMC class exists, so any SMC
   row is a **research row** — Gate D is not called on it.
6. Correct the stale PROGRAMME.md BlackJAXNUTS line.

## Gates

`ruff check . && ruff format --check .`, `build_readme.py --check`,
`scripts/misc/wall/check_submits.py --check`, `scripts/misc/test/` pytest.

## Out of scope

- Any pixelized NUTS cell (mge only — this is a first probe).
- Adding an SMC search class to PyAutoFit.
- Calling Gate D or Phase 6/7 verdicts; this task only builds the driver and
  queues the probe.
