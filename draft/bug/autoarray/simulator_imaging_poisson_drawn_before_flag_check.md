# `SimulatorImaging` draws Poisson noise before checking `add_poisson_noise_to_data`

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- simulation
- robustness
Difficulty: low
Autonomy: safe
Priority: medium
Status: draft
Consequence: check
Witness: a simulator built with `add_poisson_noise_to_data=False` simulates an image carrying a
`-1e-19` pixel without raising, and the returned data is unchanged for a non-negative image
Review-minutes: 10
Filed: 2026-09-13

## Defect

`autoarray/dataset/imaging/simulator.py:246` (`SimulatorImaging.via_image_from`) calls

```python
image_with_poisson_noise = preprocess.data_eps_with_poisson_noise_added(
    data_eps=image, exposure_time_map=exposure_time_map, seed=self.noise_seed, xp=xp
)

if self.add_poisson_noise_to_data:
    image = image_with_poisson_noise
```

The draw is **unconditional**; the flag is only consulted afterwards. So a simulator
constructed with `add_poisson_noise_to_data=False` *and*
`include_poisson_noise_in_noise_map=False` — where the Poisson result is never used at all —
still runs `np.random.poisson` (`preprocess.py:529` → `poisson_noise_via_data_eps_from`,
`preprocess.py:492`).

When any pixel of the post-convolution image is negative, that raises:

```
ValueError: lam < 0 or lam contains NaNs
```

The negatives need not be physical. PSF-convolving a strictly non-negative model image returns
round-off pixels where the true value is zero. Measured on tile
`Tile102014322RA0376568496078DECNEG0561070209358` of the `dr1_sep1_sersics` sample: the input
image has minimum `+5.0e-22`, and its real-space convolution with the tile's real VIS PSF has
**89 negative pixels at up to `-3.8e-18` against a peak of `1.9e-01`** — about `2e-17` of the
peak, i.e. pure floating-point round-off. A caller who has switched Poisson noise off cannot
see this coming, and cannot clip the input to avoid it, because the negatives are produced
*inside* `via_image_from` by its own convolution step.

Observed 2026-09-13 while resimulating the 100 `euclid_sersics` tiles through
`euclid_strong_lens_modeling_pipeline/scripts/simulator.py`: **4 of 100 died**, indices 10, 62,
63 and 69 of the sorted sample; the other 95 went through. A 4% failure rate on round-off is
what makes it a trap rather than a visible break.

## Fix

Draw only when the result is wanted:

```python
if self.add_poisson_noise_to_data or self.include_poisson_noise_in_noise_map:
    image_with_poisson_noise = preprocess.data_eps_with_poisson_noise_added(...)
```

(or at minimum guard on `add_poisson_noise_to_data` and compute the noise-map branch from
whichever image it should use). That alone fixes every caller who turned Poisson noise off, and
it removes a wasted RNG draw and a wasted array allocation from every such simulation.

Independently, the draw itself should not be handed a negative lambda: `np.maximum(image, 0)`
(or an equivalent clip) inside `poisson_noise_via_data_eps_from` before the `np.random.poisson`
call, so a caller who *does* want Poisson noise on an image with convolution round-off gets
noise rather than an exception. Consider whether a genuinely negative image — one whose minimum
is a real fraction of its maximum rather than round-off — deserves a clear `exc` instead of a
silent clip; the pipeline-side guard chose to raise beyond `-1e-10 * maximum`.

Note the JAX path: the branch must stay traceable under `xp is not np`, so prefer a
construction-time (Python-level, on `self.*` flags) conditional over a value-level one.

## Workaround in place

`euclid_strong_lens_modeling_pipeline` carries a pipeline-side guard on `main`, merged
2026-09-17 as PR #87 (issue #77, merge `dc91d9a`): `simulated_image_from`
runs the convolution itself, clips the round-off, and passes the result back with
`image_is_convolved=True`. That workaround should be removed once this lands.

## Out of scope

The simulator's other noise components, the `use_real_space_convolution` choice, and anything
about how the round-off arises in the convolution (it is ordinary floating-point behaviour, not
a defect).
