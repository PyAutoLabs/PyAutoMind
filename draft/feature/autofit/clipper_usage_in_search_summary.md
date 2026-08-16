# Report how much the Clipper actually fired — surface the count in `search.summary`

Type: feature
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Filed 2026-08-16, immediately after phase 1 shipped
(`complete/2026/08/prior-support-clipper.md`, PyAutoFit#1477 → `1f4b66a`).

## What is asked for

**The number of Clipper uses must be counted, and stored in `search.summary`.**

Half of that already exists. The other half does not, and the gap is not where
it looks.

## What already exists — do not rebuild it

`n_clipped_lane_steps` is already accumulated in
`@PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py:863`:

```python
if has_clipper:
    params, clipped_mask = self.clipper.project(vector=params, model=model, xp=jnp)
    n_clipped_lane_steps += int(
        np.count_nonzero(np.asarray(jnp.any(clipped_mask, axis=-1)))
    )
```

It is counted **per-lane, not per-coordinate** — a lane clipped in three
parameters at once is one clipped lane-step, deliberately matching how the NaN
and constrained counters are read. It is written into `search_internal`
(`search.py:919`) and restored on resume with `.get(..., 0)`
(`search.py:713`), so it survives a resumed run as a lifetime total.

So the counting is done and correct. **Keep this semantics** — do not silently
switch to a per-coordinate count while adding the reporting, or the number stops
being comparable with `n_value_nan_lane_steps` and friends.

## What is missing

**1. `search.summary` carries none of it.** `search.summary` is written by
`AbstractPaths.save_summary` (`autofit/non_linear/paths/abstract.py:583-588`) via
`text_util.search_summary_to_file` (`autofit/text/text_util.py:164-193`), whose
entire content is:

- `search_summary_from_samples(samples)`
- `Log Likelihood Function Evaluation Time (seconds)`
- `Expected Time To Run (seconds)`
- `Speed Up Factor (e.g. due to parallelization)`
- `Visualization Time (seconds)`

Every line is derived from `samples` or from timing. There is **no
search-specific channel at all** — `search_summary_to_file` never sees the
search, and `save_summary` never sees `search_internal`. This is the real work:
the counter is not hard to compute, it is hard to *route*. Adding a mechanism by
which a search contributes its own summary lines is the actual design decision,
and it is why this is `supervised` rather than `safe`.

Prefer a general channel over a one-off `n_clipped_lane_steps` parameter
threaded through two generic functions. The other multi-start counters
(`n_value_nan_lane_steps`, `n_grad_nan_lane_steps`, `n_constrained_lane_steps`,
`n_resurrections`, `stop_reason`) all have exactly the same problem and the same
readership — anyone reading `search.summary` to find out what the search did.
A single hook that lets a search emit key/value summary lines serves all of them
and is barely larger than the special case.

**2. The LBFGS path produces no count whatsoever.** This is the part most likely
to be missed. `AbstractBFGS` is *declarative* — it hands `optimize.Bounds` to
scipy and lets **scipy** enforce (`bfgs/search.py:103`, `_bounds_from`). Nothing
in PyAutoFit ever calls `project`, so there is no mask, and nothing to count.
"Number of Clipper uses" is therefore not a uniform quantity across searches:

- `MultiStartGradient` — clipped lane-steps, a real count.
- `LBFGS` — bounds were *supplied*; how often scipy pressed against them is
  scipy's business and is not reported back.

Decide and **state in the summary text** what is being reported, rather than
emitting a `0` for LBFGS that reads as "the clipper never fired" when it means
"this search cannot know". A `0` and a "not measured" are different findings —
the same distinction `clipper_validation_campaign.md` already insists on for
`0` versus `null`.

## Scope

1. A channel by which a search contributes lines to `search.summary`. Route all
   the multi-start counters through it, not just the clip count.
2. `MultiStartGradient` reports `n_clipped_lane_steps` (and, given the channel,
   its sibling counters and `stop_reason`).
3. `LBFGS` reports that bounds were supplied and that press-count is not
   observable — not a bare `0`.
4. Emit nothing about clipping when the clipper is `ClipperNone`. The default
   path must stay clean; a line saying "clipped: 0" on every existing run is
   noise on output that many downstream tools read.

## Traps

- **`search.summary` is a human-readable text file, not JSON.** It is
  `output_list_of_strings_to_file`, one `key = value` line per entry. Match the
  existing `Title Case = value` style; do not introduce a second format in the
  same file.
- **Resume must not double-count.** The counter is restored from
  `search_internal` as a lifetime total, so a summary written after a resumed run
  must report the lifetime figure and not the current-process delta. There is an
  existing comment at `search.py:705` making exactly this point about the sibling
  counters — the same reasoning applies.
- **`save_summary` is on `AbstractPaths`**, so `DatabasePaths` and `NullPaths`
  inherit whatever channel is added. `NullPaths` in particular must stay a no-op.
- **Do not confuse `search.summary` with `samples_summary`.** They are different
  artefacts: `search.summary` is the text file at `output_path`;
  `samples_summary` is the JSON `SamplesSummary` under `files/`. The request here
  is the text file.
- The float32 `save_json` bug (`draft/bug/autofit/save_json_numpy_scalar_typeerror.md`)
  is in this neighbourhood. `search.summary` is text so it is not directly
  exposed, but if any counter is routed through a JSON artefact on the way,
  a `np.int32` will hit that same bare `json.dump`. Cast to plain `int` at the
  boundary.

## Verify

- A `MultiStartGradient` run with `ClipperPriorBox` on a model with a tight
  `UniformPrior` writes a non-zero clip count into `search.summary`, and the
  value equals `search_internal["n_clipped_lane_steps"]`.
- The same run under the default `ClipperNone` writes **no** clipping line, and
  its `search.summary` is byte-identical to one produced before this change.
- A resumed run reports the lifetime total, not the post-resume delta.
- An `LBFGS` run with a real clipper says bounds were supplied without claiming a
  count of zero.
- The per-lane (not per-coordinate) semantics is asserted by a test: a lane
  clipped in several parameters on one step increments the counter by exactly 1.

<!-- Grounding: verified against PyAutoFit main at 1f4b66a93 (shallow clone,
     2026-08-16). Read multi_start_gradient/search.py:845-925 (the increment,
     the search_internal dict) and :705-745 (resume restore), bfgs/search.py:95-135
     (declarative bounds, no project call), paths/abstract.py:583-588
     (save_summary), text/text_util.py:164-193 (search_summary_to_file, the full
     current content of search.summary). -->
