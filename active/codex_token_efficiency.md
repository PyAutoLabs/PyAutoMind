# Improve Codex token efficiency without weakening Claude delegation

Type: maintenance
Target: organs
Repos:
- @PyAutoBrain
- @PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issued: 2026-09-18

## Request

> ok do all 5, but delegation works very well on claude so ensure we dont lose the delegation policy there.

Follow-up authorization:

> Allow a separate worktree

Implement the five approved Codex-efficiency changes while preserving the
effective Claude delegation policy and the Brain/Mind development workflow.

## Plan

1. Split delegation policy by provider in the workspace-root `AGENTS.md`,
   `PyAutoBrain/skills/WORKFLOW.md`, and dependent start/ship documentation.
   Preserve Anthropic's Fable → Opus, Opus → Opus, Sonnet mechanical-floor,
   and tutorial-prose behavior exactly. For OpenAI, make direct execution the
   default and delegate selectively for independent parallel work, noisy or
   long-running execution, and independent review.
2. Retain Brain/Mind routing, planning and approval gates, task registries,
   conflict-aware worktrees, Heart gates, and independent review. Reduce
   overhead without bypassing these controls.
3. Slim auto-loaded instructions and workflow prose by moving task-specific
   detail behind links, keeping skill descriptions short and unambiguous, and
   preserving generated blocks as authoritative rather than duplicating them.
4. Bound coordination: delegate with minimal relevant context, require concise
   structured returns, reuse a worker for coherent follow-ups, avoid repeating
   unchanged checks, and keep full execution logs outside chat while returning
   only decision-relevant excerpts.
5. Add a read-only, standard-library usage meter, tentatively
   `PyAutoBrain/bin/codex_usage.py`, with meaningful parser fixtures. It must
   read only explicitly selected rollout metadata, use the last cumulative
   counters, cache results separately, treat reasoning tokens as a subset of
   output, document explicit parent/child de-duplication and limitations, avoid
   raw conversation content and secrets, and report effort, model, duration,
   coordination counts, and tokens without inventing billing. Document a
   comparison across 3–5 completed tasks including outcome, corrections, and
   tokens. Astra Medium is already configured; do not add an unnecessary local
   configuration edit.

## Validation

- Run the relevant existing skill, installer, and documentation checks.
- Run focused fixture tests for the usage-meter parser, cumulative-counter
  handling, parent/child de-duplication, privacy boundary, and malformed input.
- Keep any workspace-root `AGENTS.md` update reproducible through an appropriate
  tracked PyAutoBrain documentation/install step rather than relying on an
  unexplained local-only patch.

## Branch and coordination

Use `feature/codex-token-efficiency` in an isolated worktree. Do not create the
worktree or modify source until `codex-hook-parity` releases its PyAutoBrain and
PyAutoMind claims, unless the user explicitly authorizes a coordinated
override. Do not broaden the survey to unrelated repositories.
