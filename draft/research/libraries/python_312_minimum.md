# Adopt Python 3.12 as the PyAuto ecosystem minimum

Filed: 2026-07-28 (backfilled from git)

## Original request

> Ok, lets remove support for anything below python3.12, do a census to make sure we simplify requriements, build server, testing, etc. Also make sure all docs are updated.

## Research question

What exact changes are required to make Python 3.12 the consistent minimum
across the PyAuto ecosystem, while simplifying compatibility machinery and
preserving a clear migration path for users of older releases?

## Initial scope to census

- Core/distributed packages: @PyAutoNerves, @PyAutoFit, @PyAutoArray,
  @PyAutoGalaxy, @PyAutoLens, @PyAutoCTI, and @PyAutoReduce.
- Build, release, health, and workflow infrastructure: @PyAutoHands,
  @PyAutoHeart, @PyAutoBrain, and @PyAutoMind.
- User-facing workspaces, tutorials, assistants, developer/test workspaces,
  Colab/conda installation paths, and RAL/HPC tooling where Python-version
  assumptions or support claims are present.

## Census outputs

- Inventory every Python-version declaration, classifier, conditional
  dependency marker/pin, CI/test/build/release/install-verification matrix,
  environment creator, and documentation claim affected by the new floor.
- Separate removals/simplifications from changes that require compatibility or
  dependency investigation.
- Identify cross-repository ordering, validation, release, and user migration
  requirements.
- Produce a phased, implementation-ready plan with an exact affected-repo list.

## Census findings (2026-07-28)

- This is a deliberate reversal of the April 2026 “wide support / narrow
  first-class” campaign. Its baseline commits span PyAutoNerves, PyAutoArray,
  PyAutoFit, PyAutoGalaxy, PyAutoLens, PyAutoHands, and six af/ag/al workspace
  repos; later Heart, assistant, CTI, Reduce, and documentation surfaces extend
  the removal set.
- Nine live package manifests are below the target floor: the seven maintained
  science/config packages, PyAutoHeart, and euclid_assistant. Six core manifests
  advertise 3.9–3.13 classifiers; PyAutoReduce advertises 3.10–3.13.
- Eight dependency entries carry now-redundant Python markers: JAX/JAXlib/
  jaxnnls (PyAutoNerves), optax (PyAutoFit), autofit+jax_zero_contour
  (PyAutoGalaxy), and nufftax in PyAutoArray optional+dev extras.
- Compatibility code removable at the new floor includes PyAutoArray's
  pre-3.12 nufftax error path and two PyAutoFit Python-3.7 `Protocol = ABC`
  shims. Missing-optional-dependency guards remain valid but need
  version-neutral messages. PyAutoNerves' import-time banner and
  `version.python_version_check` bypass must be retained and retargeted to warn
  on 3.14 while its known regression remains open; the bypass shares a
  `version:` config block with `minimum_library_version`, which must remain.
- PyAutoHands' weekly matrix still runs 3.9–3.13 unit tests and 3.11–3.13
  workspace smoke tests. PyAutoHeart's release install check explicitly creates
  3.9/3.10/3.11 environments and checks the old warning banner. Required
  library/release workflows already use 3.12/3.13 or 3.12.
- Six workspace/HowTo runtime files target 3.10/3.11 and autocti_workspace still
  targets 3.8. Assistant wiki checks, PyAutoMemory validation, assistant setup
  instructions/configs, developer AGENTS files, and autolens_profiling's Ruff
  target also retain pre-3.12 assumptions.
- User docs are internally contradictory: Fit/Galaxy/Lens pip guides already
  claim the floor changed in April, while live metadata re-enabled older
  versions later that month. CTI installation docs and Fit/Galaxy/Lens/CTI
  paper sources advertise still older ranges. The published Fit/Galaxy/Lens
  JOSS papers are archival and must not be rewritten; only living docs and any
  still-draft paper are migration targets. Workspace JAX guides and their
  generated notebooks/Markdown retain 3.11+ wording; the guide `.py` sources
  must change first and notebooks/Markdown must be regenerated, not hand-edited.
- The current unyanked PyPI legacy line is 2026.7.27.1 for the five-package
  lensing stack; the current unyanked lines are 2024.11.13.2 for AutoCTI and
  0.3.1 for AutoReduce. Shipping must re-query and record the actual
  last-compatible release per package rather than repeat the stale April claim.
