# Codex token-efficiency workflow

- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/409
- pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/387
- merge: `0a2174996722e505c6958cd565080f08c4bbfe06`
- shipped: 2026-09-18
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/387

## What shipped

- Split model delegation by provider while preserving Claude's Fable → Opus,
  Opus → Opus, Sonnet mechanical-floor, heartbeat, tutorial, bundle, and
  Cortex behavior. Codex now performs routine sequential work directly and
  delegates only bounded parallel, context-isolation, or independent-review
  work.
- Reduced `skills/WORKFLOW.md` from 22,095 to 5,034 bytes and moved conditional
  provider detail into the linked 4,159-byte `MODEL_DELEGATION.md`; shortened
  four relevant skill discovery surfaces.
- Added a safe, idempotent workspace-root policy installer that preserves
  symlinks, migrates both known legacy policy blocks, and fails closed on
  malformed or unordered markers.
- Added the standard-library, explicit-file `bin/codex_usage.py` report and
  comparison protocol. It reports the final cumulative snapshot, keeps cached
  input and reasoning as subsets, records model/effort changes and coordination
  counts, and leaves incomplete or ambiguous aggregation unknown.

## Validation

- Full PyAutoBrain suite: 915 passed.
- Focused usage, installer, and policy suite: 41 passed.
- Four changed skills passed `quick_validate`.
- Live explicit-rollout smoke matched input 49,762,616; cached input 48,107,520;
  uncached input 1,655,096; output 130,262; reasoning output 61,897; total
  49,892,878; and 80 collaboration calls including one spawn.
- Independent working-tree review: CLEAN; post-commit review surface contained
  no load-bearing claims to falsify. All GitHub jobs passed on reviewed head
  `a7d8fce53a2e497565cbacabea6900d6cd3473b3`.

## Heart RED override

The live human authorized `yes  commit, push and open the PR for` after the
exact RED reasons were reported: `install verification FAILED (testpypi; checks
F)` and `release validation FAILED (stage integrate)`. The contemporaneous
YELLOW reason was `manifest drift: remote-session blocks (generated) — 2
mismatch(es) vs PyAutoMind/repos.yaml`. This permitted development shipping
only. It did not resolve Heart, authorize release, or bypass CI. The later
explicit `merge` command and green checks separately authorized the merge.

## Activation

After the merge, the canonical workspace-root policy was updated with
`PyAutoBrain/bin/install.sh --write-workspace-policy` and verified with
`--check-workspace-policy`; unrelated root instructions and Claude policy were
preserved.

## Original prompt

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
