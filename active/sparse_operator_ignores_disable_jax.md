# apply_sparse_operator ignores PYAUTO_DISABLE_JAX=1 (a disable_jax() helper beside small_datasets())

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoNerves
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-06
Epic: ci-timing-fast-tests
Phase: 8c
Issued: 2026-09-06

Library leg of phase 8 (autolens_workspace#536): a shared-machinery finding from the
user-workspace slow-script diagnosis, traced to the unguarded call in the library and written
up as a diff there rather than patched per script. The measurement and the diff below are the
phase-8 executor's; nothing was applied to the library. Library-first gate: this lands before
any workspace script relies on it. Validation: the library unit tests plus a before/after of
the named workspace scripts under the smoke profile.

## (a3) PyAutoArray — `apply_sparse_operator(use_jax=True)` ignores `PYAUTO_DISABLE_JAX=1`

**Files** `autoarray/dataset/interferometer/dataset.py:211`,
`autoarray/dataset/imaging/dataset.py:579` — `apply_sparse_operator`

`PYAUTO_DISABLE_JAX=1` is a smoke-profile default and is honoured in exactly one place in the
stack, `autofit/non_linear/analysis/analysis.py:68`. `apply_sparse_operator` never consults it,
so a script that passes `use_jax=True` (the production demo, and the correct thing for the
script to demonstrate) pays a JAX JIT compile under a harness that explicitly asked for NumPy.
The workspace docs already assert the env var does this — `autogalaxy_workspace
scripts/interferometer/start_here.py:283`: *"Force NumPy with `use_jax=False` (or
`PYAUTO_DISABLE_JAX=1`)"* — so the library is not matching its own documented contract.

**Measured**: `compiler.py:backend_compile_and_load` = 3.19 s
(`al_ws interferometer/features/pixelization/delaunay.py`), 2.42 s (`al_ws
interferometer/modeling.py`), 2.34 s (`ag_ws interferometer/start_here.py`).

```diff
--- a/autoarray/dataset/interferometer/dataset.py
+++ b/autoarray/dataset/interferometer/dataset.py
@@ def apply_sparse_operator(self, ..., use_jax: bool = False):
+        # `PYAUTO_DISABLE_JAX=1` is a harness-level override, not a preference: it is
+        # the documented way to force the NumPy path (see the workspace start_here
+        # guides). An explicit `use_jax=True` in a script must not defeat it, or the
+        # smoke profile pays a JIT compile for a backend it asked to disable.
+        if os.environ.get("PYAUTO_DISABLE_JAX") == "1":
+            use_jax = False
```

(identically in `imaging/dataset.py`; `os` is already imported in both modules). The predicate
belongs in `autonerves.test_mode` as a `disable_jax()` helper beside `small_datasets()` rather
than as a bare `os.environ` read — there is currently no such helper, which is why the variable
is honoured in only one place.
