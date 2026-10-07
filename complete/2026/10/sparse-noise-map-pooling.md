# Sparse interferometer path: opt-in quadrature pooling of unequal real/imag noise sigma

Completed 2026-10-07 under human `/prm` (merged by the human 2026-10-07T10:07:50Z).

Merged PyAutoArray#619 (https://github.com/PyAutoLabs/PyAutoArray/pull/619,
merge commit 2c5cb697); feature head be725f88 verified an ancestor of
origin/main; all three CI legs green. Issue
https://github.com/PyAutoLabs/PyAutoArray/issues/617 closed.

`sparse_terms_from_chunks(..., pool_noise_map=True)` now pools unequal
real/imaginary noise sigma in quadrature, sigma^2 = (sigma_re^2 + sigma_im^2)/2,
before building the sparse terms (bit-identical to pre-pooling the chunks with
`noise_map_pooled_from`). The default call still raises on unequal sigma, so
existing behaviour is unchanged unless the user opts in.

Measured documentation pin: a 2 % real/imag asymmetry shifts the log
likelihood by 9.9e-3 nats (7.7e-5 relative) in-pytest, and by 0.01-0.096 nats
across seeds.

Source: community GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13
(external contributor @HRSAstro, pyuvimage), comment
https://github.com/PyAutoLabs/.github/discussions/13#discussioncomment-18741903 item 2.

Not released: the option reaches users with the next PyAutoArray release.
Follow-on: `sparse_terms_oversampled_fine_grids` (next task) was gated on this merge.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/619

## Original prompt

# Sparse interferometer path: opt-in quadrature pooling of unequal real/imag noise sigma

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- interferometer
- sparse-operator
- community
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-10-07
Issued: 2026-10-07
Difficulty: small
Consequence: judge
Witness: `sparse_terms_from_chunks(chunks, pool_noise_map=True)` on chunks with a 2 % real/imag sigma asymmetry returns, field by field and bit-identically, the same `SparseTerms` as the default call on the same chunks pre-pooled with `noise_map_pooled_from` (today the unequal chunks raise in `check_noise_map_real_imag_equal`); the default call still raises (existing tests `test_dataset.py:229`, `:654`, util `:1255`, `:1265` unchanged).
Review-minutes: 8
Unattended: ready
Source: GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13 (external contributor @HRSAstro, pyuvimage), comment https://github.com/PyAutoLabs/.github/discussions/13#discussioncomment-18741903 item 2; technical review 2026-10-07 (Item A, accept opt-in).

## Request (verbatim)

> **2. Unequal real and imaginary sigma**
>
> At the moment, `sparse_terms_from_chunks` raises an error when σ_re ≠ σ_im. For thermal noise, the real and imaginary parts of one integration should have the same variance, so in practice a difference usually comes from the noise estimator. With noise estimated by differencing adjacent visibilities we typically see a 1–2% difference. Pooling in quadrature, σ² = (σ_re² + σ_im²)/2, preserves the total variance and is the better estimate of both.
>
> It might be friendlier to offer pooling as an option, with a warning that reports the size of the difference (and a stronger one when it is large, e.g. above ~25%, where it may be real), rather than refusing the chunk. At minimum, the docstrings of `from_stream` and `apply_sparse_operator` could say that the sparse path assumes equal sigmas and suggest pooling before passing the data in. This is what pyuvimage does now before handing chunks over.

## What

`iiu` = `autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`, `ds` = `autoarray/dataset/interferometer/dataset.py` (origin/main lines).
- `iiu:32 check_noise_map_real_imag_equal` uses `np.allclose(re, im, atol=0.0)` (rtol 1e-5): 1-2 % estimator scatter always raises. Called at `ds:530` (`apply_sparse_operator`) and `iiu:2207` (`sparse_terms_from_chunks`, per chunk; `from_stream` `ds:379` and `apply_sparse_operator_from_chunks` `ds:738` inherit it).
- Only W~ (`iiu:2219`, builder `iiu:584` `w = 1/sigma^2`) and dirty beam / `sum_weights` (`iiu:2244`) use sigma_re alone; dirty image, `data_term`, `noise_normalization` already use both. The dense mapping path is exact for unequal sigmas (`iiu:89-124`, `inversion/interferometer/mapping.py:90-104`).
- Why sparse cannot be exact: curvature = `sum wbar cos(a-b) + dw cos(a+b)`; W~ only represents the Toeplitz `cos(a-b)` part. Quadrature pooling `w = 2/(s_r^2+s_i^2)` differs from `wbar` at O(eps^2) (4e-4 at 2 %) and preserves total variance, so it is the right substitute.

