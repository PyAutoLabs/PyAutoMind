## profiling-runtime-dashboard
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/345
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/346 (merge `114ff37e`, head `a516a0d`, 13 files, +7361/−3 of which ~7,300 are the generated `dashboard/`)
- epic: profiling-research-wiki (dashboard leg; organ birth is a later, separate epic)
- merge: by the human's typed `/prm` on green (lint.yml run 554 on `a516a0d`: one job, success; `mergeable_state: clean`). The first run on `8c8a6ea` failed on lychee alone (the README's Pages URL 404s until `pages_dashboard.yml` first publishes from `main`); fixed by excluding that URL in `lint.yml` with the reason in a comment
- heart: GREY at the door (Pages host not on the container allowlist); tooling, workflows and docs, no library change

### Summary
- `scripts/misc/tooling/build_dashboard.py` (stdlib) scans `results/**` — versioned artifacts,
  config-tagged rows and sweep `comparison.json` — into series keyed cell × instrument × config
  × sparse, one point per PyAutoLens release with the per-call headline (`build_readme.py`'s
  ladder, extended for breakdown cells), `vmap.per_call` and provenance. On the tree at merge:
  143 series, 61 cells, 4 releases (2026.5.29.4, 7.6.649, 7.23.1, 8.17.1); 6 series improved
  across releases, none drifted.
- Qualification against `hpc/release_sweep.conf`: a row above the load-average cap is refused
  (listed, never plotted); a row without a provenance block, or an HPC row off the reference
  host, is plotted hollow. Every marker is hollow today because no committed row predates
  the provenance block (#342); the first pinned sweep after a release draws the first solid line.
- Drift badge from a series' last two releases at the profiling conductor's `>= 2.0x` ratio
  with a 1 ms per-call floor (this dashboard's own floor; the conductor's 1 s is for compile).
  A flag for `profiling triage`, never a verdict.
- `dashboard/series.json` (data), `dashboard/state.json` (organ cockpit feed, contract v1,
  `python PyAutoBrain/board/_state.py` ok), `dashboard/index.html` (static, no assets: small
  multiples, categorical config colours from the dataviz reference palette validated in both
  modes — light meets the relief rule through the per-panel table — 2 px lines, ≥ 8 px markers,
  native `<title>` hover, legend + table per panel, log y, light/dark). `--check` re-renders with
  the committed stamp so only data can differ; it runs in `lint.yml`.
- Pinned release sweep: `hpc/release_sweep.conf` (`RELEASE_SWEEP_NODE=euclid-ral-gpu-2`,
  `RELEASE_SWEEP_LOADAVG_CAP=8.0`) and `hpc/batch_gpu/submit_release_sweep.sh` (the eight A100
  runtime legs, `sbatch --nodelist`, `--dry-run`); `check_submits.py` green.
- `profile.yml` builds and commits `dashboard/` after the README refresh; `pages_dashboard.yml`
  publishes `dashboard/` on push to `main` (paths `dashboard/**`) after validating the feed
  against the Brain contract (the Cortex pattern); Pages enablement on its first run.
- README, `results/README.md` and `hpc/README.md` describe the dashboard and the pin.
- Tests: `test_build_dashboard.py` (7: grammar in step with `build_readme.py`, conf,
  qualification and drift, feed contract, write/check idempotence, real tree); headless
  screenshots of both themes checked (one axis-label clip fixed before commit).

### Traps / notes
- The organ question: none needed for this leg (the draft and ORGANISM.md's growth rule both put
  birth after the dashboard spans a second profiling repo). Candidate names on the anatomical
  pattern, for whenever that day comes: Pulse (rate over time, but close to Heart's ground) or
  Reflexes. Left to the human.
- Item 4 of the scope (register the page on the Brain board) could not ride this PR: PyAutoBrain
  is claimed by `eyes-organ-order`. Re-filed as
  `draft/feature/pyautobrain/register_profiling_dashboard_on_brain_board.md`.
- The Pages URL is a dead link until the first publish; `lint.yml` carries a lychee exclude for
  it with a comment saying to drop it once the site is live.
- The first `Pages Dashboard` run on `main` (run 36357571915, on the merge commit) failed at
  `actions/configure-pages@v5`: "Create Pages site failed. Error: Resource not accessible by
  integration". `enablement: true` lets the workflow create the site only where the token may
  administer the repo; `GITHUB_TOKEN` cannot, so the site has to be created once by a human
  (repo Settings → Pages → Source: GitHub Actions), then `pages_dashboard.yml` dispatched by
  hand. The Cortex's site was created the same way. The dashboard is merged but not published
  until then.
- Importing a sibling module through `importlib.util` in a test needs `sys.modules[name] = mod`
  before `exec_module`, or `@dataclass` fails resolving the defining module.
- Second branch (`claude/profiling-runtime-dashboard-b8vtjm`) by the human's choice, so this and
  #344 could be open together.

### Remainder (re-filed)
- `draft/feature/pyautobrain/register_profiling_dashboard_on_brain_board.md` — Brain board
  registration (item 4).
- Done 2026-09-28: the human enabled GitHub Pages (Settings → Pages → Source: GitHub Actions);
  `pages_dashboard.yml` run 2, dispatched on `114ff37e`, published the site (github-pages
  deployment success, <https://pyautolabs.github.io/autolens_profiling/>). The lychee exclude
  came out in autolens_profiling#347 (merge `163704e6`, lint green with the real link check).
  Every push to `dashboard/**` on `main` now republishes by itself.

## Original prompt

# Run-time-over-time dashboard for the *_profiling repos (and the organ question)

- Work type: feature
- Target: @autolens_profiling (first), later autolens_inference and any sibling *_profiling repo
- Epic: profiling-research-wiki (dashboard leg; organ birth is a later, separate epic)
- Autonomy: human-required
- Filed: 2026-09-27
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/345
Issued: 2026-09-27

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
