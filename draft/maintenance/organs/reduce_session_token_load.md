# Reduce the organism's per-session and per-task token load by half

Type: maintenance
Target: organs
Repos:
- @PyAutoBrain
- @PyAutoMind
- @PyAutoCortex
- @PyAutoMemory
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-09-17

## Target

Three numbers, measured on 2026-09-17 after the ecosystem review
(`docs/organism/ecosystem_review_2026-09-17.md`), each to be halved:

| Load | Today | Target | Where it is measured |
|------|------:|-------:|----------------------|
| Mandatory per-session context — the four organs' `AGENTS.md` (loaded before the first tool call, every session) | ~12.4k tokens (Mind 2.9k, Brain 4.5k, Cortex 4.1k, Memory 0.9k) | **≤ 6k** | `cat */AGENTS.md \| wc -c` / 4 |
| Per-task procedure — `/start_dev` reads `start_dev.md` + `reference.md` + `WORKFLOW.md` + `GITHUB_ACCESS.md` (895 lines); `/prm` reads 786 lines | 895 / 786 lines | **≤ 350 / ≤ 300** | `wc -l` over the files a skill tells the session to read |
| Per-task record — completion records written at close-out (September: 228 records, 30,439 lines, median 124, p90 207) | median 124 lines | **median ≤ 60** | `wc -l complete/2026/<MM>/*.md` |

The numbers are the deliverable: a `scripts/token_load.sh` (Mind) that
prints all three, run by the hygiene conductor as a report line, so the
budget is measured rather than remembered.

## Levers, in order of tokens saved per line changed

1. **Brain `AGENTS.md` "Running" table** (51 lines, 20 rows with a full
   sentence of purpose each): one line per verb, purpose ≤ 12 words; the
   long descriptions stay in each agent's own `AGENTS.md` (already the rule
   — "read each agent's own AGENTS.md for its full role").
2. **The organism map table** is generated into Brain *and* Cortex
   `AGENTS.md` (25 lines each). Keep the eight organ names and one clause
   each; the roles are in `ORGANISM.md`.
3. **Cortex `AGENTS.md`**: the verb-by-verb `cortex.py` listing (21 lines)
   and the 16-line verbatim "out of scope" quote both duplicate
   `REFERENCE.md` / the shelved prompt they cite — a pointer each.
4. **"Chat register"** (Brain, 32 lines): the rule is one paragraph.
5. **`WORKFLOW.md` model-delegation section** (~50 lines) and the
   `reference.md` sidecars: `reference.md` is read only when the step that
   needs it is reached — say so at the top of each skill body — and the
   ladder is a table, not an essay.
6. **`/prm` after `lifecycle.py close`**: steps 5.3–5.4 are now one verb;
   the prose that described the legs (~120 lines) can go. Make
   `bin/check_skill_line_counts.sh` blocking once `batch` (232) and `prm`
   (357+) are under the 200-line budget.
7. **Completion-record template**: `What shipped` / `What the filed scope
   missed` / `Root cause` / `Follow-ups`, each a paragraph or a list, plus
   `## Original prompt`; no narrative of the session. `autonomy_log.md`
   rows ≤ 300 characters (today some exceed 1,000 in one cell).

## Out of scope

Removing any rule (never-rewrite-history, end-at-deliverable, the remote
sessions block) — those stay verbatim; only their surrounding prose shrinks.
Splitting the registries into per-task files (review item 6) is its own task.

## Why now

Every session pays the first number before it does anything; every task pays
the second twice (start and close) and writes the third once. At ~100 tasks
a week the September record volume alone was ~1,800 agent-written lines a
day that the memory faculty greps by title.
