# Codex gpt-6-astra adversary review — B2 (autofit_inference#3), 2026-10-08

Independent-adversary leg over branch `feature/search-ext-b2-harness` at f58a087 (`codex exec --sandbox read-only -c model_reasoning_effort=high`, run from the task worktree root). Enacted the same day; see the PR and `complete/2026/10/search-ext-b2-harness.md` once closed.

## §1 Verdict — FINDINGS

Reviewed `feature/search-ext-b2-harness` at `f58a087ad791`. This checkout contains **nine**, not ten, commits over `origin/main`. No files changed.

The basic export/check plumbing works, but the scientific instrument can miss substantial posterior modes, certify disagreeing references, and compare incompatible runs. Those defects prevent CLEAN.

## §2 Witness falsification per clause

| Witness clause | Result |
|---|---|
| CI runs one Nautilus seed and exports an accepted row | **Wired correctly; fresh execution unverified.** [witness.yml:73](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/.github/workflows/witness.yml:73) runs the specified dataset/settings/seed and invokes `--require-accepted`. Re-exporting fixture seed 0 against the **real committed reference** produces `accepted`: worst median difference 0.06σ, coverage 1/1, normalized ln Z 138.742 versus 138.853. This verifies the exporter, not a fresh sampler execution. |
| Protocol predates every wave-1 row | **Supported, presently vacuous for wave 1.** `b670379` introduces the protocol before dataset/reference commits. There are no tracked `results/searches/` rows. Comparing that commit with HEAD shows changes only in §10; **§6’s agreeing-subset fallback was present initially**. |
| README and summary `--check` pass | **Confirmed empirically.** Both pass; the committed summary contains zero records. WALL, Ruff lint and Ruff format checks also pass. |
| Summary validates against Insight `check --offline` | **Schema validity confirmed; command-level claim needs qualification.** Insight’s actual classifier accepts the committed summary, fixture, and fixture re-exported against the real reference. Plain `check --offline` passes, but the available [registry.yaml:3](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/PyAutoInsight/registry.yaml:3) registers only `lens`, so that invocation does **not** validate Fit. |

Additional checks that held up:

- **Preregistration:** thresholds and PLACEHOLDER markings precede committed results. Git establishes publication order, not when somebody first inspected an uncommitted run.
- **Criterion arithmetic:** median/ref-σ, inclusive σ-ratio band, one-sided PPC χ² difference, and offset-adjusted one-nat evidence tolerance match the written formulas. PPC uses 500 weighted-resampled curves and their pixel-wise median. See [_protocol.py:124](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_protocol.py:124) and [_runner.py:569](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_runner.py:569).
- **LogL versus logP:** I found no interchange in the inspected extraction/acceptance paths. Independently evaluating the committed MAP vector gives logL **197.65352470403823** and logP **186.6676663217698**, matching the committed values. The MAP evaluator explicitly requests posterior fitness at [run_map_reference.py:76](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/reference/run_map_reference.py:76).
- **Relabelling:** complete `(centre, normalization, sigma)` triples are sorted together; raw label-ordering weights are accumulated correctly. The separate mode-clustering defect is below.
- **CLI/WALL/RAL:** tests confirm rejection of conflicting backend/precision/location names. WALL runs in [lint.yml:67](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/.github/workflows/lint.yml:67); the template explicitly has [`--partition=ral`](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/hpc/batch_cpu/template:21). WALL is a CI gate; `hpc/sync submit` directly invokes `sbatch`, without running it first.
- **Insight shape:** the exporter supplies accepted vocabulary, `protocol_id`, `reason`, and `asserted_by`; real consumer validation passes.

## §3 Findings ranked by severity

### 1. P1 — Mode truncation can hide a scientifically significant mode

[_posterior.py:123](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_posterior.py:123) clusters only the heaviest 4,000 samples, retaining their original weights and discarding the remainder.

**Confirmed empirically:** a synthetic 90%/10% two-mode posterior becomes one mode; processing all samples recovers both. The committed reference’s 144,830 samples have effectively **100%** weight in one cluster, but its [stored mode weight](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/results/reference/gaussian_x3_blend/numpy/reference.json:205) is **0.102666**—exactly the mass of the retained 4,000.

**Failure scenario:** a reference mode exceeding the protocol’s 5% coverage threshold disappears or falls below it, allowing a run that missed that mode to pass. This violates the [registered mode definition](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/wiki/project/protocol_gaussian_x3.md:59). Approximation must preserve mode masses, not select only high-weight samples.

### 2. P1 — The reference builder declares completion when no family agrees

[build_reference.py:151](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/reference/build_reference.py:151) chooses Nautilus when `agreeing` is empty; [line 164](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/reference/build_reference.py:164) unconditionally writes `status: complete`.

