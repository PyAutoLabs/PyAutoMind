# Wire Stage 3's verify_install result into Heart's install-verification readiness leg

Type: release
Target: PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Wire Stage 3's verify_install result into Heart's install-verification readiness leg. Heart's release-fidelity Stage 3 (workspace-validation mode=release) already runs verify_install checks A-E against the TestPyPI wheels and they pass, but the readiness verdict still reports 'install verification not run' because that result is a separate ingest the leg never receives. Evidence is produced and then thrown away. This is one of three legs holding Heart at YELLOW 70; because the armed nightly release driver's step-5 gate requires GREEN and has deliberately no force input, Heart never reaching GREEN means the nightly can never ship unattended - 2026.7.15.1 shipped only because a human forced it with 'release --force'. Fixing this leg is the durable half: the other two are an ops re-run of the weekly mode=smoke workspace-validation to refresh the stale test_run leg (its 3 failures from 2026-07-09 are already disproven by the fresh release run: autolens_test 90p/0f, 543p/0f/0t overall), and hygiene triage of 58 stale parked no_run scripts (all age_days=90, category slow). Those two are follow-ups, not this task.

<!-- formalised by the Intake (Conception) Agent on 2026-07-15 from user-intake -->
