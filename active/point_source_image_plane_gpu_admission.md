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