- Python 3.14 cannot yet be advertised as supported: the existing
  `factor_graph_3_14_instance_iteration` task records a reproducible PyAutoFit
  workspace regression. It is a prerequisite for adding 3.14 to required
  matrices/classifiers, not a reason to retain Python <=3.11.
- Dependency audit conclusion: remove tautological Python markers, but retain
  behavior-driven scientific/runtime caps (notably JAX <0.11, nufftax <0.5,
  sampler pins, and current SciPy/Astropy caps) unless separately verified.
  JAX 0.11 and other cap upgrades are follow-up dependency migrations, not
  automatic consequences of the Python-floor change.
- Current Heart verdict is RED for pre-existing checkout drift, stale workspace
  validation, and manifest drift. These do not block planning but must be
  re-evaluated at each ship gate; this campaign must not absorb unrelated fixes.

## Independent Claude Opus review (2026-07-28)

Local Claude Code 2.1.220, model Opus at high effort, reviewed this census in
read-only plan mode and returned **APPROVE WITH CHANGES**. It independently
reproduced all countable census claims (nine manifests, six classifier sets,
eight tautological markers, compatibility branches, matrices, runtime files,
and the documentation contradiction). Its required corrections are incorporated
above and below:

- Record why the April 2026 policy is being reversed. The April rollback was a
  deliberate “wide support / narrow first-class” choice, but its PRs record no
  external consumer constraint beyond the assertion that 3.9-3.14 installed.
  Subsequent evidence invalidates that maintenance assumption: Python 3.11 has
  no usable nufftax release for the supported JAX stack, optional dependency
  exclusions and markers proliferated, and the Hands/Heart matrices repeatedly
  required version-specific repairs. No live <=3.11 consumer was found in the
  issue/PR record. The human's explicit July decision accepts that tradeoff and
  supersedes the April policy; existing users retain the last compatible wheels.
- Remove PyAutoArray's pre-3.12 transformer branch and its mocked 3.11 test in
  the same commit, and simplify the 3.12 test. Otherwise the required suite
  fails immediately.
- Update the five core `AGENTS.md` files that assert `requires-python >=3.9`.
- Preserve published JOSS papers as historical records and respect generated
  guide source -> notebook -> Markdown ownership.
- Release the five-package core stack coherently because sibling packages do
  not constrain one another to a matching floor/release. Handle AutoCTI and
  AutoReduce on their independent readiness/release cadences.

## Phase 0 decisions and evidence (2026-07-28)

- **Policy:** adopt `requires-python >=3.12`; declare and require-test 3.12 and
  3.13. Keep 3.14 unclassified and explicitly experimental until the existing
  PyAutoFit factor-graph bug is fixed. Add a non-required 3.14 evidence leg;
  fixing that regression remains a separate task.
- **Migration:** correct documentation to the real last-compatible unyanked
  releases; do not yank still-usable historical wheels. Recheck the values
  immediately before the coordinated release.
- **Independent packages:** include AutoCTI and AutoReduce metadata, tests, and
  living docs in the campaign, but do not force them into the core release.
  AutoCTI ships only after its own CI/resurrection readiness gate. The Euclid
  assistant and PyAutoHeart also adopt the floor but are not PyPI packages.
- **Runtime:** update all seven below-floor `runtime.txt` files (the three
  af/ag/al workspaces, the three HowTo repos, and autocti_workspace) to 3.12.
  The RAL host reports Python 3.12.4 and a `python-3.12` environment, so the new
  floor does not break the shared HPC stack.
- **3.14 evidence:** Python 3.14.4 is installed locally, but its ambient
  site-packages contain an incompatible NumPy 1.21.5 build. Do not treat that
  environment failure as the factor-graph reproducer; the experimental CI leg
  must exercise an isolated environment.

## Revised implementation phases and gates

0. **Record and verify policy:** complete the archaeology, PyPI boundary, RAL,
   3.14, and pre-existing Heart evidence above. Gate: complete.
1. **Core contract, in dependency order:** PyAutoNerves -> PyAutoArray ->
   PyAutoFit -> PyAutoGalaxy -> PyAutoLens. Raise metadata/classifiers, remove
   only tautological markers and obsolete branches/tests, retarget the 3.14
   warning, and update the five agent contracts. Retain behavior-driven caps.
   Gate: every suite green on 3.12 and 3.13 plus a clean branch-chain install.
