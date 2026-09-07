# `scripts/interferometer/likelihood_breakdown/delaunay.py` is OOM-killed on `sma` (14.6 GB RSS in the per-step JIT profiling)

Type: bug
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- interferometer
- likelihood-profiling
- jax-compile
Difficulty: small
Autonomy: safe
Priority: medium
Filed: 2026-09-07

Found while shipping `numba-interferometer-pack` (autolens_profiling#223). The existing JAX
interferometer breakdown `scripts/interferometer/likelihood_breakdown/delaunay.py` run on
the default `sma` instrument (256×256 grid, 3.5" mask, 190 visibilities, Hilbert 1500 →
Delaunay) completes PART A (`figure_of_merit_eager = -3169.6493766794806`) and is then
killed with exit 137 during PART B's per-step `jit_profile` blocks, at ~14.6 GB anonymous
RSS on a 15 GB box. Unmodified upstream code; pre-existing, not caused by the numba pack.

Consequence: there is no committed `results/breakdown/interferometer/delaunay_breakdown_sma_*`
row, so the JAX-CPU per-step comparator the `numba-interferometer-revisit` epic (phase 2)
needs has to be produced some other way. Phase 2 will use the numba pack's own JAX reference
until this is fixed.

Suspects: the `jit_profile` helper keeps every lowered/compiled object alive across the
eight steps; the `transformed_mapping_matrix_eager` section (190 × 3852 complex is tiny, so
probably not it); or the `Inversion setup (steps 5-8 combined, incl. NUFFT)` block tracing
the NUFFT with `transformer_chunk_size=None` (one-shot) on the 256×256 padded grid.

Fix shape: profile peak RSS per section, free compiled artefacts between sections
(`del` + `jax.clear_caches()`), or chunk the sma transformer; add a `--skip-part-b` flag so
PART A's figure of merit is always recorded. Acceptance: the script completes on `sma`
under ~4 GB and commits its JSON+PNG.
