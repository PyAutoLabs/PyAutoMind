## message-log-partition-tuple-shape
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1510 (closed 2026-08-22)
- completed: 2026-08-22
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1513 (MERGED as
  ffa46d19647dc2db26901564a9db9e9d54726d09)
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/152 (MERGED as
  a620a53e94436e2d9f7fb19bbe5f33508ad6a6a9) — the cap widen, merged second
  behind the library-first gate.
- record-provenance: the code shipped on 2026-08-22 from session
  `claude/message-log-partition-tuple-shape`, but the prompt was never advanced
  out of `draft/bug/autofit/` and no record was written. This record was
  reconstructed on 2026-08-25 from the closed issue, both merged PRs and the two
  merge commits when `/start_dev` was re-run on the stale draft. Nothing was
  re-implemented; the code side was already complete on both `main`s.
- root cause: jax 0.11 changed `jnp.broadcast_arrays` to return a **tuple**
  instead of a **list** (mirroring the NumPy 2 change to
  `np.broadcast_arrays`). `MessageInterface.shape` type-tested that container
  with `isinstance(..., list)`, so on 0.11 the JAX branch stopped matching,
  control fell through to `self.broadcast.shape`, and every
  `BetaMessage`/`GammaMessage` construction under `jax.jit` died with
  `AttributeError: 'tuple' object has no attribute 'shape'`.
  `jax.scipy.special.betaln` / `gammaln` were **not** implicated — the prompt's
  guess at a `jax.scipy.special` return-shape change was wrong.
- summary: `MessageInterface.shape` now returns the real broadcast shape read
  off the container's first element (matching on `(list, tuple)`, `()` for an
  empty container) instead of the unconditional `()` sentinel, and `size` /
  `ndim` derive from that shape rather than attribute-accessing the container.
  `PyAutoNerves/pyproject.toml` then widened the `jax`/`jaxlib` cap from
  `<0.11.0` to `<0.12.0` and replaced the stale "Cap stays <0.11" comment.
- key finding — the minimal fix was wrong: widening the `isinstance` to
  `(list, tuple)` turns the four failing tests green while preserving a
  **silent numerical bug that was live on jax 0.10**. The `()` sentinel made
  `_broadcast_natural_parameters` miss the equal-shape branch and match
  `shape[1:] == self.shape` instead, inserting a spurious axis, so batched
  JAX-backed `logpdf` returned an `(n, n)` matrix of wrong values where NumPy
  returns the correct `(n,)` vector. `size` and `ndim` were worse still — no
  JAX branch at all, so they raised `AttributeError` for any JAX-backed message
  on 0.10 too. The adversarial review of the first plan is what caught this.
- key finding — the fifth failure had already been fixed: the prompt reported
  five failures, but `test_autofit/graphical/functionality/test_messages.py::test_beta`
  was already cleared by the `np.generic` xp-dispatch fix (PyAutoFit
  `19c679583`). The real compat surface was the four
  `test_message_log_partition_is_jittable_and_matches_numpy` parametrisations.
- regression guard: a NumPy/JAX parity case over `NormalMessage` /
  `BetaMessage` / `GammaMessage` asserting equal `.shape` / `.size` / `.ndim`
  **and** equal batched `logpdf` values and shape. It fails six ways against the
  `()` sentinel on jax 0.10 alone, so the sentinel cannot come back silently.
- evidence: `pytest test_autofit` 2030 passed on both jax 0.10.2 and 0.11.1
  (Python 3.12, `[optional]` extras installed — blackjax and nautilus-sampler in
  particular, without which 18 tests skip). The ten
  `autofit_workspace_test/scripts/jax_assertions/` scripts were unchanged across
  every version-by-fix cell (9/10 pass; the `priors_xp_dispatch` float32
  tolerance failure is pre-existing and identical in all four cells). The cap
  widen's gate was run as forced `jax==0.11.1` installs, since downstream CI
  resolves jax from this very cap and so could not pre-verify it:
  `test_autogalaxy` 1103 passed / 1 skipped, `test_autolens` 532 passed /
  1 skipped, `test_autonerves` 157 passed, `test_autoarray` clean — identical on
  0.10.2 and 0.11.1.
