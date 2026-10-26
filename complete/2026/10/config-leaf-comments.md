## config-leaf-comments
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1732
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1733
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1733
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/656
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/656
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/667
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/667
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/802
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/802
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/264
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/602
- completed: 2026-10-26
- summary: Added 600 configuration comments and a standalone non-prior leaf-comment checker with focused regression tests. All 293 YAML mappings are unchanged. Full library suites: 8448 passed; downstream smoke 172 passed; workspace branch smoke 60 passed. Parallel Fit shared-output races and isolated Zeus order sensitivity reproduced on pristine HEAD; the full serial suite and every GitHub CI job passed. Workspace review was independently CLEAN.
- close-out: Human invoked /prm; every applicable CI run/job was green and all claimed branch tips are contained in main.
- cleanup-approval: Human approved deletion of completed-task worktrees and outputs.
- human-review: Merged unchanged, confirmed explicitly in this session.

## Original prompt

# Config yaml keys missing their one-line explanatory comment

Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1732
Type: maintenance
Target: autofit
Repos:
- PyAutoFit
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: safe
Priority: low
Status: issued
Consequence: glance
Witness: the uncommented-leaf-key check reports 0 across every library config/ folder (excluding priors/) after the sweep, and reports a non-zero count when run against main before it.
Review-minutes: 3
Unattended: ready

User request (verbatim): "can you have an issue which checks if the docs have comments in them (lots do, but look for missing one line comments)" — clarified: "I mean the config yaml files themselves which often have comments next to thing".

The packaged config yaml (general.yaml, visualize/*.yaml, non_linear/**, output.yaml, ...) under each library's config/ folder, and the workspace config/ copies, document most keys with a one-line # comment on or above the key saying what it controls and what values it takes. Some keys have no comment. Walk every config yaml (excluding priors/, whose keys are class/param names), list every leaf key with no comment on its own line or the line above, and add the missing one-line comments (short, in the same register as the neighbours). Add a small check (a test in PyAutoFit, or a script the sweep re-runs) that reports uncommented leaf keys so the gap does not reopen. Workspaces follow the packaged files: propagate the comments to autolens_workspace and autogalaxy_workspace config/ copies in the same pass. Follow-on from the config-priors-drift sweep (PyAutoGalaxy#618).

Witness: the uncommented-leaf-key check reports 0 across every library config/ folder (excluding priors/) after the sweep, and reports a non-zero count when run against main before it.

Phasing if split at start_dev: (1) PyAutoFit + PyAutoArray packaged config + the check; (2) PyAutoGalaxy + PyAutoLens; (3) the two workspace copies.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->
