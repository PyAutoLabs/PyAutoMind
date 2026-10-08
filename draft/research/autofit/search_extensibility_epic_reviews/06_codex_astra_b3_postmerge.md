# Codex gpt-6-astra adversary review — B3 (autofit_inference#5, PyAutoInsight#23, PyAutoCortex#61), post-merge, 2026-10-08

Independent read-only audit of autofit_inference `ec35be4..900648b5c665`, PyAutoInsight `c6285fd82449^1..c6285fd82449`, and PyAutoCortex `d3ab73a6c826^1..d3ab73a6c826`, using the supplied completion record, epic, PR bodies and B2 review; no files changed or compute submitted.

## §1 Verdict — FINDINGS

The pilot’s published coverage and regenerated acceptance counts reconcile: **223 rows, 35 accepted, 110 rejected, 78 not assessed; 297 deferred runs**. The implemented acceptance thresholds can fail, and pending JAX-blend references do not grant acceptance.

Six findings remain. They concern invalid bootstrap intervals, contradictory freeze instructions, lost or omitted warm-start costs, false convergence diagnostics, and an Insight board still showing zero pilot records. These prevent using the implementation unchanged for scored wave 2.

The two already-filed findings concerning fp32 and NSS are not repeated.

## §2 Witness falsification per clause (Holds / Fails / Unverified + evidence)

Paths without a repository prefix below are relative to `autofit_inference/`.

| Clause | Result and evidence |
|---|---|
| Pilot coverage is honest and ranks nothing | **Holds.** Counted 223 JSON rows; every row has `pilot: true`, PyAutoFit `0dbf258c4f5e4238fc1cfd1b2eae56c6c6e6f655`, and `resumed: false`. Catalogue contains 13 measured searches, NSS deferred and Drawer unsupported, grouped by requested task. Expected coverage reconciles to 520. |
| Acceptance thresholds are operative | **Holds for tested inputs.** Starting with an accepted separated Nautilus row, independently changing its centre median to 1.01 reference σ away, σ ratio to 0.49 or 2.01, PPC excess to 10.01, or evidence error to 1.01 nat each produces `rejected`. A point/MAP value 1.01 nat below reference also rejects. Implementations: `_protocol.py:127`, `:136`, `:221`. |
| Threshold formulas match the protocol | **Holds.** Median differences use reference σ; σ-ratio bounds are inclusive; PPC is the registered **one-sided** excess; evidence uses absolute offset-adjusted difference; MAP uses the registered lower threshold. |
| MAP values distinguish log likelihood from log posterior | **Holds numerically.** Independently evaluated all four committed MAP vectors against the committed data. Reproduced log posterior values 186.66766632 / 186.66766752 for blend numpy/JAX and 175.70635949 / 175.70636135 for separated numpy/JAX, within \(1.2\times10^{-13}\) of recorded values. This does not prove global optimality. |
| Disjoint-prior and ln 3! normalization agree between rows and references | **Holds.** Separated references have normalized evidence equal to raw evidence, approximately 122.93115577. `run_evidence_offset()` returns 0 for disjoint priors and −1.791759469 for the validated Nautilus blend convention. B3 fixes the reference builder to use that same function (`build_reference.py:82`). |
| Pending or incompatible references cannot authorize acceptance | **Holds.** All 78 JAX-blend exported rows are `not_assessed`. Changing data seed to 777, assertion mechanism, or reference status to `pending` also produces `not_assessed`. |
| Reference construction fails closed | **Holds for reproduced failure paths.** With in-memory reference runs whose evidence differs by 100 nat between seeds, the builder returns `disagreeing`, with both family checks false. Without raw samples, the supplied checkout returns `samples_missing`, not `complete`. Full pooled-reference rebuilding is **unverified**. |
| Success rates, Wilson intervals and wall point estimates are correct | **Holds for all 34 assessable catalogue cells.** Independently recomputed fractions, Wilson bounds, summed attempt/provider costs, and zero-success lower bounds. All match. **Bootstrap intervals fail:** finding 1. |
| README/catalogue/summary reproduce the committed rows | **Holds for regenerated outputs.** README and calibration checks pass; catalogue and summary rebuild byte-for-byte in memory. Raw stored verdicts require the qualification in §4. |
| `inference-summary@1` matches Insight’s reader | **Holds structurally.** Actual consumer classification returns `('ok', [])` for all 223 records. In-memory board rendering succeeds. Warm-start timing semantics are incomplete: finding 4. |
| Insight board shows the pilot records | **Fails at the pinned merge.** Its committed Fit snapshot has zero records at B2 `ec35be4`. Offline checking passes against that snapshot, not against the B3 publication: finding 6. |
| Insight/Cortex registrations satisfy their schemas | **Holds within stated limits.** Insight campaign loading and registry validation pass; offline checking passes using the available external Mind body map. `python scripts/cortex.py check` returns `cortex check: OK`. Cortex is active with an empty Runs section, consistent with no recorded RAL submission. |
| Protocol predates pilot rows; scored thresholds are frozen | **Preregistration holds; freeze intentionally deferred.** Git places original protocol `b670379` and the disjoint-prior amendment before pilot rows. Deferral is authorized, but the resume sequence contradicts the required freeze order: finding 2. |
| Fresh Nautilus CI witness passes | **Unverified.** The workflow retains `--require-accepted`; no fresh sampler execution or remote CI verification was performed. |

