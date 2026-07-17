# Profile + speed up AggregateImages/AggregateFITS (png/fits workflow aggregators)

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Final leg of the aggregator profiling arc (#1375 A-D + awt#171 all merged): the original
prompt's catalogue workflow is "csv, fits, png files" at 3000-lens scale, but only the
CSV aggregator (`af.AggregateCSV`, −25% in Fit#1376) was profiled and sped up.
`af.AggregateImages` (png_make) and `af.AggregateFITS` (fits_make) were never measured.

In @PyAutoFit + @autofit_workspace_test:

1) Extend the merged mock harness so templates carry realistic image/fits payloads
   (stub PNGs exist already; add stub .fits files), and add `aggregate_images` +
   `aggregate_fits` stages to the profiling grid.
2) Baseline, then take the low-hanging fruit in
   `autofit/aggregator/summary/aggregate_images.py` / `aggregate_fits.py` — the CSV
   sibling hid double evaluation and repeated per-row disk loads, so the same class of
   defect is plausible here. Behaviour-preserving, before/after numbers in the PR.
3) Out of scope: making single-file deserialization faster (the known deeper follow-up).
