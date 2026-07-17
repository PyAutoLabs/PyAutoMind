# PROBE: is changing `log_det_regularization_matrix_term` absolutely justified?

**This is an adversarial review request, not an implementation task. Your job is
to try to REFUTE the analysis below.** It proposes touching core PyAutoArray
source in a way that moves every reported Bayesian evidence in PyAutoLens /
PyAutoGalaxy. The author of the analysis has already been wrong three times in
the same investigation (details in "Track record", below), so treat every claim
here as suspect until you have checked it yourself.

Do not be agreeable. If the analysis is right, say so and say why. If any step
is wrong, say which one and show the counter-evidence. **"Do nothing" is a fully
acceptable verdict** — the current code has run this way for years and produces
published science.

---

## 1. The code under discussion

`autoarray/inversion/regularization/constant.py`, `constant_regularization_matrix_from`:

```python
regularization_coefficient = coefficient * coefficient          # lam^2
neighbors = xp.where(neighbors == -1, OUT_OF_BOUND_IDX, neighbors)
diag_vals = 1e-8 + regularization_coefficient * neighbors_sizes

# jax path
return (
    xp.diag(diag_vals)
    .at[I_IDX, neighbors]
    .add(-regularization_coefficient, mode="drop", unique_indices=True)
)
```

and `autoarray/inversion/inversion/abstract.py`, `log_det_regularization_matrix_term`:

```python
return 2.0 * self._xp.sum(
    self._xp.log(
        self._xp.diag(self._xp.linalg.cholesky(self.regularization_matrix_reduced))
    )
)
```

This term enters the Bayesian evidence (`fit_dataset.py`, `log_evidence`):

```
Log Evidence = -0.5 * [ chi^2 + s^T H s + ln det(F + H) - ln det(H) + sum ln(2 pi sigma^2) ]
```

## 2. The claims to check

**C1 — structure.** `H = lam^2 * L + 1e-8 * I`, where `L` is a graph Laplacian
(degree on the diagonal, `-1` on adjacency). `L` is positive *semi*-definite with
the constant vector as an exact null mode, so `H`'s smallest eigenvalue is
exactly the `1e-8` lift, while its largest grows as `lam^2 * degree`.

**C2 — the lift is below the numerical noise floor.** Symmetric-eigenvalue and
Cholesky computations carry absolute error of order `eps * ||H||`. Measured on
the real matrices (see section 3): `||H|| ~ 7e8`, so the noise floor is
`2.2e-16 * 7.3e8 ~ 1.6e-7`, which is **~16x larger than the 1e-8 lift itself**.
Therefore, past roughly `cond ~ 1/eps` (around `lam ~ 2400`), whether `H` is
numerically positive-definite is decided by rounding, not by the model.

**C3 — the consequence.** JAX's Cholesky returns NaN (numpy raises) for a matrix
that is positive-definite in exact arithmetic. The NaN wall reported in
autolens_workspace_developer#104 is therefore a **numerical artifact of the
formulation**, not a real feature of the likelihood surface. Corollary: it should
be **backend-dependent** — and one measured point (draw 12) is indeed finite on
CPU but NaN'd on an A100.

**C4 — the current lam-dependence is ALREADY CORRECT.** Expanding, with `mu_i`
the nonzero Laplacian eigenvalues:

```
log det(H) = log(eps) + sum_{i>=2} log(lam^2 * mu_i + eps)
           ~ log(eps) + (S-1) * log(lam^2) + sum_{i>=2} log(mu_i)
```

because `lam^2 * mu_i >> eps` (measured `mu_min ~ 0.011`, `eps = 1e-8`). So the
`1e-8` contributes only a **constant offset**; it does not distort the
lam-dependence that drives inference of the regularization coefficient. **If C4
is right, the current code is scientifically sound and merely numerically
fragile — which sharply narrows what a fix is allowed to do.**

