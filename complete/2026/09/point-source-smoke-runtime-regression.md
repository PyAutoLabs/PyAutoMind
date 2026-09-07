# hips2fits/catalogue downloads bounded so a stalled response cannot burn the smoke cap (not a library regression)

autolens_workspace#538 → `fa750cbb`, closing autolens_workspace#537 (transferred from PyAutoLens#730), merged 2026-09-07. One of six corrective PRs shipped 2026-09-07 under the human-authorised Heart RED corrective-PR exception (reasons: `release validation FAILED (stage integrate)` and `workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)`). Fable session planned; Opus subagents implemented per task; merged via /prm the same day. Validation of the RED clearing is the next scheduled Workspace Smoke and Release Integrate runs on fresh wheels.

- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/537
- completed: 2026-09-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/538
- corrective-red: authorization https://github.com/PyAutoLabs/autolens_workspace/issues/537#issuecomment-5573412088

## What shipped
- `scripts/multi_dataset/features/imaging_and_point_source/modeling.py`, `scripts/weak/start_here.py`, `scripts/weak/real_data/a2744.py`, `scripts/weak/features/strong_lensing/a2744.py`: inlined `_download(url, path)` — `urlopen(timeout=30)`, three attempts with 2 s / 4 s backoff, `RuntimeError` naming the URL after the third, bytes written only after a full read. Four notebooks regenerated. PyAutoLens untouched.

## Key traps / findings
- The "5.7 s → 302 s, 53x library regression" was an untimed `urlretrieve` blocked in `ssl.read` at `modeling.py:80` — the run artifact's `error_message` traceback names it, with no PyAuto frame on the stack. At the exact library mains CI cloned the script runs in 7 s (smoke) / 12 s (release). Read the artifact traceback before planning a bisect.
- Precedent: #293 (`3920ed30`, 2026-07-19) fixed the identical defect in `cluster/start_here.py`; it returned in four scripts within three weeks. Durable guard filed: `draft/test/autolens_workspace/no_untimed_network_downloads_check.md`.
- Two prompt premises falsified: the pixelized-source latents commits are skipped under any test mode (opposite signature), and `PointSolver.solve` short-circuits under `PYAUTO_SMALL_DATASETS`, so the "solver amplification" mechanism does not exist.
- Prompt `Target: PyAutoLens` was reclassified to autolens_workspace mid-task; the issue was transferred in-session (the auto-mode classifier blocks `gh issue transfer` for subagents).

## Original prompt

# multi_dataset/features/imaging_and_point_source/modeling.py runtime regressed 5.7 s -> 300 s timeout between 2026-08-31 and 2026-09-07

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-07
Witness: `autolens_workspace/scripts/multi_dataset/features/imaging_and_point_source/modeling.py` completes under `profile_smoke.yaml` in under 60 s on the fixed library main (it was 5.73 s on 2026-08-31 and 301.9 s TIMEOUT on 2026-09-07), with the offending commit named in the PR.
Unattended: ready
Issued: 2026-09-07
Finding: not a library regression — an untimed `urlretrieve` hips2fits fetch stalled at modeling.py:80 and burnt the 300 s cap (run 34099198772 artifact traceback); fix is timeout+retry in autolens_workspace, PyAutoLens untouched.

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
