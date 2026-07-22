# autofit_workspace features/interpolate: instance prints are mislabelled and aggregator order is not fit order

Type: bug
Target: autofit_workspace
Repos:
- autofit_workspace
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised

Found while clearing the stale NEEDS_FIX marker on this script (PyAutoFit#1411). The script runs
to completion (exit 0) and **the interpolation itself is correct** — this is a labelling bug in
the print statements that makes the tutorial's headline claim unverifiable.

`scripts/features/interpolate.py` fits three datasets at t=0, 1, 2 and prints, at lines 221-222
and again at 267-268:

```python
print(f"Gaussian centre of fit 1 (t = 1): {ml_instances_list[0].gaussian.centre}")
print(f"Gaussian centre of fit 2 (t = 2): {ml_instances_list[1].gaussian.centre}")
```

Two separate defects compound here.

## 1. Off-by-one in the labels (both blocks)

`ml_instances_list[0]` is the **t=0** fit and `[1]` is the **t=1** fit — the list is built by
`for time in range(3)`. The labels claim t=1 and t=2. The surrounding prose then tells the reader
the interpolated t=1.5 centre "is between the value inferred for the first and second fits taken
at times 1.0 and 2.0" — so the reader is invited to bracket 1.5 between two numbers that are
actually the t=0 and t=1 fits. The bracketing check silently fails to demonstrate anything.

## 2. The aggregator does not return fit order

The second block rebuilds the list from `agg.values("samples")`. Verified against the real
`output/interpolate` directory:

```
aggregator order (time, centre):
   0   40.049
   2   59.731
   1   49.963
```

So aggregator index 1 is the **t=2** fit, not t=1. This is why the two blocks print a different
"fit 2" value (49.96 in-memory vs 59.73 from the aggregator) despite being the same three fits —
a discrepancy the tutorial presents without comment, as if the aggregator round-trip changed the
result.

Interpolation is unaffected: `AbstractInterpolator._value_map` keys by the `time` attribute and
sorts, so both blocks correctly print the same interpolated t=1.5 centre (54.834). Only the raw
index-based prints are wrong.

## Fix

- Correct the labels to the times they actually index, or better, index by time rather than
  position so the print cannot drift again — e.g. select from the list by matching
  `instance.time`.
- For the aggregator block, sort the loaded instances by `instance.time` before printing (and say
  in the prose that aggregator ordering is not guaranteed to be fit order — that is a genuinely
  useful thing for a reader to learn here).
- Once both blocks label by time, the two blocks should print matching values, which makes the
  aggregator round-trip demonstrate the point it is meant to demonstrate.

Regenerate notebooks after.
