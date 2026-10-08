# `JAX_ENABLE_X64=False` is overridden to True, so the fp32 inference leg runs fp64 and the preflight's x64 warning is wrong

Type: bug
Target: PyAutoNerves
Repos:
- PyAutoNerves
- PyAutoFit
- autofit_inference
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: under `JAX_ENABLE_X64=False` (and `0`), importing autofit leaves `jax.config.read("jax_enable_x64")` False, and an `autofit_inference` `local_jax_cpu_fp32` row records `device.x64` False; with the variable unset, x64 is still forced on; the `preflight.py` `X64_WARNING` text matches the behaviour that actually ships, checked by a test.
Unattended: ready
Filed: 2026-10-08

Found by the A3b witness (PyAutoFit#1678 / PR #1681, record `complete/2026/10/search-ext-a3b-nss-preflight.md`). Two linked defects come from one root cause.

**1. Nerves overrides an explicit opt-out.** In `autonerves/jax_wrapper.py:88-97`:

    jax_enable_x64 = os.environ.get("JAX_ENABLE_X64")
    if jax_enable_x64 is None:
        jax_enable_x64 = False
    elif isinstance(jax_enable_x64, str):
        jax_enable_x64 = jax_enable_x64.lower() == "true"
    if not jax_enable_x64:
        os.environ["JAX_ENABLE_X64"] = "True"

   Any value other than `"true"` is treated the same as "unset", so x64 is forced on. That includes an explicit `False` or `0`. A user cannot opt out of fp64 through the environment.

**2. The fp32 inference leg is really fp64.**
   - `autofit_inference/_autofit_inference_cli.py:193` sets `{"JAX_ENABLE_X64": "False" if precision == "fp32" else "True"}`.
   - Nerves then turns that back on, so `local_jax_cpu_fp32` rows record `device.x64` True.
   - No fp32 leg has ever measured fp32, and any fp32 row already ingested by PyAutoInsight is mislabelled.

**3. The preflight warning describes the wrong behaviour.** In PyAutoFit, `autofit/non_linear/search/preflight.py:65` (`X64_WARNING`) says "setting JAX_ENABLE_X64=0 leaves it off". Today that is false.

**Why it matters:**
- fp32 vs fp64 is a declared axis of the inference protocol, and its results are currently fiction.
- The A3b x64 check (`requires_fp64`) can only be exercised by importing jax first.
- The user-facing warning gives advice that does not work.

**Suggested fix direction:**
- In Nerves, force x64 only when the variable is unset. Respect an explicit false value (`false`/`0`/`no`/`off`).
- Then align the PyAutoFit warning text with the fixed behaviour.
- Mark or invalidate the existing `*_fp32` rows in `autofit_inference` (and their Insight ingest) instead of silently re-running over them.

**Completion criterion:** the Witness above, plus a note in the `autofit_inference` README or catalogue saying that fp32 rows before the fix were fp64.