All twelve B2 findings were checked:

| B2 finding | Disposition at B3 |
|---|---|
| 1. Mode truncation | **Enacted.** `_posterior.py:128` clusters weighted samples without the 4,000-sample truncation; minority-mode regression test passes. |
| 2. Arbitrary reference fallback | **Enacted.** `build_reference.py:179` returns `disagreeing`; reproduced in memory. |
| 3. Reference identity | **Enacted.** `_protocol.py:63` includes dataset, backend, data seed and assertion mechanism; mutation tests refuse mismatches. |
| 4. Quantile-averaging fallback | **Enacted.** `build_reference.py:152` requires raw samples; reproduced `samples_missing`. |
| 5. Reference limitations omitted | **Enacted.** `_protocol.py:279` and exporter `:203` propagate them into verdicts and reasons. |
| 6. Completion substituted for termination | **Enacted.** `_protocol.py:309` requires recorded termination; Nautilus extraction and budget-stop tests pass. |
| 7. Admission probe rejected by assertions | **Enacted by inspection.** `_runner.py:779` probes the truth vector. Runtime test blocked by the environment’s temporary-directory restriction. |
| 8. Cold/warm identity collision | **Enacted.** `_runner.py:291` separates cache identities; tests pass. The JAX sample-order limitation is also recorded. |
| 9. Failed-attempt cost lost | **Partially regressed.** Ordinary fit exceptions retain elapsed cost; B3’s new provider stage falls outside that protection. Finding 3. |
| 10. Missing disjoint-prior control | **Enacted by inspection.** `models/gaussian_x3.py:169` implements separate centre ranges without assertions; committed references identify that mechanism. Runtime model test was environment-blocked. |
| 11. Platform-identical float test | **Enacted.** `test_simulators.py:21` uses `rtol=1e-12, atol=0`; dataset reproduction tests pass. |
| 12. Missing MAP diagnostic | **Enacted.** `_protocol.py:259` records it for completed assessable rows without making it a posterior/evidence acceptance condition. |

## §3 Findings, ranked by severity

### 1. P1 — Bootstrap confidence intervals discard their unbounded outcomes

**Location:** [`scripts/misc/tooling/build_catalogue.py:129`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/autofit_inference/scripts/misc/tooling/build_catalogue.py:129).

**Input → wrong output:** Actually ran:

```python
bootstrap_wall_per_success([10.0, 10.0], [True, False])
# [10.0, 20.0]
```

A bootstrap resample has zero successes with probability 25%. Those outcomes are unbounded, but `if k:` discards them. The reported interval is conditional on drawing a success, not the registered bootstrap interval.

Four committed cells exhibit this: separated DynestyStatic numpy, separated DynestyDynamic numpy/JAX, and blend Nautilus `n_live=200` numpy. Each has one success from two attempts. For example, DynestyStatic reports `[282.291064, 457.504749]` seconds despite an unbounded upper percentile.

**Fix:** Retain zero-success replicates as unbounded when computing percentiles. Serialize an explicit unbounded endpoint without JSON infinity. Rebuild the affected intervals.

