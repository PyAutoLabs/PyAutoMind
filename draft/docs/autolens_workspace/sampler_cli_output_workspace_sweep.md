# Phase 2 — drop the hand-written quick-update sentence from the workspace scripts

Blocked-by: PyAutoFit#1436     # moved the cadence message into the library — MERGED 2026-07-30
Filed: 2026-07-30 (backfilled from git)
Themes:
- samplers
- notebooks

Follow-up to **PyAutoFit#1434 / PR#1436**, which moved the on-the-fly update
cadence message into the library. Do not start until #1436 has merged.

## 2026-08-09 — UNBLOCKED, and the counts refreshed

Checked by the draft/ sweep. **PyAutoFit#1436 merged 2026-07-30T21:49:25Z**
(`daa0dbcb`, closes #1434), so the gate above is satisfied — this is ready to
start, not waiting. Nothing here has shipped.

Counts re-measured against autolens_workspace main (`9974f891`), which sharpens
the table below (it estimated "14+"):

| surface | count |
|---|--:|
| `.py` scripts still printing `On-the-fly updates every iterations_per_quick_update` | **19** |
| of those, still carrying the "notebook cell **with** progress" typo | **16** |
| `.ipynb` notebooks carrying the line | **54** |

The notebook count is much larger than the script count because the line also
appears in generated notebooks across sibling directories — confirm whether those
are all regenerated from the 19 scripts, or whether some notebooks are authored
directly, before assuming a regeneration pass covers them.

For what the library now emits in its place, see PyAutoFit#1436's own summary: the
message has two branches, because the packaged default cadence is the inf-like
`1e99` never-sentinel, so the replacement text is either a real integer cadence or
a statement that updates are disabled naming the config key.

## Problem

23 workspace scripts print this block before `search.fit(...)`:

```python
print(
    """
    The non-linear search has begun running.

    This Jupyter notebook cell with progress once the search has completed - this could take a few minutes!

    On-the-fly updates every iterations_per_quick_update are printed to the notebook.
    """
)
```

The last line printed the literal name of the config knob. As of PyAutoFit#1436
the library logs the real cadence itself at search start
(`AbstractSearch.quick_update_message`, logged in `fit()`), so this sentence is
now both wrong *and* duplicated — and the library's version is the one that
states the actual number.

## Task

In each of the 23 `.py` scripts:

1. Delete the `On-the-fly updates every iterations_per_quick_update ...` line
   from the `print()` block. The library now emits this.
2. While in the same block, fix the typo present in several copies:
   "This Jupyter notebook cell **with** progress" → "**will** progress".
   (Some copies already say "will"; some use an em-dash rather than a hyphen —
   leave those punctuation differences alone, only fix the verb.)

Then regenerate the 23 `.ipynb` and 14 `.md` counterparts.

## Repos and counts

| Repo | scripts |
|------|---------|
| `autolens_workspace` | 14+ |
| `autogalaxy_workspace` | 3+ |
| `HowToLens` | 1 |

Find them all with:

```bash
grep -rln "On-the-fly updates every iterations_per_quick_update" --include=*.py .
```

Representative paths:

- `autolens_workspace/scripts/imaging/start_here.py:343`
- `autogalaxy_workspace/scripts/interferometer/start_here.py:327`
- `HowToLens/scripts/chapter_2_lens_modeling/tutorial_1_non_linear_search.py:416`

## Gotchas

- Regeneration: `generate.py` needs the repo as CWD and the **project key**
  (`autolens`, not `al`); the wrong CWD prints "0 scripts" and regenerates
  nothing. Verify by diffing the regenerated `.ipynb`/`.md` and confirming the
  sentence is gone from all three file types.
- `autolens_workspace` has historically carried several concurrent worktree
  claims — hand-check `active.md` and `~/Code/PyAutoLabs-wt/` before claiming it,
  and pre-merge `origin/main` before opening the PR.
- Prove completeness by re-running the grep above and getting **zero** hits
  across `.py`, `.ipynb` and `.md`.

## Verification

- `grep -rc "On-the-fly updates every iterations_per_quick_update" .` returns
  nothing in any file type.
- One regenerated notebook opens and its markdown cell reads correctly.
- A real fit from one edited script still prints the intro block, and the
  cadence line now comes from the library log instead.
