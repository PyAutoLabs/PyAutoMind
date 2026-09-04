# Verify jax.jit / jax.grad parity on the critical-curve and caustic calculations

Type: test
Target: autolens_workspace_test
Themes:
- jax-gradient
- jax-compile
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-06-26 (backfilled from git)

<!-- TRIAGE RESOLVED 2026-09-04: re-filed from draft/triage/ to
     draft/test/autolens_workspace_test/ as the note asked; Type/Target/Priority
     set accordingly. -->

[resume]

claude --resume 015b4ac4-0900-4d06-b39a-e1f1bd31af80 



[JAX]

The implementation has been tested successfully and runs on the HPC.

I now want us to test whether using jax.jit and jax.grad on the critical curve and caustic calculations
works, and if it gives the same result. Do this on the @autolens_workspace_test.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
