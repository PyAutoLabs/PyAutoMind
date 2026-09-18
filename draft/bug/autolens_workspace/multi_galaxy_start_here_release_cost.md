# Profile multi_galaxy/start_here.py's release cost and retire its 3600s override

Type: bug
Target: autolens_workspace
Themes:
- release
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-09-18

## Context

`scripts/multi_galaxy/start_here.py` was swapped off the simulated `simple`
look-alike onto the archival ACS/WFC F814W frame of SDSS J1011+0143 on
2026-09-17 (autolens_workspace#554, issue #549). `config/build/profile_release.yaml`
was not updated with it, so it alone among the real-FITS `start_here` scripts kept
the profile defaults, and the first Release Integrate run that saw the change
killed it:

- PyAutoHeart run 35319361459 (2026-09-18) — `1 timeout: autolens multi_galaxy/start_here.py`
- the only failure in the leg, and the one that blocked that night's release
  (PyAutoBrain nightly run 35318011061), with PyAutoGalaxy#621 and PyAutoLens#742
  (MassField phases 1–2) waiting behind it

autolens_workspace#563 unblocked it by mirroring `imaging/start_here`:
`PYAUTO_SMALL_DATASETS: "0"` plus a per-script `BUILD_SCRIPT_TIMEOUT: "3600"`.
That is an unblock, not a verdict on the cost.

## Required work

1. Benchmark the script from a **clean** `output/` tree under
   `config/build/profile_release.yaml`, env resolved by
   `autohands.env_config.build_env_for_script` at workspace CWD. Record
   phase-level timing. Cached output is not pass evidence
   (`draft/bug/health_fixes/release_timeout_policy.md` item 4).
2. Establish where the cost sits: the real PSF and frame size, the number of
   lens galaxies in the field, sampler settings, XLA compile, or visualization.
   The `imaging/start_here` precedent was a ~26 min XLA compile of
   MultiStartProdigy before the first gradient step — check for the same shape
   before assuming the fit itself is the cost.
3. Then choose explicitly, per `release_timeout_policy.md` item 3:
   - bring it reliably under the run-wide 1800s cap and **remove** the
     `BUILD_SCRIPT_TIMEOUT: "3600"` line from `profile_release.yaml`; or
   - document why a real multi-galaxy field cannot fit the cap and keep the
     override with that reasoning recorded.
4. Do not raise the run-wide cap. It is still the only guard on every other
   entry in the profile.

## Notes

- Sibling prompt: `draft/bug/health_fixes/release_timeout_policy.md` — same
  policy, five older scripts, and the doctrine this prompt follows.
- The two SLOW-parked siblings in `config/build/no_run.yaml`
  (`cluster/start_here`, `weak/features/strong_lensing/a2744`) are the
  alternative outcome if the cost turns out to be irreducible; #563
  deliberately did not take that branch, because parking removes the script
  from release validation entirely.
