# Docstrings printed as --help still carry incident history

Type: docs
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: each tool's `--help` names no date, milestone tag or incident; the suite passes.
Review-minutes: 0
Unattended: ready
Lane: any

Docstrings printed as --help still carry incident history

Type: docs
Target: PyAutoBrain
Lane: any

PyAutoBrain#701 moved dated incident history out of comments and docstrings but left about 18 module docstrings alone because they are printed as `--help` (`description=__doc__`), so changing them changes program output. In @PyAutoBrain these are: `agents/_repo_paths.py`, `agents/conductors/clone/_clone.py`, `bin/check_boundary.py`, `agents/conductors/community/_community.py`, `agents/conductors/docs/_docs.py`, `agents/conductors/hygiene/_hygiene_extras.py` (a "2026-08-03: tfp-nightly" anecdote), `_hygiene_optdeps.py`, `_hygiene_repos.py`, `agents/conductors/workspace/_workspace.py`, `bin/codex_usage.py`, `bin/lane_backfill.py` ("M1.3, slice 2 … 12 of ~270 … since 2026-11-03"), `bin/project_discovery.py`, `bin/regroup_workspace.py`, `bin/shift_ledger.py`, `bin/sync_feedback.py`, `bin/workspace_instructions.py`, `board/_board.py`, `board/_publish.py`; plus the printed first paragraph of `_hygiene_ci.py` and first lines of `_hygiene_tokens.py` and `bin/dataset_provenance.py`. Also message strings that carry tags (for example "ruling e, 2026-11-19" in the batch worker notes, "(M2.3)" in digest messages). Rewrite each to say what the tool does, in the present tense. This changes `--help` and message text, so check for tests that pin the wording.

Witness: each tool's `--help` names no date, milestone tag or incident; the suite passes.

<!-- formalised by the Intake (Conception) Agent on 2026-11-22 from file:/tmp/claude-0/-home-user/8f120f5d-ca18-5874-ae34-519506e9751b/scratchpad/prompts/4.txt -->
