## cti-release-train-wiring
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/332
- completed: 2026-11-05
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/210
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/333
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/585
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/323
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/535
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/40
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/210

Merged 2026-11-05 via human-typed /prm, in gate order: PyAutoNerves#210 → PyAutoMind#535 → PyAutoHands#333 / PyAutoBrain#585 / PyAutoHeart#323 → autocti_workspace#40. Issue PyAutoHands#332 closed. cti-upkeep epic, phase 1.

PyAutoCTI is now part of the lockstep release train:
- **Hands:** tag_and_merge LIB_PROJECTS, pre_build WORKSPACE_SPECS (autocti_workspace with notebook generation, autocti_workspace_test without), COLAB_PROJECTS, workspaces.yaml (libraries / colab_setup / colab_gemini), release.yml (TestPyPI + PyPI matrices, smoke, label clearing, notes, release_workspaces, wiki_currency_check_autocti, Colab URL bump, rehearsal record), python_matrix cti_* on 3.12 / 3.13, and the notes / slack / aggregate / markdown maps.
- **Nerves:** setup_colab registers autocti, and its pre-install runs Heart's install_arcticpy.sh (ARCTICPY_SUDO=false, PYTHON=sys.executable), so the arcticpy pin has one home.
- **Brain:** rehearse / validate LIBRARIES and clean_slate.
- **Heart:** PyAutoCTI release_gate true (ruling R6).
- **Mind:** tenant-firewall allowlist for the 12 touched organ files.
- **autocti_workspace:** 79/79 notebooks regenerated with Colab cells (0 `Finish.` cells, 4 orphan READMEs removed), black on 6 scripts, new config/build/profile_release.yaml, AGENTS.md updated.

Evidence: the TestPyPI rehearsal from the Hands branch (run 42011123173, 92ec5f4) built, uploaded and installed all 6 wheels as 2026.11.5.1.dev86501, and Heart ingested it as rehearse:pass. The release smoke run is 3/3 PASS under profile_release. `generate.py notaproject` refuses, and howtolens gives zero diff. Suites: Nerves 292, Heart 1313, Hands 589 (the 4 test_tombstone failures also fail on main), Brain 1568.

CI note: Hands, Brain and Heart were red on the tenant firewall until Mind#535 landed the allowlist on main. Their failed jobs were re-run after that merge and went green.

Scope change, deferred to phase 3/5: Heart workspace-validation / release-integrate rows, run_all entries and the docs-build mapping. Adding them would make all 118 untriaged autocti scripts a release gate, and docs-build does nothing until PyAutoCTI has a docs.yml caller.

The release profile uses PYAUTO_FAST_PLOTS=0 because of the autocti fits_fit missing-directory bug, now filed as draft/bug/autocti/fits_fit_missing_output_dir_under_fast_plots.md (phase 3).

Next: the first modern autocti PyPI release rides the next lockstep release.

Pending release: merged is not released — the `pending-release:` key above stays until `/review_release` clears it.

## Original prompt

# CTI release-train wiring — first modern autocti release

Type: release
Target: PyAutoHands
Repos:
- @PyAutoHands
- @PyAutoNerves
- @autocti_workspace
Themes:
- release
- cti
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
Epic: cti-upkeep
Phase: 1
Filed: 2026-07-17 (backfilled from git)
Issued: 2026-11-04

Follow-up to the CTI resurrection epic (Phases 0-5; workspace_test + Heart
polling shipped 2026-07-17). Wire autocti into the release train and produce
its first modern PyPI release. Deliberately split from the epic's Phase 5:
this touches the nightly's most dangerous machinery and must be done with a
TestPyPI rehearsal, in a fresh session.

## Scope

1. **PyAutoHands**: `tag_and_merge.sh` `LIB_PROJECTS` += PyAutoCTI;
   `pre_build.sh` `run_workspace` lines for autocti_workspace (+ _test,
   generate=false); `release.yml` / `python_matrix.yml` matrices;
   `generate_release_notes.py` + `slack_release_notes.py` +
   `aggregate_results.py` repo maps; `build_util.py` `COLAB_PROJECTS` +=
   autocti; FIREWALL_ALLOWLIST tokens in Mind for every file gaining CTI names.
2. **PyAutoNerves** `autonerves/setup_colab.py`: an `autocti` `_PROJECTS` entry
   whose package list handles **arcticpy** correctly on Colab (apt
   `libgsl-dev` + `pip install numpy cython` + `arcticpy==2.6
   --no-build-isolation --no-deps` — a naive pip install downgrades numpy
   below 2.0). May need a per-project `pre_install` hook in the setup
   machinery.
