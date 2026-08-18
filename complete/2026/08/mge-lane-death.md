MGE multi-start lanes die on the PRIOR term, not the likelihood (lanes walk out of UniformPrior support and `resurrect=False` never redraws them — that accumulation IS the 62%)

Filed against the real `imaging/mge` cell, where the frozen-lane counter reported
`n_value_nan_lane_steps` at 62.42% and a population collapse from `alive 16/16` to
`alive 2/16`.

**Closed out 2026-08-18: cause found, written up, and every follow-up it owed
already shipped. SUPERSEDED** — the remaining confirmation legs (GPU / float64 /
multi-seed re-measurement of the 62%) are not carried forward as scoped; a larger
issue now owns this direction. Tracking issue autolens_profiling#128 is still open
and wants closing by hand.

## Cause: the deaths are in the PRIOR term, not the likelihood

The objective is `fom = -2 * (log_likelihood + sum(log_prior_list))`
(`Fitness(fom_is_log_likelihood=False)`). A `UniformPrior` is `-inf` outside its
box, and `MultiStartGradient` steps in PHYSICAL space with no projection back onto
that box. A lane that crosses a hard prior edge reads as non-finite; `resurrect=False`
never redraws it, so it stays dead for every remaining step. That accumulation **is**
the 62%.

**The likelihood never went non-finite in ~7200 lane-steps across three arms.**

This contradicts the documented assumption it was filed against:
`AbstractMultiStartGradient.resurrect`'s docstring held that `resurrect=False` is
safe on the parametric (MGE-class) cell because only a measure-zero singularity is
in play and `apply_if_finite` guards it. `apply_if_finite` does not rescue a
value-NaN lane — it only zeroes the step. Nothing was broken; the default is simply
wrong for this cell.

## Evidence

- **Per-lane autopsy at the death vectors.** 11/14 have finite likelihood at every
  pipeline stage and `sum(log_prior) = -inf` with 1-2 params outside a
  `UniformPrior`; 2/14 have NaN params (the gradient path); 1/14 unexplained.
- **Decisive arm.** Neutering `log_prior_list_from_vector` to zeros drops value-NaN
  1446 -> 215 (60.25% -> 8.96%) and survivors 2 -> 13, with all 3 residual deaths
  being NaN-params.
- **Refuted narrower hypothesis.** Widening the shear box (10 of the 11 exits) made
  it marginally *worse* — deaths moved later. Widening one box only moves the wall.
- **Reproduction.** 16x150 cloud CPU gave 1446/18/0/0 and `alive 2/16` against the
  filed 1498/9/0/0 and the same 2/16. The survival identity is exact:
  `sum(150 - k_i) = 14*150 - 654 = 1446` = `n_value_nan_lane_steps`.

## Counter-finding: the `ell_comps` plateau was MASKED, not cleared

The baseline's `n_constrained_lane_steps = 0` was a correctly-measured zero — the
positive control was sound — but it meant "nothing got that far": lanes died of
prior-exit first. With the prior deaths removed the constrained count is 667
(**27.79%**). PyAutoFit#1475's trapped-lane counter is measuring a live failure mode
on this cell, hidden behind a larger one. Lanes stop being dead and start being
STUCK.

Caveat for anyone citing it: 27.79% came from the prior-neutered DIAGNOSTIC arm and
is **not** a citable production number.

## How to read the 62% (trap)

It is a **survival integral, not a hazard rate**. A frozen lane keeps counting every
subsequent step, so the same death curve reports ~75% at 300 steps. Inverting it
gives a mean death step of ~43 of 150 — mid-descent, not bad initial draws. **Grade
any re-run on the alive-versus-step CURVE, not on recovering the scalar.**

## What shipped out of this investigation

Upstream (the instrument that made it visible):

- PyAutoFit#1475 (`004f798`) + PyAutoGalaxy#572 (`695b27c`) — the trapped-lane
  counter. Record: `complete/2026/08/frozen-lane-counter.md`.

