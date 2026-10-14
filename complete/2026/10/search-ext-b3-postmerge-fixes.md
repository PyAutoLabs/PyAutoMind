## search-ext-b3-postmerge-fixes
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/6
- completed: 2026-10-14
- epic: search-extensibility (phase B3c — post-merge fixes for the B3 pilot)
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/7
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/28

**Shipped:** autofit_inference#7 (merged 2026-10-14 as 6df69441b) then PyAutoInsight#28 (merged as 30cf007ce after a conflict repair against the scheduled dashboard refresh), via a human `/prm`; tier judge. Fixes all six findings of the post-merge Codex gpt-6-astra review 06 (`draft/research/autofit/search_extensibility_epic_reviews/06_codex_astra_b3_postmerge.md`). Findings 1–5 reproduced on 900648b and were fixed test-first; finding 6 (the Insight board) had already been fixed by the 2026-10-08 refresh, so only its acceptance check was added.
- Freeze rule: protocol §7, `wiki/project/state.md`, Insight `campaigns.yaml` and `tasks/gaussian_x3_search_wave1.md` now agree — freeze `@2` from the existing calibration before any scored run, keep the A2+A4 gate on scored wave 2, never restart the pilot. Decision: the freeze proceeds on 17 calibration rows, not 20 (the <20 rule keeps the σ-ratio band and ppc tolerance at `@1`, so `@2` loosens nothing; the 3 missing rows cannot come from the pilot output). The `@2` freeze commit itself is B5's first step.
- Bootstrap wall-per-success intervals keep zero-success resamples as unbounded; 4 catalogue cells now report a null upper bound (separated DynestyStatic nlive_200 numpy, separated DynestyDynamic default numpy and jax_cpu, blend Nautilus n_live_200 numpy).
- A failed warm-start provider records its elapsed cost in a `finally`; the consumer never started so its cost is 0 and the attempt cost is the provider's; any other unknown cost blanks the leg's wall estimates with a reason, never 0.
- Exporter adds `warm_start`, `provider_wall_s`, `consumer_total_s`; `total_s` on warm-start rows is the combined cost with a matching definition (separated seed 0: 73.69 s → 1150.16 s; blend seed 0: 67.55 s → 1233.72 s). Contract stays `inference-summary@1` (Insight REFERENCE.md allows additive fields; `@2` is already the setups contract). Insight board shows the combined total and names the provider's share.
- A stuck parameter with NaN R-hat/ESS now yields `not_converged` naming the parameter.
- Insight `fit` snapshot refreshed from producer main 6df69441b (223 records, 35 accepted / 110 rejected / 78 not assessed, unchanged); new `tests/test_fit_acceptance.py` pins receipt and snapshot agreement, producer revision and the 223-record count.
- Tests: autofit_inference 82 passed (6 new); PyAutoInsight 186 passed (3 new); both repos' lint/format/`check` green.
- Data: the B3 pilot output (searches 929 MB, references 413 MB) lives in canonical `fit/autofit_inference/output/` (gitignored); the catalogue rebuilds from committed `results/` rows.
- Carried: review 06 item 7 (wave-2 manifest identity, per-realization references, versioned judging) → the B5 prompt; item 8 (reassessment provenance) later.

## Original prompt

# `@autofit_inference` + `@PyAutoInsight` B3 pilot post-merge fixes (astra review 06)

Type: bug
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: B3c
Witness: (1) protocol §7, `wiki/project/state.md` and Insight `campaigns.yaml` give one consistent freeze rule — `@2` is frozen from the existing calibration before any scored run, the pilot is not restarted, and the A2+A4 gate on scored wave 2 is kept; (2) the bootstrap wall-per-success interval for a cell with zero-success resamples reports an unbounded upper limit and the 4 affected catalogue cells are regenerated; (3) a warm-start provider that raises still records its elapsed seconds, and an unknown cost is reported as missing, never 0; (4) `inference-summary` rows carry `provider_wall_s` and `warm_start` and the Insight board's total shows provider plus consumer time for the warm-start rows; (5) a parameter whose R-hat or ESS is NaN fails convergence rather than being dropped, with a test; (6) the Insight `fit` snapshot is refreshed from autofit_inference ≥ `900648b5c` and shows 223 records, with an acceptance check on producer revision and record count.
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-14

## Original request

> Continue working on the PyAutoFit refactor epic. [...] I am happy to follow
> your recommendation on everything else, try do in groups of tasks so theres
> less input from me.

Recommendation adopted 2026-10-14: issue the review-06 before-wave-2 and
before-B5 fixes as one task, in parallel with the PyAutoFit review-05 fixes
(`draft/bug/autofit/search_ext_a3_postmerge_fixes.md`), before A4/B4.

## Source

`draft/research/autofit/search_extensibility_epic_reviews/06_codex_astra_b3_postmerge.md`
(FINDINGS 6; §3 findings, §6 resume actions) and the ledger
`draft/research/autofit/search_extensibility_epic.md` "Resume (2026-10-08 night)".
Verify each finding against current main before fixing it.

## Items (ledger order)

1. **[before-wave-2] Contradictory freeze instructions** — protocol §7
   (~line 160), `wiki/project/state.md` (~line 62), Insight `campaigns.yaml`
   (~line 96). Freeze `@2` before any scored run on the calibration that
   already exists; do not restart the pilot; keep the A2+A4 gate. (P1)
2. **[before-wave-2] Bootstrap wall-per-success intervals discard zero-success
   resamples** (`build_catalogue.py` ~line 129). Keep them as unbounded and
   regenerate the 4 affected cells. (P1)
3. **[before-wave-2] Failed warm-start provider loses its elapsed cost**
   (`_runner.py` ~825/512/873) and `leg_summary` coerces unknown cost to 0.
   Persist the provider time in a `finally`.
4. **[before-wave-2] Exporter omits `provider_wall_s`/`warm_start`**
   (`export_inference_summary.py` ~line 208), so the Insight "Total s" shows
   consumer-only time (73.7 s vs 1150.2 s). Export and display the combined
   cost (Insight read-contract change if needed — version it, never silently).
5. **[before-wave-2] Convergence drops a stuck parameter with NaN R-hat/ESS**
   (`_posterior.py` ~line 285). Require valid diagnostics for every free
   parameter.
6. **[before-B5] Refresh the Insight `fit` snapshot** from autofit_inference
   ≥ `900648b5c`; check the board shows 223 records; add an acceptance check
   on producer revision and record count.

Out of scope (later tasks): wave-2 manifest identity / per-realization
references / versioned judging (review 06 item 7, before-B5, belongs to the B5
prompt); reassessment provenance (item 8, later).

## Data

The B3 pilot output (raw searches 929 MB, references 413 MB incl. JAX Nautilus
seeds) was moved on 2026-10-14 from the retired `search-ext-b3-pilot` worktree
into canonical `fit/autofit_inference/output/` (gitignored). Regenerating
catalogue cells reads from there; no new sampling runs are needed.

## Constraints

- autofit_inference PR first, then the PyAutoInsight PR (its board reads the
  producer's published summary). Insight registry PRs conflict on generated
  dashboard files when main moves: merge main, re-render with the explicit repo
  flag, commit.
- No RAL compute; nothing in this task runs new searches.
