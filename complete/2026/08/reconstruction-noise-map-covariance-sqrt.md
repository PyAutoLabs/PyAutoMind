# reconstruction-noise-map-covariance-sqrt — covariance NaNs and the Cholesky rewrite

**Date:** 2026-08-22
**Issue:** [PyAutoArray#468](https://github.com/PyAutoLabs/PyAutoArray/issues/468) (closed)
**PRs:** [PyAutoArray#469](https://github.com/PyAutoLabs/PyAutoArray/pull/469) (MERGED, `2784056`)
**Outcome:** shipped — phase 1 of a two-phase cluster; the estimator half is still open.

## What this task was

`AbstractInversion.reconstruction_noise_map_with_covariance` was one line:

```python
return np.sqrt(np.linalg.inv(self.curvature_reg_matrix))
```

`np.sqrt` applied **elementwise to the whole inverse**. The off-diagonals of a covariance matrix are
covariances and are routinely negative, so every one was `NaN` by construction — for any matrix,
however well-conditioned — with a `RuntimeWarning` on every call. The docstring promised a matrix
that "accounts for the covariance of the noise between pixels"; the entries carrying that covariance
were precisely the broken ones.

Found as an incidental finding while reproduction-gating
`complete/2026/08/numerical-inversion-failures.md`, whose own hypothesis was refuted.

## The trap this cluster kept setting

**The elementwise sqrt does not affect the 1D `reconstruction_noise_map`.** `np.sqrt` is elementwise,
so it commutes with taking the diagonal: `diagonal(sqrt(C))[i] == sqrt(C[i,i])`. This was mistaken
for the cause of unreliable source noise maps twice — once by the original gate, once during
planning. It is not. It looks exactly like evidence for a non-positive-definite matrix and is not
that either.

## The A/B refuted two of the arguments for the fix

Run **before** writing any code, which is why the reasoning in the shipped docstring is narrower than
the reasoning in the original prompt:

| Claim | Verdict |
|---|---|
| `inv` gives negative diagonals on well-formed SPD | **REFUTED** — 0 across cond 1e3–1e15, n=400, 20 trials each |
| `inv` is materially less accurate on the diagonal | **REFUTED** — matches `cho_solve`; at cond 1e15 `inv` was marginally *better* |
| Near-coincident mesh vertices degrade the inverse | **REFUTED** — with regularization the matrix stays PD (cond ~6.8e7 even at exactly duplicated columns) |
| `inv` returns asymmetric output | **CONFIRMED** — 5.2e-7 at cond 1e12 vs 2.6e-16 |
| `inv` silently succeeds on indefinite matrices | **CONFIRMED** |

**The case for Cholesky is detection, not accuracy.** `cho_factor` raises `LinAlgError` on a negative
eigenvalue; `np.linalg.inv` raises only on an *exactly* singular matrix. At eigenvalue `-1e-8` all
300 diagonals came back negative (whole noise map NaN); at `-1.0`, **zero** did — no NaN, no warning,
no error, and wrong numbers. That silent case is the failure mode worth fixing.

The `abstract.py:805` note about "the round-off of factorizing the explicitly formed inverse" at
`cond ~ 1e9` was cited as corroboration during planning. The A/B did not support it as an *accuracy*
argument for the noise map; keep it as history, not as evidence.

## What shipped

- **new `reconstruction_covariance_matrix`** — `cho_solve(cho_factor(...))`, input *and* output
  symmetrized, explicit finiteness guard raising `LinAlgError`.
- **`reconstruction_noise_map`** — decoupled to `sqrt(diag(C))`. It was previously correct only
  *incidentally*, via the elementwise sqrt; the invariant is now stated so it cannot silently become
  a variance.
- **`reconstruction_noise_map_with_covariance`** — deprecated alias, warning states the value change.
- 5 new regression tests plus 2 from review; 2 plotter monkeypatch sites repointed.

## The review caught a regression the first commit introduced

Worth recording, because it is a trap anyone swapping `inv` for a scipy factorization will hit:

**scipy's `cho_factor`/`cho_solve` default to `check_finite=True` and raise `ValueError`, not
`LinAlgError`.** Both call sites (`inversion_plots.py:169`, `:397`) catch only `LinAlgError`, and the
CSV writer's docstring explicitly promises a failure there may not abort the enclosing model-fit. So
a NaN-contaminated curvature matrix would have killed a fit that previously wrote a `nan` column and
continued. Measured: old code returned `[nan, nan]`; first fix raised `builtins.ValueError` past the
guards.

Fixed *inside* the property with an explicit finiteness check rather than by broadening the callers'
`except` clauses — the contract "raises `LinAlgError` for any input that has no covariance" then
holds for downstream callers too. `check_finite=False` is passed onward, so the check costs nothing.

Second review find: **`cho_factor` reads only the upper triangle**, so an asymmetric input was
silently inverted as though its lower triangle matched (`[[2.0, 0.5], [0.1, 2.0]]` → diag `0.5333`
vs the true `0.5063`). Output symmetrization does not fix that; the input is symmetrized now too.

Also corrected: the "no value change" claim for `reconstruction_noise_map` was overstated —
algebraically identical, only *numerically* equivalent (~7e-15 at cond 1e3, ~4e-5 at cond 1e13).
And the symmetry test was tautological, since `0.5 * (C + C.T)` is bitwise symmetric for any `C`; it
now also asserts accuracy against an exactly-constructed ground truth.

## Downstream API risk — resolved by grep, not assumption

The deprecated alias changes values under an unchanged name, and `DeprecationWarning` is invisible by
default when raised from library code. So it was checked:

| Repo | `with_covariance` | `reconstruction_noise_map` |
|---|---|---|
| PyAutoGalaxy `3ca31bf` | none | none |
| PyAutoLens `87e5827` | none | none |
| autolens_workspace | none | **4 scripts + notebooks** |

Control greps confirm the checkouts were real (394 / 237 / 465 `.py` files), so the nulls are genuine.
**Not checked:** `autogalaxy_workspace`, the HowTo repos, external user code.

`reconstruction_noise_map` **is** used, and this is the finding that matters for the sibling prompt:
`autolens_workspace/scripts/{imaging,interferometer,group,multi_galaxy}/features/pixelization/source_science.py`
compute `signal_to_noise_map = reconstruction / reconstruction_noise_map`. The noise map feeds
published S/N maps on source reconstructions.

## Still open — the larger half

`draft/bug/autoarray/reconstruction_noise_map_solver_mismatch.md` (`Priority: high`,
`Autonomy: human-required`) holds the estimator-level defects, deliberately excluded from this PR:

1. The covariance is that of the **unconstrained** Warren & Dye solve, but
   `use_positive_only_solver: true` is the shipped default, so the reconstruction is an NNLS
   active-set solve. A compact source pins a large fraction of the mesh at zero.
2. The noise map ignores `zeroed_ids_to_keep` under `use_edge_zeroed_pixels: true`, re-admitting the
   poorly-constrained boundary vertices the zeroing exists to remove.
3. ~~`use_edge_zeroed_pixels` is nested inside the positive-only branch~~ — **withdrawn 2026-08-22:
   intended behaviour, confirmed by the author, not a defect.**

First job there is to instrument a real fit: **it was never established that a real
`curvature_reg_matrix` is indefinite in a converged fit**, nor that the NNLS pinned fraction is
actually large. Both were reasoned, not measured, and the whole estimator argument rests on the
second.

## Environment note

Python 3.11 is too old for this repo (`requires-python >= 3.12`); `python3.12` was present and a venv
there installed cleanly. Three `test_transformer.py` pynufft failures reproduce on clean `a6b07cd`
in that sandbox and were **green in CI** — a local dependency artefact, not a repo problem.

## Original prompt

# `reconstruction_noise_map_with_covariance` — form the covariance properly, fix the sqrt

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Status: in-progress

## Why this exists

Found during the 2026-08-21 reproduction gate for
`draft/bug/health_fixes/numerical_inversion_failures.md` (record:
`complete/2026/08/numerical-inversion-failures.md`). That prompt alleged
non-positive-definite inversion matrices and was **refuted**; this was the real
defect the gate turned up.

**Scope note (2026-08-22).** Deeper research found the noise map is wrong in
*four* distinct ways. This prompt owns the two that need no science decision —
the numerics and the semantics. The estimator-level defects (the noise map
describes a different estimator than the default solver, and ignores edge-zeroed
pixels) are **`draft/bug/autoarray/reconstruction_noise_map_solver_mismatch.md`**,
which is the larger and more consequential of the two. Do that one second; this
one first, because it is small, safe and unblocks the other.

## Defect A — elementwise sqrt NaNs every off-diagonal

`autoarray/inversion/inversion/abstract.py:839-859`, verified on `main` @ `a6b07cd`:

```python
@property
def reconstruction_noise_map_with_covariance(self) -> np.ndarray:
    """... a two dimension matrix which accounts for the covariance of the noise between pixels."""
    return np.sqrt(np.linalg.inv(self.curvature_reg_matrix))
```

`np.sqrt` is applied **elementwise to the entire inverse**. That inverse is the
covariance matrix `C`, whose off-diagonals are covariances and are generally
negative — so they become `NaN`, and each call emits
`RuntimeWarning: invalid value encountered in sqrt`. Unconditional: any matrix
with an anti-correlated pixel pair NaNs, however well-conditioned.

**This does NOT affect the 1D noise map.** `np.sqrt` is elementwise, so it
commutes with taking the diagonal — `np.diagonal(np.sqrt(C))[i] == sqrt(C[i,i])`.
The off-diagonal NaNs never reach `reconstruction_noise_map`. Do not cite this
defect as the cause of unreliable 1D noise maps; that is the sibling prompt.

## Defect B — `np.linalg.inv` is the wrong routine, and the repo already says so

The same file, 50 lines up, documents exactly this hazard for the log-det path
(`abstract.py:805-806`):

> the analytically exact `pixels * log(coeff) - log det C` from a single Cholesky
> of their covariance `C`, **avoiding the round-off of factorizing the explicitly
> formed inverse** (which reaches ~1e-6 absolute in the evidence at
> **cond(C) ~ 1e9 on clustered traced mesh vertices**)

That reasoning was applied to the log-det and never to the noise map, which still
forms the explicit inverse — of the same matrix, at the same conditioning, on the
same clustered-mesh geometry.

Three consequences, all pointing the same way:

1. `np.linalg.inv` is LU-based. It exploits neither symmetry nor
   positive-definiteness, both of which this matrix has (when it is well-posed).
2. It **raises only on exactly-singular input.** Near-singular passes through with
   amplified error, so a diagonal entry can come back negative — impossible for a
   true PD inverse — and `sqrt` turns it into NaN, or leaves it barely positive and
   yields a wildly wrong RMS. Silently.
3. The reconstruction path never inverts: `reconstruction_positive_negative_from`
   uses `xp.linalg.solve` and `fnnls_cholesky` uses
   `slg.solve(..., assume_a="pos")`. The noise map is the only place in the
   inversion that forms an explicit inverse.

**This is already biting users.** `inversion_plots.py:395` wraps the noise map in
`except np.linalg.LinAlgError` and writes the CSV column as NaN with a warning —
a guard that exists because this fails in practice.

## The fix

Option 1 from the original draft, chosen 2026-08-22: the property should return
the actual covariance matrix, computed via Cholesky. `scipy` is already a hard
dependency (`pyproject.toml`).

```python
from scipy.linalg import cho_factor, cho_solve

@property
def reconstruction_covariance_matrix(self) -> np.ndarray:
    """The covariance matrix C = [F + λH]^-1 of the reconstruction."""
    matrix = np.asarray(self.curvature_reg_matrix)
    covariance = cho_solve(cho_factor(matrix), np.eye(matrix.shape[0]))
    return 0.5 * (covariance + covariance.T)   # remove rounding asymmetry

@property
def reconstruction_noise_map(self) -> np.ndarray:
    """1D RMS noise: sqrt of the diagonal of the covariance matrix."""
    return np.sqrt(np.diag(self.reconstruction_covariance_matrix))
```

Why this shape:

- **`cho_factor` raises `LinAlgError` on a non-PD matrix**, so the noise map now
  fails loudly on exactly the matrices the reconstruction already rejects. Today
  the two disagree: `solve` raises and resamples, `inv` returns garbage.
- **`reconstruction_noise_map` is decoupled** and computes `sqrt(diag(C))`
  directly. Today it is correct only *incidentally*, because sqrt happens to be
  elementwise — change the matrix and it silently becomes a variance. Decoupling
  removes that trap permanently.
- **Off-diagonals become real covariances**, so the docstring's promise holds.

**Naming.** `..._with_covariance` returning a covariance matrix should be
`reconstruction_covariance_matrix`. Keep the old name as a `DeprecationWarning`
alias returning the new matrix. Its values *do* change — diagonal from std-dev to
variance, off-diagonals from NaN to covariances — but every off-diagonal consumer
was reading NaN, so nothing correct can break. Note the change in the release
notes regardless.

Optional, only if profiling asks for it: if just the diagonal is needed,
`diag(C)` is available from the Cholesky factor as the squared row-norms of
`L^-1`, avoiding the full `n x n` product. Not worth the complexity up front —
this is computed once per fit, not per-likelihood.

## Verification

- **Off-diagonals finite** for a well-conditioned matrix with an anti-correlated
  pixel pair. **No such test exists today** — the only assertion on this property
  (`test_autoarray/inversion/inversion/test_abstract.py:684`) checks `[0, 0]`, a
  *diagonal* element. That gap is why this shipped.
- **No `RuntimeWarning`.** Run the regression test under `-W error::RuntimeWarning`
  so a regression fails rather than warns.
- **`reconstruction_noise_map` still returns `sqrt(diag(C))`** — assert against a
  hand-computed value, and assert the invariant explicitly, not just the numbers.
- **The `inv`-vs-`cho_solve` A/B was run on 2026-08-22 and refuted two of the
  claims above.** Recorded so nobody re-derives the wrong reasoning:

  | Claim | Verdict |
  |---|---|
  | `inv` gives negative diagonals on well-formed SPD | **REFUTED** — 0 across cond 1e3–1e15, n=400, 20 trials each |
  | `inv` is materially less accurate on the diagonal | **REFUTED** — matches `cho_solve`; at cond 1e15 `inv` was marginally *better* |
  | Near-coincident mesh vertices degrade the inverse | **REFUTED** — with regularization the matrix stays PD (cond ~6.8e7 even at exactly duplicated columns) |
  | `inv` returns asymmetric output | **CONFIRMED** — 5.2e-7 at cond 1e12 vs 2.6e-16 |
  | `inv` silently succeeds on indefinite matrices | **CONFIRMED** |

  The surviving argument is **detection, not accuracy**. `cho_factor` raises
  `LinAlgError` on a negative eigenvalue; `inv` raises only on an *exactly*
  singular matrix and otherwise returns a plausible-looking covariance. At
  eigenvalue `-1e-8` all 300 diagonals came back negative (whole noise map NaN);
  at `-1.0`, **zero** did — no NaN, no warning, no error, wrong numbers.

  **Not established:** that a real `curvature_reg_matrix` *is* indefinite in a
  converged fit. `Settings.no_regularization_add_to_curvature_diag_value` and the
  `curvature_matrix_with_added_to_diag_from` docstring ("it is common for the
  `curvature_matrix` computed to not be positive-definite") say it happens, but no
  fit was instrumented to confirm it. Worth doing under the sibling prompt.
- `test_autoarray/inversion/plot/test_inversion_plotters.py:82,110` monkeypatch
  this property to force a `LinAlgError` and check plots/CSV degrade gracefully.
  Confirm the same exception still escapes — `cho_factor` also raises
  `LinAlgError`, so this should hold, but assert it.
- **Downstream:** this sweep covered PyAutoArray only, where the sole in-repo
  consumer is `reconstruction_noise_map`. Grep @PyAutoGalaxy and @PyAutoLens for
  `reconstruction_noise_map_with_covariance` before assuming containment.

## Also fold in

`reconstruction_noise_map`'s docstring claims it "is computed as the square root
of the diagonal of the `reconstruction_noise_map_with_covariance` matrix". The
code takes the diagonal of an already-square-rooted matrix — no second sqrt. The
two agree today only because sqrt is elementwise, which is precisely the bug.
Rewrite the sentence to match whatever ships.

## Note on the JAX path

This property uses bare `np`, not `self._xp`, so it is already numpy-only even
under a JAX fit — a JAX `curvature_reg_matrix` is coerced via `__array__`, forcing
a device→host sync. The scipy fix does not regress that (there was no JAX support
to lose) but it does make it explicit. Add `np.asarray` at the boundary, as above,
and note the limitation in the docstring rather than leaving it implicit.

## Provenance

- Found during: `complete/2026/08/numerical-inversion-failures.md` (2026-08-22)
- Sibling: `draft/bug/autoarray/reconstruction_noise_map_solver_mismatch.md`
- **Not** a symptom of the refuted non-positive-definite hypothesis in that record,
  nor of `complete/2026/07/pix-inversion-not-positive-definite.md` (also refuted).
