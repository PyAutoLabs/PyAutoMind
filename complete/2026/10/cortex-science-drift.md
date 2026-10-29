## Outcome

Phase 1 of making the Cortex the Science project manager shipped on 2026-10-29. The new read-only `pyauto-brain cortex drift [--science-root PATH] [--json]` verb compares the laptop Science tree (`<root>/<category>/<project>`, root derived from the rows' `local_path`s) with `projects.yaml`.

- **Errors:** unregistered `active/` or `development/` folders; vanished `local_path`s; category vs status; a derived root that no longer exists while other rows' folders do.
- **Warnings:** unregistered `complete/` or `archive/` storage folders; `ral_root` in a different category.
- `census` and `checkin` print a one-line summary. `census()` stays drift-free, so the CI-rendered board is machine-independent.
- Paths compare after `realpath`, so the `~/Science/Science` launch symlink matches.
- Schema decision 62 records `development/` as a Science category.

Shipped with PyAutoCortex#77: `local_path`s moved to Workspace/Science; `subhalo`, `cowls` and `cowls_ansofi` retired.

Real tree on merged main: 0 errors, 11 warnings (four development projects and `euclid` with RAL under `active/`, `euclid_dr1` top-level on RAL, five unregistered storage folders). The pre-fix register gave 12 errors and exit 1: this is the incident the verb exists for.

## Review

Independent review FINDINGS, all addressed before PR: symlinked root, `checkin --dry-run` line, messages. Stated limit, tested: detecting the laptop needs some row's folder to exist (the repo-backed rows provide it).

## Heart

Shipped under a live-human development-only Heart RED override ("I authorize"). RED reasons concerned PyAutoArray, PyAutoGalaxy, PyAutoLens and release validation, not these repos. Merged by the human's explicit "Merge, then Phase 2". PyAutoCortex#78 had no CI (docs paths unwatched) and was merged on an explicit human yes.

## Remainder

Phase 2 (`cortex birth`) re-filed as `draft/feature/cortex/cortex_birth.md`.

## Original prompt

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
