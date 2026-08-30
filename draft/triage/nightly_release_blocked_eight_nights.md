# Nightly release has been blocked 8 nights running — triage the streak

Type: triage
Target: pyautobrain
Repos:
- @PyAutoBrain
- @PyAutoHeart
- @PyAutoHands
Themes:
- release
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-04 (backfilled from git)

Surfaced 2026-08-04 while listing PyAutoBrain workflow runs during the
PR-test-CI ship (#195). Not a PyAutoBrain CI problem — filed here because the
driver lives in Brain.

## First finding: the red is a SIGNAL, not a broken workflow

`agents/conductors/release/nightly.sh` exits **2** when it stops
("🚨 nightly release stopped … No release was made"), so a night where the
driver *correctly* refused to release renders as a red workflow run. Every one
of these failures is the gate doing its job. That is also why nobody was
watching it: a channel that is red whenever it works properly trains its
audience to ignore it. Whether "blocked" should render as a neutral conclusion
(or a distinct notification) rather than `failure` is the first design question
this task should answer.

## Second finding: 8 consecutive blocked nights, two distinct classes

Runs 23–30, 2026-07-28 → 2026-08-04 (run 22 on 07-27 was the last success):

**Class A — stopped at step 4b, Stage 3 release-fidelity integration (6 nights).**
A single script fails the `mode=release` leg and the night stops. The script
*rotates*, which is the interesting part:

- 2026-08-04 — `autolens database/start_here.py`
- 2026-08-03 — `autofit_test graphical/ep.py`
- 2026-08-01, 07-31, 07-30, 07-28 — no script named in the summary line

> **The four unnamed nights DO name their scripts** — in the dispatched
> PyAutoHeart run, not in the Brain log. See "Class A triaged" below; the
> summary line was the only thing missing.

**Class B — passed the readiness gate, then the LIVE release failed (2 nights).**
These are the serious ones: the gate said GREEN, step 6 dispatched a real
release, and the release run failed.

- 2026-08-02 → release 2026.8.2.1 → PyAutoHands run 30736527569 failed in
  `release_test_pypi (3.12, PyAutoLabs/PyAutoFit, main, PyAutoFit)` at step 9,
  **Tests**.
- 2026-07-29 → release 2026.7.29.1 → PyAutoHands run 30428406874 failed (no
  failing job resolvable via the API now).

A gate that passes and is then contradicted by the release run is worth more
attention than the Class A blocks: either the gate's evidence is stale relative
to what `release.yml` actually runs, or the two disagree about what "the
libraries pass" means.

## Third finding: a reporting bug in the stop summary

The 2026-08-04 line reads:

```
1 failed: autolens database/start_here.py, None verify_install
```

The count says **1** but two items are listed, and the second carries a literal
`None` where a script name belongs (the `verify_install` leg has no script). So
the summary formatter mis-counts and stringifies a null. Small, self-contained,
and it makes the nightly notification harder to read at exactly the moment it
matters.

## Suggested scope

1. ~~Decide the exit-code / conclusion contract for "correctly blocked" vs
   "driver broke" — they should not both be red.~~ **DONE 2026-08-04** —
   PyAutoBrain#196 (`a2264fe`). The workflow now classifies the driver's exit
   code: `0/2/3` leave the run green (a blocked night is the gate working, with
   a named `Blocked at a gate` step + `::warning::` + job summary), `1` and
   anything else turn it red. `bin/overnight_status.sh` reads that step so a
   blocked night gets its own `⏸` line and tally instead of reading as plain
   green — otherwise this would have traded a false alarm for a silent one.
2. ~~Fix the stop-summary count + `None` script name.~~ **DONE 2026-08-04** —
   same PR. The formatter moved out of its heredoc into
   `agents/conductors/release/stage_failure_summary.py` (a file can carry a
   test) and reports script failures and non-script legs as separate segments:
   `1 failed: autolens database/start_here.py; verify_install FAILED`.
   11 tests, shaped from the real 2026-08-04 `stage_report.json`.
3. ~~STILL OPEN — the actual releases are still blocked.~~ **TRIAGED
   2026-08-04** (evening, after run 30; no night has run since). The two
   questions this item posed are both answered below. What is left is a short
   list of named, separately-tracked bugs — not an unexplained streak.

## Class A triaged — five causes, not one (2026-08-04)

Read from the Heart Stage-3 job logs for all six Class A nights. **Genuinely
different scripts each night, not one env/profile issue wearing masks** — but
most of the set was already fixed or tracked by the time the streak was noticed.

| Night | Failing legs | Cause | Status |
|---|---|---|---|
| 07-28 | 3 × `FileNotFoundError: dataset/…/data.fits` (autogalaxy/multi, autolens/imaging) | auto-simulate guards pointed at the wrong simulator | **FIXED** — see below |
| 07-30 | `interferometer/start_here.py` in **both** autolens and autogalaxy shards; `group/start_here.py` TIMEOUT | same OOM as 07-31, message eaten by the JAX traceback filter | **FIXED** — OOM `complete/2026/08/interferometer-start-here-integrate-oom.md`; filter `complete/2026/08/jax-traceback-filtering-release-harness.md` |
| 07-31 | `interferometer/start_here.py` → `RESOURCE_EXHAUSTED: Out of memory allocating 85898814480 bytes`; `delaunay.py` TIMEOUT | 48-start `MultiStartProdigy` vmapped unbatched; XLA hang | **FIXED** — autolens_workspace#450 (`batch_size=4`), discharged by run 30901054267; autolens_workspace_test#245 |
| 08-01 | `guides/modeling/advanced/hierarchical.py` TIMEOUT; `delaunay.py` TIMEOUT | Nautilus deadlock; XLA hang | hierarchical **FIXED** (PyAutoFit#1443); #245 |
| 08-03 | `graphical/ep.py` — "`log_likelihood_function` is always returning `nan`" | EP initializer | `draft/bug/autofit/graphical_ep_nan_likelihood_release_leg.md` |
| 08-04 | `guides/results/database/start_here.py` `IndexError` | `samples_weight_threshold` pruning | **FIXED + MERGED** 08-04 09:40 — autolens_workspace#465, autogalaxy_workspace#202 |

**The streak began with a self-inflicted regression.** Run 22 (07-27 05:52) was
the last success. `autolens_workspace 6f1a8b41` — "migrate 116 raw
auto-simulate guards to `should_simulate`" (#354) — merged 07-27 15:00, that
afternoon, and pointed guards at simulators that don't write the dataset the
script then loads. The 07-28 05:16 night is the first run after it, and it fails
exactly there. Both corrective fixes (`bb272a6a` #364 and autogalaxy_workspace
`f1ae4c3` #175) merged 07-28 12:37, ~7 hours too late for that night, and the
cluster never recurred. Nothing to file.

Only two of the six nights need new work, and both are now filed as drafts.

## Class B triaged — it is a flaky test, not a gate disagreement (2026-08-04)

The 08-02 failure resolves completely. PyAutoHands run 30736527569, job
`release_test_pypi (3.12, PyAutoLabs/PyAutoFit, main, PyAutoFit)`:

```
FAILED test_autofit/interpolator/test_covariance.py::test_variable_and_constant
E  assert 30.121646313498022 == 25.0 ± 5
====== 1 failed, 1641 passed, 2 skipped, 425 warnings in 70.32s ======
```

`test_variable_and_constant` (`test_autofit/interpolator/test_covariance.py:122`)
builds its samples from **unseeded** `np.random.random()` and asserts a fixed
`abs=5.0` tolerance. 30.12 against a 30.0 boundary is a marginal miss.

So the framing above — "either the gate's evidence is stale relative to what
`release.yml` actually runs, or the two disagree about what 'the libraries pass'
means" — is wrong, at least for 08-02. Neither. The gate was right and the
release run drew a different random sample. **This matters more than the fix:
it removes the evidence that was about to justify a gate-vs-release redesign.**
Filed as `draft/bug/autofit/covariance_interpolator_test_unseeded_rng.md`; a
seed would have shipped 2026.8.2.1. The 07-29 release run is no longer
resolvable through the API, so it stays unattributed — do not assume it was the
same cause.

## A second blocker item 2 masked (2026-08-04)

`verify_install_release` failed on **08-03 and 08-04**, alongside the script
failures. Item 2 read the `None verify_install` in the summary as a formatter
artifact. It was — but it was sitting on top of a genuinely failing leg, and
fixing the formatter without noticing that would have left a blocker invisible
for a second time.

Check D — `pip install "autolens[optional]==2026.8.4.1.dev70101"` on Python
3.13.14 — resolved **autofit 2026.4.30.582** and the retired **autoconf
2026.7.15.1**, then died on `class LatentGalaxy(af.Latent)` →
`AttributeError: module 'autofit' has no attribute 'Latent'`. That is exactly
the PyAutoLens#687 extras-backtracking failure, and the floors that fix it are
in source (PyAutoLens `c5381651c`, PyAutoGalaxy `07243338`, both 2026-08-03
19:01) — but the newest *published* autogalaxy at 08-04 05:15 was 2026.8.2.1,
built before them, so the chain still had a hole. The 2026.8.4.1 wheels released
later that day do carry the floors (verified on PyPI: `autofit>=2026.7.29.2`,
`autoarray>=2026.7.29.2`, `autogalaxy>=2026.7.29.2`).

**Prediction to check, not a conclusion: this should self-heal on the next
night.** If Check D fails again on 08-05, the floors are not the whole story and
this needs its own prompt.

## What is actually left

- `draft/bug/autofit/covariance_interpolator_test_unseeded_rng.md` — Class B
  root cause. Smallest and highest value: it alone unblocks a live release.
- ~~`draft/bug/autolens/interferometer_release_leg_oom.md`~~ — **closed out
  2026-08-27.** Its OOM had already shipped on 07-31 (autolens_workspace#450,
  `batch_size=4` on the 48-start `MultiStartProdigy`;
  `complete/2026/08/interferometer-start-here-integrate-oom.md`), so the prompt
  was retired to `complete/archive/shelved/`. The one live part of its 08-04
  amendment — the JAX traceback filter that ate the 07-30 message — shipped as
  PyAutoHeart#187 (`complete/2026/08/jax-traceback-filtering-release-harness.md`).
- `draft/bug/autofit/graphical_ep_nan_likelihood_release_leg.md` — new.
- autolens_workspace_test#245 (delaunay hang) — already tracked, no action here.
- Confirm on 08-05 that Check D self-healed and that PyAutoBrain#196 renders the
  night correctly.

Related open work referenced by the original item 3: PyAutoHands#161
(env-profile + validation-gate redesign), PyAutoHands#127 (nightly live releases
behind an activity gate). Note that the Class B finding weakens the case for
#161's validation-gate half — the gate was not wrong.

Do NOT convert this into a manual release drive — `AUTONOMY.md` forbids
converting a manual release into the scheduled-nightly exception, and
`active.md`'s `release-drive` entry records that a human drives releases via
`pyauto-brain release validate`.
