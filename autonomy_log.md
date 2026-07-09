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
| 2026-07-08 | psf-oversample-inversion (#356) | supervised | tests PASS 860+940+334 / smoke n-a-opt-in (workspace tests deferred to phase 3 by human) / review CLEAN / heart YELLOW-human-approved | merged-unchanged |
| 2026-07-08 | ep-graphical-docs (PyAutoFit#1333) | supervised | tests 1422 pass/14 skip (full suite) / smoke n/a (docs-only) / review human sign-off / heart YELLOW-acked in-session | PR-open (PyAutoFit#1334) |
| 2026-07-08 | assistant-deep-audit (phase A, #35) | supervised | tests n/a (doc repo, stated) / smoke n/a (no script surface) / human review pending / heart YELLOW pre-existing (no ack) | parked |
| 2026-07-08 | assistant-deep-audit (phase A, #35) | supervised | tests n/a (doc repo) / smoke n/a / review human-approved / heart pre-existing YELLOW (no ack needed at doc scope) | PR #36 open |
| 2026-07-08 | psf-oversample-galaxy (#480) | supervised | tests PASS 944+335 (incl. user-directed linear-lp addition) / smoke deferred-to-phase-3 / review CLEAN / heart YELLOW-human-approved | amended (linear-lp addition user-directed; merged #481) |
| 2026-07-08 | assistant-deep-audit (phase B tooling, #35) | supervised | tests 39p / smoke n/a / review human pending / heart pre-existing YELLOW | parked at sign-off |
| 2026-07-08 | profiling-vram-validation (autolens_profiling#54) | supervised | tests 25/25 (downstream n/a) / smoke repo-gate + live 9-cell sweep / review CLEAN / heart YELLOW-acked at ship sign-off | merged-unchanged (autolens_profiling#55) |
| 2026-07-08 | assistant-deep-audit (phase C wiki+workflow, #35) | supervised | audit 0 broken + idiom clean / smoke n/a / review human pending / heart pre-existing YELLOW | parked at sign-off |
| 2026-07-08 | profiling-drift-check (PyAutoHeart#37) | supervised | tests 217/217 / smoke n/a (organism repo) / review CLEAN / heart YELLOW-acked in-session | merged-unchanged (PyAutoHeart#38) |
| 2026-07-08 | assistant-deep-audit (phase D AGENTS+tooling, #35) | supervised | audit 0 broken / smoke n/a / review human pending / heart pre-existing YELLOW | parked at sign-off |
| 2026-07-08 | ep-examples-tests (autofit_workspace#81) | supervised | tests: tutorial validated end-to-end + 3 integration scripts PASS / smoke n/a (new scripts, not in curated lists) / review pending at sign-off / heart YELLOW pending ack | parked (ship sign-off + heart-ack question) |
| 2026-07-08 | psf-oversample-workspace (#232) | supervised | tests PASS 861+944+335 / smoke imaging-trio PASS / review CLEAN / heart YELLOW-human-approved | merged-unchanged |
| 2026-07-08 | assistant-deep-audit (all phases, #35) | supervised | tests 39p+audits / smoke n/a / review human-approved x4 / heart pre-existing YELLOW | A-C merged-unchanged, D amended (merge fix only) |
| 2026-07-08 | ep-diagnostics (PyAutoFit#1335) | supervised | tests 1429 pass/14 skip (full suite; 7 new) / smoke n/a (additive library tooling) / review pending at sign-off / heart YELLOW pending ack | parked (ship sign-off + heart-ack question) |
| 2026-07-08 | clone-mitosis-agent (design, Brain#57) | supervised | line-count guard ok / smoke n/a (doc) / review human pending / heart pre-existing YELLOW | parked at sign-off |
| 2026-07-08 | ep-deterministic-reconcile (PyAutoFit#1336) | supervised | research (read-only): census + analysis + recommendation posted / other gates n/a | parked (decision A/B/C on #1336) |
| 2026-07-08 | psf-oversample-simulator (#482) | supervised | tests PASS 863+946+336 (simulate-and-fit in all 3 projects, human req) / smoke scripts-run-clean / review CLEAN / heart YELLOW-human-approved | merged-unchanged (5 PRs, chain order; catalogue regen added post-open) |
| 2026-07-08 | ep-analytic-updates-scope (PyAutoFit#1337) | supervised | research (read-only): inventory + gap repro + ranked candidates posted / other gates n/a | parked (prioritisation on #1337) |
| 2026-07-08 | ep-review phase 7 ideation (umbrella) | supervised | research (read-only): 11 ideas → ideas.md / other gates n/a | complete |
| 2026-07-08 | psf-oversample-docs (#234) | supervised | tests n/a (docs) / guide-runs-clean / review CLEAN / heart YELLOW-human-approved | merged-unchanged |
| 2026-07-08 | psf-oversample-refactor (#360) | safe | tests PASS 863+946+336 unchanged / smoke n-a-refactor / review CLEAN / heart YELLOW-human-approved | merged-unchanged |
| 2026-07-08 | kxs-design (#362) | supervised | tests n/a (design) / ground-truth k=1 exact / review n-a / heart YELLOW | approved-unchanged (design; phase 2 continues) |
| 2026-07-08 | hst-acs-phase1 | supervised | tests 53/53 / smoke n/a / review FINDINGS→resolved / heart YELLOW | parked |
| 2026-07-08 | hst-acs-phase1 | supervised | tests 53/53 / smoke n/a / review FINDINGS→resolved / heart YELLOW (acked) | PR-open (#3) |
| 2026-07-08 | version-pinning-design-review (#118) | supervised | tests n/a (research) / smoke n/a / review n/a (no code) / heart n/a | parked (report delivered; follow-ups pending human) |
| 2026-07-08 | kxs-core (#362 p2) | supervised | tests PASS 863+946+336 (adaptive GT exact; pixelized kxs proven) / smoke deferred-p3 / review CLEAN / heart YELLOW-human-approved | merged-unchanged (fork resolved: c now, a filed) |
| 2026-07-08 | version-check-compat-floor (PyAutoConf#118) | supervised | tests 117 pass (+7 new) / smoke n/a (library-only, no downstream edits) / review pending-at-signoff / heart YELLOW (no ack) | parked |
| 2026-07-08 | release-stamping-slim (PyAutoBuild#120) | supervised | tests 71 pass / smoke n/a (workflow-only) / review pending-at-signoff / heart YELLOW (no ack) | parked |
| 2026-07-08 | wfc3-reduction | supervised | tests 62/62 / smoke n/a / review FINDINGS(1H+2L)→resolved / heart YELLOW | parked |
| 2026-07-08 | hst-acs-phase1 | supervised | tests 53/53 / smoke n/a / review resolved / heart YELLOW acked | merged-unchanged (#3) |
| 2026-07-08 | wfc3-reduction | supervised | tests 62/62 / smoke n/a / review 1H+2L resolved / heart YELLOW acked | PR-open (#5) |
| 2026-07-08 | version-check-compat-floor (PyAutoConf#118) | supervised | tests 117 pass / smoke n/a / review human-signoff / heart YELLOW-acked-in-session | PR-open (#119) |
| 2026-07-08 | release-stamping-slim (PyAutoBuild#120) | supervised | tests 71 pass / smoke n/a (workflow-only) / review human-signoff / heart YELLOW-acked-in-session | PR-open (#121) |
| 2026-07-08 | version-check-compat-floor (PyAutoConf#118) | supervised | tests 117 pass / smoke n/a / review human-signoff / heart YELLOW-acked | merged-unchanged (#119) |
| 2026-07-08 | release-stamping-slim (PyAutoBuild#120) | supervised | tests 71 pass / smoke n/a / review human-signoff / heart YELLOW-acked | merged-unchanged (#121) |
| 2026-07-08 | kxs-cache (#362 follow-up) | supervised | tests PASS 867 / perf x750 / review CLEAN / heart YELLOW-human-cadence | merged-unchanged |
| 2026-07-08 | dpie-lenstool-param (PyAutoGalaxy#485) | supervised | tests 956+336 downstream / smoke guides-mass pass (cluster scripts timeout pre-existing, control-verified) / review CLEAN / heart YELLOW-acked in-session | amended (wrapper classes user-directed mid-run; merged #487+#576+#151 2026-07-09) |
| 2026-07-09 | cluster-visualization (PyAutoLens#577) | supervised | tests 6 new + 342 suite / smoke integration script end-to-end (per-plane physics assert) / review CLEAN / heart YELLOW-acked in-session | merged-unchanged (#578+#152, 2026-07-09) |
| 2026-07-09 | cluster-scaling-lenstool (autolens_workspace#237) | supervised | tests structural (N=12 + anchoring asserts; workspace repo) / smoke simulator end-to-end on new truth / review CLEAN / heart YELLOW-acked in-session | merged-unchanged (#238 + catalogue-regen follow-up, 2026-07-09) |
