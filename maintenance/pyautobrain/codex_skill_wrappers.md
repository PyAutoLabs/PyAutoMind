# Add Codex wrappers for PyAuto agent workflows

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoBuild
- autolens_profiling
- admin_jammy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Original request

> yes, make SKILL.md wrappers for PyAutoBrain and any other repos you see a Claude bias

## Scope

Make the PyAuto organism's reusable agent and workflow surfaces discoverable
and runnable in Codex without weakening their existing Claude Code behavior.
Start with every public PyAutoBrain conductor and faculty exposed by
`bin/pyauto-brain`, then audit the canonical skill roots handled by
`PyAutoBrain/bin/install.sh` for Claude-only discovery or installation paths.

Keep canonical workflow bodies single-sourced. Codex `SKILL.md` files should be
thin wrappers around existing command or workflow documentation and deterministic
CLI entrypoints, not copied implementations. Preserve existing Claude commands
and skills while adding equivalent Codex discovery and installation behavior.

## Acceptance criteria

- Codex can discover an intake workflow and every public PyAutoBrain agent.
- Existing Claude slash commands continue to work from their current bodies.
- The installer supports both Claude and Codex skill destinations without
  creating duplicate canonical workflow prose.
- The audit covers only the canonical installer roots and reports any remaining
  intentional harness-specific surfaces.
- Automated checks validate wrapper metadata, links, line-count constraints,
  and installer behavior without modifying a developer's live skill directories.
