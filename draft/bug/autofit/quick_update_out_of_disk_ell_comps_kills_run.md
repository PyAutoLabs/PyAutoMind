# A quick update must not kill a 36 h run because the current best sample is unphysical

Type: bug
Target: autofit
Repos:
- PyAutoFit
- euclid_strong_lens_modeling_pipeline
Themes:
- samplers
- mge
- visualization
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-09-07

Witness: a `vis_lp`-shaped Nautilus fit whose running max-likelihood parameter vector
maps to an `ell_comps` pair of magnitude > 1 completes its search instead of raising,
and the quick update logs a skip rather than propagating `ModelParameterException`
out of the likelihood call.

## The request, verbatim

> euclid phase 4 (Cortex `phases/euclid_dr1_prelim/dr1_prelim_10_lens_science_run.md`, RAL array 342301): task 3 Tile102007903RA0668831429074DECNEG0648901814905 died 3 m 52 s into `vis_lp` at the first quick update with `ModelParameterException: ell_comps must satisfy ell_comps[0]**2 + ell_comps[1]**2 < 1; got magnitude 1.00901`, raised while constructing a linear Gaussian from the max-likelihood model (log L ≈ -7.2e7, f_live 1.0, i.e. still in the prior's bad region). The other 9 lenses passed. The ell_comps box prior admits |e| ≥ 1 (21.5 % of the box); the opt-in disk projection from PyAutoFit#1538/PyAutoGalaxy#589 is not on in the pipeline. A quick update must not kill a 36 h run because the current best sample is unphysical: either the pipeline's vis_lp stage turns on the disk-constrained prior / joint clipper, or the quick update (and results-write) tolerates an out-of-disk max-likelihood instance (skip the visual, log, continue). Decide which layer owns the fix and file accordingly; this will recur across the DR1 run.

## What happened

RAL array `342301` (10-lens DR1 preliminary science run, `hpc/batch_cpu/submit_initial_lens_model_vis_lp`,
CPU stage 1 of 2). Array task 3 started `17:10:58 BST` and died at `17:14:41 BST` — the log line
immediately before the traceback is the first quick update:

```
2026-09-07 17:12:22,282 - autofit.non_linear.search.abstract_search - INFO - On-the-fly updates of the maximum likelihood model every 5000 iterations.
...
Sampling  | 5 | 1 | 4 | 4900 | 1.0000 | 1 | -71873031
2026-09-07 17:14:41,841 - autofit.non_linear.fitness - INFO - Performing quick update of maximum log likelihood fit image and model.results
```

`f_live` is still `1.0000` and `log Z ≈ -7.19e7` — the search has not left the prior yet, so the
"best" sample so far is exactly the kind of point that has no business being turned into a physical
instance. Tasks 0, 1, 2, 4–9 all cleared the same update and were still running an hour later.

## The traceback (verbatim, last 25 lines of `error.342301_3.err`)

```
  File "/mnt/ral/jnightin/PyAuto/PyAuto/lib/python3.12/site-packages/nautilus/sampler.py", line 865, in evaluate_likelihood
    result = self.likelihood(args)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/ral/jnightin/PyAuto/PyAutoFit/autofit/non_linear/fitness.py", line 533, in call_wrap
    self.manage_quick_update(parameters=parameters, log_likelihood=log_likelihood)
  File "/mnt/ral/jnightin/PyAuto/PyAutoFit/autofit/non_linear/fitness.py", line 619, in manage_quick_update
    instance = self.model.instance_from_vector(vector=self.quick_update_max_lh_parameters, xp=self._xp)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/ral/jnightin/PyAuto/PyAutoFit/autofit/mapper/prior_model/abstract.py", line 830, in instance_from_vector
    return self.instance_for_arguments(
  ...
  File "/mnt/ral/jnightin/PyAuto/PyAutoFit/autofit/mapper/prior_model/prior_model.py", line 541, in _instance_for_arguments
    result = self.cls(**constructor_arguments)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/ral/jnightin/PyAuto/PyAutoGalaxy/autogalaxy/profiles/light/linear/gaussian.py", line 28, in __init__
    super().__init__(centre=centre, ell_comps=ell_comps, intensity=1.0, sigma=sigma)
  File "/mnt/ral/jnightin/PyAuto/PyAutoGalaxy/autogalaxy/profiles/light/standard/gaussian.py", line 41, in __init__
    super().__init__(centre=centre, ell_comps=ell_comps, intensity=intensity)
  File "/mnt/ral/jnightin/PyAuto/PyAutoGalaxy/autogalaxy/profiles/light/linear/abstract.py", line 74, in __init__
    super().__init__(*args, **kwargs)
  File "/mnt/ral/jnightin/PyAuto/PyAutoGalaxy/autogalaxy/profiles/light/abstract.py", line 48, in __init__
    super().__init__(centre=centre, ell_comps=ell_comps)
  File "/mnt/ral/jnightin/PyAuto/PyAutoGalaxy/autogalaxy/profiles/geometry_profiles.py", line 237, in __init__
    validate.validate_ell_comps(ell_comps=ell_comps)
  File "/mnt/ral/jnightin/PyAuto/PyAutoGalaxy/autogalaxy/profiles/validate.py", line 159, in validate_ell_comps
    raise exc.ModelParameterException(
autogalaxy.exc.ModelParameterException: ell_comps must satisfy ell_comps[0]**2 + ell_comps[1]**2 < 1; got (np.float64(0.7157813669373315), np.float64(0.7111659244815104)), whose magnitude is np.float64(1.0090093841973504). The axis ratio is q = (1 - f) / (1 + f) with f the magnitude of ell_comps, so f must be below 1 for q to be a valid axis ratio — at f = 1 the ellipse degenerates to q = 0 and beyond it q is negative and the profile has no geometric meaning
```

The outer frames (elided above for length) are
`scripts/initial_lens_model.py:284 fit → search.fit → abstract_search.py:584 → :740 start_resume_fit →
nautilus/search.py:255 _fit → :356 fit_x1_cpu → :516 call_search → nautilus/sampler.py:441 run → :1119
add_samples → :865 evaluate_likelihood`.

## The exact frames

**The search.** `af.Nautilus` — `scripts/initial_lens_model.py` builds the `vis_lp` stage as
`af.Nautilus(name="vis_lp", n_live=750, batch_size=50, iterations_per_quick_update=..., n_like_max=200000)`.
This is *not* a gradient search: the August `ell_comps` corner work
(`feedback_gradient_lanes_settle_outside_ell_comps_disk`) was measured on MultiStartProdigy lanes, and
the conclusion "gradient lanes settle in the corner" does not cover this. Nautilus reaches the same
corner simply by sampling the prior, which is why `f_live` is still 1.0.

**The quick-update path.** `autofit/non_linear/fitness.py`. `call_wrap` (line ~533) calls
`manage_quick_update` on *every* likelihood evaluation; when `quick_update_count` crosses
`iterations_per_quick_update` the hook does, in order:

```python
instance = self.model.instance_from_vector(vector=self.quick_update_max_lh_parameters, xp=self._xp)

if self._background_quick_update is not None:
    self._background_quick_update.submit(self.analysis, self.paths, instance)
else:
    try:
        self.analysis.perform_quick_update(self.paths, instance)
    except NotImplementedError:
        pass
```

The `try` guards `perform_quick_update`, but the `instance_from_vector` line above it is **unguarded**,
and the whole hook runs inside the likelihood call the sampler is driving. So a model-construction
exception is not a failed visual — it unwinds through `nautilus.sampler.evaluate_likelihood` and
terminates the process, before any `.completed` marker or `samples.csv`.

Note this is a *different* failure point from PyAutoFit#1487, which was the same exception raised at
results-write via `SamplesSummary` / `max_log_likelihood_instance` (one sample, raising policy). #1487's
fix protected the end of the run; this one fires 2 minutes into it and there is no partial result to
salvage.

**Where the exception is raised.** `autogalaxy/profiles/validate.py:159 validate_ell_comps`, reached from
`geometry_profiles.py:237 EllProfile.__init__`. Values `(0.71578, 0.71117)`, magnitude `1.00901`.

**Why the source MGE and not the lens MGE.** `scripts/initial_lens_model.py` already tightens the *lens*
bulge basis by hand:

```python
# Tighten the lens ell_comps TruncatedGaussianPrior bounds from the
# library default of [-1, 1] to [-0.5, 0.5]. ...
ell_0 = af.TruncatedGaussianPrior(mean=0.0, sigma=0.3, lower_limit=-0.5, upper_limit=0.5)
```

`[-0.5, 0.5]²` has a corner magnitude of `0.707` — always inside the unit disk, so the lens basis
*cannot* produce this. The **source** basis is built by
`al.model_util.mge_model_from(...)` with no such override, so its Gaussians keep the library default
from `autogalaxy/config/priors/light/linear/gaussian.yaml`:

```yaml
ell_comps_0:
  type: TruncatedGaussian
  mean: 0.0
  sigma: 0.3
  lower_limit: -1.0
  upper_limit: 1.0
```

A per-component box on `[-1, 1]` whose corner is at `|e| = √2`. Both offending components are `≈ 0.71`,
i.e. above the lens cap and inside the source box. The pipeline knew about the corner on one side of the
model and not the other.

## Prior art — what already exists and is not on

- **PyAutoFit#1538 + PyAutoGalaxy#589** (merged 2026-08-28) shipped the joint disk projection:
  `__model_ball_constraints__` on `EllProfile` (radius `convert.ELL_COMPS_MAGNITUDE_CLAMP` = 0.999),
  `AbstractModel.ball_constraint_index_pairs()`, and `ClipperPriorBoxJoint` — box clip then a jittable
  radial shrink. It is **opt-in**, and `grep` over `euclid_strong_lens_modeling_pipeline/scripts`,
  `config/` and `util.py` finds no `ClipperPriorBoxJoint` / `ball_constraint` reference: the pipeline
  does not turn it on.
- **PyAutoFit#1540** (follow-up) made the joint clipper compose with the scaler/bijector.
- **PyAutoFit#1487** made `Result.instance` fall back to `Samples.max_log_likelihood()` — the
  results-write channel only.
- `draft/feature/autogalaxy/ell_comps_joint_disk_constraint.md` is the *library design* prompt behind
  #1538/#589. It asks whether the geometry should change; it does not cover an unguarded quick-update
  hook or the pipeline's opt-in status, and it is scoped to gradient lanes.

## The question this task has to answer

**Which layer owns the fix?** The two candidates are not exclusive and the task should say so explicitly:

1. **PyAutoFit (recommended primary).** A quick update is a *convenience render*. Nothing it does should
   be able to terminate a search. Wrap the instance construction (and the analysis call) so a
   model-construction failure logs a skip and the search continues — the same shape as the existing
   `except NotImplementedError: pass`, widened to the exception classes a model constructor can raise.
   This fixes the class of failure for every search, every profile and every user, not just this run.
   Decide whether the same guard is owed on the `_background_quick_update` branch and on the
   `result_max_lh_info_from` / `output_model_results` tail that follows it.
2. **euclid_strong_lens_modeling_pipeline (recommended secondary).** Turn the shipped disk projection on
   for `vis_lp` (and `vis_pix`) — the `ClipperPriorBoxJoint` route — or, at minimum, give the source MGE
   the same `[-0.5, 0.5]` box the lens MGE already has, and say why the two sides differed. This removes
   the unphysical region from the sampled space rather than tolerating it downstream.

Argument for doing both: (1) alone leaves 21.5 % of the source `ell_comps` box non-physical and every
downstream consumer (results-write, aggregator, latent summaries) exposed to the same instance; (2)
alone leaves the unguarded hook able to kill a run on any *other* model-constraint violation.

## Blast radius

10-lens DR1 preliminary run, 1 lens lost outright (~36 h of a CPU array slot when the full two-stage
`vis_lp` + `vis_pix` sequence is counted). The DR1 run scales this up; a per-lens ~10 % kill rate at the
first quick update is not survivable at DR1 volume, and the failure is silent in the sense that it looks
like a modelling/NaN failure rather than a visualisation one.

## Acceptance

- The layer decision is recorded with reasons, and whichever legs are taken are stated (not silently
  narrowed to one).
- A regression test in PyAutoFit drives a quick update whose stored max-likelihood vector maps to an
  invalid instance and asserts the search survives and logs a skip.
- If the pipeline leg is taken: the `vis_lp` model's source basis can no longer produce `|e| ≥ 1`, shown
  by construction (prior bounds) or by the clipper being on, and the change is reflected in the local
  `euclid_dr1_prelim` clone's rerun of dataset
  `Tile102007903RA0668831429074DECNEG0648901814905`.
- The relationship to PyAutoFit#1487 and #1538/#589 is stated: which channel each one closes, and that
  the quick-update channel was open until this task.

## Evidence

- RAL: `/mnt/ral/jnightin/euclid_dr1_prelim/hpc/batch_cpu/error/error.342301_3.err` (7,888 B) and
  `output/output.342301_3.out` (11,054 B; the nine siblings are ~100 KB and still running).
- Cortex phase: `phases/euclid_dr1_prelim/dr1_prelim_10_lens_science_run.md`.
- Local clone of the pipeline holding the run: `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim`
  (`origin` = `PyAutoLabs/euclid_strong_lens_modeling_pipeline`), `scripts/initial_lens_model.py`.
