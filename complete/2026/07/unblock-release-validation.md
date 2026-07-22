# Unblock release validation — 4 PRs merged, all 5 shard failures cleared

Cleared every `workspace-validation` shard failure blocking `nightly-release` at
Stage 3 (integrate), and fixed the CI hang uncovered while doing it.

## Outcome

| PR | Change | Commit |
|---|---|---|
| autolens_workspace#315 | potential_correction release-env override + 2 SLOW-skips | `8231823` |
| autofit_workspace_test#63 | MultiStartResurrect basin-level assertion | `39aa27b` |
| autolens_workspace_test#197 | smoke per-script timeout + process-group kill | `e0fde3e` |
| autolens_workspace_test#195 | gallery_build permanent no_run entry | `34e2c2a` |

Issues: autolens_workspace#314 (closed), autolens_workspace_test#196 (open, follow-ups).

## Key findings

**None of the three "failures" was a library regression.** All were harness or
assertion faults:

1. `gallery_build.py` — a *build tool* run as a test. CI executes it standalone
   without `gallery_run.sh`, so `scan_images()` is empty and it takes its
   documented `sys.exit(1)`. Permanent (untagged) no_run entry, not SLOW/NEEDS_FIX,
   since there is nothing to fix.

2. `MultiStartResurrect.py` — `np.allclose` default `rtol=1e-5` demanded
   near-bitwise identity between the resurrect-on/off arms. One resurrection
   genuinely fires (`n_resurrections` 0 vs 1), consuming RNG draws, so the arms
   diverge at the 5th significant figure (max rel delta 3.2e-5). The docstring's
   invariant is *same basin*, which holds. Relaxed to `rtol=1e-3` (31x headroom;
   verified it still rejects a 1% shift and any basin move). The test still fires
   a resurrection afterwards, so it passes genuinely, not vacuously.

3. `potential_correction` x2 — the release profile sets `PYAUTO_SMALL_DATASETS: "1"`
   in `defaults:` for *every* script; the capped 15x15 grid starves the dpsi mesh
   and `PairRegularDpsiMesh(dpsi_factor=2)` correctly refuses. The pre-existing
   `"interferometer/start_here"` override does NOT cover these — their paths are
   `interferometer/features/potential_correction/...`, which that substring misses.
   Verified fails-with-cap / passes-without; 77s and 127s against the 1800s cap.