2. **CI/build/health:** simplify PyAutoHands and PyAutoHeart to the floor,
   convert 3.11 install verification into an expected rejection, and add a
   non-required isolated 3.14 evidence leg. Gate: full scheduled matrix and
   end-to-end install verification with no new campaign-attributable Heart RED.
3. **Coordinated core release:** ship the five core packages together after a
   fresh Heart gate; verify published wheels reject 3.11 and install on
   3.12/3.13 before publishing living migration claims.
4. **Independent packages:** raise and test PyAutoCTI, PyAutoReduce,
   PyAutoHeart, and euclid_assistant; release CTI/Reduce only on their own
   readiness cadence.
5. **Workspaces and tooling:** align all runtime files, assistants, developer
   tooling, profiling, Memory validation, test workspaces, and RAL/HPC prose.
   Gate: sequential baseline-aware smoke tests and clean diffs.
6. **Living docs and generated artifacts:** correct migration versions, update
   source guides, regenerate notebooks/Markdown, and leave published papers
   untouched. Gate: documentation/navigation/link checks and confined generated
   diffs.
7. **Close-out:** record the policy rationale and final boundaries; retain
   separate tasks for Python 3.14 promotion and the JAX 0.11 migration.

## Supported-version wording

> PyAuto requires Python 3.12 or newer. Python 3.12 and 3.13 are tested and
> supported. Python 3.14 is currently experimental and may encounter known
> issues; use Python 3.12 or 3.13 for production work.

## Branch and overlap survey (2026-07-28)

- Proposed unified branch: `feature/python-312-floor`.
- Proposed isolated worktree root:
  `.codex-worktrees/python-312-floor/<repo>`.
- All 28 affected repositories are on `main`; no repository has an existing
  local or remote `feature/python-312-floor` branch and there is no open
  Python-floor PR.
- Clean and current with `origin/main`: PyAutoNerves, PyAutoFit, PyAutoGalaxy,
  PyAutoHeart, PyAutoCTI, PyAutoReduce, euclid_assistant, autofit_workspace,
  autogalaxy_workspace, autolens_workspace, HowToFit, HowToGalaxy, HowToLens,
  autocti_workspace, all three assistants, autolens_workspace_developer,
  autofit_workspace_test, and autogalaxy_workspace_test.
- Clean but behind `origin/main`: PyAutoArray (1), PyAutoLens (1), and
  autolens_workspace_test (1). New worktrees must branch from refreshed
  `origin/main`, not their local `main` checkouts.
- Existing unrelated dirt to isolate rather than touch: PyAutoHands has
  untracked `run_logs/`; PyAutoMemory has a modified `reading-queue.md` and is
  four commits behind; autolens_profiling has an untracked JWST dataset;
  autofit_workspace_developer has six modified sampler/profiling files and is
  two commits behind. PyAutoMind's only dirt is this untracked task record.
- Active-task overlap: `api-validation-and-crash-fixes` names PyAutoArray and
  PyAutoLens and reserves future PyAutoGalaxy work, but its registered worktree
  is absent and the floor targets different files. `multistart-prodigy-compile`
  has a live autolens_profiling worktree, but the floor target is `ruff.toml`.
  The test-workspace pending-release record is stale: the recorded worktree is
  absent and GitHub currently shows no open PRs in either repository. These are
  sequencing/coordination concerns, not direct file collisions.
- The only remaining Python-named remote branch is PyAutoFit
  `origin/feature/optax-python-marker`; PR #1426 is merged. Removing that marker
  at the new floor is an intentional continuation, not competing work.

Implementation remains gated on explicit approval of the unified branch and
the overlap/isolation strategy above.

## Acceptance direction for the subsequent development task

- All maintained PyAuto packages consistently declare Python `>=3.12`.
- Requirements and conditional markers needed only for Python 3.9–3.11 are
  removed or simplified where safe.
- Required, scheduled, build, release, and install-verification matrices reflect
  the new floor and cover current stable Python versions.
- Installation, contributor, workspace, Colab, conda, HPC, and release docs no
  longer claim support below 3.12.
- The migration is tested across the full affected library chain and relevant
  downstream workspaces before shipping.
