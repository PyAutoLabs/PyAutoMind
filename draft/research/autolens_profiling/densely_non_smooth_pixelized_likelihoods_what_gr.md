# Densely non-smooth pixelized likelihoods: what gradient samplers can use (mechanism C)

Type: research
Target: autolens_profiling
Repos:
- PyAutoArray
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: medium
Memory: wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/ifu-spectroscopy.md
Status: formalised
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Consequence: judge
Review-minutes: 25
Unattended: never
Lane: ral

Every Delaunay, delaunay_nn and rectangular (Bilinear) gradient cell is no_plateau in the v2 sweep: the central difference agrees with autodiff only at h ~1e-8, i.e. the gradient is that of the local smooth piece. Delaunay cause accepted by the human 2026-11-02 as intrinsic (triangle flips as mass parameters move the traced vertices; no Hilbert setting — 500/2500 px, weight_power 1/6, floor 0/1e-3, no edge pixels — gives a plateau; side project RAL 413876, write-up ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/README.md). Research question for phase 7 gradient samplers: can a gradient sampler or optimizer follow the global trend on these likelihoods, and is a smoothed variant (soft/fixed-mesh assignment, kernel-CDF rectangular once the RTU gradient investigation complete/2026/11/rectangular-gradient-rtu-sparse.md — no RTU kernel-CDF bug; jit tie fix PyAutoArray#672 — is accounted for) worth building? Not a bug.

Epic: likelihood-lifecycle (phase 6 hazard, filed by mechanism per the human ruling 2026-11-01 "File by mechanism"); parent draft/research/autolens_profiling/likelihood_lifecycle_epic.md; issue autolens_profiling#512 (6d), campaign #509. Library 2026.10.25.1, v2 gradient witness (13-step FD sweep 1e-1..1e-8 along 3 seeded directions), RAL 413791-413830 + 413890. Evidence: RAL /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient (pulled copy ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/p6_gradient_v2); FD diagnostic RAL 413781 (/mnt/ral/jnightin/scratch/p6c_fd_sweep). Rules: no compute without the human go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Science/fc52502f-bb7f-467c-a0f4-a7f93c6f004e/scratchpad/hazards/c.md -->
