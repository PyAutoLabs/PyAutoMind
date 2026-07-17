# CTI release-train wiring — first modern autocti release

Type: release
Target: PyAutoBuild
Repos:
- @PyAutoBuild
- @PyAutoConf
- @autocti_workspace
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised

Follow-up to the CTI resurrection epic (Phases 0-5; workspace_test + Heart
polling shipped 2026-07-17). Wire autocti into the release train and produce
its first modern PyPI release. Deliberately split from the epic's Phase 5:
this touches the nightly's most dangerous machinery and must be done with a
TestPyPI rehearsal, in a fresh session.

## Scope

1. **PyAutoBuild**: `tag_and_merge.sh` `LIB_PROJECTS` += PyAutoCTI;
   `pre_build.sh` `run_workspace` lines for autocti_workspace (+ _test,
   generate=false); `release.yml` / `python_matrix.yml` matrices;
   `generate_release_notes.py` + `slack_release_notes.py` +
   `aggregate_results.py` repo maps; `build_util.py` `COLAB_PROJECTS` +=
   autocti; FIREWALL_ALLOWLIST tokens in Mind for every file gaining CTI names.
2. **PyAutoConf** `autoconf/setup_colab.py`: an `autocti` `_PROJECTS` entry
   whose package list handles **arcticpy** correctly on Colab (apt
   `libgsl-dev` + `pip install numpy cython` + `arcticpy==2.6
   --no-build-isolation --no-deps` — a naive pip install downgrades numpy
   below 2.0). May need a per-project `pre_install` hook in the setup
   machinery.
3. **Notebook generation**: `generate.py autocti` (blocked today by the
   COLAB_PROJECTS registry check) → commit regenerated notebooks to
   autocti_workspace.
4. **Rehearsal then release**: TestPyPI rehearsal of the extended train
   (`release rehearse` / `release validate` through the Release Agent), fix
   fallout, then the first modern `autocti` release rides the next nightly or
   a human-authorized release. Never hand-dispatch the nightly.

## Context

- Epic records: `PyAutoMind/complete/2026/07/cti-resurrection-phase{0..5}.md`.
- PyAutoCTI pyproject floors are release-ready (setuptools-scm, Phase 0);
  CI green via Heart lib-tests (Phase 3); Heart polls the CTI repos (Phase 5).
- arcticpy traps + CI install recipe: `PyAutoCTI/AGENTS.md` and
  `autocti_workspace_test/.github/scripts/smoke_install.sh`.
