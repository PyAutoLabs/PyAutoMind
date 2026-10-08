# Park the autolens shapelets modeling smoke script that times out in release…

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Consequence: glance
Witness: config/build/no_run.yaml parks scripts/multi_galaxy/features/advanced/shapelets/modeling.py (.py-anchored) and the release-profile smoke run no longer lists/attempts it.
Review-minutes: 3
Unattended: ready
Issued: 2026-10-08

# Park the autolens shapelets modeling smoke script that times out in release smoke

Found by /review_release on PyAutoHands release run 37653172766, release 2026.10.7.1, which published fine.

**autolens_workspace smoke timeout.** In the release job `run_smoke_tests (3.12, PyAutoLabs/autolens_workspace, autolens_workspace)`, 41/42 listed scripts passed; `scripts/multi_galaxy/features/advanced/shapelets/modeling.py` hit TIMEOUT (1805s, BUILD_SCRIPT_TIMEOUT=1800) under `config/build/profile_release.yaml`. It is listed in `lens/autolens_workspace/smoke_tests.txt` line 47. Precedent: the autogalaxy shapelets script was already `no_run`'d (autogalaxy_workspace PR #131); the autolens one was earlier left out of the slow-script hygiene pass as "uncertain". Fix = park it the same way the workspace parks slow/timeout scripts (find the existing convention — e.g. `config/build/no_run.yaml` / a SLOW-park entry like commit 9059d6f6 "SLOW-park multi_galaxy/start_here" — and mirror it; `.py`-anchor the entry). Decide whether it also belongs removed from smoke_tests.txt per that convention. Do NOT change library code or the script's model to make it pass ("never modify code to make tests pass").

<!-- formalised by the Intake (Conception) Agent on 2026-10-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/714552f3-a2ad-45fd-8b3e-cf45adbd6f01/scratchpad/intake/smoke_park.md -->
