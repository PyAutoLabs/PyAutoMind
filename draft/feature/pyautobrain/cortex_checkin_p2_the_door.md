# `/cortex` — the one check-in door: pull every active project, score, render, push, hand back prompts

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `pyauto-brain cortex checkin --dry-run` lists every `status: active` project in `projects.yaml` with the exact `<local_path>/<sync_cli> pull` it would run and every live phase it would score; `pyauto-brain cortex checkin --apply --no-push` on the live tree pulls each (a failing pull is reported per project and does not abort the sweep), writes `<local_path>/.cortex/pull.json` for each project pulled, scores every submitted/running phase, applies `running → pulled → awaiting-ruling`, regenerates `dashboard.md`/`.html` (`--check` current), and prints a summary keyed BY PROJECT (state counts, live phases with health, the existing rule / launch / jobs prompts) that a fresh chat can paste from; with `--push` it commits the ledger diff on a `claude/checkin-<YYYY-MM-DD>` branch with explicit paths, pushes, and reports that `ledger_merge.yml` will land it; `~/.claude/commands/cortex.md` exists and `/cortex` in Claude reads `skills/cortex/SKILL.md`, whose body is the check-in sequence, not a verb menu; Brain + Cortex tests cover dry-run, per-project pull failure isolation, manifest write and the no-push path
Review-minutes: 20
Unattended: ready
Epic: cortex-checkin
Phase: 2
Filed: 2026-09-03

Phase 2 of `cortex-checkin`. Branch from phase 1's branches (stacked) if they
are unmerged. Two PRs (Brain, Cortex — the Cortex side is docs + a
`checkin` pointer in README/AGENTS + any `check` rule the manifest needs).

## The door — `pyauto-brain cortex checkin`

Composes the primitives phase 1 kept. Flags: `--dry-run`, `--apply`,
`--push` / `--no-push` (default: `--no-push` in a cloud session, ask-free
`--push` on a laptop where `gh auth status` succeeds — state the rule),
`--project <key>` to narrow, `--skip-pull` for an offline re-score.

1. **Sync.** Iterate `projects.yaml` rows with `status: active` (plus any row
   that owns a phase in `submitted|running`). For each, run
   `<local_path>/<sync_cli> pull` (the verb every CLI implements — verified
   2026-09-03 across all seven), streaming its output under a project
   heading. A non-zero exit is recorded per project and the sweep continues.
   After a successful pull write `<local_path>/.cortex/pull.json`
   `{project, pulled_at, cmd, rc, phases_live: [...]}` so the scorer's
   checkpoint leg stops reading UNOBSERVABLE everywhere except
   autolens_profiling (which already writes its own — do not clobber a
   richer manifest; merge keys).
2. **Score.** Run the decoupled `collect` scorer over every submitted/running
   phase; `--apply` performs the state moves. No batch record.
3. **Render + push.** `dashboard --apply`; then, with `--push`, in the Cortex
   checkout: `git checkout -b claude/checkin-<date>` from a fresh `origin/main`,
   commit the phase files + dashboard pages with explicit paths, push, and
   print the auto-merge expectation (`ledger_merge.yml`). If the diff
   classifies as code (`scripts/ledger_merge.py classify <paths>`), stop
   before pushing and say why. Never push `main` directly, never force.
4. **Summarise, by project.** For each active project: state counts, each
   live/awaiting/ready phase with its health verdict and the copy-ready
   prompt that already exists for that state (`_ruling_payload`,
   `launch_payload`, `_live_payload`), the project's `local_path`, `mirror`,
   `ral_root` and the run directories the scorer touched. Phase 3 enriches
   this; here it must at least exist and be keyed by project. Print it as
   the LAST thing so a chat sees it above the fold.

## Install `/cortex`

The slash command is advertised in `skills/COMMANDS.md` but
`~/.claude/commands/cortex.md` does not exist. Rewrite
`skills/cortex/SKILL.md` + `cortex.md` so the body IS the check-in
sequence (run `checkin`, read the summary, offer the prompts; the individual
verbs become an appendix) and install the symlink the same way the other 29
commands are installed (find the installer — PyAutoBrain owns discovery per
PyAutoMind/AGENTS.md — and add `cortex`; if installation is a documented
manual step, do it and document it). Codex discovery likewise if the others
have it.

## Guardrails

Never arm a timer, subscription, cron or loop; the door runs once and ends.
Never touch `rulings/` (append-only, human's turn). `hpc/sync pull` may take
minutes per project — stream output, do not buffer. RAL is reached only via
the projects' own CLIs; the door adds no SSH of its own.
