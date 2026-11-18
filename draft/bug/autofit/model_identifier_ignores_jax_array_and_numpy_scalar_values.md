# Model identifier ignores the value of JAX arrays and some NumPy scalars

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge

Found 2026-11-18 by the shift worker for PyAutoFit#1784 (0-d NumPy array crash) and its review and adversary legs. `autofit/mapper/identifier.py` `Identifier._add_value_to_hash_list` hashes values that a model instance carries, and several of them hash without their value:

- A JAX array of any shape has a `__dict__`, so it takes the object branch. It hashes as `['ArrayImpl']`, so `jnp.array(0.5)`, `jnp.array(3.0)` and `jnp.array([1., 2.])` all give the same identifier.
- `np.float32`, `np.int64` and `np.bool_` scalars are neither float/int/bool nor Iterable, so they are left out of the hash.

Two models that differ only in such a value therefore share an output folder, and the second fit loads the first one's result. Fixing it changes the identifiers of existing models that hold these values, which moves their output folders and re-runs those fits. That is why it is a separate, `judge` task and was not part of #1784.

Fix: decide whether to accept the identifier change (and how to announce it), then hash JAX arrays and NumPy scalars by value (`np.asarray(value).tolist()` / `.item()`), with unit tests.
