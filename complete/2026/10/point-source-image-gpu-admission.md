## Summary
A100 image-plane point-source admission measurement on the released 2026.10.17.1 stack (autolens_profiling#434, issue #427; RAL job 412519 on euclid-ral-gpu-2, `--gres=gpu:1 --exclusive`, A100 80GB PCIe, driver 610.57.04, jax 0.10.2, fp64, private tag clone; dataset `point_source/simple`, `FitPositionsImagePairAllSolved`, 100×100 grid at 0.2″).

- Single call 0.934 ms median (pre-#768 job 366916: 0.910 ms); CUDA-graphs off/on 1.207; compile 6.54 s; vmap 1/4/16/64/256 = 0.987/0.279/0.082/0.026/0.0125 ms per likelihood; 173 kernels, GPU busy 54 %.
- Forward gradient (`jacfwd`) now finite 16/16 and equal to reverse to 1.6e-11 (was NaN before PyAutoLens#768); reverse/likelihood 1.889; FD check 4/6 (same two points as before); reference logL 7.743201200876806 bit-exact.
- Compatible cross-run comparison (same script, dataset, model, fp64, GPU model, driver, jax, XLA flags; different node and date). The +2.7 % single-call difference is above the within-run MDI of 1.5 % but not attributed to the library (node/day variation not covered). Per-step breakdown rows unusable on the A100 (11/43 negative differences); step attribution stays with the 2026-09-28 trace table.
- Caveats: RAL jax 0.10.2 is excluded by the release pins; JSON `__version__` reads 2026.8.17.1 (source checkout), SHAs are the provenance.

**Human decision 2026-10-17 (Pulse chat):** point-source image-plane campaign filed as research; the A100 numbers are the reference measurement; the phase-2 inference fit measurement is dropped; no source changes. Pulse campaign `point-source-image-gpu` parked (PyAutoPulse#67).

## Process note
Shipped as one of six human-authorised parallel arms on disjoint autolens_profiling paths despite the claim guard's co-claim report (hst-mge-pilot-qualification #418 and sibling arms); merged under human `/prm` after a main merge + catalogue regeneration (head 716c487b). Heart STALE at ship, no override.

## Original prompt

# Point-source image-plane A100 admission measurement on released 2026.10.17.1

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
- jax-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-10-17
Issued: 2026-10-17
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/427
Campaign: PyAutoPulse `point-source-image-gpu` / task `tasks/point_source_image_plane_gpu_breakdown.md`

## Request (verbatim, human 2026-10-17)

"Do all that, I authorise all" — A100 compute on RAL for the image-plane admission
measurement of the point-source A100 campaign on the released 2026.10.17.1 stack, and the
development flow to record it. Merge stays human.

## Scope (one bounded phase)

Measure whether the released 2026.10.17.1 image-plane point-source likelihood (after the
correctness fix PyAutoLens#768, which closed PyAutoLens#767) is admissible as the campaign's
A100 performance baseline, using the shared breakdown harness
(`scripts/point_source_image/image_plane/likelihood_breakdown.py`) plus the phase-0+1
bottleneck-map cell for a like-for-like pairing with job 366916:

- full fused likelihood s/eval and the 8-step solver prefix breakdown; compile separate from execution;
- fp64 only (the cell defines no mixed-precision switch);
- one RAL A100, `--gres=gpu:1`, one task, `--exclusive`;
- private library checkouts at tag 2026.10.17.1 under `/mnt/ral/jnightin/profiling/` (never the shared mirror, never HPCPullPyAuto);
- record host, GPU, driver, JAX/jaxlib, dataset, model configuration and SHAs;
- pair against job 366916 (last qualified pre-#768 A100 fp64 row) only if hardware/precision/dataset match, else "no compatible comparison".

No optimization. Admissibility is stated as evidence only; acceptance of a baseline is the human's call.
