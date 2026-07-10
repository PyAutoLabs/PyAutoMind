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
| 2026-07-09 | lenstool-example (autolens_workspace#239) | supervised | tests in-run verification (0.068" parity vs published model; 72-param composition assert) / smoke data.py + modeling.py end-to-end / review CLEAN / heart-ack carried in-session | merged-unchanged (#240, 2026-07-09) |
| 2026-07-09 | weak-modeling | supervised | tests 347-pass / smoke n-a-parked / review n-a-parked / heart YELLOW-no-ack | parked |
| 2026-07-09 | weak-modeling | supervised | tests 347-pass / smoke n-a / review human-signoff / heart YELLOW-acked-at-signoff | merged-unchanged (580+241, 2026-07-09) |
| 2026-07-09 | kxs-workspace-tests (#362 p3) | supervised | scripts-run-clean (adaptive legs chi2~0) / review CLEAN / heart YELLOW-human-cadence | merged-unchanged |
| 2026-07-09 | kxs-refactor (#362 exercise) | safe | tests PASS 867 / ids bit-identical, 62->9.7ms / review CLEAN / heart YELLOW-cadence | merged-unchanged |
| 2026-07-09 | psf-visible-input (#242 flagship) | supervised | scripts run/compile clean / zero behaviour change / review CLEAN / heart YELLOW-cadence | merged-unchanged (wider chain folded into adoption-a per human ii) |
| 2026-07-09 | jwst-nircam-cosmos-web | supervised | tests 83/83 / smoke n/a / review FINDINGS(6)→5 fixed / heart YELLOW | parked |
| 2026-07-09 | wfc3-reduction | supervised | tests 62/62 / smoke n/a / review 1H+2L resolved / heart YELLOW acked | merged-unchanged (#5) |
| 2026-07-09 | jwst-nircam-cosmos-web | supervised | tests 83/83 / smoke n/a / review 6→5 fixed / heart YELLOW acked | PR-open (#7) |
| 2026-07-09 | weak-viz-profiles | supervised | tests 352-pass / smoke n-a-parked / review n-a-parked / heart YELLOW-same-acked-set | parked |
| 2026-07-09 | weak-viz-profiles | supervised | tests 352-pass / smoke n-a / review human-signoff / heart YELLOW-acked-set | merged-unchanged (582+244, 2026-07-09) |
| 2026-07-09 | jwst-nircam-cosmos-web | supervised | tests 83/83 / smoke n/a / review 6→5 fixed / heart YELLOW acked | merged-unchanged (#7) |
| 2026-07-09 | kxs-surface-refactor (#488) | safe | witnesses PASS 956+867+347+script14 unchanged / agent-decision obtained / review CLEAN / heart YELLOW-cadence | merged-unchanged |
| 2026-07-09 | weak-likelihood-function | supervised | tests n-a-docs / smoke script-ran-asserts-pass / review human-signoff / heart YELLOW-acked-set | merged-unchanged (246, 2026-07-09) |
| 2026-07-09 | cluster-likelihood-breakdown (autolens_profiling#57) | supervised | tests in-run LL assert rtol 1e-4 (8-digit match) / smoke both scripts end-to-end from clean + SMOKE=1 + ruff / review CLEAN / heart-ack carried in-session | merged-unchanged (#58 + ruff-format fix, 2026-07-09) |
| 2026-07-09 | weak-small-datasets | supervised | tests 869+356-pass / smoke modeling-30s-e2e / review human-signoff / heart YELLOW-acked-set | merged-unchanged (366+584, 2026-07-09; 584 rerun after upstream merge) |
| 2026-07-09 | point-pairing-policies (PyAutoLens#585) | supervised | tests 5 new regressions + 358 suite / smoke guide end-to-end / review CLEAN / heart-ack carried in-session | merged-unchanged (#586+#248; magnification_filter default stood) |
| 2026-07-09 | keck-ao-reduction-plan (PyAutoReduce#9) | supervised | tests n-a-research / smoke n-a-research / review n-a-no-diff / heart n-a-no-ship | parked (awaiting-input: 3 batched decisions on #9; write leg blocked on refactor-post-phase3) |
| 2026-07-09 | cluster-small-datasets (autolens_workspace#249) | supervised | tests timed evidence 24s/26s/2s/175s under authoritative sweep env from clean regen / smoke = the evidence itself / review CLEAN / heart-ack carried | merged-unchanged (#250+#123, 2026-07-09) |
| 2026-07-09 | weak-strong-lensing | supervised | tests 357-pass / smoke sim+fit+TEST_MODE+real-joint-fit / review human-signoff / heart YELLOW-acked-set | merged-unchanged (587+251, 2026-07-09) |
| 2026-07-09 | csv-api-lenstool (PyAutoGalaxy#490) | supervised | tests 12 new + 962 suite / smoke lenstool example end-to-end at identical 0.0680" parity post-port / review CLEAN / heart-ack carried | merged-unchanged (#491+#252; loud guards stood) |
| 2026-07-09 | weak-real-data (7a) | supervised | tests 364-pass / smoke n-a-library / review n-a-parked / heart YELLOW-acked-set | merged-unchanged (589+253, 2026-07-09; merge pre-authorized by human) |
| 2026-07-09 | delaunay-qhull-callback (PyAutoArray#367) | supervised | tests 873-pass / smoke n-a (no active delaunay smoke entry; production parity gate 5.4e-9 instead) / review CLEAN / heart YELLOW-acked-set in-session | merged-unchanged (368, 2026-07-09; human-directed merge in-session) |
| 2026-07-09 | delaunay-qhull-callback phase-2 (autolens_workspace_test#155) | supervised | parity delaunay.py pin-exact + 1e-8 (7e-15) / near-caustic eager==jit==vmap 1e-8 (3e-10) / review n-a (test-only, human sign-off in-session) / heart YELLOW-acked-set carried | merged-unchanged (155 after 368, 2026-07-09; human-directed merge in-session) |
| 2026-07-09 | weak-sigma-crit-jax | supervised | tests 373-pass / smoke vmap-parity-script / review human-directive / heart YELLOW-acked-set | merged-unchanged (591+156, 2026-07-09) |
| 2026-07-09 | factor-graph-viz-dispatch | safe (refactor cap) | tests 1424-pass / smoke n-a / review human-directive / heart YELLOW-acked-set | merged-unchanged (1340, 2026-07-09) |
| 2026-07-09 | keck-ao-reduction (PyAutoReduce#11) | supervised | tests 110-pass-worktree, downstream n/a / smoke n/a-no-script-surface / review 8-angles-10-findings-9-fixed-CLEAN / heart YELLOW-6-chronic-unacked | parked (awaiting-input: ship sign-off on #11; branch local-only) |
| 2026-07-09 | keck-ao-reduction (PyAutoReduce#11) | supervised | tests 110-pass / smoke n-a / review 9-of-10-fixed-CLEAN / heart YELLOW-acked-at-signoff | merged-unchanged (#12, 2026-07-09; human ship+merge) |
| 2026-07-09 | profiling-agent (PyAutoBrain#60) | supervised | tests n/a (CLI-validated live) / smoke n/a (organism repo) / review CLEAN / heart YELLOW-acked in-session | merged-unchanged (PyAutoBrain#61) |
| 2026-07-09 | release-docs-polish-learn-paths (#592) | supervised | tests n/a (docs-only) / smoke n/a / review pending / heart n/a | parked |
| 2026-07-09 | alma-interferometer (PyAutoReduce#14) | safe | tests 143-pass (downstream n/a, standalone) / smoke n/a (no workspace consumers) / review CLEAN-after-2-fixed-bugs / heart RED-unrelated-worktree-dirt human-acked in-session | merged-unchanged (PyAutoReduce#15, squash 11a2484; human-directed merge in-session) |
| 2026-07-09 | colab-link-rot (HowToLens#21) | safe | tests n/a (no test dirs) / smoke n/a (README-only) / review CLEAN / heart YELLOW-within-launch-ack | merged-unchanged (HowToLens#22, HowToGalaxy#16, HowToFit#13, euclid#24) |
| 2026-07-09 | release-docs-polish-learn-paths (#592) | supervised | tests n/a (docs-only, 0 .py) / smoke n/a (docstring-only) / review CLEAN / heart YELLOW-acked-at-ship (5 chronic) | pr-open (PyAutoLens#593+PyAutoGalaxy#492+autolens_workspace#254; awaiting human merge) |
| 2026-07-09 | release-docs-polish-learn-paths (#592) | supervised | tests n/a / smoke n/a / review CLEAN / heart YELLOW-acked (5 chronic) | merged-unchanged (PyAutoLens#593+PyAutoGalaxy#492+autolens_workspace#254; human ship+merge) |
| 2026-07-09 | regen-workspace-notebooks (#255) | safe | tests n/a / smoke n/a (deterministic nb from unchanged scripts) / review CLEAN / heart YELLOW⊆acked | pr-open (autolens_workspace#256; awaiting human merge) |
| 2026-07-09 | plot-rst-functional-rewrite (#595) | supervised | tests n/a / smoke n/a / review CLEAN / heart YELLOW⊆acked | pr-open (PyAutoLens#596+PyAutoGalaxy#494; awaiting human merge) |
| 2026-07-09 | assistant-wiki-release | supervised | tests n/a (docs repo; api-audit 0/117) / smoke n/a (docs-only; provenance 0 err) / review surface-prepared, mechanical-clean / heart YELLOW (no launch ack) | parked |
| 2026-07-09 | regen-workspace-notebooks (#255) | safe | tests n/a / smoke n/a / review CLEAN / heart YELLOW⊆acked | merged-unchanged (autolens_workspace#256; human merge) |
| 2026-07-09 | plot-rst-functional-rewrite (#595) | supervised | tests n/a / smoke n/a / review CLEAN / heart YELLOW⊆acked | merged-unchanged (PyAutoLens#596+PyAutoGalaxy#494; human merge) |
| 2026-07-09 | assistant-wiki-release (#40) | supervised | tests n/a (docs; api-audit 0/117 + citations 0/391) / smoke n/a (docs-only) / review mechanical-clean / heart YELLOW human-acked at sign-off | amended (human-directed scope addition: --check-citations mode; PR#41 human-merged) |
| 2026-07-09 | nautilus-nn-bottleneck (#18) | supervised | tests pending / smoke pending / review pending / heart pending (gate runs at ship after sign-off) | parked (ship sign-off question on issue #18) |
| 2026-07-09 | rtd-hygiene (#1341) | supervised | tests 1424+962+373+244 pass / smoke n/a (docs+CI only) / review CLEAN / heart YELLOW acked in-session at ship | merged-unchanged (Heart#48+Galaxy#495+Lens#597+Fit#1342; human-authorized merges; Fit leg via human claim override) |
| 2026-07-09 | nautilus-nn-bottleneck (#18) | supervised | tests n/a (no test dir) / smoke n/a (developer repo) / review CLEAN / heart YELLOW human-directed ship in-session | amended (human rejected rec-1 n_networks=0; findings note updated pre-commit; PR#19 human-directed merge) |
| 2026-07-09 | assistant-ref-mechanics (#43) | safe | tests 39 pass + api-audit 0/117 + citations 0/388 / smoke n/a (markdown-only skill edit) / review CLEAN / heart YELLOW⊆launch-ack (6 reasons, recorded in active.md) | merged-unchanged (assistant#44; human-directed merge in-conversation) |
| 2026-07-09 | docs-theming-hub (pyautolabs.github.io#1) | supervised | tests 1424+962+373 pass / smoke n/a (docs styling + static site) / review CLEAN / heart YELLOW same-set-as-acked (disclosed) | amended (human-merged 2026-07-10; 1 amendment: Lens pyauto.css was gitignored — caught by the new docs CI baseline check, fixed pre-merge) |
| 2026-07-09 | rect-adapt (#372) | supervised | tests 877 pass / smoke pending / review pending / heart pending (gate completes at ship after sign-off) | parked (ship sign-off question on issue #372) |
| 2026-07-10 | frame-registration (#19) | supervised | tests 176 pass / smoke pending / review pending / heart pending (gate completes at ship after sign-off) | merged-unchanged (PR#20; human approved recommendation + merge in-conversation; loud-notice rider user-directed) |
| 2026-07-10 | priors-messages-fixes (PyAutoFit#1344) | supervised | tests 1437 pass/14 skip (full suite) / smoke 2/2 PASS / review CLEAN (Fable math re-verification in-session) / heart YELLOW-acked live (6-reason set) | merged-unchanged (PyAutoFit#1345, c0b6c94b8) |
| 2026-07-10 | per-frame-psf (#21) | supervised | tests 181 pass + real-data 3/3 frames viable / smoke n-a (no downstream consumer) / review pending / heart pending (gate completes at ship) | merged-unchanged (PR#22; human-directed ship after sky-subtraction check; psf_from_frames scope amendment user-directed) |
| 2026-07-10 | prior-width-safety (PyAutoFit#1346) | supervised | tests 1447 pass/14 skip (full suite) / smoke 2/2 PASS / review CLEAN (D2 strict->permissive amendment disclosed on issue) / heart YELLOW within live 6-reason ack | merged-unchanged (PyAutoFit#1348, cf0cc4bbb) |
