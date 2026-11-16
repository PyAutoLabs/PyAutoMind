# Matern nu gradient via Bessel K order derivative

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- pixelization
- jax
Difficulty: large
Autonomy: supervised
Priority: low
Memory: wiki/methods/concepts/autodiff-implicit-diff.md
Status: formalised
Consequence: judge
Witness: `jax.grad` of `matern_kernel` (and of a Matérn regularization log-evidence term) with respect to `nu` matches a central finite difference to rtol 1e-6 across nu in [0.5, 5.5] and r spanning the regularization scale, with the z-gradient and values unchanged (existing `bessel_kve_parity.py` still passes).
Review-minutes: 25
Unattended: ready
Lane: any

Follow-up from PyAutoArray#694 (vendored `bessel_kve`, record `complete/2026/11/matern-vendor-bessel-kve.md`).
The vendored `autoarray/inversion/regularization/bessel.py` keeps tfp's semantics: its `jax.custom_jvp`
ignores the tangent of the order `v`, i.e. dK_v/dv is treated as zero. Because `nu` also enters the Matérn
kernel through `Gamma(nu)`, `z**nu` and `z = sqrt(2 nu) r / l`, a JAX gradient of the kernel with respect to
`nu` is therefore *wrong, not zero* (independent review: -0.803 vs FD +0.059 at r=0.7, l=1.3, nu=1.7).
`kv_xp` and `MaternKernel` docstrings now warn that `nu` must be treated as static.

This only matters if `nu` is sampled with a gradient-based search (NUTS/HMC, BlackJAX) or a gradient
optimiser — nu is a free prior (`Uniform(0.5, 5.5)`) on `MaternKernel`, so that is plausible.

Options to evaluate:
- an analytic/series dK_v/dv (DLMF 10.38: closed forms at half-integer v; integral representation
  `dK_v/dv = ∫_0^∞ t sinh(vt) e^{-z cosh t} dt` evaluated by quadrature) registered in the custom JVP;
- a central finite difference in v inside the JVP (cheap; v-step chosen relative to v, avoiding the
  half-integer recurrence switch);
- confirm whether any current pipeline actually differentiates w.r.t. nu before investing.
Keep the z-derivative rule and values bit-for-bit; NumPy path unaffected.

<!-- formalised by the Intake (Conception) Agent on 2026-11-15 from file:/tmp/claude-0/-home-user/3f1fc7c8-0fc2-59a3-b82b-ac29d67b5941/scratchpad/intake1.md -->
