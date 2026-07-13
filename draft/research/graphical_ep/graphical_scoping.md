# Graphical Model Scale-Up — Scoping

Type: research
Target: graphical_ep
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

Companion baseline package: `autofit_workspace_developer/graphical/`. This
document is grounded in the profile data emitted by that package's
`profiles/baseline.json` and `profiles/N10_hotspots.txt`. Re-running the
sweep refreshes both files; the tables below should be re-derived before
issuing follow-up prompts.

## Problem

PyAutoFit's graphical-model framework fits a joint posterior over N
datasets that share parameters via a single `factor_graph.global_prior_model`
search. At small N (3–10) it works fine; at moderate N (30+) three
limitations stack up:

1. **Sampler cost grows badly with dimensionality.** The toy model has
   `3·N + 1` free parameters (per-dataset normalization + sigma plus one
   shared centre). At N=30 that's 91 dimensions. Dynesty (a nested sampler
   without gradient information) doesn't scale; with default `nlive=50` it
   exits the sampling early and the max log likelihood doesn't converge
   to the truth-evaluated value.
2. **Per-factor output overhead.** Every factor's fit emits corner plots,
   latent-sample draws, samples-to-CSV passes, and a search-internal-folder
   cleanup. Visualisation alone accounts for ~20% of wall time on a
   converged joint fit and grows ∝ N.
3. **Single-point-of-reference inspection breaks down.** Once N is past
   ~10, every dataset has its own folder of corner plots, samples, and
   diagnostics. A scientist cannot scan 30+ folders to confirm a fit is
   sensible. There is no aggregated "all-factor posterior" view.

Scale-up has to address all three; the order of attack matters because
some optimisations make others measurable.

## Measured Baseline (toy 1D Gaussian, shared centre)

| N | wall time | peak RSS | output disk | max log L | truth log L | sanity |
|---|-----------|----------|-------------|-----------|-------------|--------|
| 3  | 22.8 s   | 556 MB   | 1.1 MB     | -125.1    | -128.4      | PASS  |
| 10 | 50.7 s   | 844 MB   | 3.7 MB     | -519.3    | -472.3      | PASS  |
| 30 | 132.8 s  | 2.9 GB   | 12.6 MB    | -1658.7   | -1500.6     | **FAIL** |

**Reproduce** from `~/Code/PyAutoLabs-wt/<task>/autofit_workspace_developer`:

```bash
python3 graphical/simulator.py --total_datasets=30
for N in 3 10 30; do
    python3 graphical/fit.py --total_datasets=$N --name=N$N
done
```

**Observations:**
- Wall time scales sub-linearly in N — Dynesty's per-sample cost is
  amortised across more datasets that share the JAX-jitted likelihood.
- **Peak RSS scales ~5×** between N=3 and N=30 (556 MB → 2.9 GB). At N=100+
  this becomes the binding constraint on a 16 GB laptop.
- **Sanity check FAILS at N=30**: max log L gap to truth is 158 nats vs a
  tolerance of 150 (5 nats/dataset × 30). For 90 free params, Wilks
  predicts the fit max should sit *above* truth by ~45 nats — getting
  158 nats below means the sampler did not converge. With `nlive=50` (the
  current config default) and 91 dimensions, this is unsurprising.
- Output disk size is linear in N — at N=30 it's 12.6 MB, projecting to
  ~420 MB at N=1000. Manageable, but tilts toward "sparse output" being a
  real win at the high end.

## Bottleneck Inventory (cProfile attribution at N=10)

Source: `graphical/profiles/N10_hotspots.txt` (full top-30; condensed
families below). Total wall time inside the profiled section: ~46 s of
the 59 s cProfile run.

| Family | cumulative time | % of fit | Notes |
|--------|-----------------|----------|-------|
| `scipy.stats.truncnorm.cdf` (inside `TruncatedGaussianPrior`) | 19.5 s | 33% | 184 200 calls, 7.3 s tottime |
| Dynesty sampling (`run_nested`, `_fill_queue`, `dynesty.__call__`) | 26.7 s | 45% | dominated by inner-loop prior transform + LL evaluation |
| `vector_from_unit_vector` + `prior_transform` (drives the truncnorm calls) | 23.2 s | 39% | wrapped by Dynesty but the cost is the truncnorm |
| `perform_update` + `visualize` | 18.9 s | 32% | corner-plot generation + samples_to_csv + latent-sample resampling |
| `Analysis.log_likelihood_function` (JAX-jitted) | small | <5% | numpy/JAX is fast; the prior transforms dominate |

**Headline:** ~38% of the entire fit is spent transforming uniform unit-cube
points to the TruncatedGaussian via `scipy.stats.truncnorm.cdf/ppf`. This
function is notoriously slow — it falls back to a generic
`_distn_infrastructure` path that re-builds args and broadcasts per call.
A direct erf-based implementation or a JAX-jitted prior transform that
shares the array library with the likelihood would collapse this bucket.

## Ranked Sub-Task Prompt Scopes

Order is by payoff × ease, after the cProfile attribution. Each is
written as a future `/start_dev` candidate — issue them one at a time
through `autofit/...` after the previous lands.

### 1. Gradient-based sampler for the joint factor graph

