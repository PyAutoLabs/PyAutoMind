# Fix JIT quick-update visualization output regressions

Type: bug
Target: health_fixes
Themes:
- visualization
- jax-compile
- release
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-07-06 (backfilled from git)
Issued: 2026-09-15

## 2026-08-09 — EVERY SCRIPT PATH BELOW IS STALE (they moved, they were not deleted)

Checked by the draft/ sweep. All 4 scripts named in § Scripts return **404** at the
paths written below, and **all 4 still exist** under a renamed layout. Do not read the
404s as "the scripts were deleted" or "this was fixed by removal".

Two systematic renames landed in both test workspaces since this prompt was filed:

```
scripts/jax_likelihood_functions/<dataset>/X.py  ->  scripts/<dataset>/jax_likelihood/X.py
scripts/<dataset>/modeling_visualization_jit.py  ->  scripts/<dataset>/visualization/modeling_visualization_jit.py
scripts/multi/...                                ->  scripts/multi_dataset/...
```

Verified in `autolens_workspace_test` (`4cea3f8c`, cloned) and
`autogalaxy_workspace_test` (raw, every path resolves 200). This is the **same rename
family** that cost a previous session time on
`draft/bug/autolens/jax_point_source_point_smoke_sentinel.md` — treat a 404 in this
cluster as path drift until proven otherwise.

Corrected paths:

| named in § Scripts | actual path on main | repo |
|---|---|---|
| `…/scripts/ellipse/modeling_visualization_jit.py` | `scripts/ellipse/visualization/modeling_visualization_jit.py` | autogalaxy_workspace_test |
| `…/scripts/imaging/modeling_visualization_jit.py` | `scripts/imaging/visualization/modeling_visualization_jit.py` | autogalaxy_workspace_test |
| `…/scripts/interferometer/modeling_visualization_jit.py` | `scripts/interferometer/visualization/modeling_visualization_jit.py` | autogalaxy_workspace_test |
| `…/scripts/point_source/modeling_visualization_jit.py` | `scripts/point_source/visualization/modeling_visualization_jit.py` | autolens_workspace_test |

### Parking state — read before assuming CI still exercises these

**1 of the 4 is parked.** `autolens_workspace_test` `config/build/no_run.yaml:30`:
`point_source/visualization/modeling_visualization_jit # SLOW 2026-07-08 - JIT + Part-2
live Nautilus fit exceeds 300s cap`. The three `autogalaxy_workspace_test` scripts are
**not** parked and should still be running.

Adjacent and worth knowing: `autolens_workspace_test` also parks its *own*
`imaging/visualization/modeling_visualization_jit` (SLOW 2026-07-30, "re-measured: times
out at the 300s cap") and `interferometer/visualization/modeling_visualization_jit`
(SLOW 2026-07-30, "local re-measurement OOM-killed"). Those two are not named in this
prompt but are the same script family, so the timeout problem is broader than the four
listed here.

**This changes what the prompt's premise means.** A parked script cannot fail in
release validation, so the 2026-08-07 release drive's Stage 3 result (51/51 jobs green,
`657p/0f/101s/0t` — note the **101 skips**) is *not* evidence these were fixed. Nothing
here is graded shipped; the failures are simply no longer being provoked. Note too that
the parkings are for **timeouts**, a different failure from the defect this prompt
describes — so unparking is a precondition for reproducing it at all.

Not re-graded here: whether the underlying defect still reproduces. That needs real
runs, which a cloud session cannot do.

---
## Context

Four test-workspace scripts expect real release-profile searches to invoke the JIT-cached
quick-update visualization path and produce fit images. CI reported missing files. Local
`main` still fails the ellipse, interferometer, and point-source cases, while imaging
passes.

Owners: @PyAutoFit, @PyAutoGalaxy, @PyAutoLens, @autogalaxy_workspace_test, and
@autolens_workspace_test.

## Scripts