**The CI hang (#196) — cause was mundane, and my first diagnosis was wrong.**
Smoke CI had been hitting the 6-hour Actions ceiling since ~Jul 19 (0 hangs in the
74 runs before; 10 of 12 on Jul 21). I first blamed `point_source/point.py` because
it was the last `::group::` opened in a hung log — but groups print *before* the
script runs, so that marks only where output stopped. With honest reporting,
`point.py` passes in ~30s.

The real cause: `run_smoke.py` had **no per-script timeout**, and
`jax_likelihood_functions/multi/shared_preloads.py` — already SLOW-marked in
`no_run.yaml` for flaking at the release runner's 1800s cap — was being run by the
*fast* PR gate unbounded, because `run_smoke.py` never read `no_run.yaml`. No cap
plus no skip = unbounded. Consequence: only 6 of 20 scripts ever ran on a hung run,
so green history on this repo was weaker evidence than it appeared.

## Traps recorded

- **`::group::` marks where output stopped, not which script hung.** It is printed
  before execution. Different hung runs stalled at different scripts.
- **`killpg` leaves returncode -9 when the child itself is slow.** My first patch
  mapped only `None`/`0` to 124, so CI reported `FAIL (exit -9)` instead of
  `TIMEOUT`. The local repro missed it because there the child had already exited 0
  and only the grandchild was alive — the branch was never exercised.
- **Do NOT make `run_smoke.py` honour `no_run.yaml` wholesale.** Those SLOW markers
  are calibrated against the *release* profile (1800s, real samplers); smoke runs
  `PYAUTO_TEST_MODE=2`. Two of three overlapping entries pass in ~20-25s there, so
  honouring it wholesale drops working coverage to fix one script.
- **The Feature Agent misclassified this** as `too-large`/`research-first` (score 11)
  and resolved `(none)` repos — a length+keyword heuristic on an evidence-heavy
  prompt, plus an inability to resolve repos when the target is a category
  (`health_fixes`) and repos appear in a table rather than as `@RepoName`.
- **`clean_slate.sh` deletes the tracked `autolens_workspace_test/output/.gitignore`.**

## Follow-ups (open in #196)

1. Make `multi/shared_preloads.py` fast enough to re-enable, or confirm it is
   permanently release-profile-only (PyAutoHeart#74).
2. Isolate the local-vs-CI likelihood disagreement on `point.py` (local `16.131`
   vs CI/expected `-83.380` on repo-`main` libraries). One environment is wrong.
3. **Centralise `run_smoke.py`** — duplicated across 10 repos in 3 variants; the
   other 9 copies still have NO timeout, so the same 6-hour hang is possible in
   every other workspace repo. Move it into PyAutoHands beside `env_config.py`.
4. Profile the two SLOW-skipped scripts (`cluster/start_here.py`,
   `weak/features/strong_lensing/a2744.py`) and remove their markers.

## Original prompt

# Unblock release validation — 3 workspace-validation failures, none a library bug

Type: bug
Target: health_fixes
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

Clear the three non-timeout `workspace-validation` shard failures that are
blocking `nightly-release` at Stage 3 (integrate), plus SLOW-skip the two
1800s timeouts, so release validation can reach green.

## Original Request

"ok, lets begin doing one task after another in a logical order, happy to start
with what you think makes sense"

(from the `/wake_up` digest of 2026-07-22, which surfaced Heart RED score 40,
`release validation FAILED (stage integrate)`, and nightly-release failing three
nights running — 20th, 21st, 22nd.)

## Context

`nightly-release` (PyAutoBrain) stops at Stage 3 and delegates to
`workspace-validation` (PyAutoHeart, run 29912642195), which fails 5 shards.
Each was reproduced locally on 2026-07-22. **None is a library regression** and
none needs a source edit.

### 1. `autolens_test/gallery` — `scripts/gallery/gallery_build.py`

Fails in **0.1s** with exit 1. The CI shard runs `gallery_build.py` in isolation,
without `scripts/gallery/gallery_run.sh` having produced any images first, so
`scan_images()` returns empty and the script takes its documented early exit:

```
No images found under scripts/*/images — run scripts/gallery/gallery_run.sh first.
sys.exit(1)                                       # gallery_build.py:159-163
```

Runs clean locally where images exist (9 domains, 69 png / 20 fits).

**This is a build tool, not a test script** — it has no place in the validated
script set. Fix: a *permanent* (untagged) entry in
`autolens_workspace_test/config/build/no_run.yaml`. Not SLOW, not NEEDS_FIX —
those are to-do markers, and this is correct-by-design behaviour.

### 2. `autofit_test/searches` — `scripts/searches/MultiStartResurrect.py`

```
AssertionError: (array([50.15617779, 25.19690032,  9.85848878]),
                 array([50.1559837 , 25.19609623,  9.85839795]))
```

Reproduced locally and **deterministic**. The script's own output explains it:

```
resurrect=False: centre=50.156, normalization=25.197, sigma=9.858  (n_resurrections=0)
resurrect=True : centre=50.156, normalization=25.196, sigma=9.858  (n_resurrections=1)
```

One resurrection fires on the `resurrect=True` arm. A resurrection redraws
params from the start band and reinitialises that start's optimizer state,
consuming RNG draws — so the two arms' streams diverge and the converged MAPs
differ in the **5th significant figure** (max relative delta 3.2e-5, on
`normalization`).

The failing assertion is `np.allclose(off, on)` (line 112), whose default
`rtol=1e-5` demands near-bitwise identity. That is **stricter than the property
the script documents**. From its own module docstring:

> "Resurrection may fire incidentally (a broad start drawn onto the measure-zero
> `sigma≈0` non-finite point is redrawn), but it must never move the winning
> basin — `resurrect` on and off recover the identical MAP."

The invariant is *same basin*, and it holds: the two arms agree to 5 sig figs,
while the truth-recovery asserts immediately above (lines 104-106) allow ±2.0,
±3.0, ±2.0. The safety property is satisfied; only its encoding is wrong.

Fix: give line 112 a basin-level tolerance (`rtol=1e-3`, still ~4 sig figs and
~30x tighter than any plausible basin width) with a comment naming *why* exact
equality cannot hold once a resurrection fires. This is **not** masking a
regression — the library behaves exactly as designed; the assertion mis-states
the design.

### 3. `autolens/interferometer` — `potential_correction/{start_here,likelihood_function}.py`

```
ValueError: The dpsi grid is too sparse. Try decreasing the dpsi_factor to smaller values.
  autolens/potential_correction/mesh.py:132, via al.pc.PairRegularDpsiMesh(..., dpsi_factor=2)
```

`autolens_workspace/config/build/env_vars_release.yaml` sets, in `defaults:`
(i.e. for *every* script):

```yaml
PYAUTO_SMALL_DATASETS: "1"   # cap grids/masks to 15x15, reduce MGE gaussians
```

with no `overrides:` entry for potential_correction. The capped 15x15 grid makes
the derived dpsi mesh too sparse for `dpsi_factor=2`, and the mesh constructor
correctly refuses.

Verified both ways locally:

| Env | Result |
|---|---|
| `PYAUTO_TEST_MODE=1 PYAUTO_SMALL_DATASETS=1 PYAUTO_FAST_PLOTS=1` | **FAIL** — ValueError, as CI |
| `PYAUTO_TEST_MODE=1 PYAUTO_FAST_PLOTS=1` (no cap) | **PASS** |

Uncapped `start_here.py` runs in **58s** (log evidence −6.0333e+03; dkappa
correlation 0.832, peak offset 0.14", 6.2σ) — comfortably inside the 1800s
mode=release cap, so dropping the cap for these two costs nothing.
`likelihood_function.py` likewise passes, with sparse- and dense-route log
evidences agreeing exactly (1.64164478e+03).

This is the same failure shape as the FAST_PLOTS false alarms in
`viz-refactor-asserts #187`: an env-profile gap presenting as a library bug.

Fix: an `overrides:` block in `env_vars_release.yaml` unsetting
`PYAUTO_SMALL_DATASETS` for `interferometer/features/potential_correction/`.

### 4+5. The two 1800s timeouts (user-approved: SLOW-skip now, investigate after)

- `autolens/cluster` — `scripts/cluster/start_here.py` TIMEOUT (1800s)
- `autolens/weak` — `scripts/weak/features/strong_lensing/a2744.py` TIMEOUT (1800s)

Both sit at the full cap. Every other script in both shards passes (cluster's
next-slowest is `lenstool/modeling.py` at 137.8s; weak's is `modeling.py` at
23.6s), so this is these two scripts specifically, not a shard-wide problem.
Consistent with the standing note that cluster scripts are not smoke-able
(>500s even in TEST_MODE).

Fix now: `# SLOW 2026-07-22` entries in `autolens_workspace/config/build/no_run.yaml`.
SLOW markers are surfaced with a loud warning banner on every mega-run, so they
remain a visible to-do rather than a silent permanent skip. Root-cause profiling
is deliberately deferred to a follow-up.

## Scope

Three repos, workspace-only, no library edits:

| Repo | Change |
|---|---|
| `autolens_workspace_test` | 1 permanent `no_run.yaml` entry (gallery_build) |
| `autofit_workspace_test` | 1 assertion tolerance + comment (MultiStartResurrect.py:112) |
| `autolens_workspace` | `env_vars_release.yaml` override (potential_correction) + 2 SLOW `no_run.yaml` entries |

## Acceptance

- All five shards pass, or are legitimately skipped, under the `release` profile.
- `MultiStartResurrect.py` still fails if the winning basin genuinely moves
  (tolerance stays far tighter than the basin-recovery asserts).
- The potential_correction override is scoped to those scripts only — the
  blanket `PYAUTO_SMALL_DATASETS` default is unchanged for every other script.
- Both SLOW entries carry a dated reason and surface in the mega-run banner.

## Follow-up (not this task)

Profile `cluster/start_here.py` and `weak/features/strong_lensing/a2744.py` and
remove their SLOW markers.
