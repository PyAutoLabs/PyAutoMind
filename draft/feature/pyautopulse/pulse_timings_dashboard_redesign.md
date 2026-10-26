# Pulse dashboard redesign: Profiling Timings and Inference Timings

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoPulse
- autolens_inference
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Epic: likelihood-lifecycle
Status: formalised
Consequence: judge
Witness: the published Pulse board has separate Profiling Timings and Inference Timings sections, each opening per-project (PyAutoFit / PyAutoLens) tables with the human's column layout; every table row opens a dedicated detail page (profiling rows restore the old per-setup page with the full breakdown); `pyauto-pulse check` and pytest pass
Filed: 2026-10-26

## Human rulings (2026-10-26, chat)
- Per-call / per-node toggle: DROP it from the profiling table. Add one bold column "Est. 12-core s" =
  per-call runtime ÷ 6, for **numba CPU rows only** (— elsewhere). The value is producer-emitted by
  autolens_profiling (Pulse computes nothing; emitted since autolens_profiling#467, record complete/2026/10/likelihood-lifecycle-p2a-restamp-12core.md). The projected node throughput moves to each setup's detail page.
- Profiling table columns: Dataset type | Model | Instrument | Regime | Setup | Hardware class | Model variant |
  Runtime s (bold, 5 DP, no "(single_jit_median)") | Est. 12-core s | Class | › (opens detail page).
  Status, Decision and Evidence move to the detail page.
- Inference per-eval columns come from `search.summary`, emitted by the autolens_inference exporter
  (additive walltime-validation fields; Pulse computes nothing):
  "Log Likelihood Function Evaluation Time (seconds)" and "Time Per Sample (seconds)". Headers must say clearly
  which is which.
- Setup ids display without `_fp64` (e.g. `jax_sparse`, `numba_sparse`); fp32/mixed becomes a model variant.
- Inference table: a "Profiling runtime s" column (the matched autolens_profiling per-call runtime for the row's
  likelihood/instrument/setup/hardware/model variant, producer-joined) sits right after Model variant, before the
  sampler columns. Today 0/56 rows match a profiling record (predicted_ms_per_eval null), so the join needs fixing
  in the exporter against profiling @3.
  Each row's Profiling runtime value is a LINK to that profiling setup's detail page (the same page the profiling
  table's › opens), so the inference ↔ profiling link is explicit (human 2026-10-26). The exporter emits the
  matched profiling record id; Pulse resolves it to the page URL.
- Inference table: only `nautilus:mass_total[1]` rows, Sampler shown as `nautilus`, no note about the filter.

- HUMAN 2026-10-26 (after the exporter survey; reaffirmed: "only use that column for all hardware ... dont use the search.summary log likelihood evaluation time"): the inference table shows **implied s/eval only** on all hardware (wall ÷ evals,
  in s, 5 DP) — NEITHER search.summary column (search.summary "Log Likelihood Function Evaluation Time" is one
  un-warmed call incl. JAX compile, ~12 s on GPU; "Time Per Sample" duplicates implied s/eval). This supersedes the
  earlier "replace Predicted/Measured-predicted/Parallel-efficiency with two search.summary columns" line.
- HUMAN 2026-10-26: rectangular inference runs use 28² (784 px) vs profiling standard 35²: show the Profiling runtime
  with a size-differs marker until a 28² profiling row exists (draft/feature/autolens_profiling/rectangular_28sq_profiling_rows.md).
  Parametric stages (no inversion) get no profiling link.

## Order
autolens_profiling producer (12-core field) and autolens_inference exporter (search.summary fields) first,
then the PyAutoPulse renderer. Code map: `pulse/setup_browser.py` `_render_lifecycle` (v3 table, counts text,
knowledge link), `pulse/setup_browser.js` (old v2 per-setup detail view to restore per row; v2 companion
`dashboard/catalogue/setups.json`), `pulse/board.py` `WALLTIME_COLUMNS` / `WALLTIME_NOTE` / nav,
`pulse/campaigns.py` "Profiling Results" headings.

## Original request (verbatim)

Split "Profiling Results" (turn into "Profiling Timings) and "Inference Timings" and have each open up to clickable
projects (PyAutoFit / PyAutoLens).

The interface for "PyAutoLens: setups by class" looks good, I like it showing all results as a aay can see in a table
and navigate., but a lot of cleaning up can be achieve:

This is text clustter "300 current · 379 superseded (shown with History) · 99 archived (counted, not shown). Class and status are the producer's declarations; this board ranks nothing."
Just have a single icon to the top right above the Hiistry button which tallys the otle available results which are
not superseded (have it match the green font).

Have a sub title called "Extra Information" which links to "Read: Comparing CPU-parallel and GPU-batched setups (decision rules, not a decision)." but remove the clustter "(decision rules, not a decision)."

The table is formatted annoyingly, with my words reading over two lines. We should split imaging and delaunay so its not imaging/delauany but seaprate columns.
I think "Setup" should should split into columns  remove the _fp64 (fp32 can become a model variant) which is redundant and have it just read
like jax_sparse so its concise. 

The thing I fine most confusing is having "Measurement" a column which encompasses everything because this means the table
acts as a source of finroamtion for vastly different regimes. I would remove the Measurement column and selection box,
always just show runtime (which makes for clear comparison) and then having it so that for each table row you can click 
it (e.g. on the right) to get to all information for that setup, as weas the original Pulse setup with a click taking
you to the full information. This means the full breakdown could be shown for each setup, try and restore things to what
that page lookjed like as we had it set up well.

In the table here we can save a lot of space then by removing the Measurement column, making value be to 5 DP without
brackets like "(single_jit_median)". I think everything will now give nicely makign also put the times in bodl so
they standard out on the table. 


For Inference Timings table, I think we are aiming to achieve the same setup, but again theres currently too much
info about it could bemore concise:

- This text is clutter "Full-fit measurements: one sampler run per row. Every derived number is the producer's; Pulse computes no ratio and never reads a full-fit time as a per-likelihood measurement.

- We should split imaging and delaunay so its not imaging/delauany 
- I think "Setup" should should split into columns  remove the _fp64 (fp32 can become a model variant) which is redundant and have it just read
like jax_sparse so its concise. 

- For now these left hand columns are mirroring Profiling Timings whichi s good.

- Sampler, Just put nautilus, only put results for mass_total[1] and ignore all others but dont mention this as I think
we will onyl use specific result types and this is the right simplification for now.

- Make Wall s round to 1 DP.

- convert implied ms/eval to s and round to 5 DP.


- Replace these 3 coluns Predicted ms/eval    Measured/predicted    Parallel efficiency    with the likelihood evaluation time from search.summary and a measure likelihood per eval time for search.summary make column headers clear.

- Remove these 3 Parity    Reference runtime record    Release

- Make sure table column headers dont wrap text (e.g. Likeliho - od evals)

_ think the column which pairs the run time based on "Profiling Runtmie" should be to the far left, after "Model Variant",
as this distinguishes it from all sampler settings. 

- Again as before and probably like Insight still is, each run should be clickalble and go to a dediciatdd page will the full
information. The buttons which do filtering which are curently under "PyAutoLens: setups by class" shoiudl also be made
for this. 
