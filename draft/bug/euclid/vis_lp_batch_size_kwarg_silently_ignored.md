# `vis_lp` passes `batch_size=50` to `af.Nautilus`, which has no such parameter

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoFit
Themes:
- euclid
- hygiene
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Review-minutes: 3
Unattended: ready
Filed: 2026-08-31

Found during the euclid-dr1-prep phase-3a prose restoration (issue
euclid_strong_lens_modeling_pipeline#47), while verifying the `__Search__` prose
of `scripts/initial_lens_model.py` against the code.

## The finding

`scripts/initial_lens_model.py` builds the `vis_lp` search as:

```python
search = af.Nautilus(
    name="vis_lp",
    **settings_search.search_dict,
    n_live=750,
    batch_size=50,
    ...
)
```

but `af.Nautilus.__init__` (checked against autofit 2026.8.29.1) has **no
`batch_size` parameter** — the sampler's batch is `n_batch`, and `batch_size`
exists only as a read-only property. Verified:

```python
import inspect, autofit as af
sig = inspect.signature(af.Nautilus.__init__)
"batch_size" in sig.parameters   # False
"n_batch" in sig.parameters      # True
```

So `batch_size=50` lands in `**kwargs` and is (apparently silently) swallowed —
the `vis_lp` search likely runs at the `n_batch` default rather than 50. The
`vis_pix` search in the same file correctly passes `n_batch=15`, as do all five
searches in `scripts/full_model.py`.

## What to do

1. Confirm where the stray kwarg goes (does `NonLinearSearch` store unknown
   kwargs, and does anything downstream read `batch_size`?). If it is truly
   inert, decide the intended value: was `vis_lp` tuned expecting batch 50?
2. Fix `scripts/initial_lens_model.py` to pass `n_batch=50` (or whatever the
   intended batch is), or delete the argument if the default is the tuned
   behaviour in practice (it has been running this way since the phase-1 port).
3. Consider whether `af.Nautilus` should reject unknown kwargs loudly — a
   silently swallowed tuning parameter is exactly the failure mode that hid
   this. That half may belong in a PyAutoFit prompt if pursued.

The phase-3a docs PR deliberately corrected the prose (`__Search__` no longer
claims `batch_size=50` controls GPU parallelism) without touching the code —
docs phases change no behaviour.
