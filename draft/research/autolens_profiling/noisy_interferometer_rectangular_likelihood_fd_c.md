# Noisy interferometer rectangular likelihood: FD cannot assess the gradient (mechanism D)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: low
Memory: reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/methods/concepts/autodiff-implicit-diff.md
Status: formalised
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: never
Lane: ral

interferometer/rectangular/sma (12 parameters, |grad| ~0.23): f differs by ~1e-6 at h=1e-8 and the FD error grows as h shrinks — the likelihood is numerically noisy at the level FD needs, so the sweep cannot assess the gradient. Find the noise source (w-tilde / sparse precision, solver tolerance, float accumulation) and whether it matters for samplers (noise vs |grad| scale).

Epic: likelihood-lifecycle (phase 6 hazard, filed by mechanism per the human ruling 2026-11-01 "File by mechanism"); parent draft/research/autolens_profiling/likelihood_lifecycle_epic.md; issue autolens_profiling#512 (6d), campaign #509. Library 2026.10.25.1, v2 gradient witness (13-step FD sweep 1e-1..1e-8 along 3 seeded directions), RAL 413791-413830 + 413890. Evidence: RAL /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient (pulled copy ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/p6_gradient_v2); FD diagnostic RAL 413781 (/mnt/ral/jnightin/scratch/p6c_fd_sweep). Rules: no compute without the human go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Science/fc52502f-bb7f-467c-a0f4-a7f93c6f004e/scratchpad/hazards/d.md -->
