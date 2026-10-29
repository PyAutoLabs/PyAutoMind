# Compact Colab setup across projects

Completed: 2026-10-29
Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/327 (closed)

## Shipped

The shared generator and all eight consumers now use compact Colab setup cells, with introductory explanation and advanced links. CPU/GPU options, local no-install behavior and scientific cell sources are preserved. HTML support remains future work.

All nine PRs are merged:
- PyAutoHands: https://github.com/PyAutoLabs/PyAutoHands/pull/328
- autolens_workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/604
- autogalaxy_workspace: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/265
- autolens_assistant: https://github.com/PyAutoLabs/autolens_assistant/pull/167
- autogalaxy_assistant: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/41
- autofit_workspace: https://github.com/PyAutoLabs/autofit_workspace/pull/178
- HowToFit: https://github.com/PyAutoLabs/HowToFit/pull/77
- HowToGalaxy: https://github.com/PyAutoLabs/HowToGalaxy/pull/92
- HowToLens: https://github.com/PyAutoLabs/HowToLens/pull/102

## Evidence and cleanup

On 2026-10-29, GitHub confirmed every PR merged; each of the nine local task HEADs matched its PR head and had zero commits outside freshly fetched origin/main. All task worktrees were clean. The issue was already closed. This supersedes the historical partial-merge checkpoint folded below.

Prior development evidence: 584 generator tests; 633 notebooks regenerated with unchanged science cells; all six family smoke suites passed; assistant focused tests and pinned-runtime checks passed. Hosted Colab installation/UI was not exercised. No new release or merge was performed during cleanup.

Human authorized completed-task cleanup and explicitly chose "Delete task data with worktree". Release all nine claims and remove the completed task worktrees and local feature/compact-colab-setup branches. Preserve unrelated Mind edits. Remote branch lifecycle remains with GitHub and the repository sweeper.

## Original prompt

# Make Colab setup unobtrusive across projects

Type: refactor
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/327
Target: PyAutoHands
Difficulty: medium
Consequence: judge

Primary: @PyAutoHands. Consumers: @autolens_workspace, @autogalaxy_workspace,
@autofit_workspace, @HowToFit, @HowToGalaxy, @HowToLens, @autolens_assistant.
Shared implementation: @PyAutoNerves (preserve runtime behavior).

## Original request (verbatim)

- This takes up too much space and brain capacity of a user, and should be a single line or the most brief possible
thign which doesnt require them to think about whats actually going on. This should not be the first thing a user
has to think about:

try:
    import google.colab
except ImportError:
    from autolens import setup_colab as _setup_colab
else:
    import importlib
    import subprocess
    import sys

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "autonerves", "--no-deps"]
    )
    _setup_colab = importlib.import_module("autonerves.setup_colab")

_setup_colab.for_autolens(
    raise_error_if_not_gpu=False  # Switch to False for CPU Google Colab
)

Sort this across all projects, it function is important and works as expected but its confusing and a lot of code.

## Approved plan

- Present Colab setup as one short run cell labelled "Set up Google Colab", with implementation hidden by default.
- Centralize bootstrap generation and shorten source-script setup to an import and call.
- Apply the presentation consistently to existing handwritten setup and all six generated notebook project families.
- Preserve installation, workspace/config setup, CPU/GPU choices and local execution; validate fresh-session and regeneration behavior.
- Tier: judge — merge mode: human /prm.

## Detailed implementation plan

