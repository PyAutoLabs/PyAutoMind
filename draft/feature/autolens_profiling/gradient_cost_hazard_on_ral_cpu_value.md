# Gradient cost hazard on RAL CPU: value_and_grad above 4x the forward call…

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: low
Memory: reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md
Status: formalised
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: never

grad/forward > 4x (the pre-registered hazard threshold) only on RAL CPU: cluster/source_plane 11.6x (A100 3.0x), weak/isothermal 4.8x (A100 1.9x), multi_galaxy/mge/hst 4.2x (A100 2.8x), imaging/delaunay_nn/hst 4.09x (A100 2.0x; RAL 413890_4). Every other leg is 1.2–3.7x. Profile the backward pass of these four on RAL CPU (per-step backward breakdown, as the 6a plan reserved for hazard cells) and decide whether a lever (forward-mode for few-parameter cells, remat, jit boundaries) is worth a task.

Epic: likelihood-lifecycle (phase 6 hazard, filed by mechanism per the human ruling 2026-11-01 "File by mechanism"); parent draft/research/autolens_profiling/likelihood_lifecycle_epic.md; issue autolens_profiling#512 (6d), campaign #509. Library 2026.10.25.1, v2 gradient witness (13-step FD sweep 1e-1..1e-8 along 3 seeded directions), RAL 413791-413830 + 413890. Evidence: RAL /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient (pulled copy ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/p6_gradient_v2); FD diagnostic RAL 413781 (/mnt/ral/jnightin/scratch/p6c_fd_sweep). Rules: no compute without the human go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Science/fc52502f-bb7f-467c-a0f4-a7f93c6f004e/scratchpad/hazards/cost.md -->
