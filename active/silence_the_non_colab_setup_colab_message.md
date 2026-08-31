# Silence the non-Colab setup_colab() message on CLI runs

Type: feature
Target: PyAutoNerves
Repos:
- PyAutoNerves
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: a plain CLI run of a workspace `start_here.py` prints no "You are not running in a Google Colab environment" block on stdout, while the notebook-facing path still surfaces it; asserted by a test in `PyAutoNerves/test_autonerves/test_setup_colab.py`.
Review-minutes: 0
Unattended: ready
Issued: 2026-08-31

# Silence the non-Colab setup_colab() message on CLI runs

Type: feature
Target: PyAutoNerves
Difficulty: small
Autonomy: safe
Priority: normal
Witness: a plain CLI run of a workspace `start_here.py` prints no "You are not running in a Google Colab environment" block on stdout, while the notebook-facing path still surfaces it; asserted by a test in `PyAutoNerves/test_autonerves/test_setup_colab.py`.

Every workspace `start_here.py` calls `setup_colab.for_<project>(...)` unconditionally at the top of the script, before any imports. Outside Colab that call falls into the `except ImportError` branch of `_colab_setup` in `PyAutoNerves/autonerves/setup_colab.py` and `print()`s a five-line reassurance:

    You are not running in a Google Colab environment so cannot use the setup_colab() function.

    You should therefore have <project> installed locally in your environment already (e.g. via pip or
    conda) and can run the rest of your script normally.

    You may now continue running your script or Notebook.

For a command-line user this is noise on **every single run, forever**. In a Jupyter notebook it earns its place: a user who has just executed the Colab setup cell locally does need to be told the cell was a no-op and that they can carry on.

The design question this task exists to answer is: **how does a user who genuinely needs this message still get it, without it printing on every run?** Weigh at least these, and pick one with a stated reason rather than silently defaulting:

- Detect execution context (notebook / IPython kernel vs plain interpreter) and stay silent on the command-line path.
- Print once per process or per session, deduped the way `autonerves/workspace.py::_warn_once` already dedupes the workspace version warning.
- Suppress after a persisted marker shows the user has seen it once.
- Demote to `logger.debug` / `logger.info`, so it is available when asked for and invisible otherwise.
- An explicit opt-out environment variable / config key, as a fallback or in combination.

Notes for whoever picks this up:

- The message is a `print()`, not a warning — it cannot be silenced with `warnings.filterwarnings`.
- The `warnings.warn(message)` line that appeared directly above this block in the reported terminal output is a **different emitter**: `autonerves/workspace.py::_warn_once`, the workspace-staleness version check. It is not part of this task, though it is worth confirming the chosen approach here does not conflict with the dedup pattern already used there.
- The change lands wholly in `autonerves/setup_colab.py`. The workspace `start_here.py` bootstrap blocks should not need editing, and preferably should not be — the same block is duplicated across every topic folder of every workspace repo, so a fix that requires touching them does not scale.
- The message is shared by all six registered projects in the `_PROJECTS` table, so whatever is chosen applies uniformly, not per project.

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs-autolens-workspace/9efe8f02-1886-4aa0-954b-2cbff0eff026/scratchpad/colab_noise.md -->
