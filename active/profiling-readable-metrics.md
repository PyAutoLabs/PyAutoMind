# Separate likelihood implementations and explain profiling measurements

Type: bug
Difficulty: medium
Consequence: judge
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/27
Repos: PyAutoPulse

@PyAutoPulse — workspace/organ presentation work, not a scientific library change.

## Original request (verbatim)

I think that numba results should be their own section (e.g. Delaunay (numba) as they are their own likelihood function with their own source code root. Under Likelihood runtime I think text like "Single JIT Block", "Vmap.Per Call" can be turned into easier more descriptive text, so for th forst one may (JAX jit function), but think hard how to make this clearer. Not all likelihood breaksdown have a Component Total at the top, I think they should have longest blocks at the top goin descending, For A100 there is "Setup Prefix" which is longer than the component time so I'm not sure that should all be there? I also think all the text here could be clearer what it corresponds to, like "Reconstruction JIT.Steady Per Call S" can this just say what step of the likliehood function it is? We probably need a mapping of steps into a more human readable text extract of what they are rather than these which I assume are JAX-y names?

## Approved plan — user: “go”

- Separate each Numba likelihood into its own model entry, such as Delaunay (Numba), with implementation-specific results, defaults and script links. Preserve separate-tab navigation.
- Replace raw runtime keys with labels distinguishing compiled single evaluations, post-compilation timing blocks, steady medians, total batch time and batch-average cost per evaluation.
- Show the recorded component total separately when present. Sort the main likelihood steps longest-first within comparable groups; never fabricate a missing total.
- Move cumulative prefixes, overlapping sub-step probes and duplicate low-level JIT timings out of the main chart into a collapsed diagnostic section. Preserve original measurements and links.
- Maintain an explicit, source-grounded step label/description mapping; show the scientific operation, with technical keys and timing context available in details/tooltips.
- Validate Numba/JAX isolation, script ownership, sorting, overlap handling, missing totals, labels, deep links and responsive charts; regenerate the board.

Tier: judge — merge mode: human /prm.

## Detailed implementation

Primary/only edit repo: PyAutoPulse. Proposed branch: feature/profiling-readable-metrics. Canonical Pulse and Mind clean on main; Pulse only local branch main; conflict helper returned 0. The separate autolens_profiling community-pages claim is untouched. No compute runs or producer changes.

1. `pulse/setup_browser.js`: derive a presentation implementation identity from recorded evidence/script routes, not `identity.backend` (which contains cpu/gpu) or the mere presence of numba in dependency metadata. Separate navigation entries, URL state, setup matching, curated defaults and evidence/script links. Preserve existing setup IDs and old explicit deep links. Unknown identities must remain distinguishable rather than silently joining either implementation.
2. Add a tested, explicit measurement presentation mapping in the Pulse browser assets (and update `pulse/setup_browser.py::assets` if split into a separate asset). Ground canonical labels in the profiling producers and adapter mappings; keep the source reader-only. Runtime examples: `single_jit_block` → Full likelihood (JAX-compiled, post-compilation average); `single_jit_median` → Full likelihood (JAX-compiled, steady median); `vmap.per_call` → Average per likelihood in a batch; `vmap.batch_time` → Total batch time. Include recorded batch size where available without substituting current defaults.
3. `panels`, `timingScope`, `scaleKey`: classify records into headline runtime, main component rows, totals, cumulative prefixes and overlapping diagnostics. Prefer the producer's actual attributed `steps` table for the main breakdown where both attributed and duplicate JIT probes exist. Do not strip JIT/vmap context and then merge distinct measurements. Sort descending only within compatible groups, keep units/timing semantics and existing evidence identity boundaries.
4. Scientific step labels include reconstruction → Solve for the source brightness, data vector → Build the data vector, curvature matrix → Build the curvature matrix, regularization → Build the regularization matrix, mapped reconstruction/evidence → Evaluate the model image and log evidence. Prefix labels describe their cumulative endpoint (e.g. Setup through the mapping matrix), never present them as isolated step costs. Preserve the original metric key and source link for inspection; unknown keys get an honest fallback.
5. Render recorded component totals distinctly from the sorted step list. If absent, display a concise missing-total indication and use the existing labeled maximum scale; do not sum overlapping probes or call a component total a compiled likelihood time. No raw values are altered.
6. `pulse/setup_browser.css`, `tests/browser_fixture.py`, `tests/browser_setup.cjs`, renderer tests: fixtures for Numba and JAX on CPU, numba mentioned only as dependency, script filtering, cumulative prefix exceeding a main component, duplicate probes, missing totals, descending order and reload/navigation. Required Ruff, Python, Chromium and offline checks. Regenerate dashboard artifacts through the owning CLI.

## Investigation evidence

- Heart door STALE (exit 1): published feed contains old monitoring failures; planning allowed. Fresh ship-time gate still required.
- Captured catalogue contains 59 setups whose evidence paths identify Numba, while their `model` remains e.g. `delaunay`/`rectangular`; hardware backend alone is insufficient.
- `autolens_profiling/scripts/imaging/delaunay/likelihood_breakdown.py` documents `_setup_prefix_fn` as params-to-stage output, records absolute prefixes beside attributed differences, and explicitly excludes overlapping sparse/reconstruction diagnostics from `total_step_by_step`.
- `scripts/misc/tooling/catalogue_adapters.py::DIRECT` maps `full_pipeline_single_jit` to `single_jit_block` and `total_step_by_step` to `component_total`.
- `scripts/misc/tooling/build_dashboard.py` documents the single-JIT statistic as a ten-call block after the first call, potentially affected by A100 post-compile settling; `likelihood_runtime.py` divides total vmap batch time by batch size to produce `vmap.per_call`.
- Existing reader treats all breakdown metrics as similar rows and title-cases raw keys; that is the presentation defect being corrected.
