- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/696
- pr: https://github.com/PyAutoLabs/PyAutoArray/pull/697 (merged 2026-11-17)
- user-facing: true — hub #45 (@GeorgeVassilakis, co-author); PR linked on the thread; post a release note there when it is on PyPI
- what shipped: `blurring_mask_2d_from` dilates with (ky,1) then (1,kx) instead of a dense (ky,kx) box (identical masks). Dense-reference test over (3,3), (5,3), (4,4), (6,2), (3,7), (8,5), (2,9). test_autoarray 2418 passed.
- numbers (laptop, after): HST 21² 3 ms (was 18 ms); JWST 37–51² 24–31 ms (was 0.2–0.4 s, +14–52 MiB); 101² 76 ms (was 3.2 s, +794 MiB); 499² on 1200² 5 s (George: was 401 s, 462 GiB).
- coordination: shared PyAutoArray with the stalled galaxy-duplicate-pytree-registration claim by human OK (no file overlap).

## Original prompt

# Speed up blurring_mask_2d_from for large PSF kernels (separable box dilation)

Type: perf
Target: autoarray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Community: https://github.com/PyAutoLabs/.github/discussions/45
Filed: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/696

Proposed by @GeorgeVassilakis on hub #45 (HWO-SLAPS, PSFs up to 999x999). The human chose in
the /community chat on 2026-11-17 to implement it ourselves rather than wait for his PR,
crediting him as co-author, and authorized working in PyAutoArray in parallel with the
stalled galaxy-duplicate-pytree-registration claim (no file overlap).

## What

`autoarray/mask/mask_2d_util.py` `blurring_mask_2d_from` dilates with a dense
`np.ones((ky, kx))` structure; scipy's offsets table grows as (ky*kx)^2. A box is separable:
dilate with (ky, 1) then (1, kx) for an identical mask.

Measured 2026-11-17 (byte-identical masks): HST 21x21 PSF 10-20 ms -> ~2 ms; JWST 37-51 px
0.2-0.4 s -> 11-14 ms; 101x101 3.2 s / ~0.8 GB -> 33 ms / ~0. George: 499x499 401 s / 462 GiB
-> 0.67 s / 8.7 MiB.

## Tests

Dense-reference comparison for odd, even and rectangular kernels: (3,3), (5,3), (4,4), (6,2),
(3,7), (8,5), (2,9).
