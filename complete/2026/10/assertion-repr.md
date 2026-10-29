# Safe assertion representations

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1716
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1720
- merge-commit: 46d50614dda7386ca9affbceb0cef91f6a77e1b2
- authorization: human /prm on 2026-10-25; merged unchanged at the checked head
- validation: every head workflow/job passed (Python 3.12, Python 3.13, no-JAX; applicable docs); combined serial suite 3913 passed, 1 skipped, 1 xfailed; four branches merge cleanly; model identifier parity passed
- limitation: downstream workspace smoke was not run; the gap was disclosed before the human merge command and remains recorded, not reported as a pass
- release: not performed; preserve pending-release until a published release is verified

## Outcome

Safe assertion representations. The implementation and regression tests are in the linked PR. Test-only #1723 was merged first to remove the known random start-point flake. Its three witness tests passed 200 repetitions each (600 passes). The source changes preserve representative output identifiers. Initial parallel unit failures reproduced the existing shared-output collision task; acceptance used serial combined validation and current-head GitHub CI.

## Close-out

All branch heads are ancestors of origin/main. No source changes were made during /prm. Issues closed as completed; prompts moved through lifecycle.py. The three declared glance tasks record stage-1 merged-unchanged shadow rows from the observed head equality; no independent-adversary evidence is claimed.

## Original prompt

# Assertion repr recurses forever

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: print(model.gathered_assertions()) on a model with one add_assertion prints a one-line description instead of raising RecursionError.
Review-minutes: 3
Unattended: ready

repr() or print() of any model assertion object raises RecursionError. autofit/mapper/prior/arithmetic/compound.py:87-88 defines __repr__ as return str(self), but no class in the MRO defines __str__, so str() falls back to __repr__ and recurses until the stack is exhausted. Add a __str__ (or a self-contained __repr__) on CompoundPrior / the assertion classes. Found on 2026-09-10 while writing a tutorial that wanted to print an assertion.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->

Issued: 2026-10-25
