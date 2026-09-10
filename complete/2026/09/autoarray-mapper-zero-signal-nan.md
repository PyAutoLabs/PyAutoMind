Fixed the `where`-around-a-division trap in `adaptive_pixel_signals_from`, where a
zero-signal adapt image made `max_sig` exactly 0 and put a 0/0 NaN in the branch the
`where` discards.

## PRs

- PyAutoArray#549 (merged `667deed3`) — CI green on all three legs
  (`unittest (3.12)`, `unittest (3.13)`, `unittest-nojax`).
- Issue PyAutoArray#548.

## What shipped

`autoarray/inversion/mappers/mapper_util.py` — both divisions in step 7 now use a **safe
denominator** (`max_sig = xp.where(max_sig > 0, max_sig, 1.0)` then divide), matching the
idiom `pixel_counts` already used two lines above. Step 8's exponentiation carried the
same trap one step on, so it now exponentiates a safe base and selects zero for
non-positive signals afterwards.

Eight tests in `test_autoarray/inversion/pixelization/mappers/test_mapper_util.py`: NumPy
value and finiteness, a `RuntimeWarning`-as-error assertion, finiteness parametrised over
`signal_scale in {0.5, 1.0, 2.0}`, NumPy/JAX parity with and without signal, and a finite
`jax.grad`. The JAX legs carry the repo's `requires_jax` skipif convention, which is what
kept the `unittest-nojax` CI leg green.

## The finding that mattered: the reported diagnosis was half right

The prompt (and the issue) read the symptom as "NumPy finite, JAX NaN — the two backends
disagree on the same input". **They already agreed in the forward pass.** `jnp.where`
selects correctly, so a JAX forward result was finite; six of the eight new tests pass on
the *unfixed* code, and only the clean-warning and finite-gradient legs go red.

What actually diverged was (a) NumPy's discarded `RuntimeWarning: invalid value
encountered in divide` and (b) the gradient — under `jax.grad` the NaN escapes the
discarded branch. So the fix is real and the trap is real, but it does **not** by itself
explain the originally reported `JAX(no jit) fit.log_likelihood: nan` in
`scripts/interferometer/jax_likelihood/rectangular.py`; something in that run was
differentiating. Recorded so nobody reads a recurrence of that symptom as a regression
here.

**Generalisable lesson:** for a `where(cond, a / b, …)` bug, the witness is the *gradient*,
not the forward value. A forward-parity test passes on the broken code and proves nothing.

## Behaviour deltas (deliberate, both away from a wrong answer)

- `signal_scale == 0` with a zero signal returned `1.0` (the `0 ** 0` convention), now `0.0`.
- A negative pixel signal returned NaN for a fractional `signal_scale`, or a spurious
  positive weight for an even integer one, now `0.0` — the signals are documented as
  varying between 0 and 1. Consistent with `image_mesh/abstract_weighted.py`, which already
  takes `np.abs(adapt_data)`.

## Ask (3) sweep — and the live hit it found

Done as an **AST pass over the whole package**, not grep, so multi-line calls could not
slip past: every `where(cond, x, y)` with a division anywhere inside either branch. Nine
hits. Two divide by the literal `3.0`; `image_mesh/abstract_weighted.py:72` already has an
explicit `if max_value <= 0.0` early return; four are NumPy-only preprocessing dividing by
a user-supplied scalar.

**Three in `autoarray/fit/fit_util.py` are the same bug class and live.**
`chi_squared_map_with_mask_from` (`:251`) is on the JAX likelihood-gradient path and
reproduces directly: with a masked-out pixel carrying zero noise the forward value is
finite (`2.0`) while `jax.grad` returns `[2., 1., nan]`. Arguably more serious than the
bug this task was filed for. Split out as
`draft/bug/autoarray/fit_util_masked_division_grad_nan.md` on the human's call rather than
widening the PR into a second module.

## Traps

- **`numba` is an `[optional]` extra, and without it eight `inversion/inversion` tests
  fail** with `ModuleNotFoundError` (w-tilde pixelized reconstructions are disabled). In a
  fresh remote container this reads exactly like pre-existing breakage on `main` — it is
  not. `pip install numba` takes the suite from `8 failed, 1415 passed` to a clean
  `1438 passed`. Worth checking before reporting main as red.
- PyAutoArray was **not** in the session's initial repo scope; attached with `add_repo` +
  a shallow clone at `/home/user/pyautoarray`.
- The Mind ledger branch's first push **failed to auto-merge** (`mind_ledger_merge.yml`
  run #169): `main` had moved and the two *generated* dashboard pages conflicted. Resolved
  by merging `origin/main` and **regenerating** the pages, never hand-editing them.

## Worktree

None — `web-github` session clone, no task worktree, no `gh` (GitHub via `mcp__github__*`).

## Original prompt

# Adapt-density mapper: a zero-signal adapt image is NaN on the JAX path and finite on NumPy

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Filed: 2026-09-06
Issued: 2026-09-10

Found during the phase-6 rebuild of the ci-timing-fast-tests epic
(autolens_workspace_test#293 / #294). In
`scripts/interferometer/jax_likelihood/rectangular.py` an adapt image was built
from the *unlensed* true source profile evaluated on the image-plane grid — a
compact blob sitting where the Einstein ring is not, so under
`RectangularRTUAdaptDensity` almost every source pixel receives zero adapt
signal. The NumPy path returns a finite likelihood with a warning; the JAX path
returns NaN, and `fitness._vmap` collapses to the `resample_figure_of_merit`:

```
NumPy fit.log_likelihood: -3154.8962799401297
  .../autoarray/inversion/mappers/mapper_util.py:84: RuntimeWarning: invalid value
  encountered in divide
    pixel_signals = xp.where(max_sig > 0, pixel_signals / max_sig, pixel_signals)
JAX(no jit) fit.log_likelihood: nan
raw vmap: [-1.e+99]
```

`xp.where(max_sig > 0, pixel_signals / max_sig, pixel_signals)` guards the
*selection* but still evaluates the division; NumPy's 0/0 warning is discarded
by the selection while on the JAX path the NaN propagates into the likelihood
(the usual `where`-inside-`grad`/NaN-propagation pattern; a safe denominator
`xp.where(max_sig > 0, max_sig, 1.0)` is the standard fix). The workspace script
was corrected to adapt to the *lensed* true image (the right object anyway), so
nothing is red — but the two backends disagree on the same input, which is the
class of divergence the `_test` repos exist to catch.

Ask: (1) reproduce with a unit test on `mapper_util` where `max_sig == 0` for
some source pixels, both backends; (2) fix the division so both paths agree
(finite, and identical); (3) check the same `where(cond, a / b, a)` pattern
elsewhere in `autoarray.inversion` (grep for `/ max_` and `xp.where(` around
divisions).
