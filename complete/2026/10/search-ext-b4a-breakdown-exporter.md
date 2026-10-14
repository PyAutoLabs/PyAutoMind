## search-ext-b4a-breakdown-exporter
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/2
- completed: 2026-10-14
- epic: search-extensibility (phase B4a — adopts PyAutoPulse task `autofit_profiling_bootstrap`)
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/3
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/60
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_developer/pull/30

**Shipped:** autofit_profiling#3 (merged 2026-10-14 as 007791a6f; Pages live at https://pyautolabs.github.io/autofit_profiling/, `pulse-refresh` dispatch ran and PyAutoPulse refreshed on main), PyAutoPulse#60 (merged as b593ffb55 after the online receipt step on the branch) and autofit_workspace_developer#30 (merged as 009709bc6), via a human `/prm`; tier judge.
- `scripts/gaussian_x1/nautilus/search_fit_breakdown.py` (`axis: breakdown`) re-homes the developer-workspace Nautilus anatomy with two variants: the bare-sampler reproduction gate (NN training 53.8 %, bound geometry 25.3 %, likelihood 11.6 %, proposal 5.7 %, wall 22.5 s; log Z −57.455, same as the original) and a full `search.fit` (7,501 likelihood calls, wall 28.4 s). Reproduction tolerance ±10 pp per share; the findings page is `wiki/campaigns/search_fit_breakdown.md`.
- **Headline finding (epic 1):** in a full `search.fit` on the fast gaussian_x1 likelihood, Nautilus checkpoint I/O (103 writes) is 24.5 % of the wall, NN training 43.4 %, bounds 20.4 %, visualisation 4.1 %, likelihood 1.1 %. The ranked table is `wiki/campaigns/search_fit_bottlenecks.md` and the Pulse check-in "2026-10-14 — B4a at PR; epic-1 ranked table" in `tasks/autofit_profiling_bootstrap.md`. Per-run `likelihood_share` came from autofit_inference `dashboard/summary.json` at 637713b (Nautilus numpy median 1.9 %, n=11; JAX CPU ≈0.01 %) — `catalogue/search_catalogue.json` has no `likelihood_share` field. Epic 2 (the EP loop) is NOT opened.
- Thin `profiling-summary@2` exporter `scripts/misc/tooling/build_catalogue.py` → `dashboard/catalogue.json` (validator: ok; `lint.yml` up-to-date check; 11 tests). Every record is marked unreviewed with no producer revision; a zero checkpoint time on the bare sampler is an "inapplicable" slot. Badge green, "baseline only, not a verdict".
- Pulse: `registry.yaml` row `fit` (`profiling-summary@2`, 17 records valid), fixture `tests/fixtures/autofit_profiling_v2.json`, `campaigns.yaml` `autofit` → active ("B4a at PR; B4b next"), receipts/snapshots for `fit` citing autofit_profiling 007791a6f; `check --offline` OK, 207 tests.
- autofit_workspace_developer: `searches_minimal/nautilus_profile.py` and `nautilus_bottleneck_findings.md` deleted (committed deletion; pre-delete SHA 06d86ac1deed93d3424791e71b47e6c135c7b5f1; `condemned.md` entry `autofit_workspace_developer/searches-minimal-nautilus-profile`). Leftover: `searches_minimal/nautilus_sweep.py` and `nautilus_jax_mlp.py` import the deleted module and `output/nautilus_profile_summary.txt` remains — retired the same day in autofit_workspace_developer#32 (record `complete/2026/10/retire-nautilus-leftovers.md`).
- Pages serves `catalogue.json` at the site root (not under `dashboard/`); Pulse ingests from raw.githubusercontent.com at the resolved sha, so this does not matter for the contract.
- Next: B4b (EP / graphical baseline port) when scheduled; A4 issued 2026-10-14.

## Original prompt

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