Downstream, all 2026-08-16:

- **PyAutoFit#1477** (`1f4b66a`) — bounded stepping, phase 1: the prior-support
  clipper. Record: `complete/2026/08/prior-support-clipper.md`. (`resurrect=True` is
  NOT the fix — it redraws a lane that then walks out again.)
- **autolens_profiling#132 + PyAutoFit#1482** — phase 2 validation (issues #129/#131
  closed). Record: `complete/2026/08/clipper-validation-campaign.md`. VERDICT: do
  **not** flip the clipper default on accuracy grounds — clipping eliminates the
  deaths and does not move the answer; seed dependence swings 171,272 nats and
  dwarfs it. The momentum-reset arm is a clean negative.
- **PyAutoFit#1478** (`bbceff6`) — clipper reporting in `search.summary`
  (`Clipper`, `Clipped Lane-Steps`, `Clipped Lane-Step Rate`, `Constrained
  Lane-Steps`). Record: `complete/2026/08/clipper-usage-in-search-summary.md`. A
  `ClipperPriorBox` arm reporting ZERO clips has not exercised the clipper — that is
  a broken arm, not a null result.
- **PyAutoFit#1479** (`b6e89cd`) — `save_json` float32 crash, incidental. Record:
  `complete/2026/08/save-json-numpy-scalar-typeerror.md`. Fixing it turned up a
  second unguarded writer the prompt never named, `Samples.info_to_json`, which is
  the more dangerous one since `samples_info` gains a counter every time a search
  does.
- **PyAutoFit#1480** (`5c9244b`) — crashed-run-poisons-resume, incidental. Record:
  `complete/2026/08/crashed-run-poisons-resume.md`. What reproduces is a hard
  `JSONDecodeError` on every rerun of the same search name; `JSONDecodeError`
  subclasses `ValueError`, which is why it slipped past every guard on the resume
  path.

## Not carried forward

- **GPU / float64 / multi-seed confirmation** of the 62% at production budget. The
  filed measurement stands on a single seed per arm, cloud CPU, x64 off.
- **The `ell_comps` trapping at 27.79%**, now unmasked — drafted at
  `draft/research/autolens_profiling/ell_comps_trapping_unmasked.md`. It runs on top
  of phase 1 and can share phase 2's arms.
- **Clipper phase 3**, which was never drafted. If it is ever written it must argue
  hygiene, not accuracy; `draft/feature/autofit/clipper_in_search_identifier.md` is
  its prerequisite decision.

## Unexplained, left open

One baseline death (lane 9, step 39) re-evaluates finite in every term with all
params inside their boxes. The jitted/vmapped float32 path differs from the eager
recompute there. Single seed per arm, CPU, x64 off.

## Notes

- No worktree was ever created and the `autolens_profiling` branch
  `research/mge-lane-death` was never cut — the whole investigation ran in cloud
  sessions against the existing ~6-min CPU run, per the task's deliberate ordering
  (cause-finding first, GPU confirmation last).
- The task's boundary was investigation only. Changing the `resurrect` default
  remains a separate PyAutoFit task — it would shift every existing multi-start
  benchmark.

## Original prompt

# Find what kills MGE multi-start lanes — it is not the ell_comps plateau

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

# Find what kills MGE multi-start lanes — it is not the ell_comps plateau

@autolens_profiling

