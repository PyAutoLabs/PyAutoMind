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