### 2. P1 — Resume instructions require scored-wave observations before the scored-wave freeze

**Location:** [`wiki/project/protocol_gaussian_x3.md:160`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/autofit_inference/wiki/project/protocol_gaussian_x3.md:160), `wiki/project/state.md:62`, and [`PyAutoInsight/campaigns.yaml:96`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/PyAutoInsight/campaigns.yaml:96).

**Input → wrong output:** The human ruling ends pilot compute and moves deferred cells to wave 2. Protocol §7 nevertheless says the freeze waits until those deferred runs are in, while also requiring it before the first wave-2 row. Insight instructs the next session to run the 297 deferred cells and then freeze.

Following those instructions either restarts the terminated pilot or permits scored observations to influence their judging thresholds. This is a documentary contradiction, not a criticism of the authorized decision to defer freezing.

**Fix:** Replace the resume instructions with an explicit freeze-before-scored-execution gate based on available calibration evidence. Any subsequently authorized calibration extension must be identified separately and excluded from scored results. Preserve the A2 **and A4** revision gate for scored wave 2.

### 3. P2 — Failed warm-start providers lose their entire elapsed cost

**Location:** [`scripts/misc/searches/_runner.py:825`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/autofit_inference/scripts/misc/searches/_runner.py:825), provider execution at `:512`, exception accounting at `:873`, and `build_catalogue.py:152`.

**Input → wrong output:** Executed the actual runner’s outer try/except AST in memory, omitting its filesystem-writing `finally`, with a raising provider. It produced:

```text
status: failed: RuntimeError: provider failed after 600 seconds
fit_start: None
total_wall_s: None
timing: no provider record
```

Passing that failure into `leg_summary()` produces a zero-second lower bound: both missing costs are coerced to zero.

The provider timer is local and its record is returned only after successful initialization of the consumer. A provider exception, termination, or initialization failure therefore escapes the B2 elapsed-cost repair.

**Fix:** Persist provider elapsed time in `finally`, including failure paths, and preserve it when constructing the failure row. Unknown elapsed cost must suppress or qualify wall estimates, not become zero. No current committed row has a null total wall; this is a reproduced future failure path.

### 4. P2 — Insight receives consumer-only warm-start timing without the provider cost

**Location:** [`scripts/misc/tooling/export_inference_summary.py:208`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/autofit_inference/scripts/misc/tooling/export_inference_summary.py:208); consumer display at `PyAutoInsight/insight/board.py:366`.

**Input → wrong output:** The accepted separated warm NUTS seed 0 records:

```text
consumer total_wall_s:    73.6883904
provider_wall_s:        1076.4696580
combined attempt cost: 1150.1580484
```

The catalogue correctly uses 1,150.16 seconds. The summary omits `provider_wall_s` and `warm_start`, exporting `timings.total_s = 73.6883904`. Actual in-memory Insight rendering displays **73.6883904** in “Total s”. Its definition does not disclose the excluded provider.

Schema validation passes because it checks the field’s shape, not completeness of the cost accounting.

**Fix:** Export the warm-start provenance and separate provider/consumer costs; define the board’s total as their combined attempt cost. State exclusions explicitly and verify the reader renders them consistently.

### 5. P2 — A completely stuck parameter can disappear from convergence assessment

**Location:** [`scripts/misc/searches/_posterior.py:285`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/autofit_inference/scripts/misc/searches/_posterior.py:285).

**Input → wrong output:** Generated a `(4000, 4, 10)` chain using RNG seed 4, with nine mixing parameters and `background.level` fixed at zero across every draw and chain. The actual functions returned:

```text
background R-hat / ESS: NaN / NaN
aggregate R-hat:        1.0003906723
aggregate bulk ESS:     7696.2344397
convergence:            converged
```

`finite_r` and `finite_e` silently remove the stuck parameter. Protocol §5 requires the diagnostics on **every** parameter. Sanitizing its NaNs later does not invalidate the already-finite aggregate.

**Fix:** Require valid diagnostics for every free parameter before emitting aggregate pass values. Report constant/stuck dimensions explicitly and return `not_assessed` or `not_converged` with the reason. This reproduction establishes a false-convergence path, not a falsely accepted committed row.

### 6. P2 — The merged Insight board does not satisfy the pilot-record witness

