# HowTo* no_run.yaml — 3 dead NEEDS_FIX markers + 1 inert SLOW entry removed

**Issue:** PyAutoLabs/HowToGalaxy#34 (closed 2026-07-22)
**PRs:** PyAutoLabs/HowToGalaxy#35 (merged) · PyAutoLabs/HowToLens#44 (merged)
**Type:** bug / workspace · **Difficulty:** small · **Autonomy:** supervised
**Follow-up from:** PyAutoLabs/autogalaxy_workspace#143

## Finding

The HowTo\* `no_run.yaml` lists were copy-pasted wholesale from their parent workspace repos when the
tutorials were split out. Audited every entry against the real matcher
(`PyAutoHands/autobuild/build_util.py::should_skip`) over every tracked `scripts/**.py`:

| Repo | Entries | Match ≥1 file | Match zero files |
|---|---|---|---|
| HowToGalaxy | 18 | 1 (`tutorial_searches`) | **17** |
| HowToLens | 32 | 2 (`tutorial_searches`, `tutorial_5_borders`) | **30** |

A `no_run` entry that matches nothing is indistinguishable, by eye, from a parked script. Three carried
`NEEDS_FIX` tags advertising bugs that do not exist in those repos and were inflating Heart's
stale-parked count.

## The non-obvious one

`howtolens/chapter_4_pixelizations/tutorial_10_brightness_adaption # SLOW - exceeds 60s test timeout`
was **broken, not dead**: the file really exists, but the stale pre-split `howtolens/` prefix meant the
substring never matched, so the entry had been inert since the split and the tutorial had been running
in CI regardless.

The obvious fix (repair the prefix) was wrong on two counts:
- **The 60s cap does not exist** — `run_all.py` sets `DEFAULT_TIMEOUT_SECS = 300`. See
  [[project_slow_skip_timeout_cap_myth]].
- **Measured 233.7s, exit 0** under the smoke profile — it fits the real cap.

Repairing would have newly parked a passing script. Deleting was behaviour-preserving. **When a skip
entry looks broken, measure against the real cap before restoring it — restoring a skip is not the
safe default.**

## Scope discipline

Human chose "markers + broken pattern only" over purging all 47 dead entries. Deliberately left:
- ~44 zero-match entries — several are *stem* patterns (`fits_make`, `png_make`, `data_fitting`,
  `deflections`) that would begin applying if such a script were added, so they may be prospective
  guards rather than cruft.
- `tutorial_6_model_fit` (HowToLens) — no file of that stem has ever existed in repo history;
  `tutorial_8_model_fit.py` exists in chapter_4 but the intended target is ambiguous. Not guessed at.

## Verification

Live-entry sets byte-identical before and after (HowToGalaxy `['tutorial_searches']`; HowToLens
`['tutorial_searches', 'tutorial_5_borders']`), both YAMLs re-parse, no `NEEDS_FIX` string remains.

## Gate

Heart YELLOW score 52, `red_reasons: []`, reason set identical to the human acknowledgement given
earlier in the session.

## Net effect

Together with #143, every 2026-04-10 `NEEDS_FIX` marker in the HowTo\* repos is gone, and **not one was
a real bug** — 3 were zero-match copy-paste, and HowToFit's was cleared separately by PyAutoFit#1412 +
HowToFit#24. See [[feedback_reproduce_before_trusting_needs_fix_markers]].

## Original prompt

# HowTo* no_run.yaml — dead NEEDS_FIX markers and broken patterns

Type: bug
Target: howto
Repos:
- HowToGalaxy
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up from PyAutoLabs/autogalaxy_workspace#143 (ell_comps kwargs KeyError), which found that
HowToGalaxy's `no_run.yaml` carries entries copy-pasted wholesale from the parent workspace repos when
the tutorials were split out. Auditing every entry against the real matcher
(`PyAutoHands/autobuild/build_util.py::should_skip`) shows the problem is systemic:

- **HowToGalaxy: 17 of 18 entries match zero files** (only `tutorial_searches` is live).
- **HowToLens: 30 of 32 entries match zero files** (only `tutorial_searches`, `tutorial_5_borders`).

Scope for THIS task (deliberately narrow — the human chose markers + broken patterns only):

1. Delete the dead `NEEDS_FIX` entries, which falsely advertise open bugs and inflate Heart's
   stale-parked-script count:
   - HowToGalaxy: `ellipse/modeling`, `guides/advanced/over_sampling`
   - HowToLens: `group/slam`
2. Delete `howtolens/chapter_4_pixelizations/tutorial_10_brightness_adaption` from HowToLens. This is
   a **broken** pattern, not dead cruft: the file really exists at
   `scripts/chapter_4_pixelizations/tutorial_10_brightness_adaption.py`, but the stale pre-split
   `howtolens/` prefix means the substring never matches, so the entry has not applied since the repo
   split. Its stated reason (`SLOW - exceeds 60s test timeout`) rests on a cap that does not exist —
   `run_all.py` `DEFAULT_TIMEOUT_SECS = 300`. Measured: **233.7s, exit 0** under the smoke profile, so
   it fits the real cap. It is already running in CI today, so deleting the entry is behaviour-
   preserving; repairing the prefix would instead newly park a passing script.

Out of scope, report only:
- The remaining ~44 zero-match entries in both repos. Some are stem patterns (`fits_make`, `png_make`,
  `data_fitting`, `deflections`) that would start applying if such a script is ever added, so they may
  be prospective rather than dead.
- `tutorial_6_model_fit` (HowToLens, `# InversionException due to test mode`) — no file of that stem
  has ever existed in HowToLens history, and the intended target is ambiguous
  (`tutorial_8_model_fit.py` exists in chapter_4). Needs a human call, not a guess.

Risk note: tutorial_10 uses 233.7s of the 300s budget (22% headroom) on a laptop. If CI is slower it
could time out, in which case the correct fix is a **correctly-spelled** SLOW entry, not the broken one.
