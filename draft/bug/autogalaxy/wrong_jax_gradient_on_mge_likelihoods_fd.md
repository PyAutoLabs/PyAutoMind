# Wrong JAX gradient (and value) at near-round `ell_comps`: the MGE prior median `ell_comps` = 0 gives an autodiff gradient off the smooth likelihood's

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
Narrowed: 2026-11-02 by autolens_profiling#517 (gradient-correctness sweep, item 1) — see "Narrowed" below; the original finding is kept beneath it
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: never
Lane: ral


## Narrowed (2026-11-02, autolens_profiling#517 item 1)

Measured locally on `imaging/mge/hst` (scripts + JSON: `Science/scratch/gradient_correctness_sweep_2026-11-02/item1_mge_probe.py`, `item1_cone_test.py`; write-up: autolens_profiling `wiki/research/gradient_correctness_sweep.md`, "Item 1 result"):

- **Not the NNLS solve, not the warm-start memo.** `AUTOARRAY_NNLS_WARM_START=0` leaves the gap identical. Nudging the free parameters off the prior medians by ~1e-3 makes autodiff = FD to ~1e-9.
- **It is `ell_comps` = 0.** All 8 free-parameter medians are exactly 0. Nudging only the 4 `ell_comps` closes the gap; nudging only the centres does not. Autodiff is correct for |e| ≳ 1e-6 (FD stencil off the origin).
- **The likelihood is smooth through e = 0** at scales 1e-4 to 1e-2 (even part quadratic along a line through the origin), so the exact-zero autodiff is wrong, not a kink artefact.
- **Value offset at exactly 0** of ~2.5e-4 in log L (one-sided FD, forward − backward ∝ 1/h), consistent with `convert._nudge_off_origin`'s 1e-8 nudge of e₁ for traced values.
- **Open:** small-scale structure inside |e| ≲ 1e-5 (local slope 8329.3 vs across-origin 8336 along direction 0). No light-profile near-round clamp exists, so the locus is the light geometry path (`convert.axis_ratio_and_angle_from`, the `where` guards, `geometry_profiles` rotation) near round.

Locus is **PyAutoGalaxy** (`convert.py` / light-profile geometry), same family as `draft/bug/autogalaxy/q_clamp_and_bare_sqrt_ellipticity_grad_sweep.md`; work them together. New witness: on `imaging/mge/hst` at the prior medians, autodiff along the harness's 3 seeded directions agrees with the FD plateau (h = 1e-4..1e-6) to <= 1e-6 relative, and the log L at exactly `ell_comps` = 0 matches its own limit to <= 1e-8. Also confirm `interferometer/mge/sma` (74 % in one direction) is this mechanism.

## Original finding (kept)

The v2 step sweep plateaus (stable over 3e-4..1e-8) at a value different from the autodiff gradient on every imaging/mge cell (ao, euclid, hst, jwst; hst rel error 0.8–2.8e-3; ao 1/3 directions agree) and on interferometer/mge/sma (8e-3, 1.9e-2, 0.74). CPU and A100 give identical errors, so it is not a backend issue. A smooth likelihood with a consistently wrong gradient points to a library derivative bug in the linear light profile path (MGE basis, NNLS / positive-only solve, or the inversion's implicit derivative). Locus to find (autogalaxy or autoarray). Witness: per-parameter gradient vs FD plateau on imaging/mge/hst agrees to <= 1e-6 relative after the fix.

Epic: likelihood-lifecycle (phase 6 hazard, filed by mechanism per the human ruling 2026-11-01 "File by mechanism"); parent draft/research/autolens_profiling/likelihood_lifecycle_epic.md; issue autolens_profiling#512 (6d), campaign #509. Library 2026.10.25.1, v2 gradient witness (13-step FD sweep 1e-1..1e-8 along 3 seeded directions), RAL 413791-413830 + 413890. Evidence: RAL /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient (pulled copy ~/Science/Science/scratch/delaunay_hilbert_2026-11-01/p6_gradient_v2); FD diagnostic RAL 413781 (/mnt/ral/jnightin/scratch/p6c_fd_sweep). Rules: no compute without the human go; CPU jobs only on --partition=ral.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Science/fc52502f-bb7f-467c-a0f4-a7f93c6f004e/scratchpad/hazards/b.md -->
