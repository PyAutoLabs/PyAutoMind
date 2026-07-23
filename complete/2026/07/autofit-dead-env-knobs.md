`PYAUTO_SMALL_DATASETS` and `PYAUTO_FAST_PLOTS` deleted from all four
autofit-only build profiles (8 lines, 3 repos). Issue autofit_workspace#111;
PRs autofit_workspace#112, autofit_workspace_test#68, HowToFit#29, all merged
2026-07-23.

## The finding was initially backwards

The #321 key-order sweep made the smoke and release profiles diffable for the
first time, and the first read of the result was that
`autofit_workspace_test/config/build/env_vars_release.yaml` was **missing** two
required keys — inferred from the release-profile doctrine ("every var this
profile cares about gets an EXPLICIT value, not left absent", because an absent
key falls through to the caller's ambient env). The user asked the obvious
question — *are those vars even used by autofit?* — and the answer inverted it.

**Neither knob is readable in an autofit-only workspace:**

- `PYAUTO_SMALL_DATASETS` is read only in PyAutoArray
  (`util/dataset_util.py`, `structures/grids/uniform_2d.py`, `mask/mask_2d.py`,
  `operators/over_sampling/over_sample_util.py`, `operators/convolver.py`),
  PyAutoGalaxy (`analysis/model_util.py`) and PyAutoLens. ZERO occurrences in
  PyAutoFit or PyAutoNerves — not even a docstring.
- `PYAUTO_FAST_PLOTS` is read in `autoarray/plot/utils.py` and
  `autogalaxy/{util,plot}/plot_utils.py`. In PyAutoFit it appears twice, both in
  prose (`autofit/non_linear/quick_update.py:71` + a test docstring), never in
  an `os.environ` lookup.
- PyAutoFit does not import autoarray, and no script in autofit_workspace /
  autofit_workspace_test / HowToFit imports autoarray/autogalaxy/autolens. The
  reading code never loads.
- PyAutoFit's single `tight_layout()` is `autofit/non_linear/live_viewer.py:102`,
  inside the interactive `plt.ion()` desktop viewer — never runs headless in CI,
  so honouring FAST_PLOTS there would buy nothing. Deletion, not implementation.

So `autofit_workspace_test/config/build/env_vars_release.yaml` was the one
profile that had it RIGHT, and the other four were the defective ones. The
doctrine was not violated: autofit cares about neither var, so absence is
correct rather than a fall-through hazard.

The stale comments were the giveaway all along — an autofit config claiming to
"reduce MGE gaussians" and skip "critical curve/caustic overlays", both lensing
concepts. Same bidirectional copy-paste pathology as the no_run dead-entry purge.

## How it was verified

Resolved-env delta, not a build run: 227 script x profile environments resolved
from an EMPTY base via `resolve_clean()`
(`PyAutoHands/autohands/validate_env_profiles.py`), before and after. Unlike
#321 the diff was expected to be NON-empty, so the assertion was tightened
accordingly: the delta must be EXACTLY the two keys disappearing, with no other
key added/removed/changed and `overrides:`/`args_default` byte-identical per
profile. It was. `validate_env_profiles.py` verdicts unchanged from `main`.

## Notes for next time

- **Check whether a knob is READABLE in a repo before reasoning about whether
  its value is right.** The doctrine question ("should this key be pinned?")
  only makes sense downstream of the reachability question ("can anything here
  read it?"). Getting that order wrong produced a confidently-stated finding
  that was the exact inverse of the truth.
- The Brain Feature Agent again returned `too-large -> split-into-4-phases`
  (score 11) for an 8-line deletion across 3 repos — repo count dominating the
  score. Overridden, as on #321.
- A `git push` in a per-repo loop hung past a 2-minute Bash timeout mid-way;
  the commits had landed but two pushes had not. Re-running with
  `timeout 60 git push` per repo completed cleanly. Check `ls-remote` rather
  than assuming a timed-out loop pushed nothing.

## Heart gate

Shipped under the corrective-PR exception, human-authorized against the verbatim
RED reason `release validation FAILED (stage integrate)` (red, score 40, ts
2026-07-23T14:11:21Z) — unrelated to this diff. Authorization was requested
FRESH for this task rather than carried over from #321; merge was a separate
explicit human instruction.
