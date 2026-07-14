# Extend the Profiling Agent scope to track JAX compile/eval times of release-validation heavy scripts

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Extend the **PyAutoBrain Profiling Agent** (`agents/conductors/profiling/`, workspace
`autolens_profiling`) scope to track **JAX compile-time and eval-time** of the
release-validation heavy scripts, so we can speed them up.

The 2026-07-13 release-validation tail (PyAutoHeart#72,
[[project_release_2026_07_13_blocked_3bugs]]) is largely **PERF**: real-search +
finite-difference JAX scripts blow the 300s per-script cap under `mode=release`
(`jax_grad/imaging_pixelization.py` >400s, `jax_grad/interferometer.py`,
`imaging/features/shapelets/modeling.py`, group/slam chaining, `jax_likelihood
multi/shared_preloads`). We are upping the release `BUILD_SCRIPT_TIMEOUT` to unblock
now (see PyAutoHeart#72); the **durable fix is to speed them up**.

Extend the Profiling Agent's `campaign` / `ingest` / `triage` scope so it measures,
for these scripts, the **`jax.jit` compile time** + **per-eval time** (CPU, and the
FD-gradient full-run cost), records baselines, flags regressions, and emits a
**ranked slowest-JAX-scripts report** that `/hygiene` can act on. Candidate root
causes to look for (see [[project_jax_gradient_audit_shipped]] and
[[feedback_jax_closure_cache_busts]]): recompilation / JIT cache-busting (fresh `f`
per call), finite-differences where `jax.grad` would work but a `custom_jvp` is
missing (Delaunay), and oversized problems under the real-search release profile.

Deliverable: a Profiling-Agent scope extension (compile/eval-time coverage of the
release-validation JAX scripts) + the ranked report driving a hygiene/perf backlog.
Large — expect to phase at start_dev time. Cross-ref the mode=release timeout/scope
policy question on PyAutoHeart#72.

<!-- formalised via the Intake (Conception) Agent on 2026-07-14 from user-intake; target hand-corrected PyAutoHeart -> PyAutoBrain (Profiling Agent is a Brain conductor) -->
