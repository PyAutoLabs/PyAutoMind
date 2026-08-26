# PyAuto workflow skill ownership

Where each workflow skill lives and why. Each skill lives in the organ that
owns its responsibility (boundaries: `PyAutoBrain/AGENTS.md`,
`PyAutoHands/AGENTS.md`); command names are preserved across homes, and
discovery is wired up by `PyAutoBrain/bin/install.sh`. The relocation history
behind this layout is in git (PR #26 and the skill-redesign task, 2026-07).

- **Mind** = intent + task-registry state.
- **Memory** = accumulated knowledge (consulted for context).
- **Brain** = reasoning + how-work-gets-done; **owns the development workflow**.
- **Heart** = health / validation / readiness gates.
- **Build (Hands)** = **release/packaging executor only** (tag / notebooks / PyPI
  via `release.yml`). It owns **no** workflow skills; `ship_*` is feature-dev work
  that only *calls* Build's release step at release time.

| Skill | Home | Why it lives there |
|-------|------|--------------------|
| `create_issue` | `PyAutoMind/skills/` | the issue+registry **primitive** (Brain's `start-dev` delegates the issue write to it; runnable standalone) |
| `spawn` | `PyAutoMind/skills/` | template generation from the Mind's own tree |
| `start_dev`, `start_dev_for_user` | `PyAutoBrain/skills/` | classification/routing entry points |
| `plan_branches`, `start_library`, `start_workspace` | `PyAutoBrain/skills/` | planning + dev-cycle setup |
| `ship_library`, `ship_workspace` | `PyAutoBrain/skills/` | dev-workflow → Heart gate (Build only at release) |
| `run_queue` | `PyAutoBrain/skills/` | dev-workflow orchestration loop |
| `repo_cleanup`, `update_issue` | `PyAutoBrain/skills/` | between-tasks git hygiene / issue upkeep |
| `worktree_status` | `PyAutoHeart/skills/` | diagnostic |
| `dep_audit`, `verify_install`, `review_release`, `audit_docs`, `cli_noise_clean` | `PyAutoHeart/skills/` | read-only validation / readiness checks |
| `pre_build` | `PyAutoHands/skills/` | release execution (the only skill class Hands owns) |
| `profile_likelihood` | `autolens_profiling/skills/` | science profiling |

Retired: `pyauto-status` / `pyauto-status-full` became legs of `$health`
(`/health status`, `/health full`; long-form detail in their `reference.md`
files under `PyAutoHeart/skills/`); `handoff` was deleted — `active.md` is the
shared task state, so any environment resumes a task directly.

## Discovery

`PyAutoBrain/bin/install.sh` scans the `skills/` roots above, symlinks skills
into both Claude and Codex skill homes, and preserves commands in
`~/.claude/commands/`. Registry references stay workspace-root-anchored
(`PyAutoMind/active.md`, `PyAutoMind/complete/`,
`source PyAutoMind/scripts/prompt_sync.sh`), which resolve from any sibling
repo, so skills work identically from every home.

(`*/agents/openai.yaml` and the `SKILL.md` ↔ `<name>.md` pairs are bundled Codex
agent configs / dispatcher+body pairs, not separate skills. Long-form detail is
factored into per-skill `reference.md` files and the shared
`PyAutoBrain/skills/WORKFLOW.md`, keeping every primary skill file under 200
lines.)

## Validation

- `bash PyAutoBrain/bin/install.sh` → every `/command` resolves.
- `find <each skills dir> -type l` → no stray symlinks in source.
- `bash PyAutoBrain/bin/check_skill_line_counts.sh` → all primary workflow
  skill files within 200 lines.
