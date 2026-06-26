# Expectation Propagation Scale-Up — Scoping

Companion baseline package: `autofit_workspace_developer/ep/`. This
document is grounded in the profile data emitted by that package's
`profiles/baseline.json` and `profiles/N10_hotspots.txt`. The "IC50 tier
breakdown" referenced below was supplied by James from a separate IC50
cancer use case; one goal of this scoping pass was to rerun the toy
example and confirm/refute that ranking.

## Problem

PyAutoFit's EP framework fits a graphical model factor-by-factor: each
EP iteration runs N+1 Dynesty searches (one per dataset factor plus one
global factor, in the general case) and updates the message field via a
LaplaceOptimiser-driven cavity step. For the shared-centre toy this is
N per-dataset Dynesty fits per iteration. Over the
`af.EPHistory(kl_tol=0.05), max_steps=5` budget the toy converges in
fewer than 5 iterations, so the typical workload at N datasets is
roughly `M·N` Dynesty fits where M ∈ {1, 2}.

Two consequences:

1. **EP's per-fit wrapper overhead is amplified by M·N.** A graphical
   joint fit runs Dynesty once at high dimension; EP runs it many times
   at low dimension. Every per-fit cost (visualisation, latent samples,
   sampler initialisation, search-internal-folder cleanup) is paid
   ≥M·N times.
2. **autofit-internal overhead has nowhere to hide.** Graphical fits
   amortise prior-transform cost across the inner Dynesty sample loop;
   EP runs many short Dynesty fits where the relative overhead of
   non-sampling work dominates.

The original IC50 profiling produced this tier breakdown
(reproduced verbatim from the task prompt):

> Tier 1 — Dynesty wrapper overhead (~86% of optimise time)
> Tier 2 — Local Hill LL evaluation (~6%)
> Tier 3 — Global LL evaluation (~5%)
> Tier 4 — EP-loop orchestration (~4%)
> Tier 5 — set_model_approx (~0%)

The goal of this scoping pass is to rerun on toy, confirm/refute Tier 1's
86% claim, and produce a ranked list of sub-task prompts.

## Measured Baseline (toy 1D Gaussian, shared centre)

| N | wall time | peak RSS | output disk | sanity |
|---|-----------|----------|-------------|--------|
| 3  | 251.9 s (4.2 min)   | 599 MB   | 8.1 MB     | PASS  |
| 10 | 566.9 s (9.4 min)   | 672 MB   | 27.0 MB    | PASS  |
| 30 | 1758.7 s (29.3 min) | 1.1 GB   | 84.7 MB    | **FAIL** |

Reproduce from `~/Code/PyAutoLabs-wt/<task>/autofit_workspace_developer`:

```bash
python3 ep/simulator.py --total_datasets=30
for N in 3 10 30; do
    python3 ep/fit.py --total_datasets=$N --name=N$N
done
```

**Observations:**
- **EP is ~11× slower than graphical at every N tested** (cf.
  `graphical_scoping.md`). At N=3 it's 252 s vs 23 s; at N=10 it's
  567 s vs 51 s; at N=30 it's 1759 s vs 133 s. The 11× ratio is stable
  across N — this is per-fit wrapper overhead × number of fits, not a
  scaling issue.
- **EP wall time scales linearly in N** (slope ~60 s per added dataset
  after fixed overhead). This validates the IC50 projection that the
  wrapper bucket is N-linear.
- **Peak RSS is ~constant in N** (~700 MB ± 200) because EP fits one
  factor at a time. This is EP's structural advantage over graphical's
  joint fit (which hit 2.9 GB at N=30) — at N=300+ EP is the only
  approach that fits in memory.
- **Output disk grows linearly** at ~3 MB per dataset (8 MB → 85 MB
  from N=3 to N=30). At N=1000 that's ~3 GB per run.
- **Sanity at N=30 fails** — most per-dataset normalization/sigma
  recoveries pass, but one or two factors drift outside 3σ. Likely
  symptomatic of EP convergence with `max_steps=5`; needs more EP
  iterations or KL-tolerance tightening to investigate (out of scope
  for this scoping pass).

## Bottleneck Inventory — Toy vs IC50

cProfile attribution at N=10 (5 EP iterations × 10 factor fits = 50 total
Dynesty fits inside the 723 s profiled run). Source:
`ep/profiles/N10_hotspots.txt`.