1. PyAutoHands `autohands/build_util.py`: revise `inject_colab_setup`, `COLAB_SETUP_CODE` and `COLAB_SETUP_MARKDOWN`. Use compact notebook presentation (Colab form title and hidden source metadata, Jupyter collapsed-source metadata where supported). Remove the long introductory explainer. Keep fresh-Colab bootstrap self-contained: importing the scientific library before installation is not sufficient.
2. Recognize supported handwritten `setup_colab` cells and normalize them, preserving project and keyword options; avoid duplicate setup and retain surrounding science code. Do not blindly replace arbitrary cells containing the string. Make regeneration idempotent.
3. Replace duplicated bootstrap blocks in Lens/Galaxy `start_here.py` and `scripts/**/start_here.py` with the established short import/call form; shorten adjacent setup prose. Inventory all project sources, including the assistant's `docs/colab/cosmos_web_ring_colab.py`. Generated markdown/notebooks follow their canonical generator, not manual parallel edits.
4. Cover all `COLAB_PROJECTS` keys: autofit, autogalaxy, autolens, howtofit, howtogalaxy, howtolens. Inventory CTI/Reduce too; do not introduce Colab support where none exists. Preserve `autonerves/setup_colab.py` behavior and wrapper API; only change it if investigation establishes necessity within this scope.
5. Extend `PyAutoHands/tests/test_inject_colab_setup.py`: generated and handwritten inputs, preserved options, repeated generation, mixed cells, prose-only notebooks, all projects. Exercise fresh Colab with package imports absent, local no-install behavior, CPU and GPU settings. Use existing Nerves tests and Heart Colab gate contract as behavior references; do not claim hosted Colab testing without running it.
6. Generate representative artifacts for review, then ship generator changes before consumer changes through the required development workflows. No release or merge authorized.

## Evidence and next action

Heart entry gate GREEN (2026-10-28). No matching active/planned Colab task found.
Memory consultation identified prior local-CLI silence and faithful fresh-Colab bootstrap validation; preserve both.
Branch proposal: `feature/compact-colab-setup`.
Next: user plan approval, branch/claim survey, create_issue registration, isolated worktree setup, implementation and validation.

## Approved copy and scope clarification

User approved the plan and these two prose tiers, with the correction “locally or in HTML”.
Introductory: “Run this cell to install PyAutoLens and download the files needed for this notebook on Google Colab. If you’re running locally or in HTML, it leaves your installation unchanged.”
Advanced: “Set up Google Colab as in [the introductory notebook].”
Substitute each project’s name and actual introductory link. Cell title: “Set up Google Colab”. HTML support itself is future work, not part of this change.

Branch survey: PyAutoHands, autolens_workspace, autogalaxy_workspace, autofit_workspace, HowToFit, HowToGalaxy, HowToLens, autolens_assistant all on main, clean; no conflicting active claims. Proposed branch feature/compact-colab-setup.

## Implementation checkpoint — 2026-10-28

