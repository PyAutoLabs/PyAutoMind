# CTI resurrection — Phase 5: workspace_test rebuild + release wiring

Type: feature
Target: autocti_workspace_test
Repos:
- @autocti_workspace_test
- @autocti_workspace
- @PyAutoHeart
- @PyAutoBuild
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Final phase of the CTI resurrection epic (Phases 0-4 all merged 2026-07-17:
PyAutoCTI #83/#85/#87/#89/#90, Heart #87/#88, Brain #135, autocti_workspace #2).
Wire the resurrected stack into regression testing and the release train.

## Scope

1. **autocti_workspace_test rebuild** (last touched 2023-02): modernize on the
   autogalaxy_workspace_test shape — a curated smoke runner
   (`.github/scripts/run_smoke.py` pattern), `smoke_tests.txt` (SMALL curated
   subset: a few scripts per section that pass `PYAUTO_TEST_MODE=2`; the
   ordered-trap assertion scripts are excluded until the filed autofit bypass
   fix lands), `config/build/env_vars.yaml`, and CI on the current pattern.
   **Preserve the Euclid heritage** (`euclid/`, `tvac/`, `temporal/`,
   `validation/`) unmodified under a clearly-marked legacy home — it is
   Euclid VIS history, not smoke material.
2. **Heart registration**: add the three CTI repos to
   `PyAutoHeart/config/repos.yaml` so the tick polls their CI/state.
3. **Build registration**: add autocti/autocti_workspace to the PyAutoBuild
   release path (`pre_build.sh` run_workspace list, notebook generation
   targets, release notes) so the nightly covers them.
4. **Notebook regeneration**: `generate.py autocti` over the Phase-4 scripts;
   commit regenerated notebooks to autocti_workspace.
5. **The release itself stays human/nightly** — this phase ends with the wiring
   in place and the next nightly (or a human-authorized release) producing the
   first modern `autocti` PyPI release. No manual nightly dispatch.

## Context

- Phase records: `PyAutoMind/complete/2026/07/cti-resurrection-phase{0..4}.md`.
- Smoke memory rules: curated small subset, env vars via env_vars.yaml.
- repos_sync `--check` validates the Heart/Build lists against repos.yaml.
