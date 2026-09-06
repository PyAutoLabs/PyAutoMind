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
