# Bug: fix the tracer.fits existence guard in autolens_workspace imaging modeling.py

Type: bug
Target: workspaces
Repos:
- autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Filed: 2026-08-22 (backfilled from git)

Bug: fix the tracer.fits existence guard in autolens_workspace imaging modeling.py. The script crashes with FileNotFoundError because the guard checks the wrong file. It tests whether files/tracer.json exists, then reads image/tracer.fits, which TEST_MODE never writes. This fails the release smoke gate.


## Evidence (2026-08-23, gathered during the 2026.8.23.1 release)

`autolens_workspace/scripts/imaging/modeling.py:641`. The guard and the read
name **different files**:

```python
if (result_path / "files" / "tracer.json").exists():
    tracer = from_json(file_path=result_path / "files" / "tracer.json")

    tracer_fits = al.Array2D.from_fits(
        file_path=result_path / "image" / "tracer.fits", hdu=0, pixel_scales=0.1
    )
```

Under TEST_MODE the search is reduced, so `files/tracer.json` IS written but the
visualisation output `image/tracer.fits` is not. The guard passes and the read
raises:

```
FileNotFoundError: .../output/test_mode/imaging/simple/modeling/<id>/image/tracer.fits
FAIL: imaging/modeling.py
```

- Present since `cfd5334c` (2026-04-14); the script is untouched since 2026-08-04,
  so this is long-standing, not a regression from the regime-stamp release.
- **TEST_MODE-specific.** The same script passes at release fidelity — Heart's
  Stage 3 integrate ran `run_scripts (3.12, autolens, imaging)` green
  (672p/0f), because a full-fidelity fit does write `tracer.fits`.
- Reproduced in PyAutoHands `release.yml` run 32542888112, job
  `run_smoke_tests (3.12, autolens_workspace)`.

## Why it matters (and why it is NOT urgent)

It does not block releases: the `release` job's `needs:` is
`[resolve_mode, release_test_pypi, version_number]` and excludes
`run_smoke_tests`, so the publish succeeds regardless — run 32542888112 is marked
`failure` yet published 2026.8.22.1. The real cost is that it leaves the smoke
gate permanently red, so a genuine workspace regression would look identical to
this known failure and be ignored.

## Traps

- Do **not** "fix" this by deleting the result-loading block. It is a documented
  teaching section, and `draft/maintenance/workspaces/read_through_issues.md`
  separately asks for the equivalent section to be **added** to the other
  `modeling.py` examples (group, cluster, interferometer). Coordinate with that
  prompt — whatever guard shape is chosen here should be the one propagated
  there, or the same bug ships to four more scripts.
- Guarding on `image/tracer.fits` alone would silently skip the `tracer.json`
  load in test mode. Prefer guarding each read on the file it actually reads.

<!-- formalised by the Intake (Conception) Agent on 2026-08-22 from user-intake -->
