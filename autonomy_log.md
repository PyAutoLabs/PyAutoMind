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
| 2026-07-08 | psf-oversample-core (#354) | supervised | tests PASS 857+933+331 / smoke waived-at-signoff / review CLEAN / heart YELLOW-human-approved | merged-unchanged |
| 2026-07-08 | psf-oversample-inversion (#356) | supervised | tests PASS 860+940+334 / smoke n-a-opt-in (workspace tests deferred to phase 3 by human) / review CLEAN / heart YELLOW-human-approved | pr-open (PyAutoArray#357; set at merge) |
| 2026-07-08 | ep-graphical-docs (PyAutoFit#1333) | supervised | tests 1422 pass/14 skip (full suite) / smoke n/a (docs-only) / review human sign-off / heart YELLOW-acked in-session | PR-open (PyAutoFit#1334) |
| 2026-07-08 | assistant-deep-audit (phase A, #35) | supervised | tests n/a (doc repo, stated) / smoke n/a (no script surface) / human review pending / heart YELLOW pre-existing (no ack) | parked |
| 2026-07-08 | assistant-deep-audit (phase A, #35) | supervised | tests n/a (doc repo) / smoke n/a / review human-approved / heart pre-existing YELLOW (no ack needed at doc scope) | PR #36 open |
