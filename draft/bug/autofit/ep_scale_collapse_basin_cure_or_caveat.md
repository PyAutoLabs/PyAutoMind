# EP hierarchical parent-scale collapse: cure the basin, or document the caveat

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: formalised — NOT started. Research-grade: the answer may be "inherent to
Consequence: judge
Review-minutes: 25
Unattended: never
Epic: graphical-ep
Phase: 2
        EP", so do not pick this up as ordinary work. The evidence below is the
        expensive part and it is already paid for.
Issue: (none — never issued. Parent report https://github.com/PyAutoLabs/PyAutoFit/issues/1405 stays open.)
Filed: 2026-08-11 (backfilled from git)

## Why this is `too-large` / `human-required` — read before starting

**`too-large` here means "outcome unknown", not "big".** Nobody knows whether a
cure exists.

**Leg 1 shipped** (PyAutoFit#1465 / issue #1464, record
`complete/2026/08/ep-hierarchical-scale-collapse-guard.md`): a collapsed parent
scale is flagged loudly instead of being reported as a confident answer. That was
the defensible, independently shippable deliverable, and it is done.

**Leg 2 — curing the basin — is research, not a feature.** Each candidate lever
needs a *loop* of runs to judge (the failure is intermittent), each loop is ~35-60
min of CPU on this toy alone, and a lever that looked good here would still need
validating across N, across truth values, and against the stickier near-boundary
`slope_hierarchy` case before it could change EP's defaults. That is days of work
with a real chance the answer is "inherent to EP". Work on it was started and then
stopped on that basis, on human call, 2026-08-11 — the three lever sweeps below
were killed mid-flight.

**The prompt's own acceptance already sanctions the exit:** if the basin is
inherent, the deliverable converts to a documented methods caveat (EP is fast and
correct for the parent **mean**; use a joint sampler for the **scatter**) plus the
leg-1 guard. That caveat is now **nearly writable from the evidence below** — see
"If you pick this up".

## The evidence — already paid for, do not redo it

### A working repro (the original cannot be run)

`complete/2026/07/ep_scale_collapse_assets/ep_toy_diagnostic.py` loads the
HowToFit chapter-3 dataset, which is **gitignored and ships with no tracked
files** — so it cannot be run from a fresh checkout. Its generative model is fully
specified in its own docstring, so the data is regenerated instead. The rebuild is
in `ep_scale_collapse_leg2_assets/` beside this file:

- `toy.py` — data generation + graph construction
- `run_once.py` — one EP fit, one machine-readable `RESULT` line
  (env: `TOY_SEED`, `TOY_N`, `TOY_MAX_STEPS`, `TOY_DELTA`, `TOY_OPT`, `TOY_UPDATER`)
- `sweep.sh` — N seeds, 4-way parallel
- `classify.py` — the three-state classifier below
- `trace_message_dict.py` — the closed-lead trace
- `results_baseline.txt` — the 20-run baseline, raw

Numpy + Dynesty, CPU, ~55 s per run standalone. Needs the PyAutoFit `optional`
extra (`astropy`, `nautilus-sampler`) plus `jax` for the full test suite.

### Baseline: only 3 of 20 identical-problem runs are trustworthy

Classified properly, rather than by the toy's crude `scatter < 0.4 * truth` split:

| state | count | what it is |
|---|---|---|
| **PATHOLOGICAL** | 9/20 | scatter ≈ 0 with a tiny *relative* error — the #1405 defect |
| **BIASED-TIGHT** | 8/20 | scatter 3.8-7.9, err 0.39-0.88, truth 10 is **3-15σ away** |
| **RECOVER** | 3/20 | truth within 0.4σ |

### NEW: the BIASED-TIGHT band, and a calibration gap in the shipped guard

**This state is not in the original findings**, which framed the problem as 70%
RECOVER / 7% COLLAPSE. It is a distinct failure: *not* collapsed, but confidently
wrong by up to 15σ.

**The leg-1 guard is silent on all 8 of them.** It fires on 9/9 PATHOLOGICAL and
0/8 BIASED-TIGHT, because its `scale_mean_fraction=0.2` gate means "scatter < 2.0"
and this band sits at 3.8-7.9.

Deliberately **not** retuned. Raising the threshold trades directly against false
positives when the true scatter genuinely is small, and the hard part —
recognising *over-confidence* without knowing truth — is not solved by moving a
number. This is a calibration decision for a human with the science context, and
it is recorded here rather than quietly changed.

### The leg-1 guard validated in the wild

Beyond its unit tests, on real runs: the `scale-collapse` warning fires on real
collapses (seeds 0, 1, 2, 8, ... down to `3.8e-05` with relative error `3.8e-07`),
and **seed 4 fired the repaired monotone limb** —
`std has shrunk monotonically over its last 5 updates to 9.35e-06`. That limb was
diagnosed in leg 1 as effectively dead code in any multi-factor graph; this is it
working on live data rather than a synthetic fixture, which confirms the diagnosis
independently of the tests.

### Closed lead — do NOT re-chase

**`_HierarchicalFactor.message_dict` tempering is INERT.** The override
(`hierarchical.py:195`) drops the base class's `1/(count - 1)` tempering and
carries the comment "*Does not account for inverse cavity behaviour as this caused
bugs for hierarchical factors*", which made it look like the over-counting culprit.
Traced empirically (`trace_message_dict.py`) and **refuted**: while
`FactorGraphModel` builds the global mean field the override is called **0 times**
and the tempered base implementation is called once
(`AbstractDeclarativeFactor.optimise` → `self.mean_field_approximation()` on the
*collection*). It is only reachable via a single factor's own
`mean_field_approximation()`, which the EP loop never uses.

### Untested lever worth trying FIRST when this is resumed

**`af.DynamicUpdater()` — per-variable damping, which the prompt never listed.**
It sets `delta_i ∝ min_count / count(i)`; measured on this graph that gives the
parent `mean` and `sigma` **delta = 0.5** while the well-identified drawn centres
stay at **1.0**. That is targeted at exactly the over-shared variable the
over-counting mechanism implicates.

This also supplies a hypothesis for why the *uniform* damping already on record
failed (`slope_hierarchy` `delta=0.5` → full collapse, 67 `BAD_PROJECTION`,
log-evidence to 5e7): uniform damping also cripples the drawn variables, which are
not the problem. `run_once.py` supports it via `TOY_UPDATER=dynamic`.

### Further levers from the 2026-08-19 EP campaign brief (untried)

Added at intake of the EP campaign (`research/graphical_ep/ep_campaign.md`);
try these *after* the DynamicUpdater lever above, in this order:

1. **Thorough sampling of the hierarchical-factor update.** The EP loop
   updates the hierarchical parent with a fast built-in method (Laplace /
   Newton-style optimiser), not a nested sampler or MCMC. The killed
   `TOY_OPT=laplace` sweep only compares two *fast* optimisers; the untried
   condition is a genuinely thorough sampler (nested sampling / MCMC) on the
   hierarchical factor's update step, so the parent-scale posterior — which
   is skewed and boundary-adjacent, exactly where a Gaussian/Laplace
   projection is worst — is actually explored before projection. If this
   cures the basin, the cost/accuracy trade becomes the design question.
2. **TruncatedGaussianPrior zero-boundary hypothesis.** The parent scatter
   may sit on a `TruncatedGaussianPrior` truncated at zero; the collapse may
   be (partly) a prior-boundary artefact rather than EP-intrinsic shrinkage.
   Test by (a) rerunning with the truth pulled well off the boundary vs
   pinned near it, and (b) swapping the prior family while holding all else
   fixed.
3. **Analytic referee.** The analytic benchmark shipped 2026-09-02
   (`complete/2026/09/analytic-gaussian-benchmark.md`, autofit_workspace_test#92):
   run its conjugate model — where the scatter's posterior and upper limit are known
   in closed form — through the same seed sweep. A basin that appears even
   there is strong evidence for "inherent to EP as implemented"; one that
   does not localises the pathology to non-conjugate likelihoods or the
   sampling layer.

### Sweeps that were running when work stopped

Three 20-seed conditions were in flight and were **not** completed:
`TOY_DELTA=0.5` (uniform damping), `TOY_OPT=laplace` (deterministic per-factor
optimiser in place of the nested sampler), and `TOY_UPDATER=dynamic`. Only the
baseline finished. If any partial results survived they are noted at the end of
this file; otherwise re-run from the banked assets.

## If you pick this up

Cheapest order, and the first item is not research:

1. **Write the methods caveat** — the acceptance-sanctioned deliverable, already
   supported by the baseline above: with current defaults, a *single* EP fit of a
   hierarchical parent scale is not trustworthy (3/20 runs here). Home is
   `autofit/graphical/README.md`, which already carries the damping caveat from
   leg 3. Recommend repeated fits and/or a joint-sampler cross-check for the
   **scatter**; the parent **mean** is fine.
2. **Run the three unfinished sweeps** (~35-60 min each, banked scripts) — the
   caveat is stronger if it can say which levers were tried and failed.
3. **Only then** attempt a cure, starting with `DynamicUpdater`.

## Caveat on the numbers above — read before quoting them

The rebuilt toy collapses **far harder than the original**: 45% PATHOLOGICAL here
versus the 7% recorded on the original HowToFit dataset. Same pathology, harsher
variant — most likely the regenerated data and the chosen noise level
(`TOY_NOISE=0.05`). Good for statistical power per run; **not** a calibrated
reproduction of the original rate, and the rates here must not be quoted as if
they were.

One further contamination: baseline **seed 0** ran in 8.7 s against ~55-540 s for
every other seed, because it resumed from a warm `output/` left by an earlier
standalone run — the exact trap recorded in
`complete/2026/08/ep-initializer-exception-should-not-abort.md` ("a warm `output/`
hides this bug completely"). Its verdict was PATHOLOGICAL either way, so the tally
is unaffected, but clear `output/` between conditions when re-running.

<!-- stopped 2026-08-11 on human call ("this isn't a casual feature to do right
     now"). Leg 1 shipped; leg 2 never issued. The draft/ prompt filed earlier the
     same day is superseded by this file. -->
