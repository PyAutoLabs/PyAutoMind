## search-ext-b2-harness
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/2
- completed: 2026-10-08
- epic: search-extensibility (phase B2)
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/3
- merge-commit: autofit_inference ec35be49

### Outcome
autofit_inference has its harness, datasets, pre-registered protocol and reference posteriors. `wiki/project/protocol_gaussian_x3.md` (`gaussian_x3@1`) is the first commit and predates every result; seeded `gaussian_x3_blend` (plan numbers) and `gaussian_x3_separated` (disjoint centre priors, D15 option (b), amendment A1) datasets are committed as JSON; the harness ports autolens_inference's CLI (`{local,ral}_{numpy,jax_cpu}_{fp64,fp32}`), `_runner.run_search(sampler=, dataset_class=, model_type=)`, MLTracker, WALL gate and `batch_cpu` template (`--partition=ral` only); row schema v1 carries the protocol fields, reference identity `(dataset, backend, data_seed, assertion_mechanism)`, cold/warm run identities and failure wall times; the exporter emits `inference-summary@1` with producer-asserted verdicts and reference limitations; CI runs lint gates and a 1-seed Nautilus witness that must export `accepted`. Numpy reference: Nautilus `n_live=2000` ×3 (ln Z 137.061 ± 0.019, medians to 0.015σ, single mode weight 1.000), MAP ln P 186.668, `ln 3!` validation −1.825. `--auto` run at effective supervised; one decide-and-flag decision (constant-likelihood rerun at n_live=2000), accepted at merge.

### Validation and limits
65 tests; ruff; README/summary/WALL checks; Insight classifier validates both summaries; GitHub `lint` and `witness` green (witness accepted and converged). Independent adversary (Codex gpt-6-astra, `search_extensibility_epic_reviews/03_codex_astra_b2_pr3.md`): 12 findings, 11 reproduced, all enacted before merge; the committed reference was rebuilt from the same raw samples after the mode-clustering truncation was fixed (mode weight 0.103 → 1.000, ln Z/medians unchanged). Limitations recorded in protocol §10: DynestyStatic at default `walks=5` scatters ln Z by 2.3 nat (numpy) / 5.6 nat (JAX) and is excluded from the reference; JAX Nautilus references and separated references are `pending` for B3; `DynestyStatic` accepts no seed (A4); Dynesty termination is `not_assessed` until A3 exposes it. The raw reference outputs (151 MB, `output/`) are preserved in the canonical `fit/autofit_inference/output/` (gitignored); a reference rebuild needs them.

## Original prompt

# autofit_inference harness, gaussian_x3 datasets, pre-registered protocol and reference posteriors (epic search-extensibility, phase B2)

Type: feature
Target: autofit_inference
Repos:
- autofit_inference
Themes:
- searches
- inference
- benchmark
Difficulty: large
Autonomy: supervised
Consequence: judge
Witness: a CI leg runs 1 seed of Nautilus on the committed `gaussian_x3_blend` dataset and the exporter emits an `accepted` row against the committed reference posterior; `wiki/project/protocol_gaussian_x3.md` predates every wave-1 row in git; `build_readme.py --check` and `export_inference_summary.py --check` pass; the summary validates against PyAutoInsight `check --offline`
Unattended: ready
Priority: high
Epic: search-extensibility
Status: active
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autofit_inference/issues/2
Filed: 2026-10-08

Phase B2 of the search-extensibility epic (`draft/research/autofit/search_extensibility_epic.md`; plan
`search_extensibility_epic_report.md` §4 B2, design §3.7, decisions D15 and D16 in §8 (plain-language §8.2); survey
`04_inference_profiling_infra.md` §1 (how autolens_inference works), §6 (reuse) and §7 (the benchmark)). Depends on B1
(done: repo skeleton, Mind/Heart/Cortex rows, RAL clone) and A0a (done). Human launch 2026-10-08: `--auto` for A1 and
B2. The repo is `fit/autofit_inference` (skeleton: AGENTS.md, CORTEX.md, README.md, hpc/{batch_cpu,sync}, wiki/project/state.md).

## Original request (verbatim from the epic plan)

"B2 — autofit_inference harness, datasets, protocol, reference posterior (depends on B1 and A0a). Repo:
autofit_inference. Scope: `_autofit_inference_cli.py`, `_runner.run_search(...)` and MLTracker; seeded `gaussian_x3_blend`
and `gaussian_x3_separated` simulators with committed JSON; row schema v1 plus protocol fields (relabelled statistics,
`modes_found`, max-logL and max-logP, observed/estimated timing flags, stable run IDs shared with autofit_profiling);
`wiki/project/protocol_gaussian_x3.md`, pre-registered before any wave-1 run, with the D15 label/evidence convention and
the D16 pilot-then-freeze rule; per-backend reference-posterior runs (Nautilus and Dynesty long, 3 seeds each), the MAP
reference, and the constant-likelihood constrained validation run; README auto-tables; the exporter emitting protocol
verdicts. Why it needs only A0a: the conformance suite doubles as the per-search 'standard problem' smoke, and the
harness pins the PyAutoFit `main` it ran on. Risk: low. The main danger is calibrating thresholds on too few seeds,
which the pilot-then-freeze rule addresses. Verify: a CI witness of 1 seed × Nautilus on the real dataset,
`build_readme --check`, and exporter validation against Insight `check --offline` with a fixture. Witness: the CI leg
produces an `accepted` row against the committed reference, and the protocol file predates every wave-1 row in git."

