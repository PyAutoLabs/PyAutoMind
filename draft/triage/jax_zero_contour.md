# <!-- TRIAGE: needs manual review before routing

Type: triage
Target: ?
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised

<!-- TRIAGE: needs manual review before routing. Session-resume fragment with
     little standalone context. Likely work-type `test` (verify jax.jit/jax.grad
     parity for critical-curve/caustic calcs), target `autolens_workspace_test`.
     Re-file to test/autolens_workspace_test/ once confirmed. -->

[resume]

claude --resume 015b4ac4-0900-4d06-b39a-e1f1bd31af80 



[JAX]

The implementation has been tested successfully and runs on the HPC.

I now want us to test whether using jax.jit and jax.grad on the critical curve and caustic calculations
works, and if it gives the same result. Do this on the @autolens_workspace_test.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
