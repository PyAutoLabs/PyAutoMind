Merged PyAutoArray#720 (human /prm, 2026-11-27), from shift 2026-11-26-pm.

The spurious "No blurring_image" Convolver warning is fixed in the library simulator.

Decision taken (accepted at /prm): the prompt asked for a workspace bug prompt, but the cause was in the library, so it was fixed there. Witness: the full-resolution autolens imaging/simulator.py warnings went from 2 to 0. Tests: simulator+operators 154 and imaging 50 passed; the control fails 2/2 with the fix reverted. Targeted smoke 18/18. Review FINDINGS (3 low), fixed, then CLEAN. Heart GREEN.

Follow-up filed: draft/bug/autolens/deflections_simulator_no_psf_padding.md.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/720

## Original prompt

# Convolver "No blurring_image provided" warning in canonical workspace scripts

Type: bug
Target: workspaces
Repos:
- PyAutoArray
- autolens_workspace
- autogalaxy_workspace
Themes:
- hygiene
- ci-smoke
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: One canonical script run without `PYAUTO_WORKSPACE_SMALL_DATASETS=1` records whether the `No blurring_image provided` warning persists; if it does not, the small-dataset profile silences it and the audited scripts run warning-free under smoke; if it does, a bug prompt against the workspace scripts is filed and this one closes.
Review-minutes: 3
Unattended: ready
Issued: 2026-11-26
Verified: 2026-11-26 86623611 (PyAutoArray), 6ef113ed (autogalaxy_workspace), 083c65e8 (autolens_workspace)
Lane: any
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

<!-- re-homed from draft/triage/ to draft/bug/workspaces/ at the witness-campaign close-out, 2026-09-17: the verify-first step lives in the workspace scripts either way -->
