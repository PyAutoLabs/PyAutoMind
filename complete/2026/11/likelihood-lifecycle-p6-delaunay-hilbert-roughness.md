## likelihood-lifecycle-p6-delaunay-hilbert-roughness
- completed: 2026-11-02
- compute: RAL 413876 (14 A100 configs, all rc=0); side project, not ingested into Pulse.
- Write-up: ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/README.md (table + summary.txt, raw probe.json).
- Finding (agent reading): no Hilbert setting (500/2500 px, weight_power 1/6, floor 0/1e-3, no edge pixels) gives an FD plateau on imaging/delaunay/hst or delaunay_nn/hst. Baseline narrow (±1e-4) roughness 0.027, strong adapt 0.34, 2500 px 0.11. More pixels raise the flip rate (0.20 -> 0.5 of intervals). Log L jumps coincide with triangle flips above chance (0.5–1.0 vs 0.15–0.64). ConstantSplit (fixed coefficient) was the only Delaunay config with 2/3 agreement.
- Human ruling 2026-11-02: "I accept them, no follow up."
- Spin-off: draft/bug/autoarray/rectangular_fiducial_gradient_wrong_rtu_and_cpu_sparse.md (RTU / CPU-sparse Bilinear fiducial gradient wrong; human: file it).

## Original prompt

# Likelihood lifecycle phase 6 follow-up: Delaunay roughness vs Hilbert image-mesh adaption

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/methods/concepts/autodiff-implicit-diff.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: glance
Witness: a written finding (epic ledger + record) stating, for imaging/delaunay/hst and delaunay_nn/hst, the Hilbert settings used, the FD step-sweep class and roughness amplitude at the baseline and at at least one higher-adaption setting, and whether triangle flips coincide with the log L jumps
Review-minutes: 3
Unattended: never

# Likelihood lifecycle phase 6 follow-up: Delaunay roughness vs Hilbert image-mesh adaption

Type: research
Target: autolens_profiling
Priority: high
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Unattended: never
Witness: a written finding (epic ledger + record) stating, for imaging/delaunay/hst and delaunay_nn/hst, the Hilbert settings used, the FD step-sweep class and roughness amplitude at the baseline and at at least one higher-adaption setting, and whether triangle flips coincide with the log L jumps

Do tomorrow (2026-11-02). Check the Hilbert image-mesh setup used by the Delaunay cells, and test whether Delaunay likelihood smoothness / gradient agreement improves with more mesh resolution in the brightest image pixels (better Hilbert adaption: weight_power, weight_floor, pixel count).

Context: the v2 gradient campaign (RAL 413791-413830, output/p6_gradient on autolens_profiling_p2dg) gives `no_plateau` on every Delaunay and delaunay_nn cell. On imaging/delaunay/hst and imaging/delaunay_nn/hst (A100) the central difference differs from the autodiff gradient by 3e-2..8 relative at steps 1e-1..1e-6 and agrees only near 1e-7..1e-8; delaunay_nn is no smoother than delaunay. Human's prior: most likely an intrinsic Delaunay limitation (triangle flips as mass parameters move the traced mesh vertices), but test it rather than assume it.

Questions:
- Which Hilbert settings (pixels, weight_power, weight_floor, adapt image) do the Delaunay cells use, and are they sensible for the brightest pixels?
- Does raising resolution where the source is bright (stronger adaption / more pixels) change the FD step-sweep class or shrink the roughness?
- Roughness amplitude vs global trend: a log L slice diagnostic (a few hundred points over about ±1e-2 along the seeded directions) for delaunay, delaunay_nn, rectangular (Bilinear and RTU) and mge as a smooth control — can a gradient sampler or optimizer still follow the global trend?
- Is the roughness from triangle flips? (e.g. count triangulation changes along a slice; compare against a fixed source-plane mesh.)

Pairs with: RTU vs Bilinear rectangular gradient comparison (RAL 413865 CPU / 413866 A100, output/p6_gradient_rtu, imaging/rectangular/hst with --rect-mesh rtu) — the hypothesis there is that the kernel-CDF RTU mesh is smoother than the rank-CDF Bilinear one. Outcome feeds the 6d hazard filing for mechanism C (densely non-smooth pixelizations).

Rules: no compute without the human's go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-01 from file:/tmp/claude-1000/-home-jammy-Science/ff79ca20-626d-462b-903f-ea2f3c46f954/scratchpad/intake_delaunay.md -->
