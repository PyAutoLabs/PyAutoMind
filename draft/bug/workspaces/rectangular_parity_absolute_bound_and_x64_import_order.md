# rectangular.py parity contract: absolute-nats bound, and import autogalaxy before jax

Type: bug
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: `scripts/imaging/jax_likelihood/rectangular.py` asserts `atol=1e-2, rtol=0` in nats with the PyAutoArray#552 comment; run bare (no harness env) `jax.config.jax_enable_x64` is True and `log_evidence` is finite; under `profile_smoke.yaml` it passes the new bound.
Review-minutes: 3
Filed: 2026-09-17

Split out of `mixed-precision-inversion-gap` at close-out — the library half
shipped in `complete/2026/09/mixed-precision-inversion-gap.md`
(PyAutoArray#556, closes PyAutoArray#552); this is the workspace leg, held back
because `autogalaxy_workspace_test` was claimed by `jax-runtime-and-parity`
(autolens_workspace_test#317) when the library merged. That claim cleared on
2026-09-17 (#317 closed, autogalaxy_workspace_test#122 merged, record
`complete/2026/09/jax-runtime-and-parity.md`), so this is startable now.

Two edits to `scripts/imaging/jax_likelihood/rectangular.py`:

1. **Contract shape.** Replace
   `np.testing.assert_allclose(float(fit.log_likelihood), float(fit_np.log_likelihood), rtol=2e-2)`
   with an absolute bound in nats (`atol=1e-2, rtol=0` is generous: the
   measured post-fix JAX-mixed vs NumPy-fp64 gap is 8e-5 nats at 316 pixels
   and 8e-4 at 716). Add a short comment citing PyAutoArray#552: the scalar is
   dominated by the noise normalization (proportional to N), so a relative
   tolerance shrinks the budget with pixel count while a delta-chi-squared
   error does not; the chi-squared sampling floor sqrt(2N) ~ 25 sets the scale
   a genuine model difference would show at. Keep the 17x17 mesh.
2. **Import order.** The script does `import jax` before `import autogalaxy`,
   so `autonerves` never gets to enable x64 and, run bare, the whole JAX leg is
   float32 (`log_evidence` prints `nan`; `use_mixed_precision` True/False are
   bit-identical; the JIT value is -792.88 against NumPy -791.956 where x64-on
   gives -791.9562). The autohands smoke harness exports `JAX_ENABLE_X64`, so
   CI is unaffected — but a parity script whose docstring promises an
   fp64-vs-fp64 check must not depend on the harness for it. Import
   `autogalaxy` (or `autofit`) first, or set `jax.config.update("jax_enable_x64", True)`
   explicitly. Every other `jax_likelihood` script in this workspace (and 15
   in `autolens_workspace_test`) has the same order; fix them in the same PR
   if the diff stays mechanical, else file the sweep separately.

Verification: `rectangular.py` under `profile_smoke.yaml` passes the new bound;
run bare, `jax.config.jax_enable_x64` is True and `log_evidence` is finite.

Follow-ups this prompt does not take (file via `/intake` when picked up): the
same absolute-nats contract for the other 14 mixed-precision parity scripts
across both test workspaces; `rectangular_mge.py` still using a 28x28 mesh on
the 0.3" data (the under-determined regime autogalaxy_workspace_test#117 fixed
for `rectangular.py`); `use_mixed_precision` has no YAML key unlike its
`Settings` siblings.