- User explicitly approved the wording including “locally or in HTML”; intro and advanced tiers retained.
- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/compact-colab-setup`, branch `feature/compact-colab-setup` in PyAutoHands, autolens_workspace, autogalaxy_workspace and autolens_assistant. No task code committed or pushed yet.
- Implemented locally: compact shared generator, maintained handwritten-cell expansion, option preservation, visible science tails, introductory/advanced copy; 15 Lens/Galaxy source setup sections reduced to import+call.
- Validation: PyAutoHands 581 tests passed (181.99s), including 25 setup tests; 25 setup tests rerun after final introductory-link correction. Six real introductory notebook previews generated and idempotency checked. Both real local setup imports/calls pass. Science AST unchanged in all 15 changed scripts; size guards and diff whitespace checks pass.
- Logs: worktree `logs/hands-tests.log`, `logs/readiness.json`. Previews: `/mnt/c/Users/Jammy/Science/scratch/compact_colab_setup_2026-10-28` (Windows `C:\Users\Jammy\Science\scratch\compact_colab_setup_2026-10-28`). Hosted Colab installation/rendering not tested.
- Refreshed Heart RED blocks shipping: `PyAutoArray: 4 uncommitted source change(s)`; `PyAutoGalaxy: 9 commit(s) behind origin`; `PyAutoLens: 7 commit(s) behind origin`; additional stale reason `release validation stale: source moved since rehearsal (PyAutoGalaxy, PyAutoLens)`. No override granted.
- Remaining: resolve/recheck Heart before shipping; finish assistant notebook path (its stdlib-only `autoassistant/to_notebook.py` is independent of Hands); regenerate and validate committed notebooks/markdown across all six project families in claimed worktrees; required workspace smoke; generator PR first, consumer PRs via ship-workspace. Assistant checkout still unchanged. Fit intro is `notebooks/overview/overview_1_the_basics.ipynb`, not root start_here.
- No merge or release authorized. HTML support remains future work.

## Final development checkpoint — 2026-10-28

This checkpoint supersedes the earlier blocked/in-progress checkpoint above.

Implemented the compact Colab setup rollout. Introductory notebooks use the approved two-sentence explanation (including “locally or in HTML”); advanced examples link back. Installation behavior and CPU/GPU options are preserved. HTML support itself remains future work.

## Pull requests
- [PyAutoHands](https://github.com/PyAutoLabs/PyAutoHands/pull/328)
- [autofit_workspace](https://github.com/PyAutoLabs/autofit_workspace/pull/178)
- [autogalaxy_workspace](https://github.com/PyAutoLabs/autogalaxy_workspace/pull/265)
- [HowToFit](https://github.com/PyAutoLabs/HowToFit/pull/77)
- [HowToGalaxy](https://github.com/PyAutoLabs/HowToGalaxy/pull/92)
- [autolens_assistant](https://github.com/PyAutoLabs/autolens_assistant/pull/167)
- [HowToLens](https://github.com/PyAutoLabs/HowToLens/pull/102)
- [autolens_workspace](https://github.com/PyAutoLabs/autolens_workspace/pull/604)
- [autogalaxy_assistant](https://github.com/PyAutoLabs/autogalaxy_assistant/pull/41)

Merge PyAutoHands first, then consumers; the Galaxy assistant guide also follows the Galaxy workspace. No merges or releases performed.

## Validation
- Shared generator: 584 tests pass, including 28 focused setup tests; tenant-firewall check passes after moving project metadata into configuration.
- All six families regenerated: 633 notebooks, 632 compact setup cells and one prose-only notebook. Scientific cell sources unchanged; setup normalization idempotent. Assistant adds one generated compact notebook with existing execution outputs preserved.
- Workspace smoke: Lens 42 scripts + 2 notebooks; Galaxy 14 + 2; Fit 8 + 2; HowToFit 19 scripts; HowToGalaxy 32; HowToLens 50 — all pass.
- Lens assistant: 11 focused tests pass; isolated pinned-runtime benchmark module 12 pass. Full suite: 263 pass, 1 skip, 1 xfail, with one interpreter-path assertion subsequently passing in the canonical-path preflight rerun (4 pass).
- Galaxy assistant: Colab context mapping/cap check and documentation diff review pass.
- Independent generator review finding fixed and rechecked CLEAN. Fresh-Colab behavior tested with simulation; hosted Colab installation/UI not exercised.

## Heart development override
User: “I authorize you to continue despite RED”. Exact reasons retained:
- PyAutoArray: 4 uncommitted source change(s)
- PyAutoGalaxy: 9 commit(s) behind origin
- PyAutoLens: 7 commit(s) behind origin
- release validation stale: source moved since rehearsal (PyAutoGalaxy, PyAutoLens)

This authorizes development shipping only; no readiness promotion, merge, release or CI bypass. The initial Hands CI failure was the tenant firewall; fixed in a405d14, local full suite and firewall pass. Fresh CI remains subject to review before merge.

Additional inventory cleanup: autogalaxy_assistant environment guide still taught the duplicated bootstrap. Its isolated branch claim was surveyed with no conflict; the documentation-only correction is included in the all-project rollout.

## Partial merge — human /prm

- PyAutoHands: MERGED — https://github.com/PyAutoLabs/PyAutoHands/pull/328
- autofit_workspace: OPEN — https://github.com/PyAutoLabs/autofit_workspace/pull/178
- autogalaxy_workspace: MERGED — https://github.com/PyAutoLabs/autogalaxy_workspace/pull/265
- HowToFit: OPEN — https://github.com/PyAutoLabs/HowToFit/pull/77
- HowToGalaxy: OPEN — https://github.com/PyAutoLabs/HowToGalaxy/pull/92
- autolens_assistant: MERGED — https://github.com/PyAutoLabs/autolens_assistant/pull/167
- HowToLens: OPEN — https://github.com/PyAutoLabs/HowToLens/pull/102
- autolens_workspace: MERGED — https://github.com/PyAutoLabs/autolens_workspace/pull/604
- autogalaxy_assistant: MERGED — https://github.com/PyAutoLabs/autogalaxy_assistant/pull/41

Every run/job for each current head was checked. Five fully green PRs merged in dependency order. Four remain open because their `smoke / smoke` job was skipped by the shared workflow change filter for generated-notebook-only changes; skipped is not a passing test result. Their local smoke suites passed during development. No failed jobs. Issue and Mind task remain open; worktree and claims retained. No release.