**Location:** [`PyAutoInsight/snapshots/fit.json:6`](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/b3/PyAutoInsight/snapshots/fit.json:6), `receipts/fit.json:7`, and `dashboard.md:12131`.

**Input → wrong output:** The pinned receipt and snapshot reference B2 `ec35be4`, with zero records. The board says “Qualification: no measurements”.

Actually ran offline checking with the available Mind body map:

```text
ok fit: inference-summary@1 valid, 0 records ... ec35be493712
check: OK
```

Adding `--from fit=autofit_inference` validates 223 records at `900648b5c665`, but the command ends `check: FAIL` because the dashboard input digest differs.

The PR body discloses this pending refresh. Nevertheless, at the requested post-merge pin, the witness remains incomplete; merge order alone did not refresh the capture.

**Fix:** Capture the merged producer revision and regenerate the receipt, snapshot and board. Add a B3 acceptance check requiring the expected producer revision and 223 records, alongside ordinary schema checking.

## §4 Unverifiable claims and practical limits

- **Verification executed:** 64 harness tests passed. Ten tests requiring temporary files were deselected. Two additional tests failed while importing PyAutoFit because `dill` probes for a writable temporary directory; these are environment failures, not established implementation failures. Reference-builder failure cases were additionally reproduced in memory.
- **Other checks:** Ruff lint/format, README and calibration checks passed. Summary and catalogue reconstructed exactly. Cortex checking passed. Insight offline checking passed with the external Mind body map; its Brain state-schema validator was unavailable in the supplied checkout.
- **Raw scientific evidence:** Raw sample archives are absent. I could not independently rebuild pooled marginals, PPC curves or reference mode masses, rerun offsets, establish global MAP optimality, or reproduce fresh sampler results. Recorded MAP-vector evaluations and summary arithmetic were independently checked.
- **Stored versus regenerated verdicts:** Raw row JSONs contain 14 accepted, 33 rejected and 176 not assessed. Rejudging against the final references/offsets changes 98 verdicts: 21 to accepted and 77 to rejected. That explains the published 35/110/78 counts; it is not evidence of fabricated successes. Consumers must distinguish run-time verdicts from later reference-backed reassessment.
- **Wave-2 support is unfinished:** The pilot manifest fixes ten local seeds; its grouping key omits data realization, protocol and library revision (`_pilot.py:164`). I confirmed that changing those fields leaves the cell key unchanged. Reference discovery supports only the current `*/*/reference.json` layout. These mechanisms need explicit scored-wave identities and per-realization references before handling 50 seeds × five realizations. Current identity checks safely refuse unmatched references.
- **Remote state:** Later board refreshes, GitHub CI outcomes and RAL execution were not verified. All three audited working trees remained clean.

## §5 Decisions I would overturn

I would overturn the instruction to **run deferred cells before freezing `@2`**. It conflicts with both the no-more-pilot ruling and the requirement to freeze before scored observations.

I would also reject treating `check --offline` as proof that the merged Insight board contains the pilot: it presently verifies the zero-row B2 capture.

I would retain the partial-pilot wrap-up, no-ranking policy, pending JAX reference, disjoint-prior zero offset, disclosed Nautilus-only references, and decision to defer the freeze itself.

## §6 Recommended resume actions (ordered list a next session can act on, each tagged before-wave-2 / before-B5 / later)

1. **[before-wave-2]** Resolve the contradictory resume instructions; specify the freeze gate and retain the A2+A4 revision requirement without restarting pilot compute.
2. **[before-wave-2]** Retain unbounded bootstrap replicates and regenerate the four affected intervals.
3. **[before-wave-2]** Preserve failed-provider costs and stop treating unknown timing as zero.
4. **[before-wave-2]** Export and display combined warm-start attempt cost with provider provenance.
5. **[before-wave-2]** Make convergence assessment require valid diagnostics for every free parameter.
6. **[before-B5]** Refresh Insight from `900648b5c665` or its documented successor; verify the board actually contains the 223 pilot records.
7. **[before-B5]** Implement scored-wave manifests, per-realization reference storage, versioned judging and attempt accounting that distinguish missing attempts from deliberate deferrals.
8. **[later]** Preserve reference/offset revision provenance for reassessments and rerun the environment-blocked tests and fresh witness in a writable environment.