# cortex-checkin-p2-the-door

Phase 2 of the `cortex-checkin` epic: the `/cortex` check-in door — the single
surface the human uses to check in on the science.

## What shipped

- **PyAutoBrain#350** — merged `9a039d92a5ac2c9c1ebce52636bc3b42acedd4e8`
- **PyAutoCortex#11** — merged `284097de3787aac22156dd1337e2c6749a9d5088`

Issue: PyAutoBrain#349 (closed completed 2026-09-04).

The `checkin` door lands in `agents/conductors/cortex/_cortex.py`: pull every
active project through its own sync CLI, score every live run against its
pre-registered witness, move what came back to `awaiting-ruling`, re-render the
board and push the ledger. `skills/cortex/*` and `skills/COMMANDS.md` are
rewritten around it, the slash command is installed (`.claude/skills/cortex`,
`.codex/skills/cortex`), and PyAutoCortex's `README.md` / `AGENTS.md` /
`REFERENCE.md` describe the door as the interface.

## Merge notes

Merged Brain before Cortex, after phase 1. GitHub retargeted both PRs from the
phase-1 branch to `main` automatically once phase 1 merged — no manual
`gh pr edit -B main` was needed.

PyAutoBrain#350: `Brain Tests` green on 3.12 and 3.13, `docs / docs-build`
green. PyAutoCortex#11's effective diff against `main` is three documentation
files (`AGENTS.md`, `README.md`, `REFERENCE.md`), which match no path filter in
either Cortex workflow, so **no run fired** — path-filtered by design, not a
missing or skipped check.

## Heart

RED at merge time, acknowledged by the human on 2026-09-04: "release validation
FAILED (stage integrate)"; "PyAutoArray: open PR 12d old". Both are
release-chain facts about other repos; neither PyAutoBrain nor PyAutoCortex is
in the release chain. No `pending-release:` obligation — both are organ repos.

## Tests

Brain 874 passed / 3 failed at ship time — one (`test_gh_surface::
test_every_gh_driving_skill_points_at_the_mapping`) was this branch's and was
fixed; the two `test_branch_sweep` failures reproduce unchanged on the phase-1
base and are pre-existing. Targeted re-run of `test_cortex_conductor` +
`test_skill_install` + `test_gh_surface`: 68 passed. PyAutoCortex: `cortex.py
check` OK, 115 passed, dashboard current.

## Original prompt

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
Issued: 2026-09-03

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
