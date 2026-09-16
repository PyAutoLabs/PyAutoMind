# AggregateFITS cannot read tracer.fits: files/tracer.json shadows image/tracer.fits in SearchOutput.value

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- aggregator
- fits
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: On a lens result whose zip carries both files/tracer.json and image/tracer.fits, `af.AggregateFITS(agg).extract_fits(hdus=[al.agg.fits_tracer.convergence])` returns an HDUList whose second entry is an ImageHDU with EXTNAME CONVERGENCE, instead of raising `AttributeError: 'Tracer' object has no attribute 'index_of'`.
Review-minutes: 10
Unattended: ready
Related: euclid_strong_lens_modeling_pipeline#80 (the workaround `AggregateTracerFITS` in catalogue/scripts/lens_mass_maps.py is to be deleted once this ships)
Filed: 2026-09-16

Origin: found 2026-09-16 while implementing euclid_strong_lens_modeling_pipeline#80 (per-lens
convergence/potential/deflections FITS collected from finished fits). Measured on the real
`dr1_sep1` results with PyAutoFit/PyAutoLens 2026.8.17.1.

## Defect

`AggregateFITS._hdus` (`autofit/aggregator/summary/aggregate_fits.py`) resolves an HDU enum to
its source file with `result.value(subplot_filename(hdu))`. For `al.agg.fits_tracer`
(`FITSTracer`, `autolens/aggregator/subplot.py`) that name is `"tracer"`.

`SearchOutput.value` (`autofit/aggregator/search_output.py`, ~line 229) searches `self.jsons`
**before** `self.pickles + self.arrays + self.fits`. Every lens fit writes both
`files/tracer.json` (the max-log-likelihood `Tracer`, via `save_results`) and
`image/tracer.fits` (`fits_tracer`, `config/visualize/plots.yaml`), so `value("tracer")`
returns the `Tracer` object and `_hdus` dies:

```
File "autofit/aggregator/summary/aggregate_fits.py", line 74, in _hdus
    source_hdu = source[source.index_of(hdu.value)]
AttributeError: 'Tracer' object has no attribute 'index_of'
...
File "autofit/aggregator/summary/aggregate_fits.py", line 87, in _hdus
    source.close()
AttributeError: 'Tracer' object has no attribute 'close'
```

`al.agg.fits_tracer` is therefore unusable through `AggregateFITS` for any lens result. No other
`FITS*` enum collides (`galaxy_images`, `model_galaxy_images`, `fit` have no same-named JSON),
which is why the existing `deblending.py` workflow never hit it.

## Fix candidates

1. `AggregateFITS._hdus` resolves the source through `result.fits` (name-matched `FITSOutput`)
   rather than `result.value(name)`: the FITS files are unambiguously FITS there. Minimal and
   local; this is what the pipeline's stand-in `AggregateTracerFITS` does.
2. Or give `SearchOutput.value` a kind hint / a `fits(name)` accessor used by the FITS
   aggregators.

Either way, add a unit test with a stub search output carrying both a JSON and a FITS named
`tracer` (the pipeline's `tests/test_lens_mass_maps.py::test_extraction_reads_the_fits_not_the_same_named_json`
is a ready template) and a workspace follow-up to delete `AggregateTracerFITS` from
`euclid_strong_lens_modeling_pipeline/catalogue/scripts/lens_mass_maps.py`.
