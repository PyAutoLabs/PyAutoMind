## worker-model-effort
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/672
- completed: 2026-11-18
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/673
- Shift workers and close-outs start as `claude --bg --model opus --effort medium` (`WORKER_MODEL`/`WORKER_EFFORT` in `_orchestrator.py`; `CLOSEOUT_MODEL = WORKER_MODEL`). Before this, workers passed no `--model` or `--effort` and inherited the CLI default (Opus on high).
- Human ruling 2026-11-18: spawned execution workers (Agent-tool subagents, shift workers, close-outs) default to Opus 5.5 at medium effort, whatever the session's own effort. Close-outs follow the workers. `skills/MODEL_DELEGATION.md` "Bounded worker contract" says so; an independent reviewer on another model leaves effort unset.
- Evidence: full Brain suite 2337 passed; a live `claude --bg --model opus --effort medium` spawn ran to `done`; the Fable 5.2 review's three lows (stale argv in the batch `AGENTS.md`, the live test's argv, a vacuous assert) were fixed before PR-open.

## Original prompt

# Spawned workers run Opus 5.5 at medium effort

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-18
Issued: 2026-11-18
Epic: autonomous-orchestrators
Consequence: glance
Witness: `python -m pytest tests/ -q -k "session_command or closeout_command or worker_model"` passes, with a test asserting both `session_command` and `closeout_command` argv carry `--model opus --effort medium`
Lane: local-dev
Unattended: ready

## Why

The human runs the judgment session at high effort on important work, but every
session it spawns inherits that cost. Shift workers start with
`claude --bg --name shift:<task> --permission-mode <mode> <prompt>`
(`agents/conductors/batch/_orchestrator.py`, `session_command`): no `--model`,
no `--effort`, so each one runs the CLI default (Opus on high). Close-outs pass
`--model opus` but no effort. Chat subagents get no effort from
`skills/MODEL_DELEGATION.md` either.

Human ruling (2026-11-18): spawned execution workers default to Opus 5.5 on
**medium** effort, whatever the session's own effort. Close-outs follow the
workers (medium), keeping the 2026-11-04 "same model as the workers" ruling.

## What

1. `_orchestrator.py`: `WORKER_MODEL = "opus"`, `WORKER_EFFORT = "medium"`;
   `session_command` and `closeout_command` both pass `--model WORKER_MODEL
   --effort WORKER_EFFORT`; `CLOSEOUT_MODEL` stays as an alias of
   `WORKER_MODEL` so stage-2 rows still record the model.
2. Tests for both argvs.
3. `skills/MODEL_DELEGATION.md`, "Bounded worker contract": one line saying
   Anthropic execution workers (Agent-tool subagents, shift workers,
   close-outs) are Opus at medium effort unless the human asks otherwise;
   independent reviewers on another model leave effort unset.
4. One line in `AUTONOMY.md` where shift worker sessions are described.

## Out of scope

- A per-brief override of model or effort (file separately if wanted).
- The watcher itself (Python, no model).
