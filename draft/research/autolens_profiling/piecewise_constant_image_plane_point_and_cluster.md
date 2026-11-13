# Piecewise-constant image-plane point and cluster likelihoods: zero FD, nonzero autodiff (mechanism E)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Memory: reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md
Status: formalised
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: never
Lane: ral

cluster/image_plane/simple and point_source_image/image_plane/simple give FD = 0 at fine steps (sweep class zero: h <= 1e-3 for cluster, <= 1e-5 for point_source_image) while autodiff returns a nonzero gradient (cluster ~-7.6 on a direction); coarse 1e-2..3e-3 FD is within ~3% for point_source_image. The point solver's discrete image matching makes the likelihood piecewise constant, so the autodiff value is not a usable sampler gradient. Decide what the gradient sampler phase should do with image-plane point likelihoods (use source-plane, smooth the matching, or exclude) and whether the autodiff output there should be flagged.

Epic: likelihood-lifecycle (phase 6 hazard, filed by mechanism per the human ruling 2026-11-01 "File by mechanism"); parent draft/research/autolens_profiling/likelihood_lifecycle_epic.md; issue autolens_profiling#512 (6d), campaign #509. Library 2026.10.25.1, v2 gradient witness (13-step FD sweep 1e-1..1e-8 along 3 seeded directions), RAL 413791-413830 + 413890. Evidence: RAL /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient (pulled copy ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/p6_gradient_v2); FD diagnostic RAL 413781 (/mnt/ral/jnightin/scratch/p6c_fd_sweep). Rules: no compute without the human go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Science/fc52502f-bb7f-467c-a0f4-a7f93c6f004e/scratchpad/hazards/e.md -->