**Confirmed empirically:** perturbing per-seed evidence values in memory produced:

```text
status: complete
nautilus.logz_ok: False
dynesty_static.logz_ok: False
included evidence spread: 200.004 nat
```

**Failure scenario:** future references with no agreeing subset become authoritative and judge subsequent runs. §6 permits an **agreeing** subset, not an arbitrary fallback. The current committed Nautilus subset does pass; the defect is in the builder’s failure path.

### 3. P1 — Reference compatibility omits data realization and assertion mechanism

References are keyed only by dataset class/backend at [export_inference_summary.py:125](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/tooling/export_inference_summary.py:125). Acceptance checks those two fields but not `data_seed` or `assertion_mechanism` at [_protocol.py:208](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_protocol.py:208).

**Confirmed empirically:** a reference-matching row remains `accepted` after independently changing:

```text
data_seed → 777
assertion_mechanism → no_assertions
```

**Failure scenario:** the exposed `--data-seed` option judges a new noisy dataset against seed 1’s posterior; a differently constrained run receives an evidence comparison despite §4(c)’s explicit same-mechanism requirement. Reference and offset identity must include and enforce these distinctions.

### 4. P2 — Missing raw samples silently changes the reference estimator

[build_reference.py:106](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/reference/build_reference.py:106) substitutes averages of marginal summaries and the first run’s modes when any `samples.csv` is unavailable.

**Confirmed empirically:** hiding raw-sample access in memory still yields `complete`, with `pooling: mean of per-run marginals`. The current reference’s largest median change is about **0.000951**.

**Failure scenario:** rebuilding on a fresh checkout produces a different reference under the same protocol. Averaging quantiles is not pooling distributions, and first-run modes do not represent pooled coverage. Missing required samples should prevent rebuilding a complete reference.

### 5. P2 — Verdicts omit the limitation that permits Dynesty’s exclusion

The reference records the disagreement, but [_protocol.py:274](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_protocol.py:274) and [export_inference_summary.py:176](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/tooling/export_inference_summary.py:176) never propagate `reference.limitations`.

**Confirmed empirically:** exported acceptance records contain no Dynesty/reference-disagreement limitation.

**Failure scenario:** Insight displays an unqualified acceptance based solely on Nautilus, although [protocol §6](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/wiki/project/protocol_gaussian_x3.md:130) requires the disagreement to accompany **every verdict using that reference**.

### 6. P2 — Nested convergence substitutes completion plus ESS for termination evidence

[_protocol.py:255](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_protocol.py:255) checks only completion and Kish ESS, then reports `"terminated"`.

**Confirmed empirically:** `completed=True`, ESS=1000 and explicitly false termination evidence still produces `converged`.

**Failure scenario, confirmed by inspection:** Nautilus can return from its loop because its likelihood-call budget is exhausted, independently of convergence; see [PyAutoFit’s termination branches](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/PyAutoFit/autofit/non_linear/search/nest/nautilus/search.py:622). The harness must record and inspect the actual termination condition required by protocol §5.

### 7. P2 — NumPy admission timing measures assertion rejection, not likelihood evaluation

[_runner.py:510](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_runner.py:510) times the physical prior medians. All three centre medians are **50**, violating both strict ordering assertions.

**Confirmed by inspection:** NumPy Fitness catches the resulting `FitException` and immediately returns its sentinel before evaluating the Analysis; see [fitness.py:450](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/PyAutoFit/autofit/non_linear/fitness.py:450).

**Failure scenario:** `per_call_s`, estimated likelihood cost and likelihood share measure the rejection path. The observed/estimated labels do not make this a valid likelihood-cost estimate. Use a valid representative vector.

### 8. P2 — Cold and warm runs share output and result identity

`compile_cache` is absent from [output_path_prefix](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_runner.py:294), result paths and run IDs.

**Confirmed by inspection:** changing only `--compile-cache cold` to `warm` uses the same PyAutoFit search output and overwrites the same result JSON.

**Failure scenario:** the second purportedly separate run resumes an already completed fit, records a short load-time `total_wall_s`, and destroys the first row. This cannot support the promised cold/warm comparison.

Separately, JAX “evals-to-target” comes from posterior sample order at [_runner.py:600](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_runner.py:600), not a full evaluation history. Nautilus supplies those samples through `posterior()`. The estimate needs this limitation stated; its sample index is not an observed evaluation count.

### 9. P2 — Failed attempts lose their elapsed cost

[_runner.py:548](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_runner.py:548) assigns `total_wall_s` only after `search.fit` returns successfully.

**Confirmed by inspection:** an exception during fitting reaches the failure-row writer with `total_wall_s=None`.

