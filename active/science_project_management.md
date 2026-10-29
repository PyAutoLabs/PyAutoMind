# Cortex as the Science project manager: drift check and project birth

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
Issue: PyAutoLabs/PyAutoBrain#543

## Original request (verbatim)

"5) Bring this all together with PyAutoCortex which needs to become the main tool to manage Science
projects, its meant to be but hasnt been used as such for a while."

Follow-up (2026-10-29), after the Science clean-up session proposed next steps
(1 push the path-fix PR, 2 a drift check comparing the Science folders to the register,
3 a new-project command that scaffolds a project in active/ or development/, seeds it from
dataset/ or simulators/ and registers it in one step): "yeah do it".

## Context

The Science folder (`/mnt/c/Users/Jammy/Workspace/Science`) was reorganised on 2026-10-29:
`development/` holds software-development projects, `simulators/` holds the standard simulated
lenses (shared `--dataset-path` / `--dataset-types` CLI, default output `dataset/simulated/`),
`profiling/` holds RAL pull mirrors with a generated `INDEX.md`, and `Science/AGENTS.md` names
the Cortex as the project register. Before that, the move from `C:\Users\Jammy\Science` to
`Workspace\Science` had left most `projects.yaml` `local_path`s pointing at nothing, unnoticed for
weeks: `pull --dry-run` reached 3 of 12 active projects. PyAutoCortex#77 fixes those paths and
retires `subhalo`, `cowls`, `cowls_ansofi`; it lands before this work.

The failure mode to prevent: the register and the Science tree silently diverge. And starting a
project today is manual copying from an older project, so new projects never get a row.

## Scope

### Phase 1 — drift check (conductor verb, report-only)

`pyauto-brain cortex drift [--science-root PATH] [--json]`, also summarised in `census` and
`checkin` when the Science root is on this machine (laptop-only, like `pull`; elsewhere a one-line
skip notice, never a failure). It writes nothing. Findings:

1. a project folder under `active/`, `development/`, `complete/`, `archive/` with no row
   (matched by `local_path`);
2. a non-retired row whose `local_path` does not exist;
3. category vs status: rows under `active/` or `development/` should be `active|dormant|planned`;
   under `complete/` or `archive/` should be `retired|dormant`;
4. (warning) a non-retired row whose `ral_root` category differs from its `local_path` category
   (decision 61: one layout on both machines).

The Science root is derived from the `local_path`s (`<root>/<category>/<project>`), overridable
with `--science-root`; no new absolute path enters the organism outside `projects.yaml`.
Rows under `~/Code/PyAutoLabs` (repo-backed campaign roots) are exempt from 1/3/4.

### Phase 2 — project birth (conductor verb)

`pyauto-brain cortex birth <key> --category active|development --summary "<one line>"
[--dataset <sample>[/<lens> ...]] [--simulator <type>/<lens> [--dataset-types ...]] [--apply]`:

- scaffold `Science/<category>/<key>/` from a project template kept beside the conductor
  (AGENTS.md/CLAUDE.md skeleton, `wiki/project/state.md`, `.gitignore`, `config/`, `scripts/`,
  `hpc/` with `sync`, `sync.conf` from the example, `batch_cpu/`, `batch_gpu/`), template derived
  from the current best project (`active/euclid_detailed`) with project specifics stripped;
- seed `dataset/` by copying from `Science/dataset/<sample>` or running
  `Science/simulators/<type>/<lens>.py --dataset-path dataset`;
- add the `projects.yaml` row (ral_root mirroring the category) and `cortex.py new` the ledger,
  on a `claude/birth-<key>` branch — an add-only birth diff, which lands by itself under the
  existing ledger-merge rule;
- dry-run by default; `--apply` writes. Never creates a GitHub remote or touches RAL (prints the
  `gh repo create` / `hpc/sync push-data-init` lines for the human).

## Out of scope

Moving trees on RAL; the human-readable dashboard work (draft/feature/cortex/output_summary.md).
