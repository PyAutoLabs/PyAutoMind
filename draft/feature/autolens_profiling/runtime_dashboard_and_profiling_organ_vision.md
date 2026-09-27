# Run-time-over-time dashboard for the *_profiling repos (and the organ question)

- Work type: feature
- Target: @autolens_profiling (first), later autolens_inference and any sibling *_profiling repo
- Epic: profiling-research-wiki (dashboard leg; organ birth is a later, separate epic)
- Autonomy: human-required
- Filed: 2026-09-27

## Original prompt

"The long term vision for all this is that we have a PyAuto organ, with a dashboard, directly tied
to the _profiling repos so I can see run time of everything and monitor run time over time using
this dashboard, what are your thoughts on that too?"

## Assessment recorded 2026-09-27

- The seed exists: every summary JSON is versioned by the PyAutoLens release that produced it,
  `profile.yml` runs the sweeps on release tags, and the Brain Profiling conductor already has a
  drift-triage mode. Run time over time is a rendering of data already collected.
- The organ should be Eyes-shaped, not Heart-shaped: it renders and holds the timing history and
  never judges a lever (judgement stays with the Brain's Profiling conductor), so it does not
  become a second readiness verdict competing with Heart.
- Two prerequisites or the trend lines are noise: release-cadence sweeps must run on a pinned quiet
  RAL host (laptop drifts 2.5x; GitHub runners are unsuitable), and every result JSON needs the
  mandatory provenance block (host, loadavg, job id, library revisions, dependency floors).
- Order: wiki + index (phase 1/2) → dashboard in the profiling repo (state.json + Pages, the
  organ-cockpit / Brain-board pattern) → organ birth only once it spans more than one profiling
  repo. autolens_inference supplies the second panel: fit wall clock per release beside likelihood
  per release — that is where the "likelihood share of a fit" admission number lives.

## Scope (dashboard leg)

1. `scripts/misc/tooling/build_dashboard.py`: read `results/**/summary*.json` → `dashboard/state.json`
   (per likelihood cell × device × precision: median ms per release tag, provenance) → static
   Pages site with one trend line per cell and a drift badge from the existing triage thresholds.
2. Pin the reference host in `hpc/` for the release sweep; refuse rows above a loadavg cap.
3. Wire `profile.yml` to regenerate `state.json` and publish on release tags.
4. Register the dashboard URL on the Brain board.

## Out of scope

Organ birth, repos.yaml changes, any library change.
