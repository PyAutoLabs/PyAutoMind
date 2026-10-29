# Cortex birth: scaffold, seed and register a Science project in one step

Type: feature
Target: cortex
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- science
- cortex
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-10-29
Issued: 2026-10-29
Issue: PyAutoLabs/PyAutoBrain#545
Parent: complete/2026/10/cortex-science-drift.md

## Original request (verbatim)

"5) Bring this all together with PyAutoCortex which needs to become the main tool to manage Science
projects, its meant to be but hasnt been used as such for a while."

Follow-up (2026-10-29), approving the proposed next steps including "a new-project command that
scaffolds a project in active/ or development/, seeds it from dataset/ or simulators/ and
registers it in one step": "yeah do it", then "Merge, then Phase 2".

## Context

Phase 1 (`cortex drift`, PyAutoBrain#544) shipped 2026-10-29: the register and the Science tree are
now compared on every census/check-in. Today a new project is started by hand-copying an older one,
so it gets no row and the drift check reports it as `unregistered`. Science layout:
`/mnt/c/Users/Jammy/Workspace/Science/{active,development,complete,archive,dataset,simulators}`;
simulators share `--dataset-path` / `--dataset-types` (Science/simulators/AGENTS.md).

## Scope (revised 2026-10-29, human-approved: "yes, file it and go")

Scaffolding stays with the domain assistant: `autolens_assistant` / `autofit_assistant`
`skills/start-new-project.md` is the single science-project skill, and the public assistants must
not learn the private Science tree or the Cortex. The Cortex adds only the registration half:

- `pyauto-brain cortex birth <key> --category active|development --assistant <name>
  --summary "<one line>" [--issue Repo#N] [--apply]`: checks `Science/<category>/<key>/`
  exists and has no row; derives `local_path`, `ral_root` (`<ral base>/<category>/<key>`, base
  from the other rows), `sync_cli` / `sync_verbs` from the scaffolded `hpc/sync`, `partition`,
  `witness_file` and `remote` (git origin or `none`); writes the row and runs `cortex.py new`
  on a `claude/birth-<key>` branch (an add-only birth diff, which lands by itself); then runs
  `drift` for the new project. Dry run by default. Never creates a GitHub remote or touches RAL;
  it prints those lines for the human.
- The Brain's `cortex` skill gains a "new project" section: run the assistant's
  `start-new-project` with the target `Science/<category>/<key>`, seed `dataset/` from
  `Science/dataset/<sample>` or `Science/simulators/<type>/<lens>.py --dataset-path dataset`,
  then `cortex birth`.
- Docs: Cortex REFERENCE.md (birth) and schema decision 63.

## Out of scope

Moving trees on RAL; output summaries on the board (draft/feature/cortex/output_summary.md).
