# HowToFit tutorial_5: `without_paths` prose claims 2 parameters, model has 6

Type: bug
Target: howto
Repos:
- HowToFit
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised

Found while clearing the stale NEEDS_FIX marker on this tutorial (PyAutoFit#1411). The script
runs to completion (exit 0) — this is a **prose/teaching correctness** bug, not a crash.

`scripts/chapter_1_introduction/tutorial_5_results_and_samples.py` composes a **two-component**
model at line 291:

```python
model = af.Collection(gaussian=af.Model(Gaussian), exponential=af.Model(Exponential))
```

That is 6 free parameters (gaussian centre/normalization/sigma + exponential centre/normalization/rate).

But the prose at lines 653-654 says:

> We can alternatively filter the `Samples` object by removing all parameters with a certain path.
> Below, we remove the Gaussian's `centre` to be left with **2 parameters; the `normalization` and
> `sigma`**.

and the print label at line 667 repeats it:

> "All parameters of the very first sample (containing only the Gaussian normalization and sigma)."

The actual run prints **5** values. `samples.without_paths(["gaussian.centre"])` is behaving
correctly — it removes one path from six. The prose is stale, evidently written when this
tutorial fitted a Gaussian alone (3 params → 2).

A learner following this section sees five numbers where the text promised two, with no
explanation, which undermines exactly the filtering concept the section is teaching.

## Fix

Update the prose at lines 653-654 and the print label at line 666-668 to describe the real
outcome: removing `gaussian.centre` leaves the remaining 5 parameters (the Gaussian's
`normalization` and `sigma`, plus all three of the Exponential's). Consider naming the
Exponential explicitly so the reader connects the count to the two-component model composed
earlier in the tutorial.

Check the neighbouring `with_paths` sections (lines 627-648) for the same staleness — their
labels say "containing only the Gaussian centre", which IS correct (1 value), so they likely
survived the model change intact. Confirm rather than assume.

Regenerate notebooks after (`generate.py howtofit`).
