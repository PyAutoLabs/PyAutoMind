- issue: https://github.com/PyAutoLabs/autocti_workspace_test/issues/1 (closed)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/89 (merged 358ef2f)
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace_test/pull/2 (merged a655575)
- summary: CTI resurrection Phase 5 (FINAL) — autocti_workspace_test rebuilt as a modern integration suite: 2022-23 Euclid VIS heritage (euclid/tvac/temporal/validation/overview_output + era config) preserved verbatim under legacy/ with a README; three self-contained integration scripts (dataset_1d simulate→FactorGraphModel fit→aggregator round-trip; imaging_ci fit; full autocti.plot function-surface drive with per-section output dirs — the functions have fixed default filenames, sections must not share a dir); curated smoke_tests.txt + env_vars.yaml (PYAUTO_TEST_MODE=2, single-trap models to dodge the bypass assertion tie); smoke runner + smoke_install.sh carrying the arcticpy CI recipe; thin caller of Heart's reusable smoke workflow (chain PyAutoConf PyAutoFit PyAutoArray PyAutoCTI). run_smoke.py 3/3 PASS locally. PyAutoHeart config/repos.yaml now polls all three CTI repos (observer-only).
- scope-split: release-train wiring (Build tag_and_merge/pre_build/release.yml/release-notes matrices, COLAB_PROJECTS + autoconf setup_colab autocti entry incl. the arcticpy-on-Colab problem, notebook generation — generate.py hard-requires the colab registries — TestPyPI rehearsal, first PyPI release) deliberately deferred to draft/release/autocti/cti_release_train_wiring.md (human-required). Notebook regeneration is blocked on that registry work, not on the workspace.
- traps: Clocker2D has NO express/roe kwargs (parallel_express/parallel_roe); a smoke pre-flight grepping 'output/' must anchor at path start (legacy/overview_output/ renames false-positive); the sqlite from Aggregator.from_database lands under the test-mode output namespace, not CWD.
- heart: shipped + merged through the standing pre-existing RED on human ack 2026-07-17 ("Ship + merge + close epic").
- epic: COMPLETE — all six phases merged in one day (2026-07-16 → 17). PyAutoCTI, autocti_workspace and autocti_workspace_test are fully back in the ecosystem: modern packaging, matplotlib-function viz, factor-graph autofit, green CI, validated workspace, integration suite, Heart polling. Remaining to first PyPI release: the filed release-train prompt.

## Original prompt

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
