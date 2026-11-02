## likelihood-lifecycle-p6d-gradient-ingest
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/512
- completed: 2026-11-02
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/513 (ingest 73 gradient witnesses, 24ebd94e)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/514 (512 GB rerun walls; delaunay/ao OOM recorded, 0278253a)
- organ-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/87 (freeze --measurement, 6d9a8a8d)
- organ-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/88 (freeze day_zero_gradient at 433bd778, a6695b5d)
- 73 current gradient records; 10 FD pass carry day_zero 2026.10.25.1 and are frozen in PyAutoPulse snapshots/day_zero_gradient/lens.json (runtime day_zero untouched); 63 fail by mechanism → hazards filed (B draft/bug/autogalaxy/wrong_jax_gradient_on_mge_likelihoods_fd.md, C/D/E draft/research/autolens_profiling/…, cost draft/feature/autolens_profiling/gradient_cost_hazard_on_ral_cpu_value.md).
- imaging/delaunay/ao RAL CPU: OOM at 64/192/512 GB at ~2h40 each time — recorded as a result (human ruling 2026-11-02, "Record OOM as result").
- Phase-6 witness restated by the human 2026-11-02 and met: phase 6 complete.
- Lesson: build_dashboard's plain write re-stamps every shard; render with the committed stamp (`build(root, generated=_existing_stamp(out), revision=_existing_revision(out))`) when only data changed. Day-zero page links to a Pulse snapshot that a later PR creates fail lychee until that PR merges — merge the Pulse PR first, then re-run lint.

## Original prompt

# Likelihood lifecycle phase 6d: ingest the gradient witnesses, freeze day_zero_gradient, file hazards by mechanism

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
Themes:
- profiling
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/512
Issued: 2026-11-02
Consequence: judge
Witness: every Optimal setup's gradient leg (74) has a current mirrored gradient.json under results/ read by build_catalogue as a measurement gradient record with an FD verdict; the 10 FD-pass records carry day_zero 2026.10.25.1; Pulse snapshots/day_zero_gradient/lens.json holds exactly those gradient records (runtime day_zero untouched); every non-pass verdict and every grad/forward > 4x is covered by a hazard prompt filed by mechanism; the epic's phase-6 witness is restated
Review-minutes: 20
Unattended: never
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02

## Context

- 6a autolens_profiling#506 (harness, gradient_witness, build_catalogue gradient records), 6b #508 (gradient_breakdown.py ×19, gradient_p6 74 legs), 6c #509 (RAL runs: v2 RAL 413791–413830, 72/74; OOM legs rerun at 512 GB as RAL 413890; witness v2 step sweep #510; walls #511 1cdf84bf).
- v2 sweep verdicts: agree (FD pass): cluster source_plane, group mge, multi_galaxy mge, point_source_source, weak (CPU + A100 = 10 records). mismatch: imaging mge ×4, interferometer mge sma. zero: cluster image_plane, point_source_image. no_plateau: every Delaunay / delaunay_nn / rectangular cell.
- Delaunay/Hilbert side project (RAL 413876) accepted by the human 2026-11-02 ("I accept them, no follow up"): roughness is intrinsic (triangle flips); no Hilbert setting gives a plateau.
- RTU / CPU-sparse Bilinear fiducial wrong gradient filed separately: draft/bug/autoarray/rectangular_fiducial_gradient_wrong_rtu_and_cpu_sparse.md (human handles in another chat).

## Plan (human rulings 2026-11-02)

1. autolens_profiling: copy the v2 gradient.json from RAL p2dg output/p6_gradient/results into the mirrored results/ cells (73 now; imaging/delaunay/ao RAL CPU when RAL 413890_0 lands); regenerate catalogue / coverage / day-zero pages / dashboard; lint green. The 10 FD-pass records carry day_zero.
2. PyAutoPulse: `freeze --measurement <m>` filter; `pyauto-pulse freeze --instance lens --label day_zero_gradient --measurement gradient --commit <sha>` writes snapshots/day_zero_gradient/lens.json with only gradient records; snapshots/day_zero untouched.
3. Hazards by mechanism through /intake (human: "File by mechanism"): B wrong gradient (imaging mge ×4 instruments, interferometer mge sma); C densely non-smooth pixelizations (Delaunay, delaunay_nn, rectangular; Delaunay intrinsic per the accepted finding); D noisy likelihood (interferometer rectangular sma); E piecewise-constant image-plane point/cluster; cost hazards grad/forward > 4x (cluster source_plane CPU 11.6x, weak CPU 4.8x, multi_galaxy mge CPU 4.2x, delaunay_nn/hst CPU 4.09x). A (fixed-step false alarms) recorded, not filed.
4. Epic: restate the phase-6 witness (human ruling 2026-11-02, "Restate witness"): phase 6 is met when every Optimal setup has a current gradient record with an FD verdict — pass, or a non-pass filed as a hazard by mechanism.

## Rules

No compute. Merge only by the human's /prm.

## Request (human, 2026-11-02, verbatim)

"prm the follow-up PR when it's green, can we keep going on the task as a whole as were currently just waiting on this one off slow run"

Rulings (AskUserQuestion, 2026-11-02): phase-6 witness → "Restate witness (Recommended)"; frozen label → "day_zero_gradient (Recommended)".
