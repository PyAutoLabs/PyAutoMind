## merge-search-and-plot-scripts
- issue: none — autofit_workspace cleanup
- completed: 2026-04-18
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/37
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/52
- notes: Collapsed `scripts/searches/{nest,mcmc,mle}/` into single `nest.py`/`mcmc.py`/`mle.py` files (shared data+model+analysis, one search-variant block per algorithm with distinct `name=` strings). Renamed `scripts/plot/GetDist.py` → `get_dist.py` and the four per-sampler plotters (`{Dynesty,Emcee,Nautilus,Zeus}Plotter.py`) to snake_case. Updated READMEs, `CLAUDE.md`, `smoke_tests.txt`, cookbook cross-refs, and both `no_run.yaml` files (workspace-local + PyAutoBuild). Zeus still fails under test mode so the merged `mcmc.py` is entirely skip-listed.
