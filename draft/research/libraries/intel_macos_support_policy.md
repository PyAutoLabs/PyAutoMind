# Is Intel macOS a supported platform, and what is the numpy-only contract?

Type: research
Target: libraries
Repos:
- @PyAutoNerves
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
Themes:
- release
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-22 (backfilled from git)

## Original request (verbatim, 2026-08-22)

> are you sure Intel mac can't use any JAX event CPU this seems like a bigger
> issue in general?

Asked while reviewing the pynufft removal
(`complete/2026/08/remove-pynufft-legacy-transformer.md`), whose
Intel-Mac caveat was accepted as a release-note line on the understanding that
the general platform question gets its own task.

## The finding that prompted it (verified against PyPI, 2026-08-22)

It is not a CPU-vs-GPU limitation — Google dropped x86_64 macOS builds outright:

- `jaxlib`'s last macOS x86_64 wheel is **0.4.38**, uploaded **2024-12-17**
  (`jaxlib-0.4.38-cp31{0,1,2,3}-macosx_10_14_x86_64.whl`). Every release since,
  through 0.11.1, ships `macosx_11_0_arm64` only.
- `jaxlib` has **never shipped an sdist**, for any version — so `pip` has no
  build-from-source fallback. Building it needs Bazel; conda-forge is the only
  other plausible channel and was not reachable from the session that checked.
- PyAutoNerves therefore markers jax/jaxlib/jaxnnls as
  `sys_platform != "darwin" or platform_machine == "arm64"`
  (`PyAutoNerves/pyproject.toml:38-40`) and states the intent as "NumPy-only
  path instead of failing at install".

## Why this is bigger than one transformer

The stated contract is that Intel macOS silently gets a NumPy-only path. What
that actually covers has never been audited. The pynufft removal surfaced one
concrete hole: `nufftax` is pure-JAX (even its `xp=np` path calls
`nufftax.nufft2d2`), so with JAX absent **both** NUFFT transformers are
unavailable and interferometer analysis falls back to `TransformerDFT`
(O(N_vis x N_pix) — correct, but impractical for real ALMA/SMA data).

If one "NumPy-only" path is really a JAX path in disguise, others may be too.

## Task

1. **Audit the claim.** Enumerate what actually works on a JAX-less install:
   which code paths genuinely branch on `xp`, and which import JAX
   unconditionally somewhere down the stack (`jax_wrapper`, `nufftax`,
   `jaxnnls`, `tfp-nightly`, the Matern-kernel regularization path). A CI job
   or a container with JAX uninstalled is the cheap way to get the real answer.
2. **Decide the policy explicitly** and write it down once, somewhere users
   read: is Intel macOS supported, best-effort, or unsupported? "Silently
   degrades" is the current de-facto answer and it is the worst one — a user
   gets an install that resolves and then fails at analysis time.
3. **Make the failure legible** whichever way the policy lands: if supported,
   the numpy paths need to be real and tested; if not, say so at install or
   import rather than at the first transformer construction.
4. Feed the answer back to the pynufft removal's release note, which currently
   asserts Intel-Mac users keep `TransformerDFT`.

## Acceptance

- A written, discoverable platform-support statement covering Intel macOS.
- An evidence-backed list of what does and does not work without JAX.
- No silent install-then-fail path left for the unsupported case.