**Highest scaling payoff.** Replace `DynestyStatic` on
`factor_graph.global_prior_model` with a NUTS/HMC sampler (BlackJAX or
NumPyro) that exploits the JAX-jitted likelihood's gradients. Dynesty
fundamentally cannot scale to N=300+ (dim ≈ 900); HMC sees linear
per-sample cost in dimensionality and converges in O(condition number)
iterations. Suggested first cut: re-use the existing
`autofit_workspace_developer/searches_minimal/nuts_jax.py` /
`nss_grad.py` machinery, wired in through `af.AnalysisFactor`'s
`optimiser=` kwarg. Mandatory deliverable: the sanity-check block at
N=30 must PASS (recovered shared centre within 3σ of truth, max log L
within Wilks-style tolerance of truth log L sum). This is the single
biggest win for scaling.

### 2. JAX-native fast path for `TruncatedGaussianPrior.value_for`

**Highest current-stack payoff, smallest change.** Replace the
`scipy.stats.truncnorm.cdf/ppf` call inside
`autofit/mapper/prior/truncated_gaussian.py:value_for` with an
erf-based closed-form (under the trunc bounds) or an
`autoconf.jax_wrapper`-aware path that uses `jax.scipy.special.erf` /
`erfinv` when the consumer is JAX-jitted. Expected fit-time reduction:
30–35% on any Dynesty workflow that uses TruncatedGaussianPrior heavily
(this includes most of `autofit_workspace_test` and the EP scaling
follow-ups). Sanity check: the toy graphical fit at N=3 should produce
the same max log likelihood within numerical noise.

### 3. Suppress per-factor visualisation on the joint fit

`updater.visualize` and `perform_update` together account for ~20% of
the joint fit. Most of this is producing per-dataset corner plots and
latent-sample draws that nobody inspects once N > 10. Add an
explicit `paths.suppress_per_factor_plots = True` (or similar) that
turns off everything except a single end-of-run summary view. Cross-
references EP's existing `corner_anesthetic` per-factor warning — the
plot family is doing wasted work on EP factors too. Expected payoff:
15–25% reduction in wall time on multi-factor fits; 0% effect on
single-factor / `searches_minimal/` runs.

### 4. Sparse output-to-disk with run resumability

At N=30 each fit produces 12.6 MB; at N=1000 we project ~420 MB per
run. More importantly, autofit's per-iteration `samples_to_csv` and
`search_internal/` overhead are I/O-bound during the fit, not just at
the end. Add an `output.mode = "sparse"` config knob that keeps only
the final samples + the model and skips per-iteration dumps, and
expose enough metadata that an interrupted run can resume from the
last samples file. The "remove search internal folder" wrapper line
(see Tier 1.3 of the IC50 prompt at the bottom) is the same bucket;
share infrastructure with the EP work.

### 5. Single-point-of-reference results summary

Once N > ~10, no scientist will scan 30 corner plots. Add an
end-of-fit aggregator that emits one JSON with the full per-factor
posterior table (param × dataset × mean ± σ), one composite corner
showing the shared latent variable across all factors, and one
parameter-recovery table comparing means/sigmas to the per-dataset
`ground_truth.json`. The sanity infrastructure already in
`graphical/sanity.py` is the seed for the parameter-recovery table.
This is the lowest payoff in time but the largest in scientist
confidence — it's the difference between "the fit converged" and "I
can read the result at a glance".

### 6. Posterior dashboard for cross-dataset comparison

After (5) lands, build a one-page HTML dashboard (or a notebook
template) that plots all factor posteriors aligned against the shared
latent variable's posterior, with the per-dataset truth overlaid. The
dashboard becomes the natural artefact a scientist links to in a
paper appendix or a Slack thread. Defer until (5) is shipped and the
JSON schema is stable.

## Recommended Sequencing

1. **(1) Gradient-based sampler** — unblocks N=100+ work and validates
   that the sanity-check infrastructure correctly distinguishes a
   converged from an unconverged fit. Without this nothing else
   matters at scale.
2. **(2) TruncatedGaussianPrior fast-path** — easiest 30% wall-time
   reduction across all Dynesty workflows. Independent of (1) and
   could ship in parallel. Lands first if (1) hits architectural
   surprises.
3. **(3) Suppress per-factor visualisation** — 15–25% wall-time
   reduction; small code change. Land before any large N=100+
   benchmark so the per-factor noise doesn't pollute attribution.
4. **(4) Sparse output + resumability** — defer until (1) is in
   place; the I/O overhead matters more once the sampling cost is
   knocked down.
5. **(5) Single-point-of-reference summary** — issue alongside (1),
   because the resulting JSON is what the gradient-sampler PR's
   sanity-pass evidence will reference.
6. **(6) Posterior dashboard** — last; requires (5)'s schema to be
   stable.

## Open data needed before issuing the next prompt

- Cross-check the cProfile attribution at N=30 too (the bucket mix may
  shift once the fit is unconverged — sampling-loop time grows). Add a
  `profile_N30.pstats` run to the sweep before issuing prompt (1).
- Confirm that the `searches_minimal/nuts_jax.py` and `nss_grad.py`
  prototypes work against the new `graphical/fit.py` model layout —
  they were written for `searches_minimal` and may need an
  `AnalysisFactor`-friendly wrapper. Worth a quick read before
  scoping prompt (1).
- Decide whether prompt (2) ships as a PyAutoFit-side change (modify
  `truncated_gaussian.py` directly) or an autoconf-side helper that
  both numpy and JAX call into. The dependency-graph note in
  PyAutoFit's CLAUDE.md says "shared utilities go in autoconf" — lean
  toward autoconf if the helper is non-trivial.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
