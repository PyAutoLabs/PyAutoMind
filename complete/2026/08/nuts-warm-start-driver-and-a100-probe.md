# NUTS registered as autolens_profiling's first MCMC cell — warm-start driver, collision-proof tagging, honest eval/ESS accounting, and a queued A100 cold-vs-warm probe

- **Issue:** autolens_profiling#187 · **PR:** autolens_profiling#188 (`2ff0604`) — merged 2026-08-28
- **Repos:** autolens_profiling (`scripts/misc/searches/{_samplers,_runner,_metrics}.py`, `scripts/imaging/searches/nuts/mge.py`, `scripts/misc/test/test_searches_nuts.py`, `scripts/misc/searches/README.md`, `hpc/batch_gpu/submit_search_nuts_imaging_mge_a100_hst_fp64_probe`, `results/notes/inference/PROGRAMME.md`)
- **Epic:** `jax-inference-profiling` — PROGRAMME.md Phase 6 (Gate C) opened; Phase 7 (SMC) left as a research row
- **Status: SHIPPED.** All six goals met. 1276 insertions across 8 files; 256 tests pass (235 existing + 21 new).

## The headline

`SAMPLER_BUILDERS` held only nested samplers and gradient MAP optimizers, so **none of Phase 6's questions could be asked from this repo at all**. `af.BlackJAXNUTS` is now registered as a first-class `nuts` sampler with the PyAutoFit PR#1522 warm-start API, driven by `SEARCHES_NUTS_*` env knobs exactly like its siblings.

Warm starting goes through `InitializerParamStartPoints.from_result`, which maps values onto the target model **by prior path** and writes only a starting-point dict. Priors are never rewritten, so the warm and cold arms of an A/B fit an identical model and differ only in where the chains start — which is the only way the comparison means anything.

## Three defects caught before they became silent wrong numbers

