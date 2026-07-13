## brain-agent-commands
- issue: https://github.com/PyAutoLabs/PyAutoBrain/pull/16
- completed: 2026-07-07
- repos: PyAutoBrain (PR #16, squash-merged); PyAutoMind (ROUTING pointer + registry)
- branch: feature/brain-agent-commands
- validation:
  - `check_skill_line_counts.sh`: all 24 primary skill files ≤200 lines
  - installer discovery: all 9 verbs → flat `~/.claude/commands/<verb>.md` symlinks resolve
  - no-bypass grep: every command body routes via `pyauto-brain` or `start_dev`
- notes: |
    Thin command veneer over the existing bin/pyauto-brain router — the Brain is
    implicit. Real conductors: /feature /build /health. Work-type entries (route
    through start_dev pre-tagged, no fictional agent): /bug /refactor /docs
    /research. NL router /route + debug passthrough /brain. Shared prose in
    PyAutoBrain/skills/COMMANDS.md (reference-only). Follow-ups: promote
    bug/refactor/docs/research to dedicated conductors; reconcile /health with
    /health_check and /pyauto-status.

## Original prompt

# Concise PyAutoBrain agent commands (the command veneer + NL router)

Give the PyAuto organism a thin, human-friendly **command surface** over the
already-existing PyAutoBrain router (`bin/pyauto-brain`). The Brain should be
implicit: users type short verbs (or plain natural language) and the Brain routes
to the right specialist agent — they never have to say "PyAutoBrain".

> Design sentence: **Users speak in short commands; PyAutoBrain performs the routing.**

## Original request (verbatim)

Set up concise PyAutoBrain agent invocation commands.

The Brain should be implicit. Like a human: you don't say "Brain, activate the
visual cortex" — you say "look at this", and your brain routes it. Normal usage
should never mention the Brain. Desired user-facing commands:

    /health /build /feature /bug /refactor /docs /research

Internally every one routes through PyAutoBrain to the appropriate specialist
agent, e.g. `/health -> PyAutoBrain -> Health Agent -> PyAutoHeart`. Commands are
user-facing shortcuts only; they must **not** bypass PyAutoBrain.

Also support **natural-language routing** via an optional router command
(`/route` or `/brain`) that infers the agent from the request:

    /route Fix failing tests        -> bug / health
    /route Implement issue #417     -> feature
    /route Publish PyAutoLens       -> build

Keep a lower-level debugging door (`/brain <agent>`) for explicit invocation.

Command responsibilities:

- `/health`   — health readiness, GREEN/YELLOW/RED, PyAutoHeart checks.
- `/build`    — build, release, shipping, PR/deployment execution via PyAutoBuild.
- `/feature`  — new capabilities, task selection/phasing, start_dev workflow.
- `/bug`      — regressions, failing tests, incorrect behaviour, issue triage.
- `/refactor` — architecture cleanup, internal restructuring, no behaviour change.
- `/docs`     — documentation, examples, notebooks, tutorials.
- `/research` — investigation, design notes, scientific background, pre-impl analysis.

Requirements: preserve the architecture (never bypass Brain); minimise tokens
(each command file short — under 100 lines where possible, definitely under 200;
no duplicated architecture prose — factor shared rules into a common doc); keep
Brain implicit; support NL routing; install into the correct canonical location
with no stale duplicate copies (update install scripts/symlinks if needed);
update docs; validate command discovery + that no command bypasses Brain. One PR
titled "Add concise PyAutoBrain agent commands".

## Approved design (from analysis of the current system)

The Brain already routes: `PyAutoBrain/bin/pyauto-brain <agent>` dispatches to
conductors (`feature`, `build`, `release`, `health`) and faculties (`vitals`),
and `PyAutoMind/ROUTING.md` already maps the work-type taxonomy
(feature/bug/refactor/docs/test/release/maintenance/research) to Brain agents.
So this task is a **thin honest veneer over an existing router**, not seven new
agents. Only `feature`, `build`, `health` have real conductors today;
`bug/refactor/docs/research` do **not** — they must not pretend to.

Ship, in **one PR**:

1. **`/route` (or `/brain <text>`) — the star.** A natural-language entry that
   self-classifies the request to a work-type and routes it. This is the
   "look at this" path. Lean on the existing `start_dev` / Feature-Agent
   classifier rather than re-inventing classification.
2. **Real verbs → real conductors.** `/feature`→`pyauto-brain feature`,
   `/build`→`pyauto-brain build`, `/health`→`pyauto-brain health` (→ vitals →
   Heart). `/health` becomes the human front door and *calls* the faster sweeps
   (`health_check`, `pyauto-status`) as legs of its loop rather than competing
   with them.
3. **Work-type verbs → `start_dev` pre-tagged.** `/bug /refactor /docs /research`
   enter the existing Brain feature-flow with their PyAutoMind work-type fixed —
   still through the Brain, so nothing is bypassed — documented as work-type
   entries **until** dedicated conductors earn promotion (tracked follow-ups).
4. **`/brain <agent>` debug passthrough** — execs `bin/pyauto-brain "$@"` raw.

Mechanism: each verb is a thin `PyAutoBrain/skills/<verb>/<verb>.md` command file
(the installer already turns `skills/<name>/<name>.md` with no `SKILL.md` into a
flat `~/.claude/commands/<name>.md`). Shared architecture prose lives in **one**
`COMMANDS.md` referenced (not copied) so files stay short and pass
`bin/check_skill_line_counts.sh`. Location = **PyAutoBrain** (the router). Do not
place stale copies in `admin_jammy` (vestigial) or hand-edit `~/.claude`.

Divergences from the raw spec: do **not** ship 7 co-equal commands (4 have no
agent); make the NL router primary, not optional; resist creating 4 new
conductors — add bug/refactor/docs/research as classifications first, promote
later.

## Follow-ups (not this PR)

- Promote `bug` / `refactor` / `docs` / `research` from work-type entries to
  dedicated PyAutoBrain conductors, each when its behaviour earns a front door.
- Reconcile `/health` with `/health_check` and `/pyauto-status` so there is one
  obvious health front door.

Target repo: **@PyAutoBrain** (command surface + router + docs). Touches
`PyAutoMind/ROUTING.md` docs only if the routing table needs a pointer to the
command surface.
