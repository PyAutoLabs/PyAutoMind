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

## 2026-09-18 (evening) — the script is now SLOW-PARKED; two failure modes measured

autolens_workspace#563's override did not work and made the failure worse. It was
reverted and the script parked in `config/build/no_run.yaml` by
autolens_workspace#564. Two Release Integrate runs bracket the change — same
script, and between them the only workspace diff was #563:

| | Stage 3 run | Outcome |
|---|---|---|
| profile defaults | PyAutoHeart 35319361459 | `TIMEOUT` at the 1800s `mode=release` cap; results uploaded; paged as `1 timeout` |
| `BUILD_SCRIPT_TIMEOUT=3600` + `PYAUTO_SMALL_DATASETS=0` | PyAutoHeart 35372831809 | **runner shutdown signal, exit 143, ~1478s in** — before either cap fired; results never uploaded, so the stage report named nothing |

Both runs: 1 failure of 53 jobs. Nothing else in Stage 3 failed either time.

**What this tells whoever picks this up:**

1. **The cap was never what killed it the second time.** ~1478s is under both 1800s
   and 3600s. Raising the timeout again is not the fix — do not try it a third time.
2. **Lifting `PYAUTO_SMALL_DATASETS` is the suspect.** The script died *earlier*
   with the data cap lifted than with it on. That is consistent with the uncapped
   real frame exhausting runner memory (a hosted-runner OOM surfaces exactly as
   "the runner has received a shutdown signal" / exit 143). **This is inferred from
   the failure signature — there is no memory telemetry from either run.** Item 1
   below should confirm or kill it before anything is built on it.
3. So the benchmark needs a **memory** axis, not just wall-clock: peak RSS through
   the fit, capped and uncapped, is the measurement that decides whether this script
   can run on a hosted runner at all.
4. If it cannot, that is a legitimate answer — the parking stands and the entry says
   why. The two siblings (`cluster/start_here`,
   `weak/features/strong_lensing/a2744`) have been parked on the same reasoning
   since 2026-07-22.

Note also that `PYAUTO_SMALL_DATASETS: "0"` is still the right call for the *other*
real-FITS `start_here` scripts — it exists because a 15x15 grid cannot fit a real
frame. The error in #563 was pairing it with a timeout bump as though both addressed
the same problem. Do not read this entry as an argument against the cap lift in
general.