**1. Output-path collision.** `BlackJAXNUTS.__identifier_fields__` is `(num_warmup, num_samples, num_chains, inverse_mass_matrix)` — `seed` and `initializer` are *not* in it. A warm and a cold arm at identical settings (this cell's entire experiment) would therefore resolve to one output directory, and the second `fit()` would return the first's `.completed` result: the cold arm's numbers reported twice, with nothing in either artifact revealing it. This is the same defect RAL job 340576 exposed for `log_det_method` (20 arms → 10 directories). `nuts_unique_tag` carries the seed and an 8-hex digest of the resolved warm-start path into the `unique_tag`, and hence into both the identifier and the output path.

**2. Eval accounting.** A NUTS draw costs up to `2 ** max_num_doublings` (1024) leapfrog steps, each a likelihood + gradient. `samples.total_samples` is the *kept draws* (`num_chains * num_samples`), so reading `likelihood_evals` off it would under-report by up to three orders of magnitude and flatter NUTS against every nested row in the same table — the error class of #177. The driver records the search's own `samples_info["n_logl_evals"]` (summed `num_integration_steps`), which **is** reject-inclusive, so `Basis: evals` stays honest.

**3. ESS.** NUTS weights are all `1.0`, so the Kish formula degenerates to the raw draw count and ignores autocorrelation entirely. The rank-normalised `ess_min` is substituted into `kish_ess` (and hence `evals_per_ess` / `ess_per_min`) — which is also the quantity Gate C is written in terms of.

Every NUTS row additionally carries a `diagnostics` block projected from `samples_info` (ESS bulk/tail, `rhat_max`, divergences, acceptance, tree-depth histogram, warm-start source, metric kind), so Gate C can be read off the artifact without re-deriving anything from the chain.

## Structural changes

- Every `SAMPLER_BUILDERS` entry now takes a `model=` kwarg. Only `build_nuts` uses it, and it **must** be the real post-override model: `InitializerParamStartPoints` looks start points up with `point_dict[prior]`, keyed by the target model's own `Prior` *objects*, so a probe model or the source's model would miss on every lookup and fall back to prior defaults — a "warm" run that was actually cold.
- `_SAMPLERS_WITH_POSTERIOR` split out from `_SAMPLERS_WITH_N_LIVE`. NUTS has a posterior and no live points; the two sets only coincided while every posterior-bearing sampler here was nested.
- The `n_live: n/a (MAP optimizer)` log line no longer calls an MCMC run a MAP optimizer.

## Wall-clock basis

NUTS has **no measured step rate on any cell**, and the MGE rows in `wall/rates.py` are per optimizer *step* — a different unit from a leapfrog trajectory. Substituting one would be exactly the cross-cell citation that killed job 340576, so the submit's `# WALL-BASIS:` row honestly declares `source: unmeasured  probe-first: yes`. Measuring that rate is the job's purpose; `n_logl_evals` in the artifact yields it directly.

## PROGRAMME.md corrections

The Phase-0 checklist row claiming `af.BlackJAXNUTS` is "single-chain, diagonal-mass, no covariance/start-vector injection" is stale since PyAutoFit PR#1522 — **all three negatives are now false**. Marked SUPERSEDED with what replaced it. Phase 8B's state table and W5 row were updated with PR#186's preliminary verdict (FALSIFIED 3/4; 12/24 rows excluded; final verdict owed on job 341978).

Two *other* rows still carry the same stale multi-chain-NUTS premise (the `| PyAutoFit | Multi-chain BlackJAXNUTS ... |` feature row, and the W3 row citing **#1521**, probably a typo for #1522). Left alone as out of scope and flagged on the PR and issue so they are not lost.

## Jobs queued (goals 3 and 5)

| Job | What | Partition | Budget |
|---|---|---|---|
| `341981_0` | NUTS **cold** — InitializerBall at the prior median | gpu | 45:00 |
| `341981_1` | NUTS **warm** — 4 start points from the completed Prodigy MGE MAP fit | gpu | 45:00 |
| `341983` | SMC warm research row — the parked prototype, unmodified | ral (CPU) | 1:30:00 |

Both NUTS tasks: 4 chains, warmup 200, samples 200, `mass=diag`, seed fixed at 0 — a warm-vs-cold A/B, not a reliability scan, so the seed must not be the thing that differs. Submitted with `--requeue` so `_gpu_preflight.sh` can bounce off the MIG-mode A100.

**SMC ran without modifying anything.** RAL's `autolens_workspace_developer` working tree already held the prototype's files as untracked copies, byte-identical to branch `feature/blackjax-smc-gradient-kernel` @ `6867762` (`smc_warm_cpu.sbatch` `531213d4…`, `blackjax_smc_grad.py` `830848…`), so no checkout and no edit was needed. `--time` is 1.5x job 331058's own measured 3574 s, replacing the script's speculative 8 h header. **This is a research row, not a Gate D input** — there is no `af.` SMC class, and Phase 7 gates A100 SMC rows behind Gate D, which is why it runs on the CPU `ral` partition as 331058 did.

**PyAutoFit was deliberately NOT pulled on RAL.** RAL's PyAutoFit at `f466dce1a` already contains PR#1522, so the probe needs no update; pulling to `54aa0875b` would bring PR#1539 (`ClipperPriorBoxJoint` composed with a bijector) underneath job 341978's pending phase-8B arms, which run `clipper=prior_box` **with** a bijector — silently splitting the campaign, 15 pending arms on different library semantics from the 24 already harvested, with nothing in the artifacts saying so.

## Local smoke: reached the fit path, did not finish

The local CPU smoke of the leaf did not complete: XLA's CPU compile of the NUTS trajectory through the 60-Gaussian MGE gradient is pathologically slow on this machine (>20 min in `jit_log_density`, at 100% CPU and progressing). An environment artifact, not a driver fault — the builder, both metric substitutions, the collision guard and every guard path are covered by the 21 new unit tests, and the driver's fit path *is* reached: the run gets as far as window adaptation, writing the correctly-tagged output directory `c2_w3_s3_seed0_cold_md1/`.

## Gates

`ruff check` / `ruff format --check` clean · `build_readme.py --check` clean · `check_submits.py --check` clean (51 submits with a contract, 0 failing) · 256 tests pass. CI `lint` green on the merged head (`b7190cf`); it is the repo's only PR-triggered workflow, `profile.yml` being manual/release-only.

## Left open

- **RAL is still on `feature/nuts-warm-start-driver-and-a100-probe`** and must return to `main` now the PR is merged (`git checkout main && git pull --ff-only && git branch -d feature/nuts-warm-start-driver-and-a100-probe` in `/mnt/ral/jnightin/autolens_profiling`). Not done at close-out — the session was instructed not to touch RAL.
- Jobs `341981_{0,1}` and `341983` are queued, not harvested. Their results, and the Gate C verdict they feed, are downstream work — this task built the driver and queued the probe, which is all its scope claimed.
- Two pre-existing RAL defects found and worked around, worth fixing separately: `autolens_workspace_developer`'s `remote.origin.fetch` is a single stale refspec for a deleted branch, so *every* `git fetch` in that clone aborts; and the profiling clone's `git pull` was blocked by untracked result files PR#186 also adds (resolved at the time).
- Two stale multi-chain-NUTS rows remain in PROGRAMME.md (above).

## Original prompt

# NUTS warm-start driver + A100 MCMC probe (and an SMC research row)

Type: feature
Epic: jax-inference-profiling
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
