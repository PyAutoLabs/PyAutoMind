# Assertion repr recurses forever

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Witness: print(model.gathered_assertions()) on a model with one add_assertion prints a one-line description instead of raising RecursionError.
Review-minutes: 20
Unattended: ready

Assertion repr recurses forever
Type: bug
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Witness: print(model.gathered_assertions()) on a model with one add_assertion prints a one-line description instead of raising RecursionError.

repr() or print() of any model assertion object raises RecursionError. autofit/mapper/prior/arithmetic/compound.py:87-88 defines __repr__ as return str(self), but no class in the MRO defines __str__, so str() falls back to __repr__ and recurses until the stack is exhausted. Add a __str__ (or a self-contained __repr__) on CompoundPrior / the assertion classes. Found on 2026-09-10 while writing a tutorial that wanted to print an assertion.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
