# Cortex board: blurbs gone, big green/red check-in stamp, readable project names, nothing-open table

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- dashboard
- cortex
Difficulty: low
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 10
Unattended: no
Filed: 2026-09-04

## Original request (verbatim, 2026-09-04)

> We dont need this text for a dashboard it too much info "This page is
> generated from phases/, rulings/ and projects.yaml, so it is only as current
> as they are. dashboard_refresh.yml re-renders it on every push to main.".
> Also make the date larger, and some sort of obvious green box or tick if its
> within 3 hours of now.

## Second round (verbatim, 2026-09-04, on the plan review)

> Project names are small text and hard to read, euclid / inference programme
> etc. Make them larger and ideally underline or something to help? This is
> also superflous "The science body map, active first: where each project
> lives, what it is holding, and the one phase of it to act on next. The plans
> and the issues are one click away — this page routes to them rather than
> reprinting them; census --by-project and the check-in printout keep the full
> per-phase tree." This should be in summary: 8 project(s) with nothing open:
> euclid_dr1_prelim (planned · none) · concr (dormant · none) · cowls_diana
> (dormant · none) · ic50_workspace (dormant · planned 1) · pj011646 (dormant ·
> none) · profiling (dormant · none) · slope_hierarchy (dormant · planned 2) ·
> subhalo_simulations (dormant · none) make it a table for clarity Do all this
> too.

Follow-up to `complete/2026/09/cortex-dashboard-projects-first.md`
(PyAutoBrain#355 / PyAutoCortex#14), filed from the first look at the shipped
board.

## Scope

`PyAutoBrain/agents/conductors/cortex/_cortex.py`, both twins
(`render_dashboard`, `render_dashboard_html`), tests in
`PyAutoBrain/tests/test_cortex_conductor.py`, then regenerate
`PyAutoCortex/dashboard.md` / `dashboard.html`.

- Remove the `REFRESH_BLURB` sentence from the Cortex board (the Mind's own
  `_intake.py` blurb is untouched — the request names this dashboard). The
  `Last updated <date>` render date stays as a one-line muted note so the
  `dashboard_body` normaliser keeps dropping it whole.
- The check-in stamp becomes the prominent element under the check-in chip:
  large date in a coloured box. Within **3 hours** of the viewer's clock →
  green box with a ✓ tick and "fresh"; beyond → red box with ✗ and "stale,
  paste the check-in"; missing/unparseable stamp → red "never checked in".
  The single threshold moves from 60 min to 180 min (the request's number
  supersedes the earlier one-hour rule). Age is still computed on view by the
  inline script, never at render.
- Markdown twin has no script: render the stamp as a heading-sized line
  (`### Last check-in: <stamp>`) with no colour claim.
- Project cards: `<section class="project">` wrapper with a cortex-local
  `.project h3` rule — larger, bold, accent underline — leaving the shared
  `board/_theme.py` h3 alone. Projects section blurb ("The science body map…")
  removed; `h2()` helpers tolerate an empty blurb.
- Folded projects (nothing open) leave the foot of Projects and become a
  **Project | Status | Phases** table under Summary, ordered active → planned
  → dormant.
