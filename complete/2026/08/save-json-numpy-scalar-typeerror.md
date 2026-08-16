- library-prs: https://github.com/PyAutoLabs/PyAutoFit/pull/1479
- merge-commits: PyAutoFit `b6e89cd5480018c9b9661ac2b214ec1d084e3964` (2026-08-16)
- issue: none — split out of the prior-support Clipper prompt's "do not lose these"
- summary: Adds `NumpyEncoder` in `autofit/tools/util.py` (`np.ndarray` ->
  `tolist()`, `np.generic` -> `item()`, everything else deferred to the base
  class so a genuinely unserialisable object still raises), wired into both
  output-path writers. A successful fit could previously die at its output step
  with `TypeError: Object of type float32 is not JSON serializable`.
- validation: 13 new tests; full suite 1804 passed / 4 skipped / 1 failed, the
  failure pre-existing (nautilus single-core pool) and identical on a clean tree.
- release: not performed; merged PR remains in the pending-release queue.

## Why it hid for so long

`np.float64` subclasses Python's `float`, so `json` serialises it without help.
**`np.float32` subclasses nothing `json` knows** — nor does `np.int32`/`np.int64`
(not a Python `int` on every platform) or `np.bool_`.

So a float64 run is fine, and a float32 run is fine *right up until it writes its
results*, at which point the whole computation is discarded at the last step.

It surfaced on the `imaging/mge` profiling cell during the Clipper prototype
(autolens_profiling#128) on a path that cell had apparently never taken: it did
**not** fire while 14 of 16 lanes were dead, because the float32 values never
reached the saved object. **It fires precisely when lane survival improves** —
which is what the phase-2 campaign exists to cause.

## The second site the prompt never named

The prompt described `paths/directory.py:80` only. Implementing it turned up
`Samples.info_to_json` (`samples/samples.py:338`), a second bare `json.dump` —
and the more dangerous of the two. `samples_info` is a search's own diagnostic
channel, so **every new counter added to it is another chance to reintroduce
this**. PyAutoFit#1478 added two counters to that very dict on the same day.

That is the argument for fixing at the encoder rather than at each producer:
the producers are search-specific and keep multiplying. The encoder closes the
class; chasing producers closes one instance.

## Guarantees asserted, not assumed

- `float64` unchanged, compared byte-for-byte against a bare `json.dumps`.
- No invented precision — `.item()` widens float32 to a Python double, and the
  test asserts equality with `float(np.float32(0.1))` rather than a re-rounded
  decimal.
- Still strict — `json.dumps({"x": object()}, cls=NumpyEncoder)` raises.

Reproduced against the unfixed tree before fixing:
`paths.save_json(name="c", object_dict={"clipped": np.float32(4.0)})` raised
exactly the reported `TypeError`.

## Original prompt

# `save_json` crashes on numpy scalars — a successful run dies at output

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Filed 2026-08-16. Split out of the prior-support Clipper prompt's "Two incidental
bugs found while investigating — do not lose these" section (item 1), which asked
for it to be filed separately once confirmed. It is confirmed — see Grounding.
That prompt has since shipped as PyAutoFit#1477; its record is
`complete/2026/08/prior-support-clipper.md`. **This bug was not fixed by it** —
verified still present at `1f4b66a`, the merge commit itself.

> **IN FLIGHT — PyAutoFit#1479 open 2026-08-16**, branch
> `claude/autofit-save-json-numpy`. Advance to `complete/` on merge.
>
> Reproduced against the unfixed tree first: `paths.save_json(name="c",
> object_dict={"clipped": np.float32(4.0)})` raises exactly
> `TypeError: Object of type float32 is not JSON serializable`.
>
> Fixed with a `NumpyEncoder` in `autofit/tools/util.py`, wired into **both**
> output-path writers — `DirectoryPaths.save_json` and, which the prompt below
> did not name, `Samples.info_to_json` (`samples/samples.py:338`). That second
> one is the more dangerous of the two: `samples_info` is a search's own
> diagnostic channel, so every new counter added to it is another chance to
> reintroduce this.
>
> 13 new tests. Full suite 1804 passed / 4 skipped / 1 failed, the failure
> pre-existing (nautilus single-core pool) and identical on a clean tree.

## The defect

`@PyAutoFit/autofit/non_linear/paths/directory.py:80` serialises with a bare
`json.dump`:

```python
with open_(self._path_for_json(name, prefix), "w+") as f:
    json.dump(object_dict, f, indent=4)
```

No `default=` hook and no encoder class, and there is **no JSON encoder anywhere
in `autofit/`** to fall back on (grepped for `JSONEncoder` / `cls=` / `default=`
— zero hits). So any `numpy.float32` (or any other `np.generic` / `np.ndarray`)
that reaches a saved dict raises:

```
TypeError: Object of type float32 is not JSON serializable
```

`float64` survives only because it subclasses Python `float`. `float32` does
not, which is why this is precision-dependent rather than universal.

## Why it matters more than its size suggests

**It fires at the end of a *successful* run**, in the output step, after the
whole fit has been paid for. On the `imaging/mge` profiling cell that is minutes
of compute discarded at the last moment.

Worse, **it fires exactly when things start working**. It did not fire on the
baseline multi-start runs, because 14 of 16 lanes were dead and the float32
values never reached the saved object. It appeared only once prior-clipping kept
lanes alive — i.e. on a code path this cell had apparently never taken. Any
change that improves lane survival will surface it.

It also compounds: the truncated file this crash leaves on disk is the input to
the second bug, `draft/bug/autofit/crashed_run_poisons_resume.md`. Fixing this
one removes the common trigger for that one, but does not fix it — the two are
independent and both should land.

## The fix

Give `save_json` a numpy-aware `default=` (or an encoder class, since there is
none yet and other call sites will want it): `np.generic -> .item()`,
`np.ndarray -> .tolist()`. Decide whether it lives on `DirectoryPaths` or as a
shared helper the database paths can use too — `save_json` is the only bare
`json.dump` on the output path, but the same values flow through
`save_samples_summary` / `save_samples_info`.

Prefer coercion at the encoder over hunting down each producer: the producers
are search-specific and new ones will keep appearing, which is the failure this
bug demonstrates.

## Verify

- `paths.save_json(name=..., object_dict={"x": np.float32(1.5)})` round-trips
  through `load_json` and returns `1.5`, rather than raising `TypeError`.
- Cover `np.float32`, `np.int32/int64`, `np.bool_` and a small `np.ndarray`, and
  assert the loaded types are plain Python.
- Regression at the level it was found: a `MultiStartGradient` run that ends with
  **all lanes alive** completes and writes its output. The all-alive condition is
  load-bearing — an all-dead run passes without exercising the bug.
- `float64` behaviour is unchanged (it already worked; do not let a coercion
  change its precision on the way out).

<!-- Grounding: verified against PyAutoFit main at 1f4b66a93 (shallow clone,
     2026-08-16). Read directory.py:66-80 for the bare json.dump, and grepped
     autofit/ for JSONEncoder / cls= / default= — no encoder exists. Symptom
     first observed on the imaging/mge profiling cell during the Clipper
     prototype (autolens_profiling#128). -->
