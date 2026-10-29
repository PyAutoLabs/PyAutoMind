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

## Scope

`pyauto-brain cortex birth <key> --category active|development --summary "<one line>"
[--dataset <sample>[/<lens> ...]] [--simulator <type>/<lens> [--dataset-types ...]] [--apply]`:

- scaffold `Science/<category>/<key>/` from a project template kept beside the conductor
  (AGENTS.md/CLAUDE.md skeleton, `wiki/project/state.md`, `.gitignore`, `config/`, `scripts/`,
  `hpc/` with `sync`, `sync.conf` from the example, `batch_cpu/`, `batch_gpu/`); the template is
  derived from the current best project (`active/euclid_detailed`) with project specifics stripped;
- seed `dataset/` by copying from `Science/dataset/<sample>` or by running
  `Science/simulators/<type>/<lens>.py --dataset-path dataset`;
- add the `projects.yaml` row (`ral_root` mirroring the category) and create the ledger with
  `cortex.py new`, on a `claude/birth-<key>` branch: an add-only birth diff, which lands by itself
  under the existing ledger-merge rule;
- dry run by default; `--apply` writes. It never creates a GitHub remote or touches RAL; it prints
  the `gh repo create` / `hpc/sync push-data-init` lines for the human;
- afterwards `cortex drift` is clean for the new project.

## Out of scope

Moving trees on RAL; output summaries on the board (draft/feature/cortex/output_summary.md).