| Family | cumulative time | % of fit | Toy vs IC50 |
|--------|-----------------|----------|--------------|
| Per-factor matplotlib viz (`corner_anesthetic` + `plot_2d` + `savefig` + `backend_agg.draw`) | 346 s | **48%** | **Confirms IC50 Tier 1's wrapper bucket — and toy weights it even higher than IC50's 86% (since IC50 included other overheads in that bucket).** |
| Dynesty sampling (`run_nested`, `_fill_queue`) | 300 s | **41%** | Higher % than IC50's split because the toy LL is cheap (no JAX-jitted Hill curve to amortise against). |
| Prior transforms via `scipy.stats.truncnorm` | 185 s | 25% | Not separately broken out in IC50, but a known issue (same bottleneck as graphical). 116 s is `_distn_infrastructure.cdf` alone — 16% of total. |
| EP-loop orchestration (`factor_graph.optimise`, message updates) | small | <5% | Matches IC50's Tier 4 estimate of ~4%. |
| Latent-sample regeneration (`Creating latent samples by drawing 100 from the PDF`) | ~15 s | ~2% | Inside the wrapper bucket but worth calling out — it runs per fit even though EP factors don't need latent samples. |

**Headline:** toy confirms IC50's Tier 1 (wrapper overhead dominates) but
weights matplotlib visualisation as the single largest sub-bucket — 48%
just for per-factor corner plots that nobody inspects. The
`corner_anesthetic` log line "posterior estimate not yet sufficient.
Should succeed in a later update" — which the user already flagged in
the prompt — fires on every fit and contributes no end-of-run artefact.
This is the biggest single bang-for-buck cut.

What we **don't** see in toy that was prominent in IC50:
- A separate "global factor" cost. The toy doesn't have a hierarchical
  global factor; the shared centre is just another Variable in the
  factor graph. IC50's Tier 3 (Laplace replacement on a global Dynesty
  fit) is real for IC50's 18-param hill-curve global factor but does
  not apply here.
- "Force x1 cpu" / pool-related overhead. The toy runs single-core
  by default; no pool to reuse.

So the toy run **does not refute** any IC50 finding, and **strongly
confirms** that the wrapper bucket — specifically per-factor
visualisation — is where the first cuts should land.

## Ranked Sub-Task Prompt Scopes

Order is by payoff × ease, based on the toy + IC50 evidence. Each is
written as a future `/start_dev` candidate under `autofit/...` (most
are PyAutoFit library work).

### 1. Suppress per-factor visualisation in EP iterations

**~48% of EP runtime** on the toy and a similar share in IC50. EP
factors don't need per-iteration corner plots, latent-sample draws, or
PNG saves — only the final aggregated posterior matters. Add a
`paths.ep_mode = True` (or `paths.suppress_plots = True`) flag that the
EP loop sets on each factor's paths before each iteration's `search.fit`
call, and route `nest_plotters.corner_anesthetic`, `samples.plot_2d`,
and `output_figure` through this gate. Expected wall-time reduction:
40–50% on multi-factor EP runs; 0% on `searches_minimal/` single
searches. Lands cleanly with graphical_scoping.md's prompt (3).

### 2. JAX-native fast path for `TruncatedGaussianPrior.value_for`

Same prompt as graphical_scoping.md's (2). 25% of EP runtime is
prior-transform-bound; ~16% is the underlying `scipy.stats.truncnorm.cdf`.
A direct erf-based implementation or autoconf-shared JAX-aware helper
would knock off ~20% of EP wall time. **Single prompt that covers both
graphical and EP** — issue once and both scaling stories benefit.

### 3. Skip search-internal-folder cleanup when output-to-disk is disabled