- blast radius of the cap widen: the full public-API diff 0.10.2 → 0.11.1 across
  `jax`, `jax.numpy`, `jax.scipy.*`, `jax.lax`, `jax.tree_util`, `jax.nn`,
  `jax.random` had one removal (`jax.lax.dce_sink_p`, unused here); everything
  else additive. A container-return-type sweep over 22 entry points found two
  list → tuple changes: `broadcast_arrays` (this bug) and `meshgrid` — all nine
  `meshgrid` call sites across PyAutoFit and PyAutoArray tuple-unpack, so they
  were unaffected. **Any new `isinstance` / `.append` handling of a jnp
  container is a latent repeat of this bug.** `jnp.empty` is now uninitialized
  and `take_along_axis` flipped its negative-index default — no live call sites
  in the family. `jaxnnls==1.0.1` is bit-identical under 0.11.1.
- side effect named at the cap: jax 0.11 declares `numpy>=2.1` and
  `scipy>=1.15`, so the widen raises those effective floors for every install
  that resolves jax. There is no cohort left on 0.10 — PyAutoFit, PyAutoNerves
  and PyAutoArray all declare `requires-python = ">=3.12"` and jax 0.11 requires
  `>=3.12` — so the widen is an all-users change, which is why the gate spanned
  the ecosystem rather than autofit alone.
- why it mattered: jax is a base dependency since PyAutoLens#702, and the
  `<0.11` cap conflicted with e.g. Colab's preinstalled jax.
- adjacent findings, deliberately left unfiled at ship time:
  (1) `autofit_workspace_test/scripts/jax_assertions/priors_xp_dispatch.py`
  fails on library `main` under both jax versions — float32/float64 tolerance
  mismatch, max relative difference 1.5e-7 against `rtol=1e-7`;
  (2) `.../multi_start_gradient_auto_convergence.py` fails on `main` under both
  versions — recovers `normalization = 12.32` against `25.0 +/- 3.0` after
  auto-convergence stops at 1 of 300 steps;
  (3) `NormalMessage(1.0, jnp.array([1.0, 2.0]))` dispatches to the **NumPy**
  backend — `__init__` selects `xp` from the first parameter's type only, so a
  leading Python float wins over a trailing JAX array.
  None of the three has a prompt in `draft/` as of 2026-08-25.
- prior art: #1458 / #1460 (`xp.stack` message constructors) and #1459 / #1461
  (Beta/Gamma `log_partition` xp dispatch, which introduced the code this bug
  landed in). This was a container-type regression in the shared `shape`
  property, not a backend-dispatch leak.

## Original prompt

# jax 0.11 breaks beta/gamma message log_partition under jit ('tuple' object has no attribute 'shape')

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoNerves
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-08-19 (backfilled from git)

Found during the JAX-default-dependency arc (PyAutoLens#702): widening the jax
cap in autonerves from `<0.11.0` to `<0.12.0` let CI resolve jax/jaxlib 0.11.1,
which fails five autofit tests on both Python legs
(run 32285606183; local jax 0.10.2 passes):

- `test_autofit/graphical/functionality/test_messages.py::test_beta`
- `test_autofit/messages/test_jax_trace.py::test_message_log_partition_is_jittable_and_matches_numpy[{scalar,batched}-{gamma,beta}]`

all with `AttributeError: 'tuple' object has no attribute 'shape'`.

The cap widen was reverted in PyAutoNerves#150 (commit 848a254) with a comment
pointing here — the promotion shipped with the cap still `<0.11.0`.

Task: find what jax 0.11 changed in the beta/gamma `log_partition` trace path
(likely a `jax.scipy.special` return-shape/tuple change or a shape-polymorphism
change under jit), fix autofit's message code to be compatible with both 0.10
and 0.11, then widen the autonerves cap to `<0.12.0` in the same arc
(@PyAutoNerves pyproject — remove the "Cap stays <0.11" comment). The cap
widen matters because jax is now a base dependency and the `<0.11` cap
conflicts with e.g. Colab's preinstalled jax.

Note (2026-08-19, later same day): the no-jax CI leg exposed that
beta/gamma/normal message `xp` dispatch misrouted NumPy scalars
(np.int64/np.float64 are not int/float under NumPy 2) into the JAX branch —
fixed on the same branch (PyAutoFit 19c679583, np.generic added). `test_beta`
was one of the five jax-0.11 failures, so re-test under 0.11 AFTER that fix
lands: the remaining failures are probably only the deliberate jax-trace
tests (`test_jax_trace.py`), which narrows the compat surface.
