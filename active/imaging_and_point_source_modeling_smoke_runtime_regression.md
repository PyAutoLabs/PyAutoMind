# multi_dataset/features/imaging_and_point_source/modeling.py runtime regressed 5.7 s -> 300 s timeout between 2026-08-31 and 2026-09-07

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-07
Witness: `autolens_workspace/scripts/multi_dataset/features/imaging_and_point_source/modeling.py` completes under `profile_smoke.yaml` in under 60 s on the fixed library main (it was 5.73 s on 2026-08-31 and 301.9 s TIMEOUT on 2026-09-07), with the offending commit named in the PR.
Unattended: ready
Issued: 2026-09-07

On the weekly Workspace Smoke (PyAutoHeart run 34099198772) the `autolens_workspace`
script `scripts/multi_dataset/features/imaging_and_point_source/modeling.py` (script and
notebook legs) hits the 300 s smoke cap:

```
2026-08-31  imaging_and_point_source/modeling.py  passed   5.73 s   (cap 300, profile_smoke.yaml)
2026-09-07  imaging_and_point_source/modeling.py  timeout 301.90 s  (cap 300, profile_smoke.yaml)
2026-09-07  same script, profile_release.yaml     passed  33.08 s   (cap 1800)
```

The script is untouched since 2026-08-07 and `profile_smoke.yaml` is unchanged, so this
is a library-side runtime regression in the 2026-08-31 -> 2026-09-07 window: a 53x
blow-up, not runner variance and not a cap-tuning issue. Candidates in that window:
PyAutoLens `609338fc2` / `5d6eda3f0` (pixelized-source magnification latents, 2026-09-05),
PyAutoArray Delaunay #524 / #526, PyAutoGalaxy Gaussian-deflections precompute.

Bisect the library mains across that window with the script under the smoke profile
(reproduce the 300 s first; `PYAUTO_TEST_MODE`/`test_mode` env as the smoke runner sets
it), identify the offending commit, and fix the regression in the library. The
smoke-profile vs release-profile split (300 s vs 33 s) suggests the slow path is only
reached under the smoke env grid (e.g. an eager or re-jitted path that the release
profile skips) — check that first.

Distinct from `draft/bug/autolens_workspace/delaunay_smoke_300s_cap.md`, which is a
different script and a genuine knife-edge.
