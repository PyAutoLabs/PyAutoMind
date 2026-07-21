# Multi-band FactorGraphModel value_and_grad compile — deeper dig + productize the fix

Type: research
Target: PyAutoFit
Repos:
- PyAutoFit
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to the multi-band compile investigation. **Experiment A is already done**
(autolens_profiling branch `research/multiband-compile-ab`; census in
`autolens_profiling/jax_compile/README.md` "Multi-band … heterogeneous-shape cliff"
section). Established, on local CPU MGE `vag` over a 4-band `af.FactorGraphModel`:

- **Homogeneous 4-band (1 distinct shape) == single-band**: cold compile 120s
  (≈ the 117s single-band figure). XLA fuses identical-shape factors into one
  shared kernel; the factor graph adds no compile cost when band shapes match.
- **Heterogeneous (2 distinct shapes) = 704s cold = 5.9× the control, superlinear
  in the number of distinct shapes** (2 shapes → ~6×, not 2×). Trace and steady
  eval unchanged → pure XLA fusion-*compilation* effect. This reproduces the real
  >1h cold compile of an N-distinct-shape multi-wavelength fit.
- **Persistent cache rescues both arms** (multi-band caching now certified): warm
  compile 2–7s. The cliff is a one-time first-compile (cache-miss) cost per graph
  structure.

Reproduce via the probe cells added in Experiment A: `python jax_compile/probe.py
--dataset-class datacube_img[_hetero] --model-type mge --transforms vag
--cache-dir <fresh>` (run twice cold/warm). Two distinct shapes come from
`jwst` (0.03") + `jwst_lw` (0.06") channels.

This task is the deeper dig + the fix, as **one task**:

1. **Sub-investigation B — the source lever.** Determine whether a **per-factor
   jit boundary** inside `af.FactorGraphModel.log_likelihood_function` bounds the
   cold compile to N×single-band + a linear combine, i.e. removes the superlinear
   heterogeneous penalty **without** padding. If it does, this is the productizable
   PyAutoFit change; if it doesn't, document why (e.g. AD couples the factors).
   Also confirm the `MultiStartProdigy` `batch_size` / `lax.map` transform behaves
   the same multi-band as single-band (add a `laxmap_vag` row).
2. **Sub-investigation C — A100 rows + verdict.** Add A100 multi-band `vag` rows
   (`datacube_img` / `datacube_img_hetero`) to the `jax_compile` census; the
   absolute cliff should be far lower (single-band A100 `vag` cold ~28s vs 229s
   CPU). Ship the final N-band compile verdict.
3. **Productize the immediate user workaround** — pad short-wavelength bands to a
   common grid so all factors share one fused kernel — as a documented recipe
   and/or helper for N-band gradient fits.

Deliverable: multi-band A100 census rows + either a productizable compile-reduction
lever (per-factor jit or the padding helper) or a documented "GPU-only /
same-shape-bands" verdict. **Out of scope:** re-opening the #71 single-band
settings verdict.

<!-- filed 2026-07-21 from ideas.md (research multiband-compile · Experiment A); intake misclassified as docs/autofit, hand-corrected to research/autofit -->
