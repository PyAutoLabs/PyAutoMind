## aggregate-images-fits
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1385
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1386 (MERGED)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/51 (MERGED)
- summary: Final aggregator-arc leg — the png/fits catalogue workflows profiled for the first time. Harness: mock templates carry a panelled subplot_fit.png (4×3) + multi-HDU fit.fits (4 EXTNAMEs); aggregate_images + aggregate_fits stages added to the grid.
- BUG FOUND+FIXED (Fit#1386): AggregateFITS._hdus opened the source fits once PER REQUESTED HDU and the returned ImageHDUs kept the memmaps (handles) alive — 2 leaked fds/result measured; "Too many open files" crash at ~500 results at default ulimit (Euclid = 3000). extract_csv leaked 1/result the same way. Fix: one open per source file per result, data copied out of the memmap, deterministic close. 0 leaks at 100 results, identical output, +19% at 2 HDUs (interleaved A/B — cross-run timing was poisoned by a concurrent session, in-process A/B used instead).
- AggregateImages profiled CLEAN (~1.5ms/result, caches per result) — no change made, honestly reported.
- arc totals: csv −25% (#1376), png clean, fits leak-fixed +19% — all three catalogue workflows measured and harnessed.

## Original prompt

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
