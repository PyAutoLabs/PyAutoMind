# Default XLA GPU autotuning off in the autoconf jax_wrapper (env-respecting,

Type: feature
Target: PyAutoConf
Repos:
- PyAutoConf
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Default XLA GPU autotuning off in the autoconf jax_wrapper (env-respecting, same pattern as the compilation cache). Rollout of autolens_profiling#74 verdict 2: the pathological ~7m30 cold GPU compile IS autotuning (--xla_gpu_autotune_level=0 gave 17x cold probe reduction, -40 percent cold full fit, bit-identical fixed-input logL, steady-eval parity across the measured A100 matrix; worst cell ~4 percent, and the 4800-eval full fit was faster end-to-end). @PyAutoConf jax_wrapper.py should include --xla_gpu_autotune_level=0 in the XLA_FLAGS it assembles UNLESS the user's flags already set an autotune level (respect any pre-set value; append pattern from PyAutoConf#128). Combined with the default cache this takes worst-case first-fit UX from ~70min to ~30s. Keep it env-respecting so clusters can re-enable autotune for tuned-kernel workloads. Small change: one flag in the existing append logic + tests mirroring test_jax_wrapper.py.

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from user-intake -->
