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

**Reproduction-context follow-up (2026-07-21) — what actually causes the >1h.**
Heterogeneity ALONE does not reach the reported >1h: hetero `vag` topped out at
~12 min. Profiling the `MultiStartProdigy` transform (`lax.map`/`vmap` over
starts) on the SAME (single-core, `nproc=1`) host, homogeneous 4-band graph,
located the dominant driver:
- `vag` (start-width 1): 120 s compile
- `vmap_vag` (width 2): 209 s compile
- `laxmap_vag` (MultiStartProdigy default: `batch_size` 4 / `n_batch` 16):
  **did not finish compiling in 55 min** (killed).

So compile scales steeply with multi-start width, and the full production
transform is intractable to compile cold on one core even before heterogeneity —
which then multiplies it by 5.9×. Driver order: **transform × core count >>
heterogeneity >> the factor graph itself.** The `nproc=1` dev host is worst-case
for XLA compile (host-CPU-bound); HPC/A100 numbers will be far lower. Biggest
shipped lever is the persistent cache (amortizes the whole cold cost). This is
recorded in the `jax_compile/README.md` multi-band section (findings 2 + 4).

This task is the deeper dig + the fix, as **one task**:

1. **Sub-investigation B — the source lever (now concrete + validated).** The
   dominant compile cost is the in-XLA `lax.map` scan in `MultiStartProdigy`, NOT
   the batching itself: at vmap width 1, `pyloop_vag` (Python loop over `vmap`
   chunks, batching hoisted out of XLA) compiled in 166 s vs `laxmap_vag` (in-XLA
   `lax.map` scan) intractable (>30 min). **Implement Python-loop multi-start
   batching in `MultiStartProdigy`** (the `pyloop` pattern in
   `autolens_profiling/jax_compile/probe.py`): iterate starts in Python over small
   `vmap` chunks so no scan is compiled; `batch_size` = vmap width becomes a
   compile/throughput tunable (small CPU, wider GPU). Benchmark cold compile +
   **per-eval runtime, especially on GPU/A100** vs the current `lax.map` path —
   pyloop trades on-device loop fusion for host dispatch overhead and loses
   composability (can't jit/scan over the whole search), so the win is clear on
   CPU/limited-RAM but is a compile-vs-throughput trade on A100 (pick chunk width
   per device). Clean re-confirm DONE (2026-07-21): `laxmap bs=1` compile was
   OOM-killed (~6 GB RSS) even from a 10 GB-free start → the `lax.map` scan path is
   memory-explosive to compile here, confound resolved in favour of the lever.
   Secondary: whether a per-factor jit boundary inside
   `af.FactorGraphModel.log_likelihood_function` additionally bounds the
   heterogeneity multiplier (N×single-band + linear combine) without padding.
2. **Sub-investigation C — multi-core / A100 rows + verdict, including the
   transform.** Add A100 (and/or multi-core CPU) multi-band rows for BOTH `vag`
   AND the production `laxmap_vag` transform (`datacube_img` /
   `datacube_img_hetero`) to the `jax_compile` census — the transform is the
   dominant driver (see reproduction context) and the single-core figure is
   worst-case, so the central open question is whether the full MultiStartProdigy
   compile is tractable on an HPC host (single-band A100 `vag` cold was ~28s vs
   229s CPU). Quantify the transform-width scaling and heterogeneity multiplier
   under real core counts, then ship the final N-band compile verdict.
3. **Productize the immediate user workaround** — pad short-wavelength bands to a
   common grid so all factors share one fused kernel — as a documented recipe
   and/or helper for N-band gradient fits.

Deliverable: multi-band A100 census rows + either a productizable compile-reduction
lever (per-factor jit or the padding helper) or a documented "GPU-only /
same-shape-bands" verdict. **Out of scope:** re-opening the #71 single-band
settings verdict.

<!-- filed 2026-07-21 from ideas.md (research multiband-compile · Experiment A); intake misclassified as docs/autofit, hand-corrected to research/autofit -->
