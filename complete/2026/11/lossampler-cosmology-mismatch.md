`mass_function_ab_from(cosmology_astropy=...)` and `LOSSampler(cosmology=..., cosmology_astropy=...)` now raise a ValueError naming both cosmologies when the supplied astropy cosmology disagrees with the colossus cosmology name (H0 rtol 1e-3, Om0 rtol 1e-2, Ok0 atol 1e-3). Matching pairs and precomputed coefficients are unchanged. Decision (settled in the plan on the issue, so no `decision-taken` label): raise rather than map the astropy cosmology to a colossus one.

Witness: on main, WMAP9 + default planck15 silently returned the Planck15 fit (B = 8.116; true WMAP9 B = 8.108). Now it raises, with a hint to pass `cosmology_name='WMAP9'`. `pytest test_autolens/lens/test_los.py -k "mismatched or matching_cosmology or deprecated"` 4 passed; full `test_los.py` 12 passed. Targeted smoke: import check autolens_workspace guides/galaxies.py PASS. Independent Opus 5.5 review FINDINGS(2) (wrong argument name in the hint; flatness not compared), both fixed in ebe5a6223, then CLEAN. CI GREEN at /prm.

Not checked: colossus cosmologies other than planck15, planck18 and WMAP9 (the tolerances accept planck13 against Planck15).

Related: `draft/refactor/autogalaxy/one_cosmology_module_across_pyautogalaxy_and_pya.md` removes `cosmology_astropy` altogether, and this check with it.

Shipped in PyAutoLens#874 (https://github.com/PyAutoLabs/PyAutoLens/pull/874), merged 2026-11-20 by human /prm. Issue https://github.com/PyAutoLabs/PyAutoLens/issues/873. Done by shift worker 2026-11-19-pm2 (2040fb28).

## Original prompt

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
Verified: 2026-11-19 aa02375f (PyAutoLens)
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

Unblocked 2026-11-19: PyAutoLens#868 merged (20:50Z).

## Provenance

[from: independent adversary review, Fable 5.2, shift 2026-11-19-pm] advisory 2 on PyAutoLens#868;
record `batches/2026-11-19-pm.md`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cef12910-5f37-434a-b812-60fddb7f44b6/scratchpad/intake/lossampler_cosmology_astropy_silently_ignored.md -->
