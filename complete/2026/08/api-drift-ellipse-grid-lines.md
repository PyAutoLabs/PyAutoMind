# Both HowToGalaxy API-drift markers were stale — and pointed at the wrong repo

Retired unstarted on 2026-08-26 by a `/start_dev` research pass. Never issued as
a GitHub issue and never developed. Both drifts the prompt describes were fixed
in `autogalaxy_workspace` months before it was filed (2026-04-26 and
2026-05-14), and the two `NEEDS_FIX` markers it asks to remove were already gone
from **both** repos. Recorded rather than deleted because the way it went stale
is the reusable finding — it is the second prompt filed off the same stale
2026-04-10 marker set, and the set is now exhausted.

## Verdict

| Half | Reported failure | Actually | Fixed |
|------|------------------|----------|-------|
| `guides/advanced/over_sampling` | `plot_grid() got an unexpected kwarg 'plot_grid_lines'` | **stale call-site**, script-side | 2026-04-26, autogalaxy_workspace `29b77e4` (#38) |
| `ellipse/modeling` | `KeyError on 'ellipses.0.centre_0'` | **model-composition drift**, library-side | 2026-05-14, PyAutoGalaxy #408/#410/#412; unparked 2026-05-15 in `0d6c22f` (#73) |

No PyAutoGalaxy, autogalaxy_workspace or HowToGalaxy change was needed. Nothing
to un-park, no notebooks to regenerate.

## Evidence (the reusable part)

Run against checkout heads `autogalaxy_workspace@0b81044`, `PyAutoGalaxy@05e5d13`,
`PyAutoArray@158db38`, `PyAutoFit@34d6dff`, `PyAutoNerves@535ab1b`, on Python 3.12.

1. **Clean-main reproduction passes under both build profiles.**
   - `over_sampling.py` with **no test mode at all** — exit 0.
   - `ellipse/modeling.py` at release fidelity (`PYAUTO_TEST_MODE=1`) — exit 0 in
     3m 08s across 12 real Dynesty/Drawer fits with visualization on, including
     the `result.instance.ellipses[0].centre` reads the reported `KeyError` would
     have hit. Zero `KeyError`.
   - Smoke profile (`PYAUTO_TEST_MODE=2`) on a cleared output tree: 36s and 4s,
     both far under the 300s default cap.
2. **Decisive test, `over_sampling` — pin the script, move the library.**
   `git show 2531a6e:scripts/guides/advanced/over_sampling.py` (the *unmodified*
   April-10 marker-commit script) against today's library still exits 1 with the
   verbatim `TypeError: plot_grid() got an unexpected keyword argument
   'plot_grid_lines'`. The library never grew the kwarg back; the fix was the
   call-site edit at 4 sites in `29b77e4`, shipped 2026-04-26.
3. **Decisive test, `ellipse/modeling` — the mirror image.** The April-10 script
   run unmodified against today's library exits 0 with zero `KeyError`, and its
   model-composition block (`ellipse.centre.centre_0` … `af.Collection(ellipses=[ellipse])`)
   is byte-identical to `2531a6e`. Script pinned, library moved, failure gone ⇒
   the fix was library-side — the ellipse JAX refactor.
4. **Both markers were already gone.** `ellipse/*` left
   `autogalaxy_workspace/config/build/no_run.yaml` in `0d6c22f` (2026-05-15);
   `over_sampling` left it in `29b77e4` (2026-04-26). HowToGalaxy's copies left in
   `8f52771` (2026-07-22 10:41 BST, #35). Neither repo's `no_run.yaml` mentions
   either path today.

## Key traps / findings

- **The prompt named a repo that cannot contain either script.** It says
  `Target: howtogalaxy` / `Repos: HowToGalaxy`, but `scripts/guides/advanced/`
  and `scripts/ellipse/` are `autogalaxy_workspace` paths — HowToGalaxy holds
  only `scripts/chapter_*/` and `scripts/simulators/`. The prompt was written
  from HowToGalaxy's `no_run.yaml`, whose two entries were inert copy-paste that
  matched zero files. **A `no_run` entry is evidence of a repo's bug only if it
  matches a file in that repo** — the exact trap `ell-comps-kwargs-keyerror`
  recorded, hit again by the prompt that record's own follow-up section spawned.
- **The follow-up outlived the thing it followed up on by four hours.** This
  prompt was filed 2026-07-22 from `ell-comps-kwargs-keyerror`'s "two siblings
  remain" section; `8f52771` deleted both markers at 10:41 that morning. A
  follow-up that names specific lines should re-read those lines before being
  filed, not inherit them from the parent record.
- **Two symptoms, two different fix sites — worth splitting after all.** The
  prompt bundled them as "two independent, small stale-API call-sites". One was
  a call-site; the other never was. Had either needed work they would have been
  separate PRs in separate repos, which is what hard rule 3 exists to catch.
- **The 2026-04-10 marker set is now fully adjudicated: 7 of 8 were stale.**
  `2531a6e` parked 8 scripts. Exactly one —
  `chapter_4_pixelizations/tutorial_2_mappers` — needed a real script fix
  (HowToGalaxy `5961edf`, 2026-06-09). The other seven were all fixed upstream
  and left their markers behind: `mask_irregular` (`7a5689f`), the three
  pixelization entries (`c9b509d` / `4496f2f`), `imaging/modeling`
  (`e26a2c8`, recorded as `ell-comps-kwargs-keyerror`), and both of these. A
  NEEDS_FIX marker older than a release cycle should be treated as *unverified*,
  not as a known bug — the prior is ~7-in-8 that it is already fixed.

## Follow-ups

- **Sweep, not prompts.** The 2026-04-10 set is now exhausted, but the same
  method has never been run against the *later* marker generations (2026-04-24,
  2026-05-20, 2026-07-14) or against the sibling workspaces. Heart's
  stale-parked-script count is the trigger; the recipe is the two bullets above
  — run both build profiles on a cleared output tree, then pin the script and
  move the library to localise the fix in a single run. Worth one sweep prompt
  covering every live NEEDS_FIX marker, not one prompt per marker: each of these
  has cost a full session to conclude "already fixed".
- **Cosmetic, unfiled.** `autogalaxy/util/plot_utils.py:plot_grid` accepts a
  `lines=` parameter and documents it, but never forwards it to
  `autoarray.plot.plot_grid`. No caller in either workspace passes `lines=`, so
  nothing is broken today; noted here rather than filed because it has no
  standalone trigger.

## Original prompt

# HowToGalaxy small API drifts: ellipse kwargs + plot_grid_lines (parked NEEDS_FIX)

Type: bug
Target: howtogalaxy
Repos:
- HowToGalaxy
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-07-22 (backfilled from git)

Two independent, small stale-API call-sites in HowToGalaxy, both parked since 2026-04-10 and still
parked after the 2026-07-21 census:
- `ellipse/modeling` — `KeyError on 'ellipses.0.centre_0'` kwargs after API drift in ellipse modeling.
- `guides/advanced/over_sampling` — `plot_grid() got an unexpected kwarg 'plot_grid_lines'` after a
  plotter API change (find the current plotter kwarg name and update the call).

Reproduce each on clean main, update the call-sites (or the library if the drift was unintended),
remove both NEEDS_FIX markers from HowToGalaxy/config/build/no_run.yaml, regenerate notebooks.
Only edit scripts/, never notebooks/.
