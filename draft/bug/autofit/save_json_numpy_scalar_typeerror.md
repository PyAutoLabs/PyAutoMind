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
