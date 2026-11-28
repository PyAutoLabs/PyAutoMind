# Fixed-light harness: the "dense" S3 system builds a sparse numba inversion since lazy_sparse_operator defaults to auto

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: high
Filed: 2026-11-28
Status: formalised
Consequence: judge
Lane: local-dev

@autolens_profiling

## Finding

The autolens_profiling lint job fails one test on every PR:
`scripts/misc/likelihood_breakdown/test/test_fixed_light_numba.py::test_the_factory_dispatches_a_different_class_per_formalism`.
Line 185 expects `assert isinstance(dense.inversion, InversionImagingMapping)`, but `S3_dense` now holds an `InversionImagingSparseNumba`. Pytest reports 1 failed, 1922 passed.

- The failure appears in CI run 46136607434 on autolens_profiling PR #537 (head `d05e75de`, 2026-11-28).
- It reproduces locally on the earlier PR head `177c5d10`, whose lint passed on 2026-11-26. So no autolens_profiling change caused it; the change is in the libraries.
- The likely cause is PyAutoArray `aa2ce278`, "feat: lazy_sparse_operator defaults to auto (R6)" (2026-11-26, part of PyAutoGalaxy#759). `fixed_light_system_from(..., sparse_operator="drop")` builds a dataset with no operator. Under the new `auto` default, the library builds a sparse operator lazily anyway, so the factory dispatches to the sparse numba class. The "drop" mode in `scripts/misc/likelihood_breakdown/fixed_light_system.py` says it gives "no operator, a dense `InversionImagingMapping`", and that is no longer true.

## Why it matters

- **It blocks every autolens_profiling PR.** The lint job is red for any change, including autolens_profiling#537, which only adds results and docs.
- **Any "dense" fixed-light timing taken since R6 may have measured the sparse path.** That would make dense-versus-sparse comparisons in the fixed-light campaign wrong without any error.

## Scope

1. Confirm the cause by printing the inversion class with the R6 default and with the lazy sparse operator turned off.
2. Make `sparse_operator="drop"` really mean dense, by turning off the lazy sparse operator on that fit's settings. This is a harness fix. R6's `auto` default is intended and stays as it is in the library.
3. Check whether any fixed-light results recorded after 2026-11-26 used "drop", and say so in the PR.
4. Re-run `pytest scripts/misc/*/test`. The failing test must pass without being weakened.

## Rules

- Do not change the library default or weaken the test's assertions.
- Plan first; merge stays human.
