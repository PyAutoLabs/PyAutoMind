# A joint unit-disk constraint (or reparameterisation) for `ell_comps`

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoFit
Themes:
- jax-gradient
- samplers
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: needs-slicing
Filed: 2026-09-01
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/594 (opened 2026-09-01 as a Cortex gate ref; reuse in start_dev — never open a second)

## The question

`ell_comps` is a two-component elliptical parameterisation whose physical domain
is the **unit disk** (|e| ≤ 1), but it is priored and clipped as a **per-component
box**. The box is not the disk, and the corner of the box is where gradient
searches go to die. Should PyAutoGalaxy (with PyAutoFit's prior/clipper
machinery) offer a **joint disk constraint** on the pair, or a
**reparameterisation** whose whole domain is physical? This is a library
question and is deliberately filed as a Mind prompt rather than implemented in
the profiling repo.

## The measurement that motivates it

From the JAX inference programme ledger
(`autolens_profiling/results/notes/inference/PROGRAMME.md`, work item **W10**):

> Non-physical `ell_comps`: 1,252/6,240 gradient-lane best points sit outside the
> unit disk (20.1 %; 31.5 % of final points), max |e| = 1.41421 = the box corner.
> The per-component `ell_comps` box admits 21.5 % non-physical volume,
> `validate_ell_comps` is silent on JAX tracers, and the clipper is faithful to
> the wrong box — so lanes settle there, and it is both the Phase-4 degradation
> channel and the Phase 8B crash channel. A joint disk constraint /
> reparameterisation is a library question — filed as PyAutoMind draft
> `feature/autogalaxy/ell_comps_joint_disk_constraint.md`, NOT implemented here

Four facts inside that, each independently actionable:

1. **20.1 % of gradient-lane best points are non-physical** (1,252 of 6,240), and
   31.5 % of *final* points are. `max |e| = 1.41421` is √2 — exactly the box
   corner, which is the signature of the box, not of the data.
2. **The box admits 21.5 % non-physical volume.** The measured 20.1 % is very
   close to what you would get by sampling the box uniformly, so the lanes are
   not being pushed there by the likelihood — the parameterisation simply lets
   them go there.
3. **`validate_ell_comps` is silent on JAX tracers.** The existing guard does not
   fire under `jit`/`grad`, so nothing catches it in the gradient path.
4. **The clipper is faithful to the wrong box.** `ClipperPriorBoxJoint` does what
   it is asked; what it is asked for is the box.

The same corner shows up in the Phase 8B log-coordinate bijector A/B (same
ledger, "Phase 8B log-coordinate bijector A/B (W5)" row):

> **23 of 39 best points are non-physical (59 %), clustered at the |e|=1.41421 box
> corner** — a property of the pixelized cells' box-clipped `ell_comps` geometry
> (W10), not of the bijector.

At 59 % this is the majority of a completed 39-arm campaign, and it forced a
reading caveat on the whole verdict.

## The crash channel — PyAutoFit#1535

The failure is not only a quality problem. In the same 8B campaign, **six
finished arms crashed at results-write on out-of-unit-disk `ell_comps`**
(PyAutoFit#1535) and had to be rebuilt offline from `search_internal.dill`. So a
box-legal, disk-illegal best point costs an A100 arm outright: the search
completes, and the write fails. Any fix should say what happens to that channel.

## What a good answer looks like

Not a decision made here — the point of the prompt is to ask the library the
question with the evidence attached. Plausible shapes, in rough order of
invasiveness:

- **A joint prior/clipper constraint** on the `ell_comps` pair, so the sampled
  region *is* the disk. Needs a form the gradient path can honour (differentiable,
  tracer-safe) rather than a post-hoc rejection.
- **A reparameterisation** whose full domain maps into the disk (e.g. a magnitude
  bounded by construction with a free angle), so no constraint is needed at all —
  at the cost of a coordinate change that every downstream consumer of `ell_comps`
  and every existing prior config has to be checked against.
- **A tracer-safe `validate_ell_comps`** as the minimum, so the condition is at
  least detectable under `jit`/`grad` even if the geometry is unchanged.

Whatever is chosen must be evaluated on the gradient lanes, not only on
nested-sampling runs: the 20.1 % is a *gradient-lane* number, and the whole
motivation is that gradient searches settle in the corner.

## Acceptance

- A decision recorded with reasons: joint constraint, reparameterisation, or
  neither with a stated alternative.
- Whatever lands is exercised under JAX `jit`/`grad`, with evidence that the
  non-physical fraction moves (the 20.1 % / 59 % numbers are the before).
- The PyAutoFit#1535 results-write crash channel is explicitly addressed —
  fixed, or stated to be out of scope with the reason.
- Backward compatibility of existing `ell_comps` priors and configs is stated,
  not assumed.
