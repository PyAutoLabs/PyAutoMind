Shipped in PyAutoBrain#617 (closes PyAutoBrain#616), merged 2026-11-13 by the human's `/prm`.

The Cortex board (dashboard.md / dashboard.html) no longer hides non-active projects:

- Counts: Running · Open · Active · Dormant · Retired (`counts` gains `dormant`/`retired`; `counts["active"]` and the `state.json` headline unchanged).
- Summary: Active and Dormant tables (Project · Running · Open · Last update), Retired table (Project · Note clipped at 120 chars · Last update); Planned only when one exists.
- Projects: Active and Dormant sections with full cards (resume chip active-only); Retired as visible compact entries instead of one folded line.
- Runs in each card newest first (full date, then numeric job id); runs-table Date shows `MM-DD` (HTML keeps the full date as a tooltip).
- Science mirror: `dashboard --apply` and `checkin --apply` also write the markdown board to `<science_root>/STATE.md` when that root exists (the laptop); skipped silently elsewhere; a write failure is one stderr note; `--check` ignores it.

Tests: tests/test_cortex_conductor.py 90 passed (10 updated, 8 new).

Shipped under the Heart RED development override (recorded on the issue, the PR, active.md and autonomy_log.md 2026-11-13); Heart remains RED for release purposes.

Follow-up (Science side, not this repo): re-render the Cortex board with the new renderer (first write of Science/STATE.md) and add a pointer line in Science/AGENTS.md.

## Original prompt

# Cortex board: split Active / Dormant / Retired, newest-first runs, Science STATE.md mirror

Targets: @PyAutoBrain @PyAutoCortex
Type: feature
Filed: 2026-11-13
Issued: 2026-11-13
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/616
Consequence: judge

Verbatim user requests (2026-11-13 session):

> I like the idea of the Science folder having a .md file which shows the state of everything, noting that this would need to be a mirror of the PyAutoCortex dashboard, I get its repetiiton but I will go to view both in different contexts.
>
> Also for the PYAutoCortex Summary board I think we should split active and dormant, I think we could have a third initial box "retired" under "Summary" and "Projects" as currently retired is a bit hidden.
>
> When I clikc a project like "euclid_dr1 it shows 60 runs, but they are going from first task at the top in date to last at the bottom, I think they should go the other way I want to see the latest things at the top.

Approved plan (in `organs/PyAutoBrain/agents/conductors/cortex/_cortex.py` + `test_cortex_conductor.py`):

1. Counts box: Running · Open · Active · Dormant · Retired, each linking to its section (check the Brain board parser that reads the counts rows by label; keep "Projects" if renaming breaks it).
2. Summary: three tables — Active, Dormant, Retired (retired: Status/Note columns instead of Running/Open).
3. Projects: three headed sections — Active, Dormant (full cards; resume chip only for active), Retired (visible compact cards: summary, note, ledger link) replacing the single collapsed "N retired" line.
4. Science mirror: `cortex dashboard --apply` and `checkin --apply` also write the same markdown to `<science_root>/STATE.md` (`science_root_from(projects)`); laptop only, silently skipped when the root is absent; generated/do-not-edit header + Pages link. Pointer line in `Science/AGENTS.md`.
5. Runs within each project card sorted newest first (date, then job id), md and html.
6. Tests for the split, run ordering and mirror skip; re-render the Cortex board.

Tier: judge — merge mode: human /prm

Approval: the human approved this plan in session on 2026-11-13 ("work this into the plan above and then begin it").
