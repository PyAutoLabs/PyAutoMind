- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/512 (CLOSED)
- completed: 2026-08-29
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/513 (merged b59229be -> main)
- repos: autolens_workspace
- bundle: ci-smoke — bundle 2 (shared worktree ci-smoke-bundle-2; own issue/branch/PR)
- summary: Removed the `NEEDS_FIX 2026-07-30` park for `imaging/features/scaling_relation/slam` from `config/build/no_run.yaml` (one-line deletion). Cause was PyAutoArray#430 (loader kept uncapped pixel_scales for at-or-below-cap data), fixed by PR#431 (merged 2026-08-03, released 2026.8.7.1). Verified on a cleared tree (output/, output/test_mode/, dataset/imaging/scaling_relation removed) through the CI runner under the capped smoke profile: exit 0 in 25 s, 6 searches genuinely ran (lens_light[1], source_lp[1], source_pix[1], source_pix[2], light[1], mass_total[1]), re-measured anchor luminosity 22.47 (the value that was 0.0), 0 "Fit Already Completed". CI green (Smoke Tests py3.12/3.13, Navigator Check, Script Size Guard).
- not legacy (checked at plan time): the park targets the current BGC-anchored slam.py (rewritten 2026-07-30 dfcda873, fixed 2026-08-24 1effab6d #501); the prompt's second half (rewrite the multi_galaxy sibling's reason) had already been done on 2026-08-24.
- left alone, deliberately: `multi_galaxy/features/scaling_relation/slam` stays parked until a capped run of THAT script exits 0; `interferometer/…` unaffected; the script is not in the curated `smoke_tests.txt` (only modeling.py is) — it is now in scope for the discovery-based Workspace Smoke leg; adding it to the curated list is a separate decision.
- trap: `autohands/run_python.py --report-dir` pipes script stdout and surfaces it only on failure — a passing CI-form run gives a 3-line log; run once more without `--report-dir` for grep-able evidence.
- heart-ack: shipped/merged under human-acknowledged YELLOW (2026-08-29) — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source" — unrelated to this change.

## Original prompt

# Un-park imaging/features/scaling_relation/slam — the PyAutoArray#431 gate has cleared

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci-smoke
- notebooks
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised — ready to start (upstream gate cleared 2026-08-03)
Was-blocked-by: PyAutoArray#431   # small-datasets loader fix — cleared, see below
Issued: 2026-08-29
Filed: 2026-08-03 (backfilled from git)

**Ready to start.** This prompt was filed as a gated task and its gate is long
since open — both clauses were verified by the 2026-08-09 sweep below and again
on 2026-08-25 against the Mind's own records:

- **Merged** — `complete/2026/08/small-datasets-loader-pixel-scales.md` records
  PyAutoArray PR#431 merged (`17885f38`) on 2026-08-03, closing issue #430.
- **Reached the installed stack** — `complete/2026/08/release-drive-2026-08-07.md`
  records all five libraries published to PyPI at **2026.8.7.1**, verified against
  pypi.org rather than the run conclusion.

The title and opening previously read "once PyAutoArray#431 merges" / "BLOCKED
until…", which is what the dashboard rendered for three weeks after the gate
opened — actionable work presented as waiting on something. The work itself is
unchanged and still outstanding: the park is still in `no_run.yaml`.

## 2026-08-09 — UNBLOCKED, both clauses satisfied

Checked by the draft/ sweep. This gate has two conditions and **both** are met:

1. **Merged** — PyAutoArray#431 merged `2026-08-03T18:03:14Z` (`5006f347`, "fix:
   relabel at-or-below-cap data at the capped pixel scale", fixes #430).
2. **Reached the installed stack** — #431 carried the `pending-release` label, and
   the 2026-08-07 release drive published all five libraries to PyPI at
   **2026.8.7.1** with PyAutoArray at `828d5c13`, downstream of the merge. So the
   loader fix is in a released wheel, not just on `main`. (See `active.md`
   § release-drive-2026-08-07.)

**The park is still in place**, so the work is genuinely outstanding:
`autolens_workspace/config/build/no_run.yaml:46` still carries
`imaging/features/scaling_relation/slam # NEEDS_FIX 2026-07-30 - measures its
luminosities from a preceding light stage…`.

#431's own test plan states the outcome directly: *"`imaging/features/scaling_relation/slam`
→ now exit 0 (6 real searches). Its `NEEDS_FIX` park in
`autolens_workspace/config/build/no_run.yaml` can be removed in a separate
workspace PR."* This prompt is that PR.

**Do not also unpark the `multi_galaxy/` sibling** at line 48. The same test plan
records that it gets past the 0.0-luminosity cause but then hits a separate latent
script bug — `slam.py:863` computing `image_half_width` from a hardcoded
`pixel_scale` while the mask uses `dataset_full.pixel_scales`. That is
`draft/bug/autolens_workspace/script_local_pixel_scale_vs_dataset_pixel_scales.md`,
confirmed still unfixed on main by this sweep. It stays parked.

## What

Remove this NEEDS_FIX line from `autolens_workspace/config/build/no_run.yaml`:

    - imaging/features/scaling_relation/slam # NEEDS_FIX 2026-07-30 - measures its
      luminosities from a preceding light stage, which under PYAUTO_TEST_MODE returns
      no usable samples, so every measured luminosity is 0.0 ...

## Why

The park's stated cause was never the script's fault. Root cause was
`cap_array_2d_for_small_datasets` keeping the caller's uncapped `pixel_scales` for
at-or-below-cap data, mislabelling the frame 6x so off-centre galaxies fell outside
it and their non-negative linear intensity solve correctly returned 0.0
(PyAutoArray#430, fixed by PR#431).

Measured 2026-08-03 against the fix, capped smoke profile, cleared dataset + output:
`scripts/imaging/features/scaling_relation/slam.py` → **exit 0**, 6 searches genuinely
run, 0 cached resumes, no `luminosity_from` raise.

## Do NOT also un-park the sibling

`multi_galaxy/features/scaling_relation/slam` must STAY parked. It clears the
0.0-luminosity cause with the same fix but then fails on a separate latent bug
(`slam.py:863` mixes the script's hardcoded `pixel_scale` with the dataset's
corrected `pixel_scales`, producing an empty mask). See
`draft/bug/autolens_workspace/script_local_pixel_scale_vs_dataset_pixel_scales.md`.
Its NEEDS_FIX reason should be UPDATED to name the real remaining cause rather than
the 0.0-luminosity one, which will no longer be true.

`interferometer/features/scaling_relation/slam` is unaffected and already runnable —
it hardcodes `luminosity_anchor` instead of measuring it. Leave it alone.

## Verify before removing

Re-run the script under the capped smoke profile with the merged loader fix and
confirm exit 0. Clear `output/test_mode/<path>` as well as `output/<path>` — output is
namespaced under `output/test_mode/` in test mode, and a stale tree reads as a pass
via "Fit Already Completed".
