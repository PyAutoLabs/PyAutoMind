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
Filed: 2026-07-17 (backfilled from git)

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

- **Item 3's blocker is now a clean refusal, not a destructive one** (PyAutoLabs/PyAutoHands#215
  / PR #216, 2026-07-30). `generate.py` used to `rmtree` the whole `notebooks/`
  tree *before* reaching the `COLAB_PROJECTS` check, so probing `generate.py
  autocti` deleted 113 tracked notebooks and then aborted. It now validates up
  front and exits with "Nothing was modified", leaving the tree untouched — so
  this task can probe the registry check freely. The registration itself
  (items 1-2) is untouched and still belongs here.
- **Backlog item 3 will clear when it runs:** `autocti_workspace/notebooks/`
  currently carries 34 `Finish.` markdown cells (from the crutch sweep,
  PyAutoLabs/autocti_workspace#16) and 4 mangled code cells containing a literal
  `# %%` and `'''` — a `SyntaxError` if run — in
  `notebooks/imaging_ci/modeling/features/{cosmic_rays,non_uniform,serial_cti,visualize_full}.ipynb`,
  plus the 5 script-reference fixes from `autocti_workspace#15`. All are already
  correct in `scripts/`; one successful `generate.py autocti` clears all of them.
- **Do not hand-roll the regeneration.** `build_util.py_to_notebook` alone is not
  equivalent to `generate.py`: control-tested against an unchanged script, the
  committed notebook carries a trailing empty code cell that `py_to_notebook`
  does not emit. That cell is the signature of the pre-2026-07-24 generator
  (before PyAutoHands `6916814` a closing docstring always emitted a `# %%`), so
  these 79 notebooks predate it — expect the regeneration to drop those empty
  cells across the board, which is correct.
- Epic records: `PyAutoMind/complete/2026/07/cti-resurrection-phase{0..5}.md`.
- PyAutoCTI pyproject floors are release-ready (setuptools-scm, Phase 0);
  CI green via Heart lib-tests (Phase 3); Heart polls the CTI repos (Phase 5).
- arcticpy traps + CI install recipe: `PyAutoCTI/AGENTS.md` and
  `autocti_workspace_test/.github/scripts/smoke_install.sh`.
