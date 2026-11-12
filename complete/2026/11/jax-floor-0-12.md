## Outcome

The jax/jaxlib floor `>=0.12.0,<0.13` SHIPPED in release **2026.11.12.1**
(PyAutoHands run 43222979602, attempt 2 all green; tag 2026.11.12.1 in every
library). A fresh `pip install autolens==2026.11.12.1` resolves jax/jaxlib
0.12.0.1. Research PyAutoNerves#213; decision PyAutoDNA
decisions/jax-cpu-policy-2026-11.md (approved 2026-11-11).

### Merged
- Phase 2: PyAutoNerves#216 (pins, README, Colab `_ensure_jax_floor` + restart
  prompt, no default XLA flag), PyAutoHands#336 (release.yml jax pins),
  PyAutoHeart#332 (workspace-validation pins; re-pin last + assert 0.12, since
  a later `autofit[optional]` install had silently downgraded jax to 0.11.2).
- Phase 3: PyAutoFit#1770, PyAutoArray#689, PyAutoGalaxy#702, PyAutoLens#824
  (`autonerves>=2026.11.9.1.post1`, not `>2026.11.9.1`, because PEP 440 `>V`
  rejects V.postN = source Nerves in library CI); autolens_workspace_test#364,
  autogalaxy_workspace_test#135, euclid_strong_lens_modeling_pipeline#126
  (smoke asserts 0.12; un-quarantined 5 hang scripts; re-pinned 2 #683 values
  by +2·½ln 1e8; NEEDS_FIX + smoke-allowlist removal for 2 zero-contour grad
  scripts).

### Validation
- Phase 1: 0 hangs on 0.12.0.1 in 15 runs at 4 cores, no flag. CPU unit
  suites clean (Fit's local failures were an xdist race). GPU CUDA 12/13 extras
  run; the GPU-only failures are identical on 0.11.2.
- Release validation dev87601: 818 pass / 0 fail / 0 timeout. Fresh workspace
  smoke on main: 136/136. Released with --force over YELLOW (PyAutoArray#675
  stale PR + docs-only PyAutoLens#826 drift), human-approved.

### Follow-ups / not done
- draft/bug/autogalaxy/zero_contour_grad_fails_on_jax_0_12.md: jax.grad through
  jax_zero_contour fails on 0.12 (custom_root transpose).
- PyAutoCTI still floors `autonerves>2026.10.4.1` (not in scope); raise it.
- PyAutoHeart jax-compatibility.yml matrix (0.9.2/0.11.2) is unchanged: it
  needs a fresh incident manifest from a 0.12 candidate.
- RAL shared venv still on jax 0.11.2: the human runs the upgrade (remote
  write blocked from the session).
- The existing drafts for eigen-flag workaround removal and the Heart hang
  guard can now start.
- PyAutoFit docs.yml `generated-search-docs` should go green post-publish;
  re-check.

## Original prompt

# Raise the JAX floor to 0.12.0 (jax and jaxlib) after a Heart validation

Type: feature
Target: PyAutoNerves
Repos:
- PyAutoNerves
- PyAutoHeart
Priority: high
Consequence: judge
Issued: 2026-11-11

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## Why
jax/jaxlib 0.11.2 (today's resolved version and "recommended baseline") deadlocks XLA:CPU likelihoods: on RAL at 4 cores every reproducer hung on the first call (25/25 cells), intermittent at 8 cores, none at 16. jax 0.12.0 and 0.12.0.1 passed 100/100 cells per setting (0 hangs in 30,000 calls) with no flag. The FFT-pool part is upstream jax#41265, fixed by openxla/xla#50091 in 0.12.0.

## What
1. Heart validation on jax 0.12 first: full library unit suites + workspace smoke on CPU and GPU (CUDA 12/13 plugins), including blackjax, optax, nufftax, jaxnnls; rerun autolens_workspace_test multi_dataset/jax_likelihood/delaunay_mge.py, delaunay.py, shared_preloads.py, rectangular.py (all hung in release-integrate on 0.11.2, delaunay_mge even with the eigen flag).
2. PyAutoNerves pyproject: `jax>=0.12.0,<0.13` AND `jaxlib>=0.12.0,<0.13` (both: jax 0.12.0 accepts jaxlib 0.11.2), replacing the 0.7 floor and the 0.10.*/0.11.0 exclusions; README "JAX compatibility" + "recommended baseline" updated. numpy floor becomes 2.2; x86-64 needs Haswell+.
3. Do NOT add a default XLA:CPU flag: the eigen flag costs +18-50 % per call on pixelized likelihoods on 0.12.
