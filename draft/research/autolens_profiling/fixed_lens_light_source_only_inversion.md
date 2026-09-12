# Fixed lens light after SLaM light[1]: cost of the source-only pixelized inversion on the A100

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gpu
- pixelized-likelihood
- positivity
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Witness: results/notes/fixed_lens_light_source_only_2026_09.md reports, per mesh, the A100 per-call ms of the S3 fixed-MGE system with positivity (A1) and without (A2) against the S0 fiducial (50.6 ms single / 32.1 ms @vmap16), each with its log-evidence agreement to the CPU probe, and a measured pass count for the certified active-set scheme
Filed: 2026-09-12

Original request (verbatim): "begin the analysis and report and investigation in
autolens_profiling of what happens if we fix the mge light profiles".

## Why

The 2026-09-11 CPU probe + independent review (durable copy
`~/Code/PyAutoLabs-wt/matrix-free-pixelized-likelihood/_session_2026-09-11_artefacts/`)
showed that removing the 60 linear MGE columns from `F + λH` is the whole conditioning
story: cond 4.1e10 → 1.2e7 (rectangular 1521) / 2.1e6 (Delaunay 1500); NNLS PDIP
21–22 → 15–17 iterations; Jacobi PCG 5589 → 147–187 iterations. Converting the MGE to
regular profiles at the light[1]-solved intensities (system "S3", via the library's
`basis_no_linear_from` / `tracer_linear_light_profiles_to_light_profiles`) reproduces the
current evidence exactly and is algebraically identical to foreground subtraction. The
positive-vs-unconstrained evidence gap scales with lens-light error (+195 → +1049 nats for a
3 % effective-radius error), so dropping positivity (A2) is a science approximation that
needs its own witness; keeping it (A1) is a pure speed lever. This is the successor of the
a100-pixelized-baseline / reconstruction-row-split / matrix-free line (this repo's issues
#241 / #243 / #247), and the lever the human named next.

## Scope (this repo only)

1. **CPU falsifier of a certified active-set positive solve** on the source-only system:
   seed from the unconstrained solve, restricted Cholesky on the free set, KKT check,
   PDIP fallback. Measure factorisations to certification, evidence error after a fixed
   1–4 pass budget, and active-set stability across mass-model draws (Jaccard of the
   active set). Commit the probe under `scripts/misc/likelihood_breakdown/` with tests.
2. **A100 benchmark** (`--fixed-lens-light` on the three imaging breakdown cells, or a
   dedicated `source_only.py` cell): S0 current vs S3 fixed-MGE, with positivity (A1) and
   without (A2 — note the signed path silently disables edge zeroing and routes to
   `xp.linalg.solve`, not the Cholesky comparator). Rows: reconstruction, NNLS iterations
   × ms/iteration, Cholesky solve, log-dets, per-call total, vmap16. If step 1 certifies
   in ≤ 4 factorisations, add a JAX certified active-set sub-row. Rectangular, Delaunay,
   Delaunay-NN; euclid-ral-gpu-2, fresh cache, pins on S0. Subtract on the dataset and
   rebuild the sparse operator (the w-tilde weight-map bug is a separate library prompt).
3. **Note** `results/notes/fixed_lens_light_source_only_2026_09.md` + README prose row:
   measured A1 and A2 speed-ups against the fiducial, the certified-scheme verdict, and
   what the science witness must show before A2 enters production.

## Out of scope (separate prompts)

The workspace SLaM change (mass[1] with fixed light + per-stage positivity flag); the
matched-injection science witness (Einstein radius / slope bias < 0.2σ, subhalo ΔlogZ
drift < 0.3–0.5 nat); the library fix for the sparse-path weight map.
