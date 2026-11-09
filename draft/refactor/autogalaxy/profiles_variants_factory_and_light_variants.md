# Profiles variants factory and light variants

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace_test
Themes:
- hygiene
- mge
Difficulty: medium
Autonomy: safe
Priority: high
Memory: wiki/methods/concepts/aggregator-performance.md
Status: formalised
Filed: 2026-11-09
Epic: profiles-unified-api
Phase: 1
Consequence: glance
Witness: `test_autogalaxy/profiles/files/public_surface.json` is byte-identical before and after (no regeneration in this PR), `pytest test_autogalaxy` and `pytest test_autolens` green, the `docs` CI leg builds, `autolens_workspace_test/scripts/profiles_jit.py` passes, the committed `.pyi` stubs equal the generator's output, and `autogalaxy/profiles/light/` loses at least 1,500 lines
Review-minutes: 3
Unattended: ready
Lane: any

Phase 1 of the profiles-unified-api epic (`draft/refactor/autogalaxy/profiles_unified_api_epic.md`;
report `profiles_unified_api_report.md` §4 design, §7 phase 1). Depends on phase 0 (the golden
file) being merged. Behaviour-preserving by the epic's invariant: every public class keeps its
module path, qualname, constructor signature, defaults, MRO, prior yaml, JSON round trip and
numerics; only how the class object comes into existence changes.

## Change

1. New `@PyAutoGalaxy/autogalaxy/profiles/variants.py` with four factories and a numpydoc
   paragraph-dropper: `spherical(base, *, module)` (signature minus `ell_comps`, pinned
   `(0.0, 0.0)`, name `<Base>Sph`), `linear(base, *, module)` (minus `intensity`, pinned `1.0`,
   bases `(base, LightProfileLinear)` in that order, records `_standard_cls = base`),
   `snr(base, *, module)` (prepends `signal_to_noise_ratio: float = 10.0`, pins `intensity=0.0`,
   mixes `LightProfileSNR` and calls its `__init__` as today), `operated(base, *, module)` (mixes
   `LightProfileOperated`). The generated `__init__` is source-generated and `exec`'d (the
   `dataclasses` technique) with real parameter names, defaults and `__annotations__`, so
   `inspect.getfullargspec(cls)`, `typing.get_type_hints(cls.__init__)`, `help()`, Sphinx and
   `deflections_memo._init_argument_names_from` all see an ordinary function; `__module__`,
   `__qualname__`, `__name__`, `__doc__` and `__init__.__doc__` are set. Every generated class
   carries `_variant_of = base` and `_variant_kind`.
2. Rewrite as factory calls: `autogalaxy/profiles/light/linear/**` (19 classes incl. shapelets),
   `light/snr/**` (14), `light/operated/**` and `light/linear_operated/**` (7), and every thin
   `*Sph` class in `light/standard/**` including `shapelets/` (16). The module files stay where
   they are (prior yaml and `tracer.json` class paths key on them — report §1.3); each becomes a
   few lines, e.g. `Sersic = linear(lp.Sersic, module=__name__)`.
3. Ruling D4, same PR: `@PyAutoGalaxy/autogalaxy/profiles/geometry_profiles.py:421,442` and
   `profiles/light/linear/abstract.py:159` read `_variant_kind == "sph"` instead of
   `__class__.__name__.endswith("Sph")`; `standard_lp_parent` returns `_standard_cls` for
   generated classes and keeps today's `__bases__` walk as the fallback for hand-written ones (the
   lmp dictionary itself goes in phase 2).
4. Ruling D2: a stub generator (`python -m autogalaxy.profiles.variants --stubs`, or a module
   under `test_autogalaxy/profiles/` if the package must stay import-pure) that writes a `.pyi`
   beside every module containing factory calls, with explicit class signatures for IDE
   completion; a test asserts the committed stubs equal the generator's output. Add `*.pyi` to
   package data.
5. Dead code in the same files: `AbstractSersic.elliptical_effective_radius` and
   `AbstractSersic.image_2d_via_radii_from` (`light/standard/sersic.py:62-98`, reference an undefined
   `xp`, shadowed by `Sersic`); the redundant `LightProfile` base on `class Sersic(AbstractSersic,
   LightProfile)`; the `LightProfileSNR.image_2d_from` stub (`light/snr/abstract.py:31-49`).

## Out of scope

`light_and_mass_profiles.py` / `light_linear_and_mass_profiles.py` (phase 2); mass profiles
(phase 3); the parity tests (phase 4); any docstring the human has not asked to change beyond the
derived variant docstrings (wording is outside the invariant, report §3).

## Gotchas

MRO must match today's `class Sersic(lp.Sersic, LightProfileLinear)` and
`class GaussianMultipole(_LightProfileMultipoleMixin, Gaussian)`; `LightProfileLinear.__init__`
assigns `pytree_token` and must still run; classes must be bound at module scope under their own
name for pickling and `autonerves.dictable.get_class`; keep no JAX import at module level; the JAX
path is witnessed only by `profiles_jit.py`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/p1.md -->
