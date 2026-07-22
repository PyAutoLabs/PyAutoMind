# ell_comps kwargs KeyError — both NEEDS_FIX markers were stale

**Issue:** PyAutoLabs/autogalaxy_workspace#143 (closed 2026-07-22)
**PRs:** PyAutoLabs/HowToGalaxy#32 (merged) — `autogalaxy_workspace` half was already shipped in #142 (merged 2026-07-21)
**Type:** bug / workspace · **Difficulty:** small · **Autonomy:** supervised

## Verdict

The prompt asked whether the `KeyError on ('galaxies','galaxy','bulge','ell_comps'...)` drift was a
**stale call-site** or **model-composition drift**. Answer: **model-composition drift, library-side,
already fixed upstream between 2026-04 and 2026-07.** No PyAutoGalaxy change was needed — the repo
dropped out of scope.

## Evidence (the reusable part)

1. **Clean-main reproduction passes** under both build profiles — smoke (`PYAUTO_TEST_MODE=2` + skips,
   on a *cleared* output tree so no completed fit is resumed) and release-fidelity
   (`PYAUTO_TEST_MODE=1`, real sampler/output/visualization/checks, JAX on). Exit 0, zero `KeyError`.
2. **The call-site never changed** — the model-composition block is byte-identical to the marker
   commit `48dad395` (2026-04-10), which rules out the stale-call-site hypothesis outright.
3. **Decisive test:** `git show 48dad395:scripts/imaging/modeling.py` — the *unmodified April-10
   script* — run against today's installed library exits 0 with zero `KeyError`. When a script and a
   library have both moved, pinning one and moving the other localises the fix in a single run.
4. **Timing gate before un-parking:** 27.4 s vs the 60 s CI cap, so returning it to validation is safe.

## Two traps this task hit

- **A stale local `main` faked a live marker.** I fetched PyAutoMind but not the *target* repo, so I
  planned against `autogalaxy_workspace@3c0c7e42` and saw a marker that PR #142 had removed the
  previous evening. Only the worktree checkout (which fetches) surfaced it. **`git fetch` the repo the
  marker lives in before trusting the marker** — syncing Mind is not enough.
- **A no_run entry that matches nothing reads exactly like a parked script.** HowToGalaxy's entry was
  the literal path `autogalaxy_workspace/scripts/imaging/modeling`, copy-pasted from the workspace's
  list. Patterns containing `/` substring-match the file path, and HowToGalaxy holds only `chapter_*/`
  and `simulators/`, so it gated zero files. Its list still carries dead `guides/`, `gui/`, `ellipse/`,
  `fits_make` entries from the same copy-paste. **Confirm a no_run pattern actually matches a file
  before treating it as evidence of a bug.**

## Gate

Heart YELLOW score 52, `red_reasons: []`, human-acknowledged before push. All four YELLOW reasons
pre-existing and unrelated; this change reduces one of them (58 stale parked scripts).

## Follow-up

Two siblings from the same 2026-04-10 parking commit remain and are plausibly stale for the same
reason: `ellipse/modeling` (`KeyError on 'ellipses.0.centre_0'`) and `guides/advanced/over_sampling`
(`plot_grid() got unexpected kwarg 'plot_grid_lines'`). A concurrent session independently found its
own marker stale (autolens_workspace_test#193), and Heart still counts 58 stale parked scripts — the
2026-04 marker set looks systematically out of date and warrants a sweep rather than one-by-one work.

## Original prompt

# `ell_comps` kwargs KeyError in imaging/modeling after API drift (parked NEEDS_FIX)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autogalaxy_workspace
- HowToGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Parked since 2026-04-10; still parked after the 2026-07-21 census. Same failure in two repos (one
root cause): `KeyError on ('galaxies','galaxy','bulge','ell_comps'...)` kwargs after API drift.

Affected: `autogalaxy_workspace/scripts/imaging/modeling` and the HowToGalaxy copy of the same script.

Decide whether the drift is in the model-composition/kwargs path (PyAutoGalaxy/PyAutoFit) or just a
stale call-site in the scripts — reproduce on clean main first. Fix, then remove the NEEDS_FIX marker
from BOTH repos' config/build/no_run.yaml. If scripts change, regenerate notebooks.