3. **Notebook generation**: `generate.py autocti` (blocked today by the
   COLAB_PROJECTS registry check) → commit regenerated notebooks to
   autocti_workspace. This is a fork, not a formality: either register
   autocti (items 1-2 above, if its notebooks are meant to carry Colab setup)
   **or** give `generate.py` a documented no-Colab mode for workspaces that do
   not. Whichever path is taken, update `autocti_workspace/AGENTS.md`'s
   *Notebook regeneration* line to match it — that line currently implies the
   standard path works, which it does not.
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
  (items 1-2) is untouched and still belongs here. Pinned by
  `PyAutoHands/tests/test_generate_validates_project.py`; the ordering is
  invisible in a passing run, so do not remove that test while reworking
  `generate.py` for item 3.
- **Why this stayed invisible.** `autocti_workspace` is absent from
  `PyAutoHands/pre_build.sh`'s `run_workspace` matrix entirely (the
  `generate=true` set is autofit_workspace, autogalaxy_workspace,
  autolens_workspace, HowToGalaxy, HowToLens, HowToFit), so no release path has
  ever exercised `generate.py autocti`. Corroborating: **0 of the repo's 79
  notebooks carry a Colab setup cell**, dating them to before
  `inject_colab_setup` became strict. They do still track `scripts/` 1:1 (79
  scripts, 79 notebooks, no orphans either way), so they were maintained by
  some path that no longer works. Item 1's `pre_build.sh` line is what closes
  this hole for good.
- **Backlog item 3 will clear when it runs:** `autocti_workspace/notebooks/`
  currently carries 34 `Finish.` markdown cells (from the crutch sweep,
  PyAutoLabs/autocti_workspace#16) and 4 mangled code cells containing a literal
  `# %%` and `'''` — a `SyntaxError` if run — in
  `notebooks/imaging_ci/modeling/features/{cosmic_rays,non_uniform,serial_cti,visualize_full}.ipynb`,
  plus the 5 script-reference fixes from `autocti_workspace#15`. All are already
  correct in `scripts/`; one successful `generate.py autocti` clears all of them.
  So item 3 is the single gate on three separate merged sweeps reaching the
  notebooks.
- **Do not hand-roll the regeneration.** `build_util.py_to_notebook` alone is not
  equivalent to `generate.py`: control-tested against an unchanged script
  (`scripts/dataset_1d/extract.py` vs the committed
  `notebooks/dataset_1d/extract.ipynb`), the committed notebook carries a
  trailing empty code cell that `py_to_notebook` does not emit — 343 vs 336
  lines, otherwise identical. That cell is the signature of the pre-2026-07-24
  generator (before PyAutoHands `6916814` a closing docstring always emitted a
  `# %%`), so these 79 notebooks predate it — expect the regeneration to drop
  those empty cells across the board, which is correct. Control-test against an
  unchanged script before trusting any regeneration path here; that is what
  caught this.
- Epic records: `PyAutoMind/complete/2026/07/cti-resurrection-phase{0..5}.md`.
- PyAutoCTI pyproject floors are release-ready (setuptools-scm, Phase 0);
  CI green via Heart lib-tests (Phase 3); Heart polls the CTI repos (Phase 5).
- arcticpy traps + CI install recipe: `PyAutoCTI/AGENTS.md` and
  `autocti_workspace_test/.github/scripts/smoke_install.sh`.

## Validation

- `generate.py autocti` exits 0 from `autocti_workspace/`; all 79 notebooks
  regenerate; no code cell contains a literal `# %%` or `'''`; no markdown cell
  is `Finish.`.
- `generate.py <unknown-project>` still exits non-zero with `notebooks/`
  **intact** and no stray `.ipynb` beside any script
  (`PyAutoHands/tests/test_generate_validates_project.py` stays green).
- `generate.py howtolens` from `HowToLens/` still gives a zero diff — the
  registry change must not perturb the projects already on the train.
- `autocti_workspace/AGENTS.md`'s *Notebook regeneration* line matches whatever
  path item 3 actually chose.
- `pre_build.sh`'s `run_workspace` matrix names autocti_workspace, so the next
  nightly exercises the path rather than skipping it.

## Provenance

Folded 2026-08-26: `draft/bug/pyautohands/generate_rejects_autocti_after_deleting_notebooks.md`
was retired into this file. That prompt tracked two defects — the destructive
ordering in `generate.py` (fixed by PyAutoLabs/PyAutoHands#215 / PR #216,
regression-tested) and the missing `autocti` registration. Only the second was
ever this file's items 1-3, so the bug prompt had no startable work of its own;
its residual requirements (the `AGENTS.md` doc line, the pre_build-matrix
evidence, the control-test detail) are absorbed above. It had itself
consolidated three independently-filed prompts describing the same defect.
