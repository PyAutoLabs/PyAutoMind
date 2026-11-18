# Model identifier raises "TypeError: iteration over a 0-d array" when a Galaxy…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: the identifier of a model holding an instance with a 0-d array attribute is computed without error and is identical across two runs
Review-minutes: 3
Unattended: ready
Verified: 2026-11-18 45e8cd3a (PyAutoFit)
Lane: any

Found 2026-11-14 in the science project ep_gnfw_slope and never reported. Fixing a lens to its truth by inserting the true `al.Galaxy` instance (stellar `Basis` of `lmp.Gaussian` + `gNFWSph`, from an `al.twins` truth tracer) into an `af.Collection` model made PyAutoFit's model identifier raise `TypeError: iteration over a 0-d array` at `autofit/mapper/identifier.py:185` when the search computed its unique tag. Worked around by fixing the parameters as floats with `model.replacing` (`/home/jammy/Science/Science/development/ep_gnfw_slope/scripts/common.py::reference_model_from`, note in `wiki/project/2026-11-14-single-lens-recovery.md`). Probable cause: an instance attribute that is a 0-d NumPy (or JAX) array is treated as an iterable by the identifier's hashing.
Fix: first write a minimal reproducer (a model containing an instance with a 0-d array attribute); make the identifier hash 0-d arrays as scalars; add a unit test.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/2_identifier_0d_array.md -->