**C5 — the candidate fixes are not equivalent.**
- *Relative lift* `eps -> eps * (1 + lam^2)`: one-line, keeps Cholesky, lifts
  `eig_min` to ~0.5 (well above the noise floor). **But** it adds `log(1 + lam^2)`
  to `log det(H)`, changing the lam-dependence by one power, which shifts the
  inferred regularization coefficient. Science-visible **in inference**.
- *Pseudo-determinant* (drop the null mode; sum log over non-null eigenvalues):
  differs from current by the **constant** `-log(eps) ~ +18.42`, so inference and
  model comparison are unchanged and only the absolute evidence shifts. Needs an
  eigendecomposition rather than a Cholesky (cost, and JAX-differentiability).
- *Analytic log-det*: for a **rectangular** mesh the neighbour topology is fixed
  (e.g. 30x30, 4-connected), so `L` and its eigenvalues `mu_i` are **constant for
  the whole fit** and independent of lam. Then
  `log det(H) = sum_i log(lam^2 * mu_i + eps)` is exact, cheap, differentiable in
  lam, and **identical to the current formula in exact arithmetic** — zero science
  change. Unclear whether this generalises to Delaunay/Voronoi meshes, whose
  topology varies per model.

## 3. The evidence (reproduce it — do not take it on trust)

Real `regularization_matrix_reduced` (900x900) at two parameter points from the
seed-0 draw sequence of `autolens_workspace_developer/searches_minimal/pix_lr_free.py`
(the objective is `searches_minimal/pix_multi_start.py`: `RectangularKernelAdaptDensity(shape=(30,30), bandwidth=0.1)`,
`reg.Constant`, os_pix=1, free Isothermal+shear, MGE light geometry fixed):

```
draw 12: r_E=1.2824  coefficient=6.927324e+03  (lam^2=4.7988e+07)
  full    (920x920): eig_min=-3.80e-08  eig_max=3.83e+08  n_negative=1  n_|eig|<1e-7=21
                     numpy cholesky RAISES;  JAX cholesky NaN
  reduced (900x900): eig_min=+3.03e-08  eig_max=3.83e+08  cond=1.26e+16  n_negative=0
                     numpy cholesky ok;      JAX cholesky ok
                     log_det_regularization_matrix_term = 16882.7398957747   (FINITE on CPU)
                     10 smallest: [3.035e-08 5.258e+05 5.258e+05 1.052e+06 2.097e+06 ...]

draw 35: r_E=5.9252  coefficient=9.582283e+03  (lam^2=9.1820e+07)
  reduced (900x900): eig_min=-9.90e-08  eig_max=7.33e+08  cond=inf  n_negative=1
                     numpy cholesky RAISES;  JAX cholesky NaN
                     log_det_regularization_matrix_term = nan
                     10 smallest: [-9.900e-08 1.006e+06 1.006e+06 2.012e+06 ...]
```

Notes on this data:
- The 920x920 full matrix has **21** near-zero eigenvalues: 20 **exactly** zero
  (the unregularized MGE linear light amplitudes) + 1 near-zero (the Laplacian
  null mode). `regularization_matrix_reduced` correctly strips the 20.
- `eig_max / lam^2 = 3.8285e8 / 4.7988e7 = 7.98 ~ 2 * degree`, consistent with a
  4-connected Laplacian. This is the main quantitative support for C1.
- **Draw 12 is finite on CPU but NaN'd on an A100** (job 330609/330611). That is
  the direct evidence for C3.

Reproduce with (~30 s on a laptop, no GPU needed; the earlier claim that this
needs an A100 was wrong — 10.9 GiB was `value_and_grad`, this is forward-only):