- `autogalaxy_workspace_test/scripts/ellipse/modeling_visualization_jit.py`
- `autogalaxy_workspace_test/scripts/imaging/modeling_visualization_jit.py`
- `autogalaxy_workspace_test/scripts/interferometer/modeling_visualization_jit.py`
- `autolens_workspace_test/scripts/point_source/modeling_visualization_jit.py`

## Required work

1. Reproduce from clean output directories with JAX enabled and real release-profile
   searches.
2. Trace search update cadence, visualization dispatch, cached fit creation, output-path
   routing, and exception handling for all four dataset types.
3. Fix the shared library path where possible; do not add sleeps, weaken assertions, or
   fabricate image files in scripts.
4. Add focused tests proving quick updates invoke visualization and write the expected
   artifact for ellipse, imaging, interferometer, and point-source analyses.
5. Run owning-library tests and all four scripts under the release profile.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## 2026-08-21 — REPRODUCTION GATE RUN: **4/4 PASS — prompt refuted**

Method (identical to the gate that closed the sibling `autofit_sampler_database`, PyAutoFit#1508):
every script run from a **cleared** `output/`, under its workspace's
`config/build/profile_release.yaml`, env resolved by `autohands.env_config.build_env_for_script`
at workspace CWD, 1800s `mode=release` cap. Libraries at `main`: PyAutoFit `248ca971f`,
PyAutoArray `b808a9b1`, PyAutoGalaxy `7e3856dd`, PyAutoLens `d8f6bb3df`, PyAutoNerves `f6d6d52`.
Three workspace checkouts were **behind `origin/main`** and were synced first.

| Script (resolved path) | Result | Secs |
|---|---|--:|
| `autogalaxy_workspace_test` `imaging/visualization/modeling_visualization_jit.py` | PASS | 67 |
| `autogalaxy_workspace_test` `ellipse/visualization/modeling_visualization_jit.py` | PASS | 45 |
| `autogalaxy_workspace_test` `interferometer/visualization/modeling_visualization_jit.py` | PASS | 71 |
| `autolens_workspace_test` `point_source/visualization/modeling_visualization_jit.py` *(parked)* | PASS | 168 |

The prompt's Context says "local `main` still fails the ellipse, interferometer, and point-source
cases, while imaging passes." **All four now pass**, each writing its image and saying so:

```
fit.png files produced: 1
  output/scripts/imaging/images/modeling_visualization_jit/mge_linear/.../image/fit.png
First call (compile + run): 5.239s     Second call (cached): 0.270s
PASS: jit-cached fit_for_visualization fires during Nautilus quick updates …
```

The scripts' own `assert len(produced_pngs) > 0` and JIT-cache assertion
(`cached < 0.5 x compile`) both held — the latter with ~19x margin.

**Correction to the 2026-08-09 sweep note above:** it says ellipse + interferometer are parked in
`autogalaxy_workspace_test`. Driving the real matcher (`autohands.build_util.should_skip`) over
each repo's `no_run.yaml` shows **all three `autogalaxy_workspace_test` visualization scripts are
LIVE**; the parked one is `autolens_workspace_test` `point_source/visualization`. Two repos were
conflated.

**That parking IS stale.** Its note claims a deterministic `SLOW 2026-07-08 — exceeds 300s cap`;
it ran in **168s**. Unlike the jax_likelihood parkings, this one is not described as intermittent,
so it is a genuine unpark candidate.

### Script-path corrections (three renames, verified on disk 2026-08-21)

The tables in this folder have drifted **again** since the 2026-08-09 sweep. All paths resolve;
a 404 here still means drift, never deletion.

- `scripts/jax_likelihood_functions/<dataset>/X.py` -> `scripts/<dataset>/jax_likelihood/X.py`
- `scripts/<dataset>/modeling_visualization_jit.py` -> `scripts/<dataset>/visualization/modeling_visualization_jit.py`
- `scripts/multi/...` -> `scripts/multi_dataset/...`  (this one bit `slam/simultaneous.py`, still
  listed under `multi/` above)
- `double_einstein_ring` -> `double_source_plane_lens`  (autolens_workspace#394) — so
  `imaging/features/advanced/double_einstein_ring/chaining.py` is now
  `imaging/features/advanced/double_source_plane_lens/chaining.py`

## 2026-09-15 — GATE RE-RUN: **4/4 PASS again** — defect refuted a second time

Same method as the 2026-08-21 gate: every script from a **cleared** `output/` (moved aside, restored
afterwards), under its workspace's `config/build/profile_release.yaml`, env resolved by the real
harness (`autohands.env_config.build_env_for_script`, workspace CWD), `timeout 1800`, `mode=release`.
All repos on `main`, clean:

| Repo | SHA | vs 2026-08-21 gate |
|---|---|---|
| PyAutoFit | `27d41e7c8` | +186 commits |
| PyAutoArray | `5e2bc0f4` | +120 |
| PyAutoGalaxy | `840ffde0` | +67 |
| PyAutoLens | `ccf9295f3` | +58 |
| PyAutoNerves | `fac8b17` | moved |
| autogalaxy_workspace_test | `2102699` | — |
| autolens_workspace_test | `3079994` | — |

| Script | Result | Secs (08-21) | image | compile → cached |
|---|---|--:|---|---|
| `autogalaxy_workspace_test` `imaging/visualization/modeling_visualization_jit.py` | PASS | 68 (67) | `fit.png` ×1 | 8.95 s → 0.49 s (18x) |
| `autogalaxy_workspace_test` `ellipse/visualization/modeling_visualization_jit.py` | PASS | 46 (45) | `fit_ellipse.png` ×1 | 2.49 s → 0.05 s (54x) |
| `autogalaxy_workspace_test` `interferometer/visualization/modeling_visualization_jit.py` | PASS | 53 (71) | `fit.png` ×1 | 4.94 s → 0.26 s (19x) |
| `autolens_workspace_test` `point_source/visualization/modeling_visualization_jit.py` *(parked)* | PASS | **202** (168) | `fit.png` ×1 | 23.6 s → 2.99 s (7.9x) |

Every script printed its own final `PASS:` line; `assert len(produced_pngs) > 0` and the JIT-cache
assertion (`cached < 0.5 x compile`) both held. No `Fit Already Completed` (all four logged `Starting
new Nautilus non-linear search (no previous samples found)`), no traceback, no OOM, no timeout.

**Resolved env, verified rather than assumed:** all four scripts carry an in-file `ENV:` declaration
(`real_output`; point_source also `full_datasets`) and it is honoured — applied last, after profile
defaults and `derive_jax_markers` — so the resolved env has **no** `PYAUTO_TEST_MODE`,
`PYAUTO_DISABLE_JAX`, `PYAUTO_SMALL_DATASETS` or `PYAUTO_FAST_PLOTS` (absent == real). Only
`PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1` is set; `JAX_ENABLE_X64=True`,
`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`, `JAX_TRACEBACK_FILTERING=off`.

**Trap:** the ellipse script asserts on **`fit_ellipse.png`**, not `fit.png` — a bare
`find -name fit.png` returns 0 there and mis-reads as a failure.

**Point-source parking (`autolens_workspace_test/config/build/no_run.yaml:30`, "SLOW 2026-07-08 —
exceeds 300s cap"):** 202 s is under the cap, so the deterministic claim still does not reproduce —
but it is 20 % slower than August's 168 s, leaving ~33 % headroom on this machine. A CI runner could
plausibly cross 300 s. Per the 2026-08-24 retime convention (autolens_workspace_test#274, `783a6ff`),
a SLOW marker is rewritten or deleted **only on a CI measurement** — this entry was not in that
sweep.

**New incidental defect (not this prompt's, filed separately):** ellipse and point_source both logged
`Visualization warm-up failed (non-fatal); first quick update may be slow.` —
`PyAutoFit/autofit/non_linear/fitness.py:327-333` `_warmup_visualization` swallows the exception with
a bare `except Exception` and logs no reason. Imaging and interferometer warm up fine. Consistent with
point_source's weakest cache ratio (7.9x) and its 7.4 s first quick update vs 2.8 s later ones. Also
seen twice in point_source: `lens_calc.py:565 LensCalc Hessian: 1 of 625 points did not converge
after 20 halvings (largest relative error estimate 2.58e+00); values kept`.
→ `draft/bug/autofit/visualization_warmup_swallowed_exception.md`.

## Plan (2026-09-15) — DEFERRED, NOT STARTED

Issued and registered in `active.md` on 2026-09-15 at the human's request so the task is visible as
in flight; **no worktree, no branch, no code change exists yet**. Resume with `/start_workspace`.

**Verdict.** The defect this prompt describes does not exist on current `main` (two gates, 8/8 passes,
libraries moved 58–186 commits between them). `pyauto-brain bug` still returns
`combined / library source / too-large (21)` because it reads the stale Context above at face value;
that classification is overridden. The only code change is one line of
`autolens_workspace_test/config/build/no_run.yaml`. Classification: **workspace**, small, owner
**autolens_workspace_test**. Close-out mirrors the siblings `autofit_sampler_database` (PyAutoFit#1508)
and `numerical_inversion_failures` (PyAutoArray#467): no library fix, record states "no defect
exists to fix".

**Steps when resumed**

1. `/start_workspace` → worktree `~/Code/PyAutoLabs-wt/jit-visualization-outputs/`, branch
   `feature/jit-visualization-outputs` on `autolens_workspace_test`; push the empty branch.
2. Dispatch the CI retime and wait in the foreground (`gh run watch`; no timers armed):
   ```
   gh workflow run retime.yml -R PyAutoLabs/autolens_workspace_test \
     --ref feature/jit-visualization-outputs \
     -f scripts=point_source/visualization/modeling_visualization_jit.py -f repeats=5 -f script-timeout=300
   ```
   Read the 5 wall times from the run.
3. Edit `no_run.yaml:30` **from the measurement**:
   - all 5 < 300 s → delete the entry (unpark);
   - any ≥ 300 s → keep parked, rewrite the marker as
     `# SLOW <date> - retime <run-id>: k/5 over 300s cap (min–max s); 202 s local; the 2026-07-08
     "deterministic" claim was wrong, cap margin is the real reason`.
   No script edits, no assertion changes, no sleeps, no fabricated images (Required work rule 3 holds).
4. `ship_workspace`: commit, push, smoke, PR with `## Scripts Changed` = the one line and the retime
   run-id + timings in the body. Library-first gate is vacuous (no library PR).
5. `/prm` when green: `complete/2026/09/jit-visualization-outputs.md` in the sibling record format
   ("no defect exists to fix; one parking settled by CI measurement"), `health_fixes/README.md` row
   struck through and pointed at the record, prompt retired from `draft/`.
6. Out of scope: the `imaging/…` and `interferometer/visualization/modeling_visualization_jit`
   parkings in `autolens_workspace_test` (SLOW 2026-07-30, not this prompt's scripts) — a retime-sweep
   follow-up, noted on the issue.

**Verification when resumed:** retime run green with 5 timings quoted in PR and record;
`autohands.build_util.should_skip` over the edited `no_run.yaml` matches the branch taken (LIVE or
still parked); Smoke Tests green on the PR — if unparked and it TIMEOUTs there, re-park with the
measured note only; `lifecycle.py check` / `issues` show no DRIFT after close-out.

Gate artefacts (session scratchpad, not committed): `repro-{1..4}-*.log`, `env-{1..4}.json`.
