# reg_split_from (JAX) silently drops the self term when a split stencil is full

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- regularization
- jax
- correctness
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Review-minutes: 3
Witness: a split stencil table whose row is full and lacks its own pixel raises (or poisons with NaN under jit) on the JAX path exactly as reg_split_np_from raises InversionException; unit test covers both backends.
Filed: 2026-11-09

## Symptom

Found in the PyAutoArray#609 investigation (https://github.com/PyAutoLabs/PyAutoArray/issues/609#issuecomment-6726735167).
`regularization_util.reg_split_from` (JAX branch) inserts the -1 self entry at column `sizes[i]`; when a row is full
(KNN split tables are width k with every size k) and the row does not contain its own pixel, `insert_mask` is all
False and the self term is silently dropped. The row then sums to -1 instead of 0: a pull-to-zero penalty instead of
smoothing. The NumPy branch (`reg_split_np_from`) raises `exc.InversionException` in the same case. Under #609 this
hid the KNN bug as 279 corrupted rows on 72 pixels.

## Fix

Make the JAX branch fail loudly in the same case — under jit, poison the matrix with NaN (the existing
NaN-on-overflow convention of `pixel_splitted_regularization_matrix_from`) so the sample is resampled — and add a
both-backend unit test. Confirm no current mesh hits it after #609 (0 rows in the jax_grad/knn.py fixture).
