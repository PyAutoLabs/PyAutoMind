- completed: 2026-08-27
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/303 (closed)
- prs:
  - https://github.com/PyAutoLabs/PyAutoBrain/pull/305 (merged, `ef887f8`)
- classification: feature (PyAutoBrain; phase 1 of 2)
- summary: |
    The Brain board is the morning door, and on the surface it is actually read
    from — a session on a phone — eleven of its legs were dark: they read GitHub
    through `gh api`, and a remote session has no `gh`. Phase 1 gives the
    renderer a way to be handed what it cannot fetch, and proves it on the seven
    overnight rows.

## The shape, and why it is a seam

`mcp__github__*` is an **agent** capability. `board/_board.py` is a subprocess
and cannot reach it however it is invoked — which is why "port the board to
MCP" was never a substitution and always a seam:

```
pyauto-brain board --github-data <file>      # {endpoint: response}
```

Keyed by the endpoint string exactly as `gh_json()` receives it, so injected and
live data are interchangeable by construction rather than by convention: a key
that drifts from its call site simply misses, and a miss is a state the board
already renders honestly. The `gh` path is untouched — no flag, no injected map,
identical behaviour on a developer box.

The `/board` skill (which *is* the agent) gathers when `command -v gh` fails,
writes the file, and invokes the renderer. The file's shape is a documented
contract in `board/AGENTS.md`, because it outlives whoever wrote it.

## The three rules, all one invariant

Restatements of what the 2026-08-26 degraded-render work established:

1. A **miss is *could not ask*** (`None`) — never an empty answer. That is
   exactly how a board goes green by never looking.
2. An explicit **`null` means the gatherer's own fetch failed** — same outcome,
   stated rather than implied. `{"workflow_runs": []}` is the opposite: a real
   answer that happens to be empty.
3. A **malformed or missing file is fatal, not degrading.** Every leg reading
   `could not read` renders as a GitHub outage; if the truth is that the
   gatherer wrote a broken file, the board must say so instead.

## Key traps

- **The contract includes the field names.** Store each response as GitHub
  returns it. The overnight row's age reads `created_at`; the first
  hand-written fixture used `updated_at`, and the row rendered `success (?)` —
  which reads as a rendering bug rather than a bad input file. Documented in
  both places and asserted in the tests, because the next gatherer will guess
  the same way.

- **Phase 0 was a probe, not a design.** The prompt offered three options and
  said to probe before building; the probe (2026-08-27) returned 200 on `/user`
  and `/rate_limit` and **403 on every repo-scoped path**, which killed options
  2 and 3 and selected this one. Recorded in the parent prompt so the next
  session starts at the design. If an org admin ever connects the Claude GitHub
  App, `gh_json()` becomes a plain REST helper on every surface and this seam is
  deletable — which is why it is small.

- **Proved on the surface it exists for.** The end-to-end check ran in this
  session, which has no `gh`: one injected endpoint rendered
  `✓ PyAutoLabs/PyAutoBrain/nightly-release.yml — success (6h)` with its run
  link while the six uninjected legs still said `could not read`, and the render
  stayed degraded and non-green.

- **PyAutoMind's PR-open event fired no workflows — twice, in one session.**
  Both close-out PRs (#354, #357) showed **zero** check runs at open, on diffs
  matching three path filters plus `spawn_drift.yml`, which has none. Actions
  was healthy throughout: other PRs on the repo ran normally in the same
  minutes, and a `workflow_dispatch` started instantly. #354 recovered the
  moment an unrelated push produced a `synchronize` event, which fired all four
  at once.

  The 2026-08-26 record logged this as a one-off GitHub-side miss; at two
  occurrences it is worth treating as a repeatable condition on this repo
  rather than a blip, and the response is the one that record named: **verify
  by dispatch, never merge unchecked**. Note that only `firewall_gate.yml` is
  safely dispatchable here — `lifecycle_drift.yml` and `dashboard_refresh.yml`
  self-heal `main` on a manual dispatch (they reset to `origin/main` and push),
  so dispatching them proves nothing about the branch and writes to main.
  Where they cannot be dispatched, run their commands locally — they are the
  same four: `lifecycle.py check`, `lifecycle.py index --check`,
  `registry_toc.py --check`, `intake dashboard --check`.

## Validation

569 PyAutoBrain tests (`-n auto`), `ruff` clean. 8 new tests, fixture-driven,
with `BOARD_GH` pointed at a nonexistent command so a leak to a live `gh` fails
loudly rather than answering.

## Scope note

A full seven-row live render was not demonstrable from the shipping session:
three of the watched repos (PyAutoHeart, PyAutoHands, autolens_assistant) were
outside its repository scope, so the gatherer could not reach them. The
mechanism is identical per leg.

## Follow-up

`draft/feature/pyautobrain/board_without_gh_phase2_legs.md` — the remaining four
legs (versions, community, resume, upkeep), now unblocked. Two of them live in
scripts rather than in `_board.py`, so the phase's real question is whether each
script grows its own seam or the board gathers for them; answer it in this
contract's terms rather than inventing a second shape.

## Original prompt

# Board phase 1: the injection seam, proven on the overnight legs

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27
Parent: draft/feature/pyautobrain/board_without_gh.md

Phase 1 of the board's gh-less work. The parent prompt holds the design, the
measurements and the 2026-08-27 probe that selected this option; read it first
and do not re-derive them.

## Scope

Build the seam and prove it on **one** leg family — the seven `overnight:
could not read <repo>/<workflow>` rows, the largest block of the eleven.

- `board/_board.py` accepts pre-fetched GitHub JSON (`--github-data <file>`),
  and `gh_json()` reads from it when present. The `gh` path is untouched, so a
  dev box behaves exactly as today.
- The `/board` skill — which *is* the agent, and so is the only thing that can
  call `mcp__github__*` — gathers that JSON when `command -v gh` fails, writes
  it, and invokes the renderer with the flag. `_board.py` stays a pure
  renderer; a subprocess cannot reach MCP tools and this is the whole reason
  the seam exists.
- The file's shape is a documented contract in `board/AGENTS.md` (extend
  "Reading the board in a remote session"), because it outlives whoever writes
  it.

## Guards

- Tests drive the seam from a **fixture file**, never a live call.
- A leg with no injected data still reports `could not read` — the invariant
  from the 2026-08-26 work: no leg may substitute an empty answer for an
  unasked question. A green badge still requires a render that read everything.

## Done when

The overnight rows are live in a remote render, the degraded count drops by
seven, the dev-box path is byte-identical, and `tests/test_board_degraded.py`
plus the new fixture tests pass.