## Scope (design from report §3.7, verbatim numbers)

- **Model**: 3 `af.ex.Gaussian` + a thin `Background(level)` profile summed in the Analysis, 10 free parameters;
  ordered-centre assertions `g0.centre < g1.centre < g2.centre`; priors centre U(0,100), normalization
  LogUniform(1e-2, 1e2), sigma U(0.5, 30), background U(−1, 1). The JAX leg uses the `xp.where` penalty mechanism
  already in `Fitness`; the numpy leg the raising assertion (D15 records that these differ).
- **Datasets** (committed JSON: data, noise_map, model_*.json, truth.json, mirroring autofit_visualization's seeded
  simulator pattern): `gaussian_x3_blend` 100 pixels, centres 25/45/60, σ 3/6/10, normalizations 30/50/40, background
  0.02, noise σ=0.04, `np.random.default_rng(data_seed)`; `gaussian_x3_separated` the disjoint, non-overlapping control.
- **Harness**: copy and generalise from `lens/autolens_inference`: `_inference_cli.py` → `_autofit_inference_cli.py`
  with grammar `{local,ral}_{numpy,jax_cpu}_{fp64,fp32}` (no `a100`/`jax_gpu` leg at birth; no `batch_gpu` template);
  `scripts/misc/searches/_point_runner.py` → `_runner.run_search(sampler=, dataset_class=, model_type=)` with literal
  kwargs (the Brain faculty's AST parser reads them); MLTracker from
  `fit/autofit_workspace_developer/searches_minimal/_metrics.py` (its JAX fallback interpolates times, so label values
  observed/estimated); `hpc/sync`, the WALL-BASIS gate, `scripts/misc/tooling/{build_readme,export_inference_summary}.py`
  with `project` parametrised; `config/general.yaml` keeping outputs; `activate.sh` merged with the RAL
  `PYAUTO_HPC_BASE` branch. No shared package: copies are fine at birth.
- **Row schema v1**: the autolens_inference row plus protocol fields: sorted-centre relabelled statistics,
  `modes_found`, `max_log_likelihood` and `max_log_posterior` (never interchanged), timing flags
  observed/estimated, `compile_s` from separate cold/warm runs, `per_call_s`/`likelihood_share` as estimates, stable
  run IDs in the form autofit_profiling will share, and the PyAutoFit commit it ran on.
- **Protocol** `wiki/project/protocol_gaussian_x3.md`, committed BEFORE any wave-1 row: success criteria (a) point/MAP
  searches optimise the log posterior and are judged against the MAP reference; (b) posterior accuracy
  `|median − ref|/ref_σ ≤ 1`, a σ-ratio band (placeholder, calibrated in the pilot then frozen), posterior-predictive
  residual χ², mode coverage; (c) evidence `|logZ − ref| ≤ 1` nat within one backend and one assertion mechanism under
  the `ln 3! ≈ 1.79` nat convention; convergence diagnostics separate (R-hat/ESS for chains, dlogz/n_eff for nested);
  headline = success rate (Wilson) and expected wall per right answer (bootstrap, failures and warm-start cost included,
  zero-success defined); wave 1 is a pilot that ranks nothing; wave 2 (50 seeds, 5 data realisations, RAL
  `--partition=ral` ONLY, never `gpu`/`ral,gpu`/`gpu,ral`) ranks; catalogue groups by task, never ranks tasks against
  each other; NSS on the blend is `deferred` until A3b.
- **Reference posteriors** per backend (numpy and JAX): 3 long Nautilus (`n_live=2000`) + 3 long DynestyStatic
  (`nlive=1000`) runs each; agreement within 0.2 nat on logZ and 0.1σ on medians, or the protocol records why not; a
  MAP reference (long MultiStart + LBFGS polish from the reference's best sample); a constant-likelihood constrained
  run validating the `ln 3!` convention. Committed as JSON under `results/reference/`. These are the only long runs in
  B2; run them locally in the background, numpy first.
- **Exporter**: `inference-summary@1` (contract in `lens/autolens_inference/INFERENCE_SUMMARY.md` and
  `organs/PyAutoInsight`), emitting producer-asserted `scientific.convergence/acceptance` with `protocol_id` and
  `reason`; a fixture validated with Insight `check --offline`. No Insight registry row yet (B3).
- **CI witness**: a workflow leg running 1 seed × Nautilus (`n_live=100`, numpy) on the committed blend dataset and
  asserting the exporter emits `accepted` against the committed reference; `build_readme.py --check`; lint.
- **Docs**: README auto-tables (`build_readme.py`), `wiki/project/state.md` updated (still `planned` in Cortex until B3's
  first runs; do not edit Cortex here), `CORTEX.md` untouched.

Not in scope: wave-1 runs (B3), Insight registration (B3), the autofit_profiling exporter (B4a), any PyAutoFit change
(if the harness needs one, add a strict xfail/skip naming the phase and report it).

## Verification

Harness unit tests (simulators reproducible from seed, row schema, exporter fixture, protocol verdict logic); the CI
witness leg green; `build_readme.py --check`; `export_inference_summary.py --check`; Insight `check --offline` on the
fixture; `ruff` clean; `repos_sync --check` unchanged (no registry edits).

## Shape

One autofit_inference PR, in reviewable commits (protocol first, then datasets, harness, reference runs, exporter, CI).
Difficulty large → effective `supervised`: under `--auto` the ship checkpoint is decide-and-flag (one flagged decision
at most); a second fork parks on the issue. Tier judge: human /prm.
