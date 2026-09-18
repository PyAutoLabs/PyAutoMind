## Remote sessions (Claude Code on web and mobile)

Three facts, measured in a web/mobile container. A session holding several
organs is cwd'd at the repos' *parent*, where no project hook fires, so
nothing has set it up — this block is what does.

- **Bootstrap in the first turn, unconditionally** — before the first test
  command, not as a remedy: `bash PyAutoMind/scripts/session_bootstrap.sh`
  (`--check` reports only). It supplies pytest/PyYAML/xdist and **unshallows
  the clones**, without which `git merge-base --is-ancestor` calls a merged
  branch "not an ancestor" and the close-out acts on it.
- **Run the suite in parallel**: `python3 -m pytest -q -n auto` (4 cores,
  ~3.5x).
- **There is no `gh`, and installing one does not help** — it authenticates,
  then 403s every repo-scoped call through the egress proxy. GitHub is the
  `mcp__github__*` tools; `PyAutoBrain/skills/GITHUB_ACCESS.md` maps each
  `gh` operation onto its tool and is the one full page on the subject.
