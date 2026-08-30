# Triage: Convolver "No blurring_image provided" warning in canonical workspace scripts

Type: triage
Target: PyAutoArray / workspaces
Repos:
- PyAutoArray
Themes:
- hygiene
- ci-smoke
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-06 (backfilled from git)

Filed 2026-08-06 from the `/cli_noise_clean` audit. Every audited workspace
script run (`autolens_workspace` + `autogalaxy_workspace` `imaging/simulator.py`
and `imaging/start_here.py`, under `PYAUTO_WORKSPACE_SMALL_DATASETS=1`)
emitted `UserWarning: No blurring_image provided. Only the direct image will
be convolved.` from `autoarray/operators/convolver.py:1424`.

Suspected test-mode artifact (the degraded-profile trap): capping the grid to
15×15 px likely collapses the blurring-region mask to empty, so
`blurring_image` legitimately comes back `None` under the small-dataset
profile.

**Verification step first — do not fix blind:** re-run one script WITHOUT
`PYAUTO_WORKSPACE_SMALL_DATASETS=1`.
- Warning gone at full resolution → test-mode-only artifact; silence under the
  small-dataset profile (smoke env config), scripts are correct.
- Warning persists → real defect in the canonical `start_here.py` narrative
  (missing blurring image in the flagship examples) — becomes a bug task
  against the workspace scripts, not a noise item.
