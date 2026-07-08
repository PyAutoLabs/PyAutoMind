# Autonomy calibration log

Append-only record of `--auto` workflow runs — the evidence base for raising
or lowering the per-work-type autonomy caps in `PyAutoBrain/AUTONOMY.md` (the
autonomy contract). One row per run, appended at PR-open or on parking.

Outcome ∈ `merged-unchanged` / `amended` / `rejected` / `parked`.

| date | task | effective level | gates (tests/smoke/review/heart) | outcome |
|------|------|-----------------|----------------------------------|---------|
| 2026-07-08 | psf-oversample-design (#353) | supervised | tests n/a (no source diff) / smoke n/a / review n/a (design note) / heart YELLOW-unack | parked |
| 2026-07-08 | samplers-faculty (PyAutoBrain#54) | supervised | tests n/a / smoke n/a / review CLEAN / heart n/a (organism-doc; sign-off human) | PR-open (Memory#16, Brain#55) |
| 2026-07-08 | profiling-polish-design (autolens_profiling#52) | supervised | tests 8/8 (downstream n/a) / smoke repo-gate pass (workspaces n/a) / review CLEAN after 1 fixed finding / heart YELLOW-acked at ship sign-off | merged-unchanged (autolens_profiling#53) |
| 2026-07-08 | psf-oversample-core (#354) | supervised | tests PASS 857+933+331 / smoke not-run / review CLEAN / heart YELLOW-unack | parked |
