# `autoreduce 0.9` on PyPI never got the Python 3.12 floor

Type: bug
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: small
Autonomy: supervised
Priority: normal
Status: issued
Issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/71
Filed: 2026-08-19 (backfilled from git)

`autoreduce 0.9`, published **2026-08-12**, declares on PyPI:

```
Requires-Python: >=3.9,<=3.14.7
```

That is after phase 4b of the Python 3.12 floor campaign
(complete/2026/07/python-312-floor.md — PyAutoReduce#60, `d7bd916a`, merged
2026-07-30). The floor landed in source but never reached the published
artifact, so every other package in the family advertises `>=3.12` while
`autoreduce` still advertises `>=3.9`.

Two things to establish:

1. **Why the published metadata does not match source.** Was 0.9 cut from a
   pre-floor tree, or does the build path assemble metadata independently of
   `pyproject.toml`? The second would be the more serious finding — it would
   mean any repo on that path can publish a floor it does not hold.
2. **The `<=3.14.7` upper cap.** No other package in the family carries one, and
   an upper bound on Python patch versions expires on its own without anyone
   noticing. Establish what it was defending against and whether it should
   survive; an unexplained cap is a trap for the next 3.14 patch release.

Found while diagnosing the sub-3.12 silent-backtrack bug
(draft/bug/pyautohands/sub_312_pip_install_backtracks_silently.md), which
confirmed a stale `Requires-Python` keeps a package installable on Pythons it no
longer supports. `autocti` on PyPI is stale at 2024 with `>=3.7` and is not a
live install path, so it needs no action here.

## Done when

- The published `autoreduce` metadata declares the same floor as its source.
- The `<=3.14.7` cap is either justified in a comment or removed.
- The gap between merged floor and published artifact is understood, and closed
  if it is a build-path defect rather than a one-off stale cut.