The frozen-lane counter shipped (PyAutoFit #1475, PyAutoGalaxy #572) and its
first run cleared the ell_comps plateau as a suspect for the MGE cell — and
surfaced a much larger effect nobody has characterised.

Real `imaging/mge` cell (production dataset, model and analysis via
`build_for_cell`; 16 starts x 150 steps, cloud CPU, 352s):

| counter | lane-steps | share |
|---|---:|---:|
| `n_value_nan_lane_steps` | 1498 | **62.42%** |
| `n_grad_nan_lane_steps` | 9 | 0.38% |
| `n_constrained_lane_steps` | 0 | 0.00% |

The population fell from `alive 16/16` to `alive 2/16`. **Roughly seven of every
eight starts die, and the best-fit is being found by two survivors.**

## Why this is worth a task

It contradicts a documented assumption. `AbstractMultiStartGradient`'s
`resurrect` docstring states the default `resurrect=False` is safe because "the
parametric (MGE-class) cell has only the measure-zero singularity, so the
`apply_if_finite` guard suffices". The measurement says otherwise: value-NaN,
not gradient-NaN, dominates at 62% of lane-steps, and `apply_if_finite` does not
rescue a value-NaN lane — it only zeroes the step, so the lane stays dead and
`resurrect=False` never redraws it.

If that holds at production budget, the MGE cell is running at a small fraction
of its nominal start count, and `n_starts` is not buying what it appears to.

`n_resurrections: 0` in the JSON closes the mechanism: the counter fired 1498
times and nothing was ever redrawn, which is exactly `resurrect=False` behaving
as documented. Nothing is broken — the default is simply wrong for this cell.

## Read 62% as a survival curve, not a hazard rate

**The percentage is budget-dependent by construction, so it is not a portable
number and must not be compared across budgets as if it were.** A value-NaN lane
is frozen by `apply_if_finite` and never redrawn, so it keeps counting a
value-NaN lane-step on *every* subsequent step. The 1498 is therefore the
integral under the death curve, not a per-step hazard.

That makes the number invertible, which is worth doing before spending GPU time.
With 14 of 16 lanes dead at the end and no resurrections, a lane dying at step
`k` contributes `150 - k`:

```
sum(150 - k_i) = 1498   over 14 lanes
  =>  sum(k_i) = 14*150 - 1498 = 602
  =>  mean death step ≈ 43 of 150
```

So the deaths are **neither at step 0 nor spread evenly** — they concentrate in
roughly the first third. That already discriminates between the two hypotheses in
"When they happen" below: it is not bad initial draws (`_broad_starts` filtered
those, and they would give mean ≈ 0), it is trajectories walking into a wall
early in the descent.

The corollary matters for step planning: hold that same death curve fixed and run
300 steps instead of 150, and the *same physics* reports **75%**, not 62%. A
production-budget run that comes back higher than 62% is therefore not
automatically a worse result — it may be the identical landscape measured over a
longer window. **Compare the alive-versus-step curve across budgets; use the
scalar percentage only within a fixed budget.**

## What to establish

Ordered by information per unit time, which is **not** the order they were
originally listed in. The cause is the unanswered question and it is the cheap
one; the GPU reproduction confirms an effect that has already been measured once.
Do not queue for a GPU before step 1 has been attempted.

1. **Where the NaNs come from** — the actual question. Which parameters/regions
   produce a non-finite likelihood in the MGE cell: the mask edge, a Gaussian
   `sigma` collapsing, the linear inversion / NNLS solve, the `sqrt` at r=0,
   something else. **This does not need production budget or a GPU.** The
   existing ~6-minute 16x150 CPU run already produces 1498 deaths; instrument it
   to dump each lane's parameter vector at the step its value first goes
   non-finite, and the distribution of those vectors is the answer. That is a
   minutes-long iteration loop, not a queued one. Record the finding in this
   repo's hazard index.
2. **Whether `resurrect=True` recovers the budget** on this cell, and what it
   costs. The docstring says resurrection is for pixelized sources; this evidence
   suggests the parametric cell may need it too. Measurement of the candidate
   remedy — not adoption of it (see Boundary).
3. **Whether it holds at production budget, on GPU, across seeds.** The
   measurement above is one seed at reduced budget on CPU, and the float64 GPU
   path is not the same numerics. **Grade this on the alive-versus-step curve,
   not on recovering "62%"** — per the survival-curve section above, the scalar
   is budget-dependent by construction and the same landscape reports ~75% at 300
   steps. Log `alive N/16` per step so the curves can be overlaid across budgets;
   a run that only reports the final percentage cannot be compared to this one.

**When they happen** is already partly answered and should not be re-derived from
scratch: inverting the 1498 gives a mean death step of ~43 of 150, so deaths
concentrate in the first third — trajectories walking into a wall mid-descent,
not bad initial draws that `_broad_starts` failed to filter. Step 1's per-lane
death steps should confirm or overturn that inversion; if they disagree with a
mean of ~43, the disagreement is itself a finding (it would mean lanes are
recovering and re-dying, which `resurrect=False` says they cannot).

## Boundary

Investigation and measurement, in `@autolens_profiling`. Do not change the
`resurrect` default or any search behaviour as part of this — if the evidence
supports a change, that is a separate PyAutoFit task with its own benchmark
impact, since it would shift every existing multi-start result.

## Provenance

Measured 2026-08-15 with the frozen-lane counter; see
`complete/2026/08/frozen-lane-counter.md` for the full run, the positive control
that validates the zero, and the environment notes (`jaxnnls` is a required
extra; the runner writes into `dataset/`).

<!-- formalised by the Intake (Conception) Agent on 2026-08-15 from file:/tmp/claude-0/-home-user/ef0adef1-5fcd-5111-9cdf-bcb1014fc23d/scratchpad/nan_death_prompt.md -->

## CAUSE FOUND (2026-08-15, cloud CPU) — it is the prior, not the likelihood

Written up in full on autolens_profiling#128. Summary, so the file stands alone:

`_fit` builds its objective as `Fitness(..., fom_is_log_likelihood=False,
convert_to_chi_squared=True)`:

```
fom = -2 * (log_likelihood + sum(log_prior_list))
```

A `UniformPrior` is `-inf` outside its box, and `MultiStartGradient` steps in
**physical** parameter space with **no projection back onto that box**. A lane
crossing a hard prior edge reads as non-finite; `resurrect=False` never redraws
it; it stays dead for every remaining step. That accumulation is the 62%.

**The likelihood never went non-finite** — not once in ~7200 lane-steps across
three arms. Every pipeline stage (positions penalty, deflections, convergence,
model data, residuals, chi-squared, NNLS reconstruction, log-determinants,
`figure_of_merit`) was finite at every death vector.

| arm (16x150, cloud CPU) | value-NaN | grad-NaN | constrained | dead | alive end |
|---|---:|---:|---:|---:|---:|
| reproduction | 1446 (60.25%) | 18 | 0 | 14/16 | 2 |
| shear box widened to ±1 | 1422 (59.25%) | 36 | 13 | 15/16 | 1 |
| **prior term neutered** | **215 (8.96%)** | 27 | **667 (27.79%)** | **3/16** | **13** |

Per-lane autopsy at the death vectors: 11/14 finite likelihood with
`sum(log_prior) = -inf`; 2/14 NaN params; 1/14 unexplained. All three residual
deaths in the neutered arm are NaN-params, not likelihood deaths.

The survival identity is exact: `sum(150 - k_i) = 14*150 - 654 = 1446`, which is
`n_value_nan_lane_steps` to the unit — the counter *is* the area under the death
curve.

**A narrower hypothesis was refuted.** 10 of the 11 box exits were the shear
`UniformPrior(-0.3, 0.3)`, but widening only those two priors did not collapse
the deaths — they moved later and got marginally worse. Widening one box only
moves the wall. Test the mechanism, not the parameter.

### The docstring claim is correct, and irrelevant

The parametric MGE likelihood does appear to have only measure-zero
singularities. What is wrong is using that to justify `resurrect=False`, since
the deaths come from the prior, which the claim never covered. And this is not
MGE-specific: any model with a hard-box prior and unbounded stepping has it.

### Counter-finding: the ell_comps plateau was MASKED, not cleared

The baseline's `n_constrained_lane_steps = 0` was correctly measured and the
positive control was sound — but it meant *"nothing got that far"*, not
*"nothing gets trapped there"*. Lanes died of prior-exit before reaching the
saturation plateau. Remove the prior deaths and the constrained count is **667
(27.79%)**. #1475's counter is measuring a live failure mode on this cell that
was hidden behind a larger one. Lanes stop being dead and start being **stuck**.

### Out of this task's boundary, now owed elsewhere

1. **PyAutoFit** — bounded stepping (projection/clipping onto prior support) or
   soft-walled priors. `resurrect=True` is *not* the fix: it redraws a lane that
   then walks out again.
2. **The ell_comps trapping at 27.79%**, now that it is visible.

### Still owed here

GPU / float64 / multi-seed confirmation, graded on the alive-versus-step curve.
One caveat: baseline lane 9 (step 39) re-evaluates finite in every term with all
params inside their boxes — the jitted/vmapped float32 path differs from the
eager recompute there, unexplained.

## Reproducer

Both scripts below are self-contained and were used to produce the numbers in
this prompt. They live here rather than in `@autolens_profiling` because they
are throwaway measurement drivers, not part of that repo's script tiers — copy
them out to run, do not commit them there.

### The measured result (verbatim)

```json
{
  "cell": "imaging/mge",
  "instrument": "hst",
  "hardware": "cloud_cpu",
  "n_starts": 16,
  "n_steps": 150,
  "batch_size": null,
  "lane_steps": 2400,
  "wall_s": 352.21100759506226,
  "free_parameters": 15,
  "counters": {
    "n_value_nan_lane_steps": 1498,
    "n_grad_nan_lane_steps": 9,
    "n_constrained_lane_steps": 0,
    "n_resurrections": 0
  }
}```

### `rerun_cell.py` — runs one production cell at reduced budget

Invoke as `SEARCHES_DISABLE_VIZ=1 N_STARTS=16 N_STEPS=150 python rerun_cell.py mge`.
Environment: Python 3.12+, `pip install jaxnnls`, and install `autolens` with
`--no-deps` if using editable local `autofit`/`autogalaxy`.

The `MESH_SHAPE` / `HILBERT_PIXELS` block is **inert for this cell** — it only
touches the pixelization knobs, and `mge` has no mesh. The 62% was measured on
the unmodified production MGE cell; nothing was shrunk. The block is there for
the pixelized cells, and for those the image-plane grid at `mask_radius 3.5`
dominates the cost anyway, so shrinking the mesh is the wrong lever there too.
Leave both unset.

```python
"""Re-run one autolens_profiling search cell on CPU at reduced budget, to read
the new constrained-lane counter.

Uses the repo's own `build_for_cell` so the dataset, model and analysis are
exactly the production ones. Only the search budget is reduced (n_starts,
n_steps, batch_size) — that changes how thoroughly the space is explored, not
the shape of the likelihood surface, which is what the counter reports on.
"""

import os, sys, time, json
from pathlib import Path

ROOT = Path("/workspace/pyautolabs/autolens_profiling")
sys.path.insert(0, str(ROOT / "scripts" / "misc"))
sys.path.insert(0, str(ROOT))

# Dataset paths in `_setup.py` are relative to the repo root.
os.chdir(ROOT)

import numpy as np
import autofit as af

from searches import _setup
from searches._setup import build_for_cell

# Optional mesh shrink. The production fiducial is a (39, 39) = 1521-pixel mesh
# with 1500 Hilbert pixels, whose JIT compile alone exceeds an hour on CPU. A
# shrunken mesh is NOT the production cell — the landscape differs — but it
# keeps the same clamp, the same unbounded stepping, and the same mesh-shaped
# likelihood, so it can still say whether lanes reach the plateau at all.
MESH = os.environ.get("MESH_SHAPE")
HILBERT = os.environ.get("HILBERT_PIXELS")
if MESH:
    n = int(MESH)
    _setup._PIXELIZATION_MESH_SHAPE = (n, n)
    print(f"  [shrunk] pixelization mesh {(n, n)} (production is (39, 39))")
if HILBERT:
    _setup._HILBERT_PIXELS = int(HILBERT)
    print(f"  [shrunk] hilbert pixels {HILBERT} (production is 1500)")

MODEL_TYPE = sys.argv[1] if len(sys.argv) > 1 else "mge"
N_STARTS = int(os.environ.get("N_STARTS", "16"))
N_STEPS = int(os.environ.get("N_STEPS", "150"))
BATCH = os.environ.get("BATCH_SIZE")
INSTRUMENT = os.environ.get("INSTRUMENT", "hst")

print(f"=== cell: imaging/{MODEL_TYPE} [{INSTRUMENT}] "
      f"starts={N_STARTS} steps={N_STEPS} batch={BATCH or 'all'} ===")

t0 = time.time()
dataset, model, analysis = build_for_cell(
    dataset_class="imaging",
    model_type=MODEL_TYPE,
    instrument=INSTRUMENT,
    use_jax=True,
    use_mixed_precision=False,
)
print(f"  build: {time.time() - t0:.1f}s   free parameters: {model.total_free_parameters}")

constrained = model.constrained_model_tuples()
print(f"  components declaring a model constraint: {len(constrained)}")
for path, sub in constrained[:8]:
    print(f"    {'.'.join(p for p in path if p) or '<root>'} -> {sub.cls.__name__}")

kwargs = dict(
    name=f"rerun_{MODEL_TYPE}",
    n_starts=N_STARTS,
    n_steps=N_STEPS,
    iterations_per_log=25,
    convergence=af.MultiStartGradientConvergence(check_for_convergence=False),
)
if BATCH:
    kwargs["batch_size"] = int(BATCH)

search = af.MultiStartProdigy(**kwargs)

t0 = time.time()
result = search.fit(model=model, analysis=analysis)
wall = time.time() - t0

primary = result[0] if isinstance(result, list) else result
si = primary.search_internal
if not isinstance(si, dict):
    si = getattr(si, "__dict__", {}) or {}

counters = {
    k: si.get(k)
    for k in (
        "n_value_nan_lane_steps",
        "n_grad_nan_lane_steps",
        "n_constrained_lane_steps",
        "n_resurrections",
    )
}
lane_steps = N_STARTS * N_STEPS

print(f"\n=== imaging/{MODEL_TYPE} — {wall:.1f}s wall, {lane_steps} lane-steps ===")
for k, v in counters.items():
    pct = f"({100.0 * v / lane_steps:.2f}% of lane-steps)" if isinstance(v, int) and lane_steps else ""
    print(f"  {k:<28} {v}  {pct}")

out = {
    "cell": f"imaging/{MODEL_TYPE}",
    "instrument": INSTRUMENT,
    "hardware": "cloud_cpu",
    "n_starts": N_STARTS,
    "n_steps": N_STEPS,
    "batch_size": int(BATCH) if BATCH else None,
    "lane_steps": lane_steps,
    "wall_s": wall,
    "free_parameters": model.total_free_parameters,
    "counters": counters,
}
dest = Path(f"/tmp/claude-0/-home-user/ef0adef1-5fcd-5111-9cdf-bcb1014fc23d/scratchpad/rerun_{MODEL_TYPE}.json")
dest.write_text(json.dumps(out, indent=2))
print(f"\nwrote {dest}")
```

### `validate_zero.py` — the positive control that makes the zero meaningful

Proves the counter was watching that exact model and would have fired. Note it
probes with `jnp` arrays: concrete Python floats trip `validate_ell_comps` and
raise before the constraint is ever reached.

What it covers, precisely: constraint **discovery** on the production model,
**evaluation** (zero inside / positive outside), and the **predicate**. All four
checks call those pieces directly with hand-built arrays, so none of them
exercises the search loop that actually accumulates the counter. The thing that
closes that last gap is in the result JSON rather than in this script:
`n_value_nan_lane_steps` and `n_constrained_lane_steps` come back as integer `0`
and `1498`, not `null` — and `rerun_cell.py` reads them with `si.get(k)`, which
would have given `null` had `_fit` never written the key. So the zero is a
measured zero, not an absent one. **Keep that distinction when re-running: a
`null` in the counters block means the plumbing broke, and it is not the same
finding as a `0`.**

```python
"""Positive control: prove the zero from imaging/mge is a real zero.

A count of 0 is only evidence if the counter would have fired had a lane been
trapped. This builds the SAME production model the mge cell used, then checks:

  1. the constraint is discovered on it at all;
  2. a vector inside the valid region reports zero violation;
  3. a vector placed beyond the clamp reports a positive violation;
  4. the lane-count predicate turns that into a counted lane.

If (1) failed, the zero would mean "nothing was watching", not "nothing happened".
"""

import os, sys
from pathlib import Path

ROOT = Path("/workspace/pyautolabs/autolens_profiling")
sys.path.insert(0, str(ROOT / "scripts" / "misc"))
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import numpy as np
import jax.numpy as jnp
import autofit as af
from autofit.non_linear.search.mle.multi_start_gradient.search import (
    AbstractMultiStartGradient,
)
from searches._setup import build_for_cell

dataset, model, analysis = build_for_cell(
    dataset_class="imaging",
    model_type="mge",
    instrument="hst",
    use_jax=True,
    use_mixed_precision=False,
)

# --- 1. discovery on the real production model
constrained = model.constrained_model_tuples()
print(f"1. constrained components discovered: {len(constrained)}")
for path, sub in constrained:
    print(f"     {'.'.join(p for p in path if p) or '<root>'} -> {sub.cls.__name__}")
assert constrained, "NOTHING WAS WATCHING — the zero would be meaningless"

# JAX arrays, not Python floats: concrete scalars trip the component's own
# `validate_ell_comps` guard before the constraint is ever reached (exactly as
# the method's docstring warns). The real search path is traced, where that
# guard returns early — jnp arrays reproduce that.
vector = [jnp.asarray(float(v)) for v in model.physical_values_from_prior_medians]

# --- 2. valid region -> zero
inside = float(model.model_constraint_from_vector(vector, xp=jnp))
print(f"\n2. violation at prior medians: {inside}")

# --- 3. beyond the clamp -> positive.
# Brute-force which parameters drive the constraint rather than guessing names:
# push each one past the clamp in turn and see which move the violation.
responders = []
for i in range(len(vector)):
    probe = list(vector)
    probe[i] = jnp.asarray(3.0)
    v = float(model.model_constraint_from_vector(probe, xp=jnp))
    if v > 0.0:
        responders.append((i, v))

print(f"3. parameters that drive the constraint when pushed to 3.0: "
      f"{len(responders)} of {len(vector)}")
for i, v in responders[:6]:
    print(f"     index {i:>3} -> violation {v:.4f}")
outside = responders[0][1] if responders else 0.0

# --- 4. the predicate counts it
counted = AbstractMultiStartGradient._constrained_lane_count(
    alive=np.array([True, True]),
    grad_finite=np.array([True, True]),
    constraint_violation=np.array([inside, outside]),
)
print(f"4. lanes counted from [valid, trapped]: {counted}")

ok = bool(constrained) and inside == 0.0 and outside > 0.0 and counted == 1
print(f"\nVERDICT: the mge zero is {'a REAL zero' if ok else 'NOT TRUSTWORTHY'}")
sys.exit(0 if ok else 1)
```
