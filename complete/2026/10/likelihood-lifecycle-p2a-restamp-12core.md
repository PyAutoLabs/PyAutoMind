- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/466
- completed: 2026-10-26
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/467 (merge 5263ac7f, head ab625c73; merge commit — new rows' provenance cites branch commit 65b17065)
- heart: shipped under the live-human Heart RED development override 2026-10-26 ("I authorize you to work and overrude heart red"); merged by a separate human /prm with CI green
- summary: |
    Pins: catalogue/release_revisions.json v2 declares carry_forward 2026.10.23.1 → 2026.10.25.1 (imaging only;
    basis = per-library diff, no per-call imaging change). 231 imaging records publish 2026.10.25.1 with
    measured_release_pin + measured SHAs; build_dashboard applies the same carry-forward (one code path);
    dashboard record ids <series>@<published pin>; a release's own measurement beats a carried point, the
    displaced point falls back to its measured pin. Pulse pair: 191 comparisons, 9 pre-existing host-change refusals (= main).
    12-core: estimated_12_core {value_s = per_call/6, divisor 6, cores 12} on the 9 numba CPU runtime records,
    beside projected_node_throughput (human ruling 2026-10-26).
    ao OOM: the dense breakdown held jnp.array duplicates of the operated/mapping matrices (~4 GB each) during the
    eager step-8 PSF convolution (10.76 GiB broadcast_in_dim); freed (no measured quantity changed, hst
    before/after identical). RAL 413033 (--array=2,16 of the batch-0 A100 submit, 2026.10.23.1 libraries)
    delaunay 131 s / rectangular 111 s; coverage 104 → 106 current (imaging 106/106); BATCH0_LIMITATIONS emptied.
    Test fixture copies catalogue/reference_hosts.json (main was red locally after Pulse 5749e25).
- witness: |
    MET — build_catalogue --check --validate-with ../PyAutoPulse passes; no 2a imaging record stale or at
    2026.10.23.1; estimated_12_core only on numba CPU runtime records; both ao cells current. CI lint green (attempt 2;
    attempt 1 timed out in the browser-setup step after every check passed). Independent review: 2 rounds, all fixed.
- follow-ups: autolens_inference#47 (profiling @3 join on wall-time records); draft/feature/autolens_profiling/rectangular_28sq_profiling_rows.md; draft/feature/pyautopulse/pulse_timings_dashboard_redesign.md

## Original prompt

# Likelihood lifecycle 2a follow-up: pin 2026.10.25.1 re-stamp, 12-core estimate, ao GPU breakdown rerun

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: likelihood-lifecycle
Phase: 2
Status: formalised
Consequence: judge
Witness: build_catalogue --check passes with every 2a imaging record at release_pin 2026.10.25.1 carrying its measured pin/SHAs as provenance and no row turned stale; numba CPU records carry the producer-emitted 12-core estimate (per-call ÷ 6); the two ao jax_gpu_dense breakdown cells (delaunay, rectangular) are current from a RAL A100 rerun, or recorded as limitations with measured memory numbers if they still do not fit
Filed: 2026-10-26
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/466

## Human rulings (2026-10-26, chat)
- Update library pins to 2026.10.25.1: phase 2b onward measures on it, and the 104 2a rows are RE-STAMPED
  (not rerun) "so we're all in sync". Justification: 2026.10.23.1..2026.10.25.1 touches no per-call imaging
  likelihood (PyAutoArray finufft on the NumPy NUFFT path only; PyAutoLens PointSolver; PyAutoGalaxy docstring;
  PyAutoFit search/fork side). Keep the measured pin + library SHAs on each row (e.g. `measured_release_pin`,
  `pin_carried_forward_from`) so provenance stays honest.
- Add an "estimated time per likelihood at 12 cores" = per-call runtime ÷ 6, numba CPU rows only, as a
  producer-emitted field (Pulse displays it; see draft/feature/pyautopulse/pulse_timings_dashboard_redesign.md).
  This is an extra row/column alongside the #465 same-host projection, not a replacement.
- Rerun the two ao GPU dense breakdowns that OOM'd on A100 (384,753×1,280 fp64 blurred mapping matrix; runtime
  legs at the same size succeeded). Diagnose first from the RAL .err files, fix memory (XLA preallocation off /
  free per-stage arrays), rerun on the private RAL checkout; compute needs a human go per batch.
- RAL: private lib checkout /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1 (clone 2026-10-26, verify tags);
  private profiling checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a.