```python
# from the autolens_workspace_developer root
import numpy as np, jax, jax.numpy as jnp
jax.config.update("jax_enable_x64", True)
from searches_minimal.pix_multi_start import build_model, build_analysis
from searches_minimal._setup import build_dataset
from searches_minimal.lr_free_multistart import START_LOW, START_HIGH

model, analysis = build_model(), build_analysis(build_dataset())
rng = np.random.default_rng(0)
for t in range(1, 36):                       # draws 12 and 35 are the rejects
    u = rng.uniform(START_LOW, START_HIGH, size=model.prior_count)
inst = model.instance_from_vector(vector=list(model.vector_from_unit_vector(unit_vector=list(u), xp=np)), xp=jnp)
H = np.asarray(analysis.fit_from(instance=inst).inversion.regularization_matrix_reduced)
print(np.linalg.eigvalsh(H)[:5], np.linalg.cond(H))
```

## 4. Questions to answer

1. **Is C1 right?** Is `H` really `lam^2 * L + eps * I` with a Laplacian `L`?
   Check the code, not the prose. Does the `unique_indices=True` scatter at
   `constant.py:55-58` ever receive duplicate `(i, j)` pairs — which would make
   that flag a false promise to XLA and the result undefined?
2. **Is C2 right?** Is `1e-8` genuinely below the noise floor at production
   coefficients, and what IS the realistic range of `coefficient` in production
   lens modelling? (If real fits never exceed `lam ~ 100`, this whole issue is
   confined to the broad-prior search regime and the urgency collapses.)
3. **Is C4 right — and is this the crux?** Does `eps` really only contribute a
   constant to `log det(H)`? If so, the current code's *inference* is correct and
   any fix that changes the lam-dependence (i.e. the relative lift) is a
   REGRESSION dressed as a bug fix. Verify the asymptotics numerically across a
   lam sweep rather than trusting the algebra.
4. **What does the literature actually require?** Warren & Dye 2003
   (astro-ph/0302587), Suyu et al. 2006, Nightingale & Dye 2015
   (arXiv:1708.07377) define this evidence. How is `ln det(H)` supposed to treat
   a rank-deficient regularization matrix? Is the `1e-8` a principled proper-prior
   choice on the null mode, or an undocumented numerical hack that happens to be
   constant? Does the pseudo-determinant correspond to a defensible prior (flat /
   improper on the constant mode)?
5. **Is the analytic-log-det route real?** For `RectangularKernelAdaptDensity`, is
   the neighbour topology genuinely fixed across the fit (so `mu_i` can be
   precomputed once)? What about Delaunay/Voronoi? If it holds for rectangular
   meshes only, is a mesh-class-specific implementation acceptable or a
   maintenance trap?
6. **Should we do nothing?** Steelman this. The NaN only bites gradient-based
   searches at broad-prior coefficients; Nautilus already wins decisively on
   pixelized cells (autolens_workspace_developer#101). Is the right answer to
   constrain the coefficient prior, or to document the regime, rather than touch a
   term that sets published evidence values?
7. **If a fix IS justified**, which one, and what parity evidence would you demand
   before it ships? Be specific: which fiducials, what tolerance, and what result
   would make you reject the change?

## 5. Track record (why this needs an independent check)

In the same investigation the author asserted, then had to retract:
1. that the **curvature-reg Cholesky** (`abstract.py:719`) was the prime suspect —
   it is finite (1.69e4); the bug is the neighbouring regularization-only term;
2. that the fix for a related PyAutoFit guard was the "standard double-`where`"
   pattern — **measured, it does nothing**; only input-side sanitisation works;
3. that a **numpy-vs-JAX divergence was "ruled out"** — that test was on a
   *synthetic* matrix; on the real one, draw 12 diverges CPU vs GPU.

Each was caught only by measurement. Assume the analysis above contains a fourth
error and go find it.

## 6. Deliverable

A verdict — **JUSTIFIED / NOT JUSTIFIED / JUSTIFIED BUT NOT AS PROPOSED** — with,
for each of C1-C5, whether you confirm or refute it and on what evidence. Prefer
numbers you generated over the numbers quoted here. Where you cite the
literature, cite the specific equation.
