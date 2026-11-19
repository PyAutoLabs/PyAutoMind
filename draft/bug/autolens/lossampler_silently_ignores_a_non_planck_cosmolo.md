# LOSSampler silently ignores a non-Planck cosmology_astropy

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: A test calls the LOSSampler mass-function fit with `cosmology_astropy=astropy.cosmology.WMAP9` and the default `cosmology_name_colossus="planck15"` and asserts it raises a ValueError naming both cosmologies (or uses a matching colossus cosmology, whichever the fix chooses), and a second test asserts `LOSSampler(cosmology=<non-Planck>)` with a mismatched colossus name does the same; passing a matching pair works unchanged.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

After PyAutoLens#868 (hmf → colossus), `@PyAutoLens/autolens/lens/los.py:179-186` and `648-655`
accept `cosmology_astropy` for backward compatibility but ignore it, raising only a
`DeprecationWarning`. Python hides DeprecationWarning from non-`__main__` callers, so a caller
passing e.g. WMAP9 with the default `cosmology_name_colossus="planck15"` silently gets the Planck15
mass function: intercept 8.116 vs 8.108, about 2% in halo counts (measured by the independent
adversary review, Fable 5.2, shift 2026-11-19-pm). `LOSSampler(cosmology=...)` is likewise never
checked against the colossus cosmology name (that was already true for the concentration relation).

## Ask

1. Either map the astropy cosmology to a colossus cosmology (`cosmology.fromAstropy` or the named
   equivalent) or raise a clear ValueError when they disagree; no silent mismatch.
2. Apply the same check between `LOSSampler(cosmology=...)` and the colossus name.
3. Add the witness tests (skip without colossus).

Blocked-by: PyAutoLens#868 merged.

## Provenance

[from: independent adversary review, Fable 5.2, shift 2026-11-19-pm] advisory 2 on PyAutoLens#868;
record `batches/2026-11-19-pm.md`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cef12910-5f37-434a-b812-60fddb7f44b6/scratchpad/intake/lossampler_cosmology_astropy_silently_ignored.md -->
