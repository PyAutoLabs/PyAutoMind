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

> **IMPLEMENTED AND VERIFIED 2026-08-16, NOT YET PUSHED.** A cloud session wrote
> and tested this against `1f4b66a` but could not obtain push access to
> PyAutoFit, so it exists only as a patch: `tmp/clipper-search-summary.patch`
> (gitignored — take a copy before relying on it; the session container is
> ephemeral). 4 files, +243 lines, no deletions.
>
> Verified on Python 3.13: `test_autofit/non_linear` + `test_autofit/text` =
> **501 passed**, 3 skipped, 1 failed. The one failure
> (`test_nautilus.py::test__single_core_builds_no_pool`) is **pre-existing** —
> reproduced identically on a stashed clean tree — as is the `astropy` collection
> error in `paths/test_save_and_load.py`, both already recorded in
> `complete/2026/08/frozen-lane-counter.md`.
>
> Also verified end-to-end by running four real searches and reading the
> `search.summary` files they wrote: LBFGS default (no clipping lines), LBFGS
> clipped (`not measured`), MultiStart default (no clipping lines), MultiStart
> clipped (`Clipped Lane-Steps = 414`, rate `0.958`). Incidental finding worth
> keeping: on that toy 3-parameter Gaussian the unclipped arm showed
> `Value-NaN Lane-Steps = 378` (94.5%) and the clipped arm `0` — the #128
> mechanism reproducing on a model with nothing astrophysical in it.
>
> **Someone with push rights must apply, review and open the PR.** The scope
> below is what was built.

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

**1. `search.summary` does not report it.** *(Corrected 2026-08-16 — an earlier
revision of this prompt claimed there was no search-specific channel at all.
That was wrong, and it would have sent an implementer off to build a mechanism
that already exists. The channel is `samples_info`.)*

`search.summary` is written by `AbstractPaths.save_summary`
(`paths/abstract.py:583-588`) via `text_util.search_summary_to_file`
(`text/text_util.py:164-193`), which calls `search_summary_from_samples`
(`text/text_util.py:115-161`). That function **already** reads
`samples.samples_info` and already emits, guarded on the key so searches without
it are unaffected:

- `Resurrections`, `Value-NaN Lane-Steps`, `Gradient-NaN Lane-Steps`
- `Value-NaN Lane-Step Rate`, `Gradient-NaN Lane-Step Rate`, denominated by
  `n_starts * total_steps` and omitted when that is zero

So the routing is solved. What is missing is narrow and specific:

- `n_clipped_lane_steps` **never reaches `samples_info`** — it is written to
  `search_internal` (`multi_start_gradient/search.py:919`) but not copied into
  the `samples_info` dict at `search.py:1147`.
- `n_constrained_lane_steps` **does** reach `samples_info` but is **never
  emitted** by `search_summary_from_samples`. The trapped-lane counter from
  PyAutoFit#1475 has been invisible in the one artefact a user reads to find out
  what the search did, ever since it shipped.

Follow the existing key-guarded pattern rather than inventing a second one.

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

## Scope — as built in the patch

1. `multi_start_gradient/search.py` — publish `clipper` (the strategy's class
   name, not a bool, so a later strategy needs no schema change) and
   `n_clipped_lane_steps` into `samples_info`, cast to `int`, read from
   `search_internal` with a `.get(..., 0)` default so a legacy file does not
   `KeyError` and a resumed run reports the lifetime total.
2. `bfgs/search.py` — publish `clipper` **and deliberately no count**, with the
   reasoning in a comment at the site.
3. `text/text_util.py` — a `_clipper_summary_from(samples_info)` helper handling
   the three cases (no clipper → nothing; counted → `Clipper`, `Clipped
   Lane-Steps`, `Clipped Lane-Step Rate`; clipper but no count key →
   `Clipped Lane-Steps = not measured (bounds enforced by scipy)`), plus the
   one-line `Constrained Lane-Steps` emission the trapped-lane counter was
   owed.
4. `test_autofit/text/test_text_util.py` — 6 tests: `ClipperNone` emits nothing,
   counted reports count and rate, no-count says not-measured and never a bare
   `0`, absent key unaffected, constrained emitted, constrained absent when never
   written.

**One deliberate behaviour change to note in review:** multi-start summaries gain
a `Constrained Lane-Steps` line they did not have before. Everything else is
strictly additive and gated, so the `ClipperNone` path is otherwise unchanged. If
a reviewer wants byte-identity for existing multi-start runs too, drop that one
line — it is independent of the clip count.

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
