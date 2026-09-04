# interferometer/jax_grad/gradient.py: eager and jitted likelihoods diverge ~5e-7 on Python 3.13 only

Type: bug
Target: autolens_workspace_test
Repos:
- @autolens_workspace_test
- @PyAutoArray
Themes:
- jax-gradient
- interferometer
- pixelization
Difficulty: medium
Autonomy: safe
Priority: normal
Status: SHELVED 2026-09-04 — resolved 2026-08-26 (autolens_workspace_test#279). Originally `draft/bug/autolens_workspace_test/gradient_eager_jit_divergence_py313.md`.
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-24

## Shelved 2026-09-04 — resolved, do NOT start dev on this prompt

The bug was fixed on **2026-08-26** (autolens_workspace_test **#279**). The cause
was neither `pure_callback` constant-folding nor anything Python-3.13-specific —
3.12 reproduced the divergence identically on the same host — but a discrete
**cell-assignment flip in PyAutoArray's adaptive rectangular mapper**, fixed in
**PyAutoArray#490**. `interferometer/jax_grad/gradient.py` is back in mega-run
coverage: its `NEEDS_FIX` entry is gone from
`@autolens_workspace_test/config/build/no_run.yaml`, whose surviving comment block
records the fix and points at autolens_workspace_test#274. Every item of the
prompt's Acceptance section is therefore met. Archived rather than left as pickable
backlog.

**The appended `UPDATE 2026-08-24 — investigation` below is preserved verbatim**,
including its NNLS solver-branch-quantum analysis (the ΔLL ≈ 1.577e-3 PDIP
`lax.while_loop` trip and the FD step-sweep table backing it out to 4–5 significant
figures). That analysis is not what the fix turned out to be, but it is the standing
record of how the positive-only solve behaves at a knife-edge evaluation point, and
of why `assert_eager_jit_consistent`'s `rtol=1e-10` must not be widened.


## The failure

`@autolens_workspace_test/scripts/interferometer/jax_grad/gradient.py` runs three
`util.assert_eager_jit_consistent` checks. The third — Variant B,
`RectangularRTUAdaptDensity` mesh + `reg.Adapt()` on the sparse-operator path
(`dataset.apply_sparse_operator(use_jax=True)`) — fails on **Python 3.13 only**:

```
eager   -3164.0196392095145
jitted  -3164.021216643465
```

That is ~5e-7 relative, against the guard's `rtol=1e-10`
(`@autolens_workspace_test/scripts/misc/util.py:185`). The guard exists precisely
for this: its message reads *"possible `pure_callback` constant-folding; do not
trust jitted gradients"*, and it is the gate that must pass before the variant's
finite-difference/AD gradient comparison means anything.

## Measurement

2026-08-24 retime sweep, 5 repeats per Python leg, 300 s cap
(run 32741386752; see autolens_workspace_test#274):

- **3.13: deterministic failure, 5/5**, same two values every repeat.
- **3.12: fully green, 61.2 s** — 7% of its 900 s cap.
- The *eager* value is identical on both legs. Only the **jitted** value moves,
  and only on 3.13.
- Not a timeout and not performance. The script's old
  `# SLOW 2026-07-14 - flakes at the 1800s cap (PyAutoHeart#74)` marker was a
  misdiagnosis; it has been rewritten to `NEEDS_FIX 2026-08-24` in
  `@autolens_workspace_test/config/build/no_run.yaml` pointing here.

Eager agreeing across legs while jitted does not is the informative part: the
Python-version-dependent behaviour is inside compilation, not in the model, the
dataset, or the mesh.

## Task

1. **Localise the divergence inside the jitted graph.** Variants A and C pass on
   both legs, so it is not the sparse operator or `assert_eager_jit_consistent`
   in general — it is specific to `RectangularRTUAdaptDensity` + `reg.Adapt` on
   the sparse path. Bisect within that variant (regularization matrix, mesh
   density/CDF transform, the linear solve) to find which sub-computation's
   jitted value moves on 3.13.
2. **Test the `pure_callback` constant-folding hypothesis the guard names.** Any
   `pure_callback` boundary in this path is a prime suspect: if XLA folds a
   callback result on one leg and not the other, the jitted graph is evaluating
   something the eager path is not. If confirmed, the fix is library-side —
   pin/annotate the callback so it cannot be constant-folded — not a tolerance
   change in the script.
3. **Rule the alternative in or out**: the same jaxlib/XLA version compiling
   differently under 3.13 (fastmath/fusion or reduction-order differences),
   making this a genuine ~5e-7 numerical difference in a solve rather than a
   correctness bug. Compare the jaxlib/XLA versions actually installed on each
   leg first — if they differ, that is the likelier story and this becomes an
   environment-pinning task.
4. **Only then decide about the tolerance.** A ~5e-7 disagreement in a linear
   solve may be legitimate, but `rtol=1e-10` is a deliberate constant-folding
   tripwire; loosening it to make the script green would disarm the guard for
   every variant that uses it. If the conclusion really is "this magnitude is
   expected here", the tolerance change must be argued in the commit and scoped
   to this variant, not applied to `util.assert_eager_jit_consistent` wholesale.

## Why it matters

The variant's whole purpose is that this mesh must carry live, strictly
FD-matched gradients on the sparse path, which has no over-sampling to fall back
on. While the eager/jit guard fails, the jitted gradients it protects cannot be
trusted, and the script stays out of coverage on 3.13 — the leg where the problem
lives.

## Acceptance

- A named cause: `pure_callback` constant-folding, an XLA/jaxlib compilation
  difference, or a genuine numerical property of the solve — with evidence, not
  a tolerance bump standing in for a diagnosis.
- `scripts/interferometer/jax_grad/gradient.py` green on **both** 3.12 and 3.13.
- `assert_eager_jit_consistent` still able to catch the constant-folding it was
  written to catch.
- The `interferometer/jax_grad/gradient.py` `NEEDS_FIX` entry is removed from
  `@autolens_workspace_test/config/build/no_run.yaml`, restoring mega-run
  coverage on 3.13.

---

## UPDATE 2026-08-24 — investigation (read-only; no code changed)

Investigated ahead of the fix. Result: **the `pure_callback` constant-folding
hypothesis in the guard's own message is refuted, and the jax-version-delta
hypothesis (Task item 3) is refuted.** The divergence is a **discrete branch
change in the positive-only NNLS solve**, and its magnitude is *exactly* the
solver-branch quantum this script already documents at the failing call site.
Nothing was edited in `@autolens_workspace_test` — in particular the guard's
`rtol` was NOT widened; see "Why the tolerance must not be widened" below.

### 1. `pure_callback` is structurally absent from Variant B's path

Repo-wide grep of the installed chain (`PyAutoNerves PyAutoFit PyAutoArray
PyAutoGalaxy PyAutoLens`) finds `jax.pure_callback` in exactly one family — the
**Delaunay/Sibson qhull triangulation**:

```
autoarray/inversion/mesh/interpolator/delaunay.py:149:    return jax.pure_callback(
autoarray/inversion/mesh/interpolator/sibson.py:514  (docstring)
autoarray/inversion/mesh/mesh/delaunay.py:30         (docstring)
autoarray/inversion/mesh/mesh/delaunay_nn.py:22      (docstring)
```

Variant B is a **rectangular** mesh (`RectangularRTUAdaptDensity`), which never
constructs a triangulation. A grep for `callback` across
`autoarray/inversion/inversion/`, `autoarray/inversion/regularization/`,
`autoarray/inversion/mesh/mesh/rectangular_rtu_adapt_density.py`,
`autoarray/operators/transformer.py`,
`autoarray/dataset/interferometer/` and `autolens/interferometer/` returns
**zero hits**. There is no callback boundary in this likelihood for XLA to
constant-fold. Task item 2 is answered: hypothesis refuted, no library-side
callback pinning is needed.

### 2. Both legs resolve the *same* jax/jaxlib — Task item 3 refuted

From the install logs of retime run **32741386752** (`resolved jax …` is printed
by `.github/scripts/smoke_install.sh`'s `JAXCHECK` block):

- 3.12 job **97476472522**:
  ```
  resolved jax 0.11.1
    Downloading jax-0.11.1-py3-none-any.whl.metadata (13 kB)
    Downloading jaxlib-0.11.1-cp312-cp312-manylinux_2_27_x86_64.whl.metadata (1.3 kB)
  ```
- 3.13 job **97476472555**:
  ```
  resolved jax 0.11.1
    Downloading jax-0.11.1-py3-none-any.whl.metadata (13 kB)
    Downloading jaxlib-0.11.1-cp313-cp313-manylinux_2_27_x86_64.whl.metadata (1.3 kB)
  ```

Every numerically relevant package is identical version-for-version on the two
legs: `jax-0.11.1`, `jaxlib-0.11.1`, `jaxnnls-1.0.1`, `numpy-2.5.2`,
`scipy-1.17.1`, `ml_dtypes-0.6.0`, `opt_einsum-3.4.0`, `jax_zero_contour-2.0.0`.
Only the CPython ABI tag of the `jaxlib` wheel differs (`cp312` vs `cp313`).
**This is not an environment-pinning task** — there is nothing to pin.

### 3. The mechanism: a PDIP iteration-count / branch flip in the NNLS solve

`use_positive_only_solver: true` (autoarray `config/general.yaml:5`, and the
workspace's shadowing `config/general.yaml:16`), so the inversion solves through
`inversion_util.reconstruction_positive_only_from` →
`autoarray/util/jax_nnls.py:solve_nnls`, a **primal-dual interior-point** NNLS
whose termination is a data-dependent `lax.while_loop`:

```python
def converged_check(inputs):
    _, _, _, _, _, _, converged, pdip_iter = inputs
    return jnp.logical_and(pdip_iter < max_iter, converged == 0)

init_inputs = (Q, q, x, s, z, solver_tol, 0, 0)
outputs = jax.lax.while_loop(converged_check, pdip_pc_step, init_inputs)
```

with `solver_tol = jax.lax.min(Q.shape[0] * EPSILON, 1e-2)`. The returned `x` is
therefore accurate only to a **finite KKT residual tolerance**, not to machine
precision, and the *number of PDIP iterations actually taken* is a step function
of the iterates. Any O(1e-16) difference in how the dense Cholesky inside
`pdip_pc_step` is evaluated — exactly what differs between JAX's eager
op-by-op dispatch and a single fused XLA program under `jax.jit` — can move the
convergence trip by one iteration and return a materially different `x`.

### 4. The decisive quantitative evidence: the gap IS the documented quantum

`gradient.py:251-257` and `util.py:97-107` already document that this exact
configuration has measure-thin solver branch flips of **ΔLL ~1.6e-3**:

> "single float inputs (width < 1e-15) where the solve lands on a marginally
> different branch (ΔLL ~1.6e-3, identical for two orthogonal parameter
> directions; also present under reg.Constant, so not mesh- or reg-specific)"

The failing gap is:

```
jitted − eager = -3164.021216643465 − (-3164.0196392095145) = -1.5774339503877854e-03
                                                    (= 4.9855e-07 relative)
```

And in the **same retime run**, the *passing* 3.12 leg's FD step sweep for
Variant B prints the poisoned steps whose magnitude is that same quantum divided
by the FD step (`h = rel_step * max(|x|, 0.1)`, so `h = rel_step * 0.1` here):

```
FD step sweep (rel_steps=(1e-08, 1e-07, 1e-06); * = used for comparison):
 p[ 0] ad= -4.822776e-01  fd:    7.887165e+05    -4.822823e-01  * -4.822778e-01
 p[ 1] ad=  1.035652e-01  fd:    1.034550e-01  *  1.035687e-01     7.887273e+03
 p[ 3] ad= -1.675453e+00  fd:   -1.675517e+00  * -1.675448e+00     7.885495e+03
 p[ 5] ad= -9.340543e-01  fd:   -7.887179e+05    -9.340511e-01  * -9.340533e-01
 p[ 6] ad=  3.146983e+00  fd:    3.147079e+00     7.887485e+04  *  3.146984e+00
```

Back out ΔLL = outlier × 2h from each:

| outlier | rel_step | 2h | implied ΔLL |
|---|---|---|---|
| 7.887165e+05 | 1e-8 | 2e-9 | **1.5774330e-03** |
| 7.887179e+05 | 1e-8 | 2e-9 | **1.5774358e-03** |
| 7.887485e+04 | 1e-7 | 2e-8 | **1.5774970e-03** |
| 7.887273e+03 | 1e-6 | 2e-7 | **1.5774546e-03** |
| 7.885495e+03 | 1e-6 | 2e-7 | **1.5770990e-03** |

All five agree with the eager/jit gap (**1.5774340e-03**) to 4–5 significant
figures, across three step sizes and both flip directions. The eager and jitted
programs are not disagreeing by accumulated round-off — **they are sitting on
opposite sides of one documented branch of the positive-only solve.** That is
the named cause the Acceptance section asks for: *a genuine (discrete) numerical
property of the solve*, not constant-folding and not a version delta.

Variant C passes because its base point is not near a flip; the flip is
knife-edge and evaluation-point-specific (the script's own note already records
it is "also present under reg.Constant, so not mesh- or reg-specific").

### 5. Caveat on the "3.13-only" framing

The evidence establishes the *mechanism* but not that CPython 3.13 is the causal
variable. `jaxlib` 0.11.1 cp312 and cp313 are the same XLA sources; a more
ordinary explanation for which leg tips is that the two matrix jobs ran on
different runner hardware (CPU vector width changes reduction association inside
fused kernels, which is a ~1e-16 perturbation — enough to tip a knife-edge
`while_loop` trip). Note the *eager* value is bit-identical across legs, which
is consistent with either story: eager dispatch is unfused. Before writing
"Python 3.13" into a fix, falsify cheaply by re-running the retime on 3.12
several times (and on 3.13) and printing `converged` / `pdip_iter` from
`solve_nnls` on both the eager and jitted evaluation.

### 6. Why the tolerance must NOT be widened (why nothing was edited)

Considered and rejected — this is the "report, don't change" outcome:

- **`rtol=1e-10` is not the only thing the guard buys here.**
  `compare_gradients` computes autodiff on the **eager** `f` and finite
  differences on the **jitted** `f_fd` (`gradient.py:258-264`). If eager and
  jitted sit on different NNLS branches, the two halves of that comparison are
  derivatives of two different piecewise branches, and a passing FD/AD check
  would be luck, not certification. The guard is what makes the downstream
  FD-certification meaningful, so a run that trips it genuinely must not
  proceed.
- Passing would require `rtol >= 5e-7`, a five-order widening, and it would
  bless the exact 1.577e-3 LL quantum that the `rel_steps` sweep machinery
  exists to *route around*, not to accept.
- `assert_eager_jit_consistent` is used at 11 call sites across
  `imaging/jax_grad/{lp,mge,knn,delaunay,pixelization,regularization}.py`,
  `interferometer/jax_grad/gradient.py` (×3) and `weak/jax_grad.py`, all at the
  default `rtol` — there is no precedent of a looser value to point at.

### 7. Suggested fix directions for whoever takes this

In rough order of preference; all keep the guard armed.

1. **Make the solve compilation-path-independent** rather than the guard
   tolerant. `Settings(nnls_solver_tol=..., nnls_max_iter=...)` are already
   plumbed through to `solve_nnls` (`settings.py:18-19`,
   `inversion_util.py:337-338`). Fixing the iteration count (or tightening
   `solver_tol` well below the flip's sensitivity) makes the PDIP loop take the
   same number of steps under both compilations, so eager and jit land on the
   same branch by construction. Scope it to this script's `AnalysisInterferometer`
   settings, not globally.
2. **Move the base point off the branch boundary** — `param_vector_from` uses a
   fixed `PRNGKey(42)` perturbation, so the evaluation point is arbitrary; a
   different seed that is not knife-edge would restore both legs without
   touching any tolerance. Cheap, but it hides rather than fixes the
   sensitivity, so pair it with a recorded note.
3. **Compare like with like** — run autodiff under `jax.jit` too, so AD and FD
   are both taken on the compiled program. This removes the eager/jit mismatch
   from the FD certification, but leaves the eager/jit guard failing, so it is
   only useful combined with (1).

Do NOT close this by relaxing `assert_eager_jit_consistent`, and do not remove
the `NEEDS_FIX` entry in `config/build/no_run.yaml` until the underlying solve
is deterministic across compilation paths.
