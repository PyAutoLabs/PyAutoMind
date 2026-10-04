# Forward-mode gradient is NaN for FitPositionsImagePairAll(Solved) — released default gradient_mode="forward"

Type: bug
Target: autolens
Repos:
- PyAutoLens
Themes:
- point-source
- jax
- gradients
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-28
Issued: 2026-10-04
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/767
Found-by: autolens_profiling#350 (point-source A100 phase 0+1, RAL job 366916), independently reproduced 2026-09-28

## Symptom

Since 2026.9.27.2 (PyAutoLens#752 + PyAutoFit#1649), `AnalysisPoint.gradient_mode = "forward"`
(`autolens/point/model/analysis.py:49`) makes every gradient search (`Fitness.grad`,
`af.MultiStartAdam` & co.) differentiate the point-source likelihood with `jax.jacfwd`. For the
**image-plane all-pairs** fits `FitPositionsImagePairAll` / `FitPositionsImagePairAllSolved` the
forward gradient is **NaN in every component**, at every point tested (16 stream points, A100 and
laptop CPU), so every start is non-finite and the search cannot move. Reverse mode is finite and
agrees with a finite difference at h=1e-3. Workaround: `gradient_mode="reverse"` on the search.

Reproduction through the library's own path (`Fitness.call` via
`autofit.jax.gradient.value_and_grad_from`, as `MultiStartGradient` builds it at `search.py:1028`;
model registered with `register_model`), simple SIE, autolens_profiling
`dataset/point_source/simple/point_dataset_positions_only.json`, prior-median point, CPU fp64:

| | value | gradient |
|---|---|---|
| forward / `Fitness.grad` | 7.743201200876812 | NaN ×5 |
| reverse | 7.743201200876812 | [-41.62, 53.13, 31.79, 2.80, 1781.74] |
| FD h=1e-3 | | [-48.5, 57.8, 18.0, -4.2, 1727.8] |

Controls, forward == reverse and finite: `FitPositionsSource`, `FitPositionsSourceSolved`,
`FitPositionsImagePairRepeatSolved`. `FitPositionsImagePairAll` (unsolved) shares the same
χ² code, confirmed by reading it but not run. PointFlux not checked.

## Root cause (localised, not yet fixed)

The solver's JVP is fine: per-parameter `jax.jvp` gives model-position tangents exactly 0.0 on
all padded rows. The NaN is created in the all-pairs χ²:
- padded model positions are `inf` sentinels (`autolens/point/solver/point_solver.py:274-276`);
- `square_distance` (`autolens/point/fit/positions/image/abstract.py:117`) computes `(d-inf)**2`,
  whose forward tangent is `2(d-inf)·0 = inf·0 = NaN`;
- that flows into `log_p` (`pair_all.py:93`, `-inf` on padded columns), then
  `exp(log_ps - max)` (`pair_all.py:134`), tangent `exp(-inf)·NaN = NaN`, summed into log L.
  NaN tangents sit exactly on the padded columns.
- Reverse mode escapes only because the NaN cotangent on padded rows is discarded by
  `where(finite, dtheta, 0)` in `implicit_diff.py:102`.

## Fix direction

In `FitPositionsImagePairAll.all_permutations_log_likelihoods`, substitute a finite placeholder for
padded model positions before `square_distance` and mask their `log_p` to `-inf` with `jnp.where`
(the double-where pattern), so the primal is bit-identical and both modes are finite. Add a unit
test (JAX, tiny grid) asserting forward == reverse and finite for ImagePairAll(Solved); keep the
`gradient_mode="forward"` default (it is the right choice once the NaN is gone). Check the primal
fiducial stays bit-exact (autolens_profiling gate `FIDUCIAL_SOLVED_LOG_L_BY_BACKEND`, CPU `…812`,
GPU `…806`). Consider a patch release: the defect is live for users of 2026.9.27.2.

## Reproduction script (verbatim)

```python
import os, sys
import numpy as np, jax, jax.numpy as jnp
import autofit as af, autolens as al
from autofit.jax import register_model
from autofit.jax import gradient as G
from autofit.non_linear.fitness import Fitness

DS = "/home/jammy/Code/PyAutoLabs/lens/autolens_profiling/dataset/point_source/simple/point_dataset_positions_only.json"
dataset = al.from_json(file_path=DS)
grid = al.Grid2D.uniform(shape_native=(100,100), pixel_scales=0.2)
solver = al.PointSolver.for_grid(grid=grid, pixel_scale_precision=1e-3, magnification_threshold=0.1, neighbor_degree=1)

def model_for(point_cls):
    mass = af.Model(al.mp.Isothermal)
    mass.centre.centre_0 = af.GaussianPrior(mean=0.0, sigma=0.005)
    mass.centre.centre_1 = af.GaussianPrior(mean=0.0, sigma=0.005)
    mass.einstein_radius = af.GaussianPrior(mean=1.6, sigma=0.05)
    mass.ell_comps.ell_comps_0 = af.GaussianPrior(mean=0.05263158, sigma=0.01)
    mass.ell_comps.ell_comps_1 = af.GaussianPrior(mean=0.0, sigma=0.01)
    lens = af.Model(al.Galaxy, redshift=0.5, mass=mass)
    source = af.Model(al.Galaxy, redshift=1.0, point_0=af.Model(point_cls))
    m = af.Collection(galaxies=af.Collection(lens=lens, source=source))
    register_model(m)
    return m

def run(label, fit_cls, point_cls):
    model = model_for(point_cls)
    analysis = al.AnalysisPoint(dataset=dataset, solver=solver, fit_positions_cls=fit_cls, use_jax=True)
    fitness = Fitness(model=model, analysis=analysis, use_jax_jit=False)
    x0 = jnp.asarray(model.physical_values_from_prior_medians, dtype=float)
    print(f"\n== {label}: declared mode = {G.resolve_gradient_mode(analysis)} ; params {model.total_free_parameters}")
    vf, gf = jax.jit(G.value_and_grad_from(fitness.call, "forward"))(x0)
    vr, gr = jax.jit(G.value_and_grad_from(fitness.call, "reverse"))(x0)
    gF = jax.jit(fitness._grad)(x0) if False else None
    f = jax.jit(fitness.call)
    fd = []
    for i in range(len(x0)):
        h = 1e-6 * max(1.0, abs(float(x0[i])))
        e = jnp.zeros_like(x0).at[i].set(h)
        fd.append((float(f(x0+e)) - float(f(x0-e))) / (2*h))
    print("value fwd/rev:", float(vf), float(vr))
    print("fwd :", np.asarray(gf))
    print("rev :", np.asarray(gr))
    print("FD  :", np.array(fd))
    print("Fitness.grad (declared mode):", np.asarray(fitness.grad(x0)))
    return model, analysis, fitness, x0

which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all","image"):
    run("image-plane AllSolved", al.FitPositionsImagePairAllSolved, al.ps.PointSolved)
if which in ("all","source"):
    run("source-plane", al.FitPositionsSource, al.ps.Point)
if which in ("all","pair"):
    run("image-plane RepeatSolved", al.FitPositionsImagePairRepeatSolved, al.ps.PointSolved)
if which in ("all","srcsolved"):
    run("source-plane Solved", al.FitPositionsSourceSolved, al.ps.PointSolved)
```
