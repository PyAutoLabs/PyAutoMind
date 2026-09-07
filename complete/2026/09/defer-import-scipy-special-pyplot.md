# Two imports paid by every process and needed by almost none: scipy.special out of `import autofit`, pyplot out of `import autolens`

PyAutoFit#1566 → `088013c` and PyAutoLens#729 → `9468e3e`, closing PyAutoFit#1565, merged
2026-09-07. Census options O2 and O3 of the `ci-timing-fast-tests` epic. Fable-planned from a
web session (no task worktree); implemented by an Opus subagent under the delegation ladder.

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1565
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1566
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/729
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1566
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/729

## What shipped
- PyAutoFit: `TransformedMessage._support` is a `functools.cached_property` of the same name
  instead of an eager computation in `__init__`; the five module-level literals in
  `autofit/messages/normal.py` no longer evaluate `phi_transform`'s inverse (`scipy.special.ndtri`)
  at import. `-X importtime` scipy.special 177–180 ms → absent; `import autofit` 0.436 → 0.227 s;
  identifiers of `UniformPrior`, `LogUniformPrior`, `Model(Gaussian)` and a `Collection`
  byte-identical; pickles round-trip; 2454 passed; ten new tests.
- PyAutoLens: the matplotlib family imports in `potential_correction/visualize.py` are
  function-local (the pattern `mesh.py` and `iterative.py` already used). pyplot 325 ms → absent;
  `import autolens` 1.54 → 1.17 s alone, 1.09 s with the PyAutoFit change; 623 passed; three new
  tests, one of which fails if any matplotlib name is bound on the module again.

## Key traps / findings
- The import cost was not in the import statement but in a *module-level object construction*
  whose `__init__` did numerical work; `-X importtime` attributes it to the module that built the
  object, not to the transform module whose function-local import fired.
- `cached_property` caches under the same `__dict__` key the eager code wrote, so default pickling
  and old pickles are unchanged — the reason it beat a `None` sentinel + property pair.
- Still imported at top level of `import autolens`, deliberately left: `matplotlib` core via
  `autoarray.plot.*` (a real plotting layer) and `scipy.special` via
  `autogalaxy.profiles.mass.abstract.mge` (a real numerical dependency).

## Follow-ups
- Both libraries are `pending-release`; the `import_s` column of PyAutoHeart
  `timings/unit/{PyAutoFit,PyAutoLens}.jsonl` reads the change back after their next `main` run.
- Census O4 (`kaplinghat.py` quadrature, which also carries the third deferrable import,
  `scipy.integrate`) remains its own decision.

## Original prompt

# Defer two imports paid by every process and needed by almost none: scipy.special out of `import autofit`, matplotlib.pyplot out of `import autolens`

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `python -X importtime -c 'import autofit'` has no `scipy.special` node and `python -X importtime -c 'import autolens'` has no `matplotlib.pyplot` node, with both library suites green
Review-minutes: 3
Unattended: ready
Filed: 2026-09-06
Issued: 2026-09-06

Census options O2 and O3 of the ci-timing-fast-tests epic (PyAutoHeart
`timings/unit_import_census_2026-09.md` §4 and §6). Two library PRs, one per
repo, independent of each other — library-first, both `pending-release`.

**O2 — PyAutoFit.** `autofit/messages/normal.py:678` builds module-level
`TransformedMessage` literals (`UniformNormalMessage` and siblings) at import,
which evaluates a transform and pulls in `scipy.special`: **0.150 s per
`import autofit`, 0.235 s per `import autolens`** (census §4.2). Make the
literals lazy — a module `__getattr__` or a cached factory — so no transform is
evaluated at import. Public names in `autofit.messages.normal` and
`from autofit.messages.normal import UniformNormalMessage` must keep working;
pickling and identifier hashing of these objects must be checked (they feed the
search identifier). Risk medium: public namespace.

**O3 — PyAutoLens.** `autolens/potential_correction/visualize.py:19` imports
`matplotlib.pyplot` at module level, reached via `potential_correction/__init__.py:16`
from `import autolens`: **0.239 s per `import autolens`** (census §4.1). Move
the pyplot import inside the functions that draw (or make the sub-package
import lazy), matching what `autogalaxy.plot` already does. Risk low: one
module, pattern already in the stack.

**Why it is worth two PRs.** The multiplier (census §4 "The multiplier") is
494 script processes per board round plus every unit-test process and every
`should_simulate` subprocess: ~74 s local-equivalent (~133 s CI-scaled) per
round for O2 and ~55 s (~100 s CI) for O3, realised in every process that
never draws — which is almost all of them.

**Measure.** Before/after `python -X importtime -c "import autofit"` and
`"import autolens"` (report the cumulative for `scipy.special` and
`matplotlib.pyplot` going to zero), and the `import_s` column of
`timings/unit/<repo>.jsonl` once the daily run has ingested a post-merge CI
run — the census's numbers are the baseline, per repo, same runner class.

**Validation.** PyAutoFit suite (2446 tests) then the `autolens_workspace_test`
and `autogalaxy_workspace_test` smoke gates for the identifier/serialization
surface (O2); PyAutoLens suite plus `autolens_workspace` and HowToLens smoke
gates, which *do* draw and so prove the deferred import still lands (O3). No
behaviour change anywhere: same objects, same names, same figures.

**Guard.** Import deferral only — no likelihood, sampler or plotting logic
changes; nothing JAX-related. Do not fold in the third import the census names
(`scipy.integrate` via `kaplinghat.py:5`): it belongs with O4, which changes
numerics.
