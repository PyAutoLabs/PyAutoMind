# Workspace API-drift call-site fixes (kwargs / Prior / interpolator / plotter) (parked NEEDS_FIX)

Type: bug
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- autolens_workspace_test
- HowToGalaxy
- HowToLens
- HowToFit
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

A set of independent "script uses stale API after a library change" NEEDS_FIX markers. Each is a
targeted call-site (or small library) fix; some pairs share one bug across repos. Reproduce each on
clean main; remove its NEEDS_FIX marker when green. Split into separate PRs if they touch different libs.

NOTE (2026-07-21 triage): this is a curated list from an earlier sweep — several items proved STALE
on clean-main reproduction. Reproduce EVERY remaining item before claiming a worktree.

- ~~**InstanceInterpolator IndexError**~~ — **DONE 2026-07-21 (PyAutoFit#1402 merged).** Root cause was NOT the interpolator: `features/interpolate.py:265` aggregator/DB section under test mode (searches write `output/test_mode/<prefix>`, `Aggregator.from_directory` read `output/<prefix>`). Fixed by making `from_directory` test-mode-aware. HowToFit `tutorial_5` was mis-paired — does NOT use the interpolator/aggregator, EXCLUDED.
- **`ell_comps` kwargs KeyError** on `('galaxies','galaxy','bulge','ell_comps'...)`: autogalaxy_workspace `imaging/modeling` + HowToGalaxy same. **BLOCKED** — autogalaxy_workspace + HowToGalaxy claimed by active `pix-inversion-not-positive-definite`. Re-triage on clean main before starting.
- **ellipse kwargs KeyError** `'ellipses.0.centre_0'`: HowToGalaxy `ellipse/modeling`. **BLOCKED** (HowToGalaxy claimed by `pix-inversion`).
- **plotter kwarg drift** `plot_grid() unexpected 'plot_grid_lines'`: HowToGalaxy `guides/advanced/over_sampling`. **BLOCKED** (HowToGalaxy claimed by `pix-inversion`).
- **group/slam PriorException** (upper<=lower): autolens_workspace `group/slam` + HowToLens `group/slam`. **BLOCKED** — autolens_workspace + HowToLens claimed by active `slam-adapt-inversion-cascade`.
- ~~**`__hash__` returns non-int TypeError**~~ — **STALE (verified 2026-07-21), no fix needed.** Reproduced `autolens_workspace_test database/scrape/general.py` as a REAL run (env_vars.yaml unsets PYAUTO_TEST_MODE for `database/scrape/`) → exit 0, subplot/FitImagingAgg section clean. Already fixed by PyAutoGalaxy#374 (`0dcea475` marks pytree_token ephemeral via __getstate__/__setstate__); marker predates it. Also note: general.py under FORCED test mode dies earlier at line 112 (database `Aggregator.add_directory` scrape not test-mode-aware — a separate latent issue, but that path is intentionally run real, so not a live bug).

Status: 1 shipped (interpolator), 1 verified-stale (__hash__ #374), tutorial_5 excluded. The 4 remaining
items are all BLOCKED by active worktree claims (pix-inversion, slam-adapt). Unblock as those ship, then
re-triage each on clean main (expect more staleness) before claiming worktrees.