## Plan

1. Helpers in `iiu` beside the check: `noise_map_pooled_from(noise_map)` → complex `s + 1j*s`, `s = sqrt((re^2+im^2)/2)` (accept the forms `_complex_visibilities_from`, `iiu:2051`, accepts); `noise_map_real_imag_asymmetry_from(noise_map)` → (median, max) of `|re-im|/max(re,im)`.
2. `pool_noise_map: bool = False` (default keeps raising — no silent behaviour change):
   - `sparse_terms_from_chunks` (`iiu:2066`): after `_complex_visibilities_from` (`iiu:2196`) record chunk asymmetry and replace the noise map **before every term** (W~, dirty image, beam, data_term, noise_normalization). Accumulate stats across the generator; log once at the end.
   - `from_stream` (`ds:328`): pass through.
   - `apply_sparse_operator` (`ds:419`): pool `self.noise_map`, build from it, and **return the dataset with the pooled noise_map** (`ds:604-611` returns `self.noise_map` today) so dense residual/chi^2/noise_normalization agree with the cached sparse terms.
   - `apply_sparse_operator_from_chunks` (`ds:613`): **refuse** `pool_noise_map=True` with `DatasetException`, mirroring the phase_centre refusal `ds:701-709`; message: pool first (`Interferometer(..., noise_map=noise_map_pooled_from(nm))`) or use `from_stream(..., pool_noise_map=True)`.
3. Messages via module `logger`: none at exact equality (rtol 1e-5); INFO "pooled sigma_re/sigma_im in quadrature: median difference X %, max Y % (consistent with noise-estimator scatter)" for median <= 25 %; WARNING above 25 % (contributor's `REIM_ASYMMETRY_WARN`): "difference may be real; pooling weights real and imaginary parts equally, which the noise map does not; the dense InversionInterferometerMapping path (no apply_sparse_operator) is exact".
4. Docstrings (ship even if the option slips): `from_stream` (`ds:342-378`), `apply_sparse_operator` Precondition (`ds:516-526`), `apply_sparse_operator_from_chunks`, chunk contract (`iiu:2104`), error text (`iiu:69-86`): equal-sigma assumption, `pool_noise_map=True` / `noise_map_pooled_from`, cos(a+b) caveat; phase-centre paragraph (`iiu:2120-2131`): with pooling `data_term` is exactly phase-invariant. Evidence caveat: do not compare log-evidences of pooled vs unpooled fits (noise_normalization differs O(eps^2) per visibility).
5. No `SparseTerms.noise_pooled` provenance field (pooled + exactly-equal chunks sum correctly).

Tests (`test_inversion_interferometer_util.py`, `test_autoarray/dataset/interferometer/test_dataset.py`): pooled helper preserves `re^2+im^2` with equal parts; asymmetry helper on a known 2 % map; the witness; `apply_sparse_operator(pool_noise_map=True)` returns pooled noise_map and sparse log_evidence == mapping-path log_evidence on the pooled dataset (existing tolerance); caplog INFO at 2 %, WARNING with percentage at 30 %, nothing at equality; `apply_sparse_operator_from_chunks(pool_noise_map=True)` raises; one documentation pin of pooled-sparse vs unpooled-mapping log_evidence at 2 % (record the number, assert an order-of-magnitude bound).

Risks: pooling is approximate when sigmas truly differ (drops cos(a+b)); returned noise_map differs from input under the opt-in only. Must merge before `sparse_terms_oversampled_fine_grids` (same repo claim; fine grids inherit the equal-sigma K).
