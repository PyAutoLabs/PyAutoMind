# Multi-band compile census completion — A100/multi-core + hetero GPU rows

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- multi-band
- jax-compile
- hpc-gpu
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-07-30 (backfilled from git)

Follow-up to the multiband-pyloop-batching ship (PyAutoFit#1430 → PR#1431 +
autolens_profiling#95, merged 2026-07-30). The dominant driver is fixed at the
source (Python-loop batching + jitted broad-start filter in
`AbstractMultiStartGradient`); these are the confirmatory census legs that were
out of scope:

1. **A100 / multi-core rows** for the multi-band matrix (`datacube_img` /
   `datacube_img_hetero` × `pyloop_vag` / `laxmap_vag` at production widths) —
   re-run `sbatch /mnt/ral/jnightin/pixgrad_logs/census_gpu.sbatch` (or the
   local pattern in `scripts/misc/jax_compile/probe.py`) once the RAL A100s
   free up. Verify backend from the results path, never the partition (the
   silent-CPU-fallback trap from #93).
2. **`datacube_img_hetero` GPU rows** on the laptop RTX 2060 — quantify the
   heterogeneity multiplier under the CUDA pipeline (the laptop GPU rows so far
   are homogeneous only; the scan explosion proved CPU-backend-specific, tags
   `mb_homo_cold_{pyloop,laxmap}_gpu`).
3. **Verdict on the remaining secondary levers** — with the transform fixed,
   reassess whether the band-padding/shape-canonicalization helper and the
   per-factor jit boundary (heterogeneity-multiplier attacks, README verdict
   bullets) are still worth building, and either file them or close them in
   `scripts/misc/jax_compile/README.md`.

Context: `autolens_profiling/results/notes/multiband_pyloop_productized.md`,
`scripts/misc/jax_compile/README.md` multi-band section.

<!-- filed 2026-07-30 at multiband-pyloop-batching completion -->
