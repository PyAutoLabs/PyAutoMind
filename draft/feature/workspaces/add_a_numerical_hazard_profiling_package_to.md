# Add a numerical-hazard profiling package to autolens_profiling

Type: feature
Target: workspaces
Repos:
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Create a new first-class package in `@autolens_profiling` under `misc/`, with
subfolders, that profiles model components — and their interaction with the
linear solver — for the numerical properties that determine how a likelihood
surface behaves under sampling.

This is scaffolding work. Build the capability and the results convention; do
not generate the full result set in this task (it will be re-run in
autolens_profiling once the package exists). The one exception is the written
summary described under "Seed result" below.

## Why this is needed

Downstream profiling tasks measure likelihood evaluation and gradient
performance for samplers. Those measurements are uninterpretable without knowing
where the surface is non-smooth: a flat plateau, an active-set kink or a
non-finite derivative changes sampler behaviour far more than a few percent of
evaluation time does. The organism currently has no systematic record of where
those sites are, so each investigation rediscovers them by hand.

An ad-hoc audit of three components (MGE lens light, power-law mass, external
shear) turned up fourteen such sites, including one that silently changes a
scientific result. That audit is the specification for what this package should
detect automatically, and is summarised in the artifact
https://claude.ai/code/artifact/9c6cc3b0-4652-47c4-aa81-8abccb350cd3

## What to build

Extend coverage to **all light and mass profiles and their combinations**, on
**both the JAX and numpy backends**. The natural matrix is
`component x backend x hazard class`, and the package should make adding a new
profile or a new hazard class a small, local change rather than a new script.

Support these hazard classes as the initial taxonomy — each derived from a real
finding, none speculative:

- **Saturating reparametrisations.** A clamp that maps an unbounded region of
  parameter space onto one value, producing an exactly flat likelihood with zero
  gradient. The `ell_comps` magnitude clamp is the reference case.
- **Active-set kinks.** The non-negative linear solver pins basis components at
  exactly zero, so the likelihood is piecewise-smooth and a pinned component
  contributes no gradient. This is the core of the linear-solver interaction.
- **Conditioning floors.** Absolute values added to a curvature-matrix diagonal
  to make an ill-conditioned solve tractable, whose effective strength depends
  on the data's flux and noise scale rather than being scale-free.
- **Non-finite value sites.** Parameter values inside the prior at which the
  model returns NaN or inf — including exact prior boundaries, which samplers do
  reach.
- **Non-finite gradient sites.** Points where the value is finite and correct
  but the derivative is not, typically a square root evaluated at zero. These
  are invisible to any check that only inspects likelihood values.
- **Backend divergence.** Places where the numpy and JAX paths implement
  different approximations of the same quantity and disagree by more than
  round-off. Report as relative error against the more exact path, as a function
  of the parameter that drives the divergence.
- **Structural degeneracies.** Directions in which a parameter stops affecting
  the likelihood as another approaches a prior edge — funnels that waste live
  points and defeat mass-matrix adaptation.

Each check should report the parameter region affected, the fraction of prior
volume it covers under that component's default priors, and which backends it
applies to. Prior-volume weighting is what separates a real risk from a curiosity
and should be built in from the start, not added later.

## Results convention

Write results into the repo's existing `results/` folder, following the style
already used there for overall results, so they persist as organism memory.
Two consumers matter and should shape the format:

- **Downstream tasks** that profile likelihood and gradient performance read
  these results programmatically, so emit a machine-readable record alongside
  any human-readable summary.
- **A human** reading the results months later needs the finding, its code
  anchor, and how it was measured — a bare number is not enough.

Keep the record keyed so a re-run can be compared against the previous one; the
point of storing them is to notice when a hazard appears, moves or is fixed.

## Seed result

Write one good summary of the `ell_comps` clamp work into the `results/` folder
as part of this task, in the convention the package establishes. It is the
worked example that shows the format carrying real content, and the finding is
already fully characterised:

- `convert.py:71-77` clamps the magnitude at `0.999`, pinning the axis ratio at
  `q = 5.0025e-4` for every `|ell_comps| >= 1`. Present since 2020-11-08. The
  region is a finite, very low, exactly flat likelihood — never NaN — so
  samplers were never rejecting it, only wasting effort in it.
- The constructor guard added in issues #440/#568 (`profiles/validate.py:145-167`)
  rejects the region on numpy via `FitException` to the resample sentinel, but
  returns early for tracers, and `Fitness.call`'s JAX branch has no exception
  handling — so under gradient-based sampling the plateau is unchanged.
- Prior volume beyond the unit circle: 0.22% under the default
  `TruncatedGaussian(0, 0.3)` per component, 5.1% at sigma 0.5, 21.4% under
  `Uniform(-1, 1)` per component.

## Boundary

All work lands in `@autolens_profiling`. This task creates the package, its
structure and its results convention, plus the one seed summary. It does not
touch or fix any of the findings in the source libraries — each of those is its
own task, filed separately. Source-library file paths cited above are evidence
for the seed summary, not work to be done here.

<!-- formalised by the Intake (Conception) Agent on 2026-08-13 from file:/tmp/claude-0/-home-user/ed97e64a-5c90-56a4-96ce-23855e9c9173/scratchpad/prompt_body.md -->
