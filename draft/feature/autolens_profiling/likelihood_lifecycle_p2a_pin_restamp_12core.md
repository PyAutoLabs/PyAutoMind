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
