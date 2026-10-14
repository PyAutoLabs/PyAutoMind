# `@autofit_profiling` B4a: `search.fit` breakdown cell, `profiling-summary@2` exporter, Pulse `fit` row and the epic-1 bottleneck table

Type: feature
Target: autofit_profiling
Repos:
- autofit_profiling
- PyAutoPulse
- autofit_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: B4a
Blocked-by: none — both group-1 PRs open 2026-10-14 (PyAutoFit#1683, autofit_inference#7)
Witness: `bin/pyauto-pulse check --offline` passes with a `fit` row in `registry.yaml` whose `dashboard/catalogue.json` validates as `profiling-summary@2`; the autofit_profiling Pages board is live and shows the breakdown cell; `scripts/gaussian_x1/nautilus/search_fit_breakdown.py` reproduces the committed Nautilus anatomy shares (NN training, bounds, likelihood) within their stated tolerance on the laptop CPU; epic 1's ranked bottleneck table for one `search.fit` on a fast likelihood is filed as a Pulse campaign entry under `autofit`, with `likelihood_share` fed by the B2/B3 rows.
Review-minutes: 20
Unattended: ready
Filed: 2026-10-14
Issued: 2026-10-14

Adopts PyAutoPulse `tasks/autofit_profiling_bootstrap.md` (campaign `autofit`,
status `ready`) as agreed on 2026-10-07; scope per the epic report
`draft/research/autofit/search_extensibility_epic_report.md` "B4 — B4a scope"
(D17) and survey `search_extensibility_epic_surveys/04_inference_profiling_infra.md`
§ "Epic-1 cells". autofit_profiling main is the B1 skeleton `86c77345`.

## Scope (B4a only)

1. **Re-home the Nautilus anatomy** from
   `autofit_workspace_developer/searches_minimal/{nautilus_profile.py,nautilus_bottleneck_findings.md}`
   as `scripts/gaussian_x1/nautilus/search_fit_breakdown.py` (`axis: breakdown`)
   with its findings page under `wiki/`. The developer-workspace originals are
   retired via Gut-style committed deletion in a separate autofit_workspace_developer
   PR (record the pre-delete SHA), not bannered.
2. **Thin `profiling-summary@2` exporter** writing `dashboard/catalogue.json`
   (not a port of autolens_profiling's 1,272-line v1 renderer); validated with
   Pulse's validator (`--validate-with ../PyAutoPulse` or the equivalent the
   Pulse REFERENCE.md names).
3. **Pages + `pages_dashboard.yml` → `pulse-refresh`** dispatch, mirroring
   autolens_profiling's workflow and the project-feed identity shipped in
   `complete/2026/10/pulse-refresh-project-identity.md`.
4. **Pulse side**: fixture + `registry.yaml` row `fit` (`supported_schema:
   profiling-summary@2`, `library_refs: [PyAutoFit]`, `cortex_project: null`),
   `campaigns.yaml` `autofit` campaign updated, `check --offline` green.
   Registry PRs conflict on generated dashboard files when main moves: merge
   main, re-render with the explicit repo flag, commit.
5. **Epic 1 table**: a ranked bottleneck table for one `search.fit` on a fast
   likelihood (gaussian_x1), fed by the B2/B3 `likelihood_share` rows from
   autofit_inference's catalogue, filed as a Pulse campaign entry. Epic 2 (the
   EP loop) is NOT opened — it waits for epic 1's top findings to ship.

Out of scope: B4b (EP/graphical baseline port, its own research-grade
reproduction task); any RAL runs (laptop CPU only for B4a).

## Order

autofit_profiling PR first (exporter publishes), then the Pulse PR (row reads
the published summary; Pulse `check` fails any row without one), then the
autofit_workspace_developer deletion PR.