When the user already opted into "Output to hard-disk disabled" by not
supplying a search `name`, the per-fit "Removing search internal folder"
step has nothing to do but still runs. Toy data doesn't isolate this as
a separately measurable line (it's buried inside `perform_update`), but
the IC50 prompt's Tier 1.3 calls it out, and the toy log shows the
INFO line firing on every fit. Cheap fix, modest payoff. Bundle with
(1) since both are paths flags.

### 4. cProfile attribution inside `factor_graph.optimise`

IC50's Tier 4 — the EP loop orchestration. Toy's <5% share suggests
this is not currently a bottleneck, but at N=10000 (per IC50's
projection) a 4% bucket grows to a 30-hour problem. Drop a cProfile on
`factor_graph.optimise(...)` excluding `search.fit(...)` cumulative
time, and report which `autofit/graphical/` functions exceed 5% time.
Cheap (~30 min to write the harness, ~30 min to run), informative,
and may surface a quadratic prior-walk that the toy is too small to
expose. Issue this *before* (5) and (6) because the data informs
whether parallelisation or sampler reuse is the better next bet.

### 5. Parallelise local Dynesty fits across CPU cores per EP iteration

IC50's Tier 2 win. Each EP iteration's N local fits are
embarrassingly parallel — no message passing within an iteration. A
process pool around the `analysis_factor_list` loop inside
`factor_graph.optimise` would give near-linear speedup up to the core
count. Care needed: the existing `force_x1_cpu` carve-out for
JAX-pooled searches and the search-cache state need to be re-entrant.
Sanity: results must match within numerical noise of the serial run.

### 6. Reuse Dynesty sampler / pool across fits

IC50's Tier 1.2 — at every EP iteration each factor's `search.fit`
re-instantiates a Dynesty sampler from scratch. EP's structure
("fit the same factor with mildly different priors each iteration")
is the textbook caching target. The first cut can be small: cache the
sampler object on the `AnalysisFactor` and re-seed its priors at each
iteration. Mandatory deliverable: matching posteriors to within a
tightened tolerance on the toy sanity checks.

### 7. (Out of scope for toy) Replace Dynesty on a global factor with
LaplaceOptimiser

IC50's Tier 3, item 6 — replace `DynestyStatic` on the global factor
(18 free params, smooth Gaussian likelihood) with a Newton-step
Laplace approximation. The toy doesn't have a hierarchical global
factor so this isn't measurable here, but the prompt should still
exist for the IC50 / cosmology use cases. Defer until a project with a
distinct global factor is the use case (cancer / cosmology). Note in
the prompt that PyAutoFit already exposes `LaplaceOptimiser` — wiring
it through `factor_graph.optimise(..., search_global=)` is the work.

## Recommended Sequencing

Mirrors IC50's prescribed ordering but tuned by the toy data:

1. **(1) Suppress per-factor visualisation + (3) skip internal-folder
   cleanup** — biggest single-PR win (~50% of EP runtime). Bundle into
   one prompt under the `paths.ep_mode` flag. Issue this first; the
   measured baseline tables will need a refresh afterwards.
2. **(2) TruncatedGaussianPrior fast-path** — shared with
   graphical_scoping. Issue independently, can land in parallel.
3. **(4) cProfile inside `factor_graph.optimise`** — small, fast,
   data-gathering prompt. Runs after (1) and (2) so the attribution
   isn't dominated by visualisation/prior noise.
4. **Re-measure baseline at N=100 toy.** Project to N=1000. If wall
   time projections look feasible, move to (5); if memory grows
   unexpectedly, divert to memory profiling.
5. **(5) Parallelise local fits** and **(6) sampler reuse** — likely
   the next big wins once the wrapper bucket is gone. Issue (5) before
   (6) because parallelisation is more straightforward and yields a
   bigger absolute reduction.
6. **(7) Global-factor Laplace** — defer until a non-toy use case
   needs it.

## Open data needed before issuing the next prompt

- Re-confirm the visualisation share at N=30 (where there are 30+
  factors × 5 iterations × 2 plot calls per iteration). The toy
  cProfile at N=10 already shows 48%; at N=30 we expect this to
  approach 60%+. Worth one extra cProfile run after the worktree is
  spun back up.
- Verify the `paths.ep_mode` flag interacts cleanly with
  `autofit_workspace_test`'s graphical/ep scripts — those run the
  same visualisation paths and may need their own toggle.
- The N=30 sanity FAIL needs root-causing before being treated as a
  regression baseline. Possible causes: `max_steps=5` insufficient at
  large N, KL tolerance too loose, message-field convergence stuck.
  This is a small standalone prompt of its own (likely in autofit:
  "investigate EP convergence on toy at N=30") — list it as a
  prerequisite to the optimisation prompts so we don't accidentally
  validate optimisations against a known-broken baseline.

## Reference — IC50 detail used as input

(Preserved verbatim from the task prompt for traceability when issuing
follow-up prompts.)

> Tier 1 — Dynesty wrapper overhead (~86%): corner_anesthetic plotting,
> latent-sample draw, search-internal-folder cleanup, sampler
> reconstruction, paths setup.
> Tier 2 — Local Hill LL (~6%): linear in N; parallelise across CPU
> cores per EP iteration.
> Tier 3 — Global LL (~5%): constant in N (18 free params); replace
> Dynesty with LaplaceOptimiser.
> Tier 4 — EP-loop orchestration (~4%): cProfile to find any
> quadratic-in-N loops.
> Tier 5 — `set_model_approx` (~0%): skip.
> Sequence: cProfile attribution → suppress plotting + folder cleanup
> → Laplace global → measure at N=100 → sampler reuse + parallelisation
> → orchestration profile.
