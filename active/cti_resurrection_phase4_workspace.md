# CTI resurrection — Phase 4: autocti_workspace update

Type: feature
Target: autocti_workspace
Repos:
- @autocti_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4 of the CTI resurrection epic (Phases 0-3 merged: PyAutoCTI #83/#85/#87/#89
+ Heart#87 + Brain#135). Bring autocti_workspace (118 scripts / 79 notebooks;
last updated 2024-11) onto the current library APIs.

## Scope

1. **Plot API migration** (70 scripts reference the old API): the deleted
   `aplt.*Plotter` / `MatPlot*` / `Output` / `Title` object stack → the Phase-1
   matplotlib function API (`aplt.subplot_*`, `figure_*`, `output_path=` /
   `output_format=` kwargs). The `scripts/plot/` tutorials are rewritten as
   function-API tutorials; other sections' plotting calls converted in place.
2. **Library API drift**: `add_poisson_noise` → `add_poisson_noise_to_data`,
   instance `.output_to_fits` → `autoconf.fitsable`, prior-config
   `gaussian_limits` → `limits`, multi-dataset `analysis + analysis` →
   `af.AnalysisFactor`/`af.FactorGraphModel`, dataset output format notes.
3. **Configs**: sync `config/visualize.yaml` plots schema (new keys), priors
   yaml `limits:` rename, general.yaml version keys; mirror new library
   defaults per workspace-config convention.
4. **Validation**: run a representative subset per section under
   `PYAUTOFIT_TEST_MODE=1` (arcticpy installed); fix fallout.
5. **Notebooks**: regenerated from scripts by the PyAutoBuild pipeline at
   release (Phase 5) — not hand-edited here beyond deleting stale ones if the
   generator requires it.

## Conventions

Tutorial narrative prose is preserved; only code cells and prose that names
the old API change. Judgment-tier session edits the prose-bearing overview +
plot tutorials; mechanical per-directory conversions may be delegated with a
strict cookbook.
