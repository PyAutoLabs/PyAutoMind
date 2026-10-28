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
