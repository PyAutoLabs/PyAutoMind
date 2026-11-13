# Nightly ships when Heart is YELLOW only because of an active Stage 3 quarantine

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: a nightly whose Heart release verdict is YELLOW with only active-quarantine (and flaky) reasons ships, with the quarantined scripts named in the release record; any other YELLOW reason still parks; an expired or removed entry (RED) still stops it
Review-minutes: 15
Unattended: never
Lane: any

Human ruling (programme M2 gate, 2026-11-13): "a quarantine-only YELLOW may let the nightly ship". Today `nightly.sh` ships on GREEN only, so an active quarantine (PyAutoHeart#344) still parks the nightly and buys nothing. Heart should expose whether a YELLOW is quarantine-only (a machine-readable flag on the release verdict); the nightly ships on GREEN or quarantine-only YELLOW and names the skipped scripts in its outcome. Record the ruling in AUTONOMY's M2 rulings section. Tier judge: it changes when a release publishes.

<!-- filed 2026-11-13 by the programme lead session -->
