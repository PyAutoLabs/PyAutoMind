# EP campaign — phase map for the 2026 Q3 graphical/EP push

Type: research
Target: graphical_ep
Themes:
- graphical-ep
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: graphical-ep
Filed: 2026-08-19 (backfilled from git)

Filed 2026-08-19 from James's multi-phase EP brief (raw text preserved in the
intake session). This is the umbrella view; each phase's real content lives in
its own prompt file. Update the table as phases ship.

## End goals (acceptance for the campaign as a whole)

1. An analytic Gaussian model that statistically demonstrates the graphical
   and EP source code is correct (means *and* errors against closed form).
   The model shipped in phase 1 as a single-seed CI gate; the *statistical*
   half moved to the Cortex on 2026-09-09 as science project
   `analytic_gaussian` (task `tasks/analytic_gaussian/ensemble_parity.md`),
   which runs it as a seed ensemble on RAL.
2. slope_hierarchy cosmology: accurate graphical + EP results, EP scaling to
   100+ datasets, fast, interpretable/inspectable output for a scientist,
   running on RAL A100s.
3. IC50: graphical + EP scaling to 10 000+ datasets, with EP-vs-graphical
   parity demonstrated at small N.

## Phases

| # | Phase | Prompt | State (updated 2026-09-09) |
|---|-------|--------|--------------------|
| 1 | Analytic Gaussian benchmark (the keystone — start here) | `complete/2026/09/analytic-gaussian-benchmark.md` | **SHIPPED 2026-09-02** — autofit_workspace_test#91, PR #92 merged `54af208398ae7fd336d3d9bca363776ad50da037` (`scripts/graphical/analytic_*.py`); record `complete/2026/09/analytic-gaussian-benchmark.md`. Verdict: closed form, minimal EP and the graphical joint fit agree everywhere; **every failing cell is autofit's EP column, including the exactly Gaussian leg A**. Six PyAutoFit mechanisms root-caused and filed (see Findings below); the autofit-parity scripts are parked NEEDS_FIX until they land, the closed-form reference + minimal EP are curated into the smoke gate. **Review follow-ups shipped 2026-09-07**: Codex review of PR #92 (autofit_workspace_test#96 / PR #97, record `complete/2026/09/ep-review-92-followups.md`) — the θ = σ Laplace leg is the STALE state, not a collapse; `log_sigma` moments pinned against quadrature. D6 shipped 2026-09-07 — findings table complete. **Ensemble scale-up 2026-09-09**: the keystone became Cortex science project `analytic_gaussian` (PyAutoCortex PR #27, human merge pending), the third alongside `slope_hierarchy_scale` and `ic50_workspace`. Wave 1 = job `342413_[0-199]`, 200 independent draws at N=5 on the `ral` partition, submitted against RAL PyAutoFit mirror `66f9f8d5d` (verified to contain #1580 first). Its witness was pre-registered before submission. **First post-D1–D6 measurement: leg A autofit EP is now EXACT** (mu 50.8595 ± 4.1104 against the same reference, a = b = 0.000) — the leg that parked `analytic_gaussian.py` NEEDS_FIX; leg B returns σ 9.37 ± 3.57 against 6.57 ± 2.88, outside the cell tolerance, inside the closed-form [q05, q95], not collapsed. The ensemble turns that caveat into a rate and gives the moment-matching cure a number to beat |
| 2 | Scatter-collapse cure or caveat | `complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md` | **SHIPPED 2026-09-02** — cure of the mechanism (#1558/#1560/#1562) + caveat (README §3.5); record `complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md`; cure follow-on filed `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md` (human decision). Close-out 2026-09-02: `complete/2026/09/ep-collapse-unpark.md` (autofit_workspace_test#94 / PR #95) curated `analytic_gaussian_collapse.py` into the smoke gate (RECOVER 5/5). **Codex review of the fixes shipped 2026-09-07** as bundle `ep-phase2-review`: PyAutoFit#1572 coupled-transform covariance in `from_mode` (`transformed-from-mode-coupled-covariance.md`), #1573 P1 deterministic variables kept cavity covariance on the fd-Hessian path (`ep-laplace-deterministic-hessian.md`), #1574 fully reverted projection counted as updated (`ep-full-revert-not-updated.md`), #1576 + autofit_workspace_test#98 per-(factor, variable) stale tracking with `reverted_variables` in `ep_history.csv` (`ep-stale-tracking-per-variable.md`) |
| 3 | Graphical (non-EP) JAX scaling | → PyAutoCortex `tasks/slope_hierarchy_scale/n25_scale_up.md` (the task of record for project `slope_hierarchy_scale`; carries the measurement addendum) and `graphical_scoping.md` sub-tasks | **gated 2026-09-08** — a fresh Cortex science project `slope_hierarchy_scale` was born for it (Cortex PR #25, issue Cortex#24): the wrapped-up N=5 tree was vaulted to `Science/z_projects_complete/slope_hierarchy` and its row retired, the code borrowed into `Science/slope_hierarchy_scale`, and the task moved `planned → gated` on `Gates: PyAutoFit#1405, #1558, #1560, #1562`. PR #25 **merged 2026-09-08** (merge `866d8f0`; issue Cortex#24 closed, record `complete/2026/09/slope-hierarchy-scale-birth.md`). Next: `/cortex` → `move tasks/slope_hierarchy_scale/n25_scale_up.md ready` → submits the N=25 runs |
| 4 | IC50 EP end-to-end + scale ladder | → PyAutoCortex `tasks/ic50_workspace/ep_scale_up.md` (phase 1 of project `ic50_workspace`; dev companion stays in the Mind as `feature/autofit/ep_lbfgs_jax.md`) | **RUNNING ON RAL 2026-09-09 — parity at N=5 achieved.** The 2026-09-08 blockers (dirty checkout, no `results/` witness path, row `dormant`) are all cleared; Cortex row `active` and task `submitted` via PyAutoCortex PR #26 (human merge pending). Runs `342408` (EP, sim, nlive 150, max_steps 12, 56.7 s) and `342409` (graphical joint Dynesty, sim, nlive 150, 21.4 s), partition `ral`, against a mirror **verified to contain #1580** — so unlike phase 3's EP arm these carry the full D1–D6 wave. **Result: 33/33 within 3σ for both methods, 0/33 cross-method disagreements** (`results/graphical_ep_comparison_sim.txt`). Caveats: N=5 only, the scale ladder is not started; EP's median σ is still 2.3× the graphical fit's on `hill_coef` (0.980 vs 0.423); and the gain over the archived `_v1` run confounds the D1–D6 fixes, nlive 50→150 and laptop→RAL. Setup shipped as 5 commits on `feature/ep-phase4-ral-setup` (unpushed, public repo — see Phase 4 notes below). The companion dev prompt `draft/feature/autofit/ep_lbfgs_jax.md` is still open and is now the scale lever, not a blocker |
| 5 | Diagnostics sufficiency checkpoint | no prompt yet — deliberate | judge after phases 2 & 4 produce real runs; the 2026-07 diagnostics wave (#1330/#1335) shipped and caught #1383; graphical_scoping sub-tasks 5–6 (summary JSON, dashboard) are the likely follow-ups; concrete item from phase 1–2: STALE = zero SUCCESS updates is now warned by the library (#1562); 2026-09-07: #1574/#1576 extended STALE to full reverts and to per-(factor, variable) tracking, and `ep_history.csv` gained `reverted_variables`; the BIASED-TIGHT guard calibration stays a human call |
| 6 | Profiling: autofit_profiling repo + two epics | `research/autofit/autofit_profiling_bootstrap.md` | filed; repo creation human-gated |

Adjacent live work this campaign leans on but does not own: priors/messages
phase 4 (`bug/priors/` tracker — design #1500, findings #1498/#1501) and the
slope_hierarchy methods write-up (moved to the Cortex 2026-09-03 as
PyAutoCortex `tasks/slope_hierarchy/methods_writeup.md`, state `planned` — it stayed
under the retired `slope_hierarchy` row on 2026-09-08 and is the human's to move or drop).

## Findings (phase 1, 2026-09-02)

The benchmark's referee verdict, from autofit_workspace_test#91 (evidence in
its two phase comments) and the read-only root-cause pass, recorded on
PyAutoFit#1405. Each mechanism is a Mind prompt under `draft/bug/autofit/`:

| # | Mechanism | Prompt | Size |
|---|-----------|--------|------|
| D1 | The first prior of a process (id 0) compares equal to the `FactorValue` sentinel, so every multi-variable factor gradient is corrupted; leg A `mu` stays at its start (50.00 ± 20.6 vs 50.86 ± 4.11) | `complete/2026/09/ep-prior-id-zero.md` | **SHIPPED 2026-09-02** — PyAutoFit#1558 merge `809b4fd85ce308cb7bcd18b58e1202ad73d82fba` (PyAutoFit#1557). Leg A `mu` mean now exact (a = 0.000), SUCCESS = 20; remaining std bias (3.76 vs 4.11) is D2 |
| D2+D3 | Laplace "covariance" = mean-field precision + one non-accumulating random diagonal secant (no factor curvature; result depends on prior ids through sampling order); a failed line search still projects the start point and overwrites the message | `complete/2026/09/ep-laplace-hessian.md` | **SHIPPED 2026-09-02** — PyAutoFit#1562 merge `5375f4d631547bc946687cf3645d3689654e510d` (PyAutoFit#1561). FD Hessian at the mode (deterministic, K-invariant), skip-not-write on failed/non-concave updates, per-variable backstop naming variables, STALE covers skips. Leg A 18/18 byte-identical across prior ids; collapse config RECOVER 5/5; leg B `sigma` 9.37 ± 3.57 inside the exact interval |
| D4+D5 | Truncation limits dropped by `from_natural_parameters`/`__pow__` (leg B σ message returns limits (−inf, inf)); `TransformedMessage.from_mode` skips the Jacobian for scalar variables (log-σ leg never moves) | `complete/2026/09/ep-message-support.md` | **SHIPPED 2026-09-02** — PyAutoFit#1560 merge `9eb80852233590205bc53366cb4ddf26b0be1ba5` (PyAutoFit#1559) + workspace autofit_workspace_test#93 merge `7d175ddbf3d2774e09fde4131cf35d2d95146351`. Leg B scatter message keeps limits `(0, 100)`; loggaussian `log_sigma` moves 2.30 → 1.55; truncated `mu` row still collapses ~2e-4 = D2/D3 |
| D6 | `errors_at_sigma(as_instance=True)` crashes on a prior-valued global model | `samples_errors_at_sigma_instance_prior_valued_model.md` | **SHIPPED 2026-09-07** — PyAutoFit#1578 merge `6331b800` (PyAutoFit#1577) + autofit_workspace_test#99 merge `93219107`; record `complete/2026/09/samples-errors-at-sigma-instance.md`. Fix keeps the tuple-attribute instance contract (`Model.instance_for_arguments` returns a `ModelInstance` of bounds pairs for Prior-class components). Phase-1 findings D1–D6 all shipped; side finding: `analytic_gaussian.py`'s graphical column is unseeded (`draft/bug/graphical_ep/analytic_gaussian_unseeded_graphical_column.md`) |

Cure follow-on: `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md` — un-parks `analytic_gaussian.py` / `analytic_gaussian_priors.py` when it lands.

Calibration facts to reuse: EP with a Gaussian site on σ is biased on this
model by construction (seeds 0–4 scatter row a ≤ 0.077, b ≤ 0.145 for the
minimal EP) — that is the analytic ceiling any autofit fix should be judged
against, not zero. Phase 5's diagnostics checkpoint gains a concrete item:
zero SUCCESS updates on a factor is a STALE result that no library warning
currently reports.

## Phase 4 notes (2026-09-09) — IC50 setup

The setup was almost entirely defect-clearing, not new science: both fit arms,
all 8 SLURM submit scripts and a 560-line `hpc/sync` already existed and had
never once been run end to end. Five defects would each have blocked or
corrupted a RAL run, all now fixed in `ic50_workspace`:

1. `--partition=cpu` in all four CPU submit scripts — **RAL has no `cpu`
   partition** (`ral`, `gpu`, `cam`, `imp`). Every CPU submission would have
   been rejected. `slope_hierarchy_scale`'s generic template carries the same
   bug; its working script uses `ral`.
2. `PROJECT_PATH` was never exported to `sbatch`, though every submit script
   begins `source $PROJECT_PATH/activate.sh`.
3. `activate.sh` put a **two-month-stale `PyAutoConf` checkout on PYTHONPATH**,
   shadowing the pip-installed package, and omitted `PyAutoNerves`. `autoconf`
   is not even an importable module on RAL any more — the line was pure legacy.
4. A plain `push` shipped **5.6 GB** (the rnaseq CSV plus a symlink into a
   sibling `concr` checkout that does not exist on RAL). Excluding them takes
   it to 1.7 MB.
5. `PULL_DIRS=(output)` would never have retrieved `results/` — the very path
   the Cortex witness glob watches.

Two findings worth carrying forward:

- **The existing witness under-reports.** `ep_sim.py`/`graphical_sim.py` assert
  only on `coef_mean`; `coef_matrix` and `hill_coef` are printed but never gate.
  Run against the archived `_v1` sidecars, the new comparator found the
  graphical arm had 3/33 parameters beyond 3σ that no run ever reported as a
  failure. Widening the assertion is an open follow-up.
- **IC50's EP cannot hit the dead-pool-worker hang.** It passes
  `force_x1_cpu=True`, so Dynesty runs with no process pool — the failure mode
  that has had phase 3's `342351` stuck for 27+ hours is structurally absent
  here.

`concr` consolidation (assessed 2026-09-09): `ic50_workspace` is canonical;
concr's cancer code has been frozen since 2026-05-07. Ported
`compare_graphical_ep.py` (the parity table). Still open: `one_by_one.py` (no
per-dataset baseline exists here), `graphical_nuts.py` (a second sampler, only
ever tested at n=3). **Do not copy concr's ~3,500 preprocessed drug-1073
datasets** — their `x` is `ln(dose index)`, not `ln(µM)`, and their latent is
20-dim against this workspace's 5; the corpus predates concr's own
`n_latent 20→5` reduction. Scaling real data means re-running
`preprocess_real.py` with `N_DATASETS` raised. **Sign convention:** the
inverted form `n*(log_ic50 - x)` is in `concr/model_api.py`, all of
`scripts/cancer`, all of `scripts/cancer_sim` **and `simulators/cancer_sim.py`**
— concr's own simulator. Only `cancer_legacy/real/{ep,viz_hill}.py` match the
canonical decreasing form. `concr/model_api.py`'s log-likelihood is separately
broken (`+0.5·z·z`, no `/noise_sigma`) and must never be copied.

Scale-ladder blocker now removed: `--n_datasets` / `--nlive` / `--max_steps`
are CLI flags on the sim scripts (they were module constants). `simulator.py`,
`preprocess_real.py`, `ep_real.py` and `graphical_real.py` still hard-code
their counts.

## Sequencing

Phase 1 first (cheap, unblocks 2, referees everything). Phase 2 shipped
2026-09-02 from its banked evidence once 1 gave the analytic upper limit
(`complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md`). Phase 3 runs in
parallel (different machine profile — RAL). Phase 4 after 1–2 establish
trust. Phase 6 epic 1 (general profiling) can start any time; epic 2 (EP
profiling) last, once end-to-end runs exist to profile.

## Deferred — check-in gates, not scoped work

- **JAX/gradient/Hessian EP internals** — against changing EP internals while
  end-to-end models are the goal; adopt only if a genuinely simple change
  dramatically simplifies/speeds things. (`feature/autofit/ep_lbfgs_jax.md`
  covers the *factor-fit sampler*, which is allowed; this gate is about the
  EP update maths itself.) — 2026-09-02: the moment-matching cure prompt is the first candidate for this gate. 2026-09-07: still the human's call (`Autonomy: supervised`); the phase-2 review bundle did not touch the update maths.
- **Sampler-result reuse across EP passes** — complicated for efficiency-only
  gains; revisit via profiling epic 2 evidence (ep_scoping sub-task 6).
- **Parallel factor updates on HPC** — revisit when scaled runs approach
  multi-day wall times (ep_scoping sub-task 5 holds the sketch).
- **Multi-dataset factors (EP/graphical middle ground)** — revisit once
  scaling has hit whichever wall (memory or wall-time) shows up first.
