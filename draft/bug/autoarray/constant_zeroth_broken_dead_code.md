# ConstantZeroth regularization is broken twice over — dead code presenting as a feature

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft

Found during the reg-logdet investigation (autolens_workspace_developer#104
follow-up), and **independently confirmed by a second reviewer who actually ran
it**. `al.reg.ConstantZeroth` has never worked through its class API — it raises
before returning a matrix — yet it is a public, exported scheme
(`autoarray/inversion/regularization/__init__.py`).

Two distinct defects in `autoarray/inversion/regularization/constant_zeroth.py`:

1. **Shape bug.** `constant_zeroth_regularization_matrix_from` builds the
   neighbour term `const` as an `S x S` matrix (`S` = number of mesh pixels) but
   then builds the zeroth term as `xp.eye(P)` where `P = neighbors.shape[1]` is
   the **neighbour count** (e.g. 4), not `S`. `const + zeroth` therefore
   broadcasts `900x900 + 4x4` and raises. `constant_zeroth.py:68-72`:
   ```python
   reg_coeff = coefficient_zeroth**2.0
   zeroth = xp.eye(P) * reg_coeff        # P is the neighbour count, should be S
   return const + zeroth
   ```
   The zeroth-order term is meant to be a full `S x S` scaled identity
   (`+lam_z^2` on every pixel's diagonal), which is precisely the term that would
   lift the graph-Laplacian null mode and make this scheme well-conditioned.

2. **Missing-argument bug.** `ConstantZeroth.regularization_matrix_from` (the
   class API path) does not pass `neighbors_sizes` to
   `constant_zeroth_regularization_matrix_from`, so a correctly-shaped call raises
   `TypeError` before reaching the shape bug. Verify the exact call site and
   signature.

**Why this matters beyond "a broken scheme":** in the reg-logdet investigation,
`ConstantZeroth` was hypothesised to be the *already-correct* answer — a scheme
that adds a genuine model-scaled zeroth-order term (`+lam_z^2 * I`) lifting the
null mode, immune to the `1e-8`-below-the-noise-floor conditioning collapse that
afflicts `Constant`/`Adapt`. That hypothesis is **dead on arrival** because the
scheme itself is dead. Fixing it would resurrect a genuinely useful,
well-conditioned regularization option — and is a prerequisite for "just point
users at the zeroth-order variant" ever being a real answer.

Task: reproduce both failures on clean main FIRST (a two-line call through the
class API, then through the function with correct args). Then fix the `eye(P)` →
`eye(S)`/`S x S` shape and thread `neighbors_sizes`. Check the sibling
`adapt_split_zeroth.py` and `brightness_zeroth.py` for the same `eye(P)` / missing
-arg pattern — they may share the copy-paste. Add a unit test that builds the
matrix and asserts shape `(S, S)` and positive-definiteness (the whole point of a
zeroth-order term is that the result has NO null mode). Numpy-only test per repo
policy.

Do NOT bundle this with the reg-logdet log-det change or the Adapt double-square
probe — it is an independent, self-contained defect.
