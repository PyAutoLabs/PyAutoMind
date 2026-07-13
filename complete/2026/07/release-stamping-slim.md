## release-stamping-slim
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/120 (closed)
- completed: 2026-07-08
- prs: PyAutoBuild#121 (merged e912219; merge-gated after PyAutoConf#119)
- notes: |
    R3-core of the pinning review: releases are wheels+tags only. Scheduled
    versions <date>.1 (run_number fallback removed — the .641-.649 accident
    mechanism); __init__ sed stamps build-tree only, no commit-back, branch
    push dropped, tag push kept; release_workspaces no longer writes
    version.txt/general.yaml pins or README stamps. Notebook regen + Colab
    bumps kept per-release (Q2 answered by maintainer: same cadence, rides
    each release). 71 tests. Follow-ups: Heart version_skew floor-vs-tag
    rework (check now inert); __version__ via importlib.metadata (polish).

## Original prompt

# Release stamping slim: wheels+tags only, no daily bump commits (R3-core)

Type: feature
Target: PyAutoBuild
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Original request (verbatim)

> ok, I support all this input — R1–R4 endorsed on PyAutoBuild#118. [After the
> rehearsal PRs merged:] ok, those PRs are done so we can do this work now --auto

## Context

R3-core of the version-pinning design review (PyAutoLabs/PyAutoBuild#118).
Every release currently pushes "Update version to X" commits to all five
library mains, "pin workspace version" + README-stamp commits to every
workspace main — the noise engine behind the June/July accidental-release
cascade. The wheels already receive their version via `sed` at build time, so
the commit-backs are not needed for published artifacts.

## Scope (endorsed core only; notebook/Colab cadence is Q2 on #118, untouched)

- `release.yml` `version_number`: scheduled runs default the minor to `1`,
  never `github.run_number` (the accidental-series mechanism; rehearsal
  uniqueness already comes from the `.devN` segment).
- `release.yml` `release` job: keep the build-tree `sed` stamp + tag +
  `git push --tags`; drop the `__init__.py` commit and branch push to
  library mains.
- `release.yml` `release_workspaces`: drop the "Write workspace version"
  step (version.txt + general.yaml — obsolete under the R2 floor check in
  PyAutoConf#118) and the README version-stamp commit. Keep notebook regen,
  Colab bumps, API baseline, and workspace tags exactly as they are.
- Merge-ordering: only merge after PyAutoConf#118 (R2 floor semantics) is
  merged, so the release that stops writing pins also ships the floor check.

## Out of scope (follow-ups to file separately)

- Notebook regen / Colab-bump cadence under daily live releases (Q2 on #118).
- Library `__version__` via `importlib.metadata` (avoids PyAutoConf conflict
  with the parked R2 task).
- PyAutoHeart `version_skew` check rework for floor semantics (it compares
  workspace pins vs `__init__` stamps; goes inert once both freeze).
