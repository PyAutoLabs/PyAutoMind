# The Brain board should work in a session that has no `gh`

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- dashboard
- mind-workflow
Difficulty: large
Autonomy: supervised
Priority: normal
Status: phased
Consequence: judge
Review-minutes: 25
Unattended: ready
Split-into: complete/2026/08/board-github-data-seam.md (phase 1, shipped 2026-08-27), draft/feature/pyautobrain/board_without_gh_phase2_legs.md
Filed: 2026-08-26

The board is the morning door, and on mobile it is mostly blind. Eleven of its
legs read GitHub through `gh api`, and **a Claude Code remote session has no
`gh` at all**. The render is honest about it now (see "Already done" below) — it
says `could not read`, banners the degraded count, and refuses to show a green
badge — but honest-and-blind is still blind. A morning glance on a phone should
be worth taking.

The one leg that was fixed by configuration rather than code proves the value:
adding `*.github.io` to the environment's network allowlist made the readiness
leg live, and it immediately surfaced a **Heart verdict RED · 45** that the
board had been rendering as "clear to work · brightgreen". The other eleven legs
are still dark for a reason no allowlist can fix.

## What is actually true in a remote session

Established by direct measurement on 2026-08-26; **do not re-derive these, and
do not assume they still hold — re-check the two marked (verify) first.**

| Surface | State |
|---|---|
| `gh` binary | **Not installed.** Not in the image, and not installable as a fix — see the token row. |
| `mcp__github__*` tools | **Work.** This is the session's real GitHub surface. Available to the *agent* only. |
| `$GH_TOKEN` / `$GITHUB_TOKEN` | **Set, but refused.** A direct REST call with them returns `GitHub access is not enabled for this session. An org admin must connect the Claude GitHub App for this organization.` (verify) |
| `api.github.com` | Reachable (200 unauthenticated), and in the default Trusted allowlist. |
| `git` push/fetch | Works — separate credential path via the GitHub proxy. |
| A subprocess calling MCP | **Impossible.** MCP tools are an agent capability; `_board.py` is a subprocess and cannot reach them. |

That last row is the crux, and it is why "port the board to MCP" is not a
one-line substitution: `board/_board.py` cannot call these tools itself.

## The eleven legs

From a live remote render: 7 × `overnight: could not read <repo>/<workflow>`,
plus `versions: no stamps resolved`, `community: scan unavailable (exit 4)`,
`resume: pending-release PR search failed`, `upkeep: open-issue count
unavailable`. All route through `gh_json()` in `board/_board.py`, or through
`bin/overnight_status.sh` / `bin/version_drift.sh` /
`agents/conductors/community/_community.py`.

## Three ways to close it — decide before building

Phase 0 is choosing, not coding. They are not equal in cost or in permanence.

1. **An injection seam.** `_board.py` gains a way to accept pre-fetched GitHub
   JSON (a `--github-data <file>`, or stdin), and the `/board` skill — which
   *is* the agent — gathers it via `mcp__github__*` when `command -v gh` fails,
   then renders. `_board.py` stays a pure renderer and its `gh` path is
   untouched for the dev box. Works today, needs no external permission, and is
   testable with a fixture file. Costs a documented contract between the skill
   and the script.
2. **Enable raw REST.** If an org admin connects the Claude GitHub App for
   PyAutoLabs, the injected `$GH_TOKEN` may start working from subprocesses —
   at which point `gh_json()` becomes a small REST helper with no seam, no
   skill contract, and no MCP involvement, on *every* surface. Much the
   cleanest end state **if** it works. Unverified: the refusal message above is
   all the evidence there is, so probe it before betting the task on it.
3. **Install `gh` in the environment setup script.** Cheap to try, and probably
   dead: `gh` under the proxy authenticates through the same injected-credential
   path that option 2's probe tests, so it likely fails identically. Test it in
   the same probe; a five-minute answer either way.

Prefer 2 if the probe says it works, else 1. Do not build 1 before running the
probe — it is the more complex design and option 2 would obsolete it.

### The probe was run — 2026-08-27. Options 2 and 3 are dead; build 1.

`$GH_TOKEN` is set, and from a subprocess it reaches exactly what it reached in
August: nothing repo-scoped.

| Request (Bearer $GH_TOKEN, direct REST) | Result |
|---|---|
| `GET /user` | **200** — returns the login |
| `GET /rate_limit` | **200** |
| `GET /repos/PyAutoLabs/PyAutoBrain` | **403** — "GitHub access is not enabled for this session. An org admin must connect the Claude GitHub App for this organization." |
| `GET /repos/PyAutoLabs/PyAutoBrain/actions/runs` | **403** — same |

So option 2 needs an org-admin action that has not happened, and option 3 dies
on the same credential path without the install being worth trying. **Option 1
(the injection seam) is the design**, and the header stays `Autonomy:
supervised` because the seam is a contract between the `/board` skill and
`_board.py` that outlives whoever writes it.

Re-run the probe before starting anyway — it is four `curl`s, and the day an
admin connects the App, option 2 obsoletes the seam.

## Already done (2026-08-26 — `complete/2026/08/mobile-performance-review.md`)

Do not redo these; build on them.

- Rows distinguish *asked and got nothing* from *could not ask*
  (`unreadable` on each overnight row) — `no runs` is no longer claimed by a
  board that never asked.
- A `⚠️ Degraded render — N leg(s) could not be read` banner above the sections,
  a headline qualified with `partial view (N legs unread)`, and a grey badge —
  green is emitted only by a render that read everything.
- `_fetch_reason()` names an egress-policy block (403 on CONNECT) as one, rather
  than as a retryable "unreachable".
- `fetch_heart_board()` falls back to a sibling checkout's local
  `board/board.json` when the published copy is unreachable — **the pattern to
  copy** for any leg whose data also exists locally.
- `bin/_gh.sh` (`have_gh` / `require_gh`) and `skills/GITHUB_ACCESS.md`, the
  gh→MCP mapping every gh-driving skill now points at.
- `tests/test_board_degraded.py` pins all of the above.

## Done when

- A remote render reports **zero** unread legs, or names each remaining one with
  a reason that is not "no `gh`".
- The dev-box path is unchanged — `gh` still used where present, same output.
- Whichever option is chosen, the *decision* and its evidence are written down
  (`board/AGENTS.md` already has a "Reading the board in a remote session"
  section; extend it).
- Tests cover the gh-less path with a fixture, not a live call.
- No leg silently substitutes an empty answer for an unasked question — the
  invariant the 2026-08-26 work established, and the one worth protecting.

## See also

- `PyAutoBrain/board/AGENTS.md` → "Reading the board in a remote session"
- `PyAutoBrain/skills/GITHUB_ACCESS.md` → the gh→MCP operation mapping
- `PyAutoMind/complete/2026/08/mobile-performance-review.md` → the record for
  the work this builds on, including the measurements above
- `draft/feature/pyautobrain/brain_board_follow_ups.md` → the small-nit catch-all
  for the same board; this prompt is deliberately separate because it is not a
  nit.
