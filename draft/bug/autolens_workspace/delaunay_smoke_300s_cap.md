# `imaging/features/pixelization/delaunay.py` sits on the 300 s smoke cap (330–354 s under the release profile)

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: safe
Priority: medium
Status: draft
Issued: 2026-09-04
Consequence: glance
Witness: `scripts/imaging/features/pixelization/delaunay.py` completes in under ~200 s under the smoke profile (`PYAUTO_TEST_MODE`) on a clean `main` checkout, measured twice, with no change to the global 300 s smoke cap; or the script is removed from `smoke_tests.txt` and named in the release-profile list instead.
Review-minutes: 3
Unattended: ready

## Symptom

`scripts/imaging/features/pixelization/delaunay.py` is a knife edge on the smoke gate's 300 s
per-script cap. It does not fail reproducibly and it is not a regression — it simply takes about
as long as the cap allows, so whether it passes depends on machine load.

Measured under the **release** profile (1800 s cap, all PASS):

| Run | Date | Time |
|-----|------|------|
| [33602064424](https://github.com/PyAutoLabs/PyAutoHands/actions/runs/33602064424) | 2026-09-02 | 353.9 s |
| [33847995194](https://github.com/PyAutoLabs/PyAutoHands/actions/runs/33847995194) | 2026-09-04 | 338.8 s |
| [33899429414](https://github.com/PyAutoLabs/PyAutoHands/actions/runs/33899429414) | 2026-09-04 | 332.9 s |

And on the **post-release smoke leg** of the live release run
[33908218375](https://github.com/PyAutoLabs/PyAutoHands/actions/runs/33908218375) (300 s cap):
attempt 1 **TIMEOUT at 305 s**, attempt 2 **PASS**. Same script, same commit, one retry apart —
the definition of a cap that the script is sitting on rather than a script that is broken.

The script entered the smoke gate in autolens_workspace#307 (`9eba5071`, 2026-07-21), which added
it to `smoke_tests.txt` when the 2026-04-10 `FitException` was fixed. Its cost has grown with the
script since.

## Cause (to confirm by profiling)

The script is 1628 lines and runs **seven** separate `Nautilus` fits in one file
(`n_live=` 100, 75, 200, 150, 75, 150, 150), covering the `Overlay` image-mesh, the `Hilbert`
image-mesh, the adapt-image path and a multi-search source pipeline. Even at `PYAUTO_TEST_MODE`
live-point counts, seven searches plus the Delaunay/qhull mesh construction in each is the bulk
of the runtime. Profile the stages before assuming which one dominates.

## Fix

Pick whichever the profile supports; **do not raise the global smoke cap** — the cap is the only
thing keeping the gate's total runtime bounded, and one script's convenience is not worth it.

1. **Cut it under ~200 s under the smoke ENV.** Reduce live points and/or the mesh grid size for
   the smoke profile only (the script already reads `PYAUTO_TEST_MODE`), so the release profile
   keeps the scientifically meaningful settings.
2. **Split it.** Seven searches in one file is a lot for one gate entry; a `delaunay.py` +
   `delaunay_hilbert.py` (or similar) split halves the per-script time without dropping coverage,
   and each half stays well under the cap.
3. **Move it to the release-profile list only.** Remove it from `smoke_tests.txt` and rely on the
   Release Integrate leg (1800 s cap) that already exercises it three times a week. This is the
   cheapest option and the honest one if the script genuinely needs 330 s of real work — but it
   costs pre-release coverage, so prefer 1 or 2 if the profile shows easy savings.

Whichever route, re-measure twice under the smoke profile and regenerate the notebook if the
script changes.