**Failure scenario:** expensive failed attempts cannot contribute their cost to the protocol’s expected wall per right answer. A hard timeout can also leave no row; the `finally` block does not guarantee accounting for terminated processes.

### 10. P2 — The separated control does not implement D15’s disjoint-prior control

The [final design decision](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/PyAutoMind/draft/research/autofit/search_extensibility_epic_report.md:880) identifies `separated` with option (b), **disjoint centre priors**.

**Confirmed by inspection:** [build_model](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/models/gaussian_x3.py:106) has no dataset-specific choice: both datasets use shared `U(0,100)` centre priors and ordering assertions.

**Failure scenario:** separated generating peaks are treated as the planned disjoint-prior experiment, although prior geometry and assertion-volume effects remain. Implement the intended control or explicitly reconcile the design and protocol.

### 11. P2 — The committed reproducibility test still demands platform-identical floats

[test_simulators.py:19](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/test/test_simulators.py:19) still uses `assert_array_equal`.

**Confirmed by inspection; reported CI failure not independently verified:** seeded noise does not guarantee identical floating-point Gaussian-profile evaluation across NumPy builds/platforms.

`np.testing.assert_allclose(..., rtol=1e-12)` is a reasonable fix for the reported one-ULP difference. I verified that one-ULP perturbations of both datasets pass it. Its tolerance is negligible relative to noise σ=0.04. Keep seed/truth assertions exact; document any added absolute tolerance.

### 12. P3 — The promised MAP diagnostic is absent from posterior/evidence verdicts

[Protocol §4(a)](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/wiki/project/protocol_gaussian_x3.md:84) requires those rows to record criterion (a) diagnostically. [_protocol.py:222](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/scripts/misc/searches/_protocol.py:222) evaluates it only for point/MAP tasks.

**Confirmed by inspection:** raw max-logP is recorded, but the promised reference-MAP diagnostic is not. Add it without making it an acceptance condition for other tasks.

## §4 Unverifiable claims and practical limits

- **Fresh witness execution:** the sandbox cannot create even temporary files; importing PyAutoFit reaches `dill`’s temporary-directory lookup and fails. I did not rerun Nautilus.
- **GitHub CI:** `gh run list` could not connect to `api.github.com`. Therefore I cannot confirm that the one-ULP discrepancy was the **only** CI failure, or that subsequent jobs/installations passed.
- **Tests:** **45 passed, one deselected** because it writes a new dataset using `tmp_path`. Ruff and all three requested project check scripts passed.
- **Dependencies:** the [witness installation recipe](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/.github/workflows/witness.yml:51) is plausible against the available TOMLs: it collects both libraries’ dependencies, removes the source-provided `autonerves` requirement and adds Nautilus. I found no definite install contradiction. Fresh resolution, current remote `main`, and the downloaded lychee archive remain unverified.
- **Laptop dependence:** no laptop absolute path is required by the Python runner/exporter. CI explicitly supplies source checkouts through `PYTHONPATH`. HPC activation and the [batch template](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/hpc/batch_cpu/template:31) have explicit RAL defaults. Reference rebuilding, however, depends materially on unpublished local raw outputs—finding 4.
- **Preregistration completeness:** this is a preregistered **pilot**, not frozen scored-wave criteria. Pending JAX/separated references are clearly disclosed in [§10](/home/jammy/Code/PyAutoLabs-wt/search-ext-b2-harness/autofit_inference/wiki/project/protocol_gaussian_x3.md:188).

## §5 Decisions I would overturn

**Nautilus constant-likelihood rerun:** I would **not overturn the n_live=2000 rerun itself**. The live-point count was not preregistered; the ±0.1 window was preserved, and the failed NumPy attempt remains recorded. The measured −1.825116 differs from −ln 6 by only 0.033357 nat.

The check really measures the registered **relative evidence convention**: assertions on versus off, separately by backend. I additionally inspected raw samples: constrained runs have essentially 100% ordered-centre weight; unconstrained runs have roughly one-sixth. Thus the current measurements are not merely a zero-difference pass caused by absent constraints. They do not establish robustness across seeds/settings or absolute evidence accuracy; a fixed replication plan would strengthen scored-wave use.

**Dynesty exclusion:** I would **not overturn it as a retrospective protocol amendment**: §6 expressly allowed it in `b670379`. The committed reference rebuilds exactly from local samples, and the included Nautilus runs satisfy the registered agreement thresholds.

I **would overturn its presentation as an unqualified reference-backed verdict** until finding 5 is fixed, and reject the builder’s ability to certify a reference when no subset agrees. Nautilus-only repeatability does not restore the independent cross-sampler agreement that failed.
