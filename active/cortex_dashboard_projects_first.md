# Cortex dashboard: projects first, check-in prompt on top, epics discarded

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- dashboard
- cortex
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Review-minutes: 30
Unattended: no
Filed: 2026-09-04
Issued: 2026-09-04

## Original request (verbatim, 2026-09-04)

> Feedback on Cortex dashboard: 1) stuff at top goes on way too long, I dont
> want to see every phase of the euclid plan and have to scroll down before
> getting to next thing. All this stuff with phases and plans to me feels like
> it should be accessible by clicking a button to the GithUb issue(s) 2) This
> stuf, local /mnt/c/Users/Jammy/Science/euclid · RAL
> /mnt/ral/jnightin/euclid_strong_lens_modeling_pipeline — phases: planned 3 ·
> ready 1, should be over multiple lines with "Local" and "RAL" in bold to
> stand out 3) Awaiting Ruling is good, should be first thing on dashboard
> (other than many a clean summary of everything at the top, which currently
> isnt there. 4) I think Running submitted is ok but I dont like the Run it
> again blocks which take up space. 5) I like the "Ready" block, but I dont
> want multiple phases (E.g. the 4 of subhalo_Validation ) all showing. I
> think it should be one visible per science project, which is th enext
> phase, and maybe a sub-drop down menu with other phases ahead which are
> ready? 6) Gated is good, rdecent rulings is good, 7) I don't think we want
> "epics" anymore, all science projects cortex handles are by their very
> nature long exploratory things with many steps, often with them being
> updatred more on the fly. epics makes sense for chaining together
> pyautomind tassks, not science projects. "Epics" is really just all active
> science projects, which should probably be the thing at the top followed by
> awaiting ruling 8) Ok actually "Projects" should be top, Epics should just
> be discarded I think albeit we need it clear how to go from "ProjectS" to
> then actually doing follow up work, also for "Projects" put active top then
> planned then dormant. 9) It should be that on my laptop a single ai chat
> handles all RAL / cortex / science project management, I would like at the
> top a copyable button before the list which is the thing I paste to that
> chat to get the full updates on projects (And update the board) Since last
> time

## Where the board is rendered

`PyAutoBrain/agents/conductors/cortex/_cortex.py` — `render_dashboard`
(markdown) and `render_dashboard_html` (Pages twin), the `SECTIONS` tuple,
`phase_chips`, `by_project_keys` / `project_groups` / `project_paths`.
Tests in `PyAutoBrain/tests/test_cortex_conductor.py` (67 tests, several pin
the current section order — e.g. "the by-project section leads the board").
`PyAutoCortex/epics.md` is parsed by `parse_epics` and rendered as the Epics
section; `dashboard.md` / `dashboard.html` in PyAutoCortex are regenerated
by `pyauto-brain cortex dashboard --apply` and by `dashboard_refresh.yml`.

## New reading order (both renderers, one section list)

1. **Hero + counts + the check-in button.** One 📋 chip *before* everything
   else whose payload is the paste for the laptop's science chat:
   "`/cortex` — check in on every active science project since the last
   board render (<generated stamp>): pull each project through its sync
   CLI, score every live run against its witness, move what came back,
   re-render and push the board, then read me the by-project summary with
   the prompt each phase needs next." (`pyauto-brain cortex checkin` is the
   door it lands on.)
2. **Summary** — a short table, one row per *active* project: next phase
   (number + state), awaiting / running / ready counts, last ruling date.
   This is the "clean summary of everything" that is missing today.
3. **Projects** (replaces both today's leading "By project" and the trailing
   "Projects" table) ordered **active → planned → dormant**. Each card:
   - `**Local**` and `**RAL**` (and `**Mirror**` when set) on their own lines;
   - one line of phase counts;
   - the *next* phase as a single row with its own chip (rule / submit /
     open / gates — whichever its state carries) — this is the route from
     "Projects" to follow-up work;
   - a `<details>` fold ("N more open phases") holding the rest of the open
     phases as plain links to their phase files on GitHub, plus a link to
     `phases/<project>/` and to the project's `remote:` issues page — the
     plans live behind a click, not on the page. No `where to look` bullets
     on the board; they stay in the phase file and the check-in printout.
   - Dormant projects stay one folded line as today.
4. **Awaiting ruling** — unchanged in content (rule / accept-and-open / run
   it again chips), now the first state section.
5. **Running / submitted** — drop the "run it again" chip (it stays in
   Awaiting, where a rerun is a verdict); keep "where the jobs stand".
6. **Ready** — one row per project (its lowest-numbered ready phase) with the
   submit chip; further ready phases of the same project fold into a
   `<details>` under it.
7. **Gated** — unchanged. 8. **Recent rulings** — unchanged.
9. **Epics — removed.** The Cortex section, `parse_epics`, `epics.md` and the
   `REFRESH_BLURB` mention go; the Mind keeps its own epics for chaining
   development tasks. The `Epic:` phase header stays as an optional join key
   to a Mind epic (`cortex.py new --epic` untouched) so nothing in `phases/`
   has to be rewritten. `PyAutoCortex/AGENTS.md`, `README.md`,
   `REFERENCE.md`, the cortex skill (`PyAutoBrain/skills/cortex/cortex.md`)
   and `ledger_merge.py` lose their epics.md references.

`census --by-project` and the check-in printout keep the full per-phase tree
— the page is the thing that gets shorter, not the door.

## Freshness stamp (added 2026-09-04 after the plan review)

> I guess I will go to the dashboard and if I havent done the local science
> chat via paste, the project dashboard and other things may be outdated
> (e.g. from the day before). I think we should also therefore have paired to
> that at the top a "date last updated" type thing, which is red if its been
> longer than 1 hour so I know when the dashboard has been updated etc.

The stamp means *last check-in*, not last push: `cmd_checkin` already computes
a refresh stamp (`--refreshed` / `_utc_now()` / newest pull manifest) but only
prints it. Persist it in the Cortex repo as `checkin.yaml`
(`refreshed: <UTC ISO 8601>`, one key, committed and pushed with the ledger by
`push_ledger`), have `census()` read it, and render it beside the check-in
chip in both twins as "Last check-in <stamp>". In the HTML twin it is a
`<time datetime=…>` element and a few lines of inline script colour it red
(and append "· stale, paste the check-in") when the viewer's clock is more
than 60 minutes past it — the page is static, so the age is computed on view,
never at render. A CI re-render (`dashboard_refresh.yml`) reads the same file,
so a doc-only push never fakes freshness, and the file is stable between
renders so `--check` needs no new normaliser rule. Missing file → render
"never checked in" in red.

## Tests

Rewrite the order/section pins (summary table present; check-in chip is the
first task row; Projects precedes Awaiting; active before planned before
dormant; Ready shows one visible row per project with the rest folded; no
rerun chip in the live section; no Epics section; `epics.md` absent is not a
problem). Regenerate `dashboard.md` / `dashboard.html` in PyAutoCortex with
`PYAUTO_CORTEX=<worktree>` and commit them with the epics.md removal.
