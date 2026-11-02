# Wrong JAX gradient on MGE likelihoods: FD plateaus off the autodiff value…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Memory: wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md; wiki/galaxies/sources/light-profile-fitting.md
Status: formalised
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: never

The v2 step sweep plateaus (stable over 3e-4..1e-8) at a value different from the autodiff gradient on every imaging/mge cell (ao, euclid, hst, jwst; hst rel error 0.8–2.8e-3; ao 1/3 directions agree) and on interferometer/mge/sma (8e-3, 1.9e-2, 0.74). CPU and A100 give identical errors, so it is not a backend issue. A smooth likelihood with a consistently wrong gradient points to a library derivative bug in the linear light profile path (MGE basis, NNLS / positive-only solve, or the inversion's implicit derivative). Locus to find (autogalaxy or autoarray). Witness: per-parameter gradient vs FD plateau on imaging/mge/hst agrees to <= 1e-6 relative after the fix.

Epic: likelihood-lifecycle (phase 6 hazard, filed by mechanism per the human ruling 2026-11-01 "File by mechanism"); parent draft/research/autolens_profiling/likelihood_lifecycle_epic.md; issue autolens_profiling#512 (6d), campaign #509. Library 2026.10.25.1, v2 gradient witness (13-step FD sweep 1e-1..1e-8 along 3 seeded directions), RAL 413791-413830 + 413890. Evidence: RAL /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient (pulled copy ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/p6_gradient_v2); FD diagnostic RAL 413781 (/mnt/ral/jnightin/scratch/p6c_fd_sweep). Rules: no compute without the human go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Science/fc52502f-bb7f-467c-a0f4-a7f93c6f004e/scratchpad/hazards/b.md -->
