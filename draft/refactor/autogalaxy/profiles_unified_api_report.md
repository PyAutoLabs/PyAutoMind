# Profiles module — survey, unified-API design and detailed phase bodies

Type: refactor
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace_test
Themes:
- hygiene
- mge
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: evidence record for the profiles-unified-api epic — never issued; read it from the epic ledger
Consequence: glance
Lane: any
Review-minutes: 0
Unattended: never
Epic: profiles-unified-api
Filed: 2026-11-09

Written 2026-11-09 by the Refactor Agent session (`/refactor`) from read-only shallow clones of
PyAutoGalaxy `bc3918a`, PyAutoLens `bb87dad`, PyAutoArray `1482dd9`, PyAutoFit and PyAutoNerves at
`main`. No code was edited and no test suite was run; every number below comes from `ast` walks of
the clones (scripts in the session scratchpad, reproducible from the file:line references). The
ledger (phase cards, rulings, status) is `profiles_unified_api_epic.md` beside this file. The
cross-library survey that produced this epic is `draft/refactor/libraries/line_count_reduction_survey.md`.

**What was not found.** The human's own notes on a "clear unified API" for profiles were searched
for in PyAutoMind (`draft/`, `complete/`, `ideas.md`, `epics.md`, `parked.md`, `planned.md`),
PyAutoMemory (`wiki/`), PyAutoBrain and the three library repos (`*.md`, `*.rst`, `TODO`/`unified`
greps). Nothing written exists. §4 therefore proposes a design from the code's own constraints and
§6 lists the rulings the design needs; the human's notes should be pasted into the ledger's
"Human design notes" section before phase 1 is issued, and §4 reconciled against them.

## 0. Summary

`autogalaxy/profiles/` is half of PyAutoGalaxy by every measure and the single largest
behaviour-preserving lever in the three libraries:

| Measure | profiles/ | all of autogalaxy/ | share |
|---|---:|---:|---:|
| source files | 132 | 241 | 55 % |
| source lines | 20,842 | 42,921 | 49 % |
| of which docstring lines | 7,252 | 15,891 | 46 % |
| classes | 198 | 276 | 72 % |
| test files | 89 | 168 | 53 % |
| test lines | 13,468 | 29,019 | 46 % |
| test functions | 735 | 1,349 | 54 % |

The size is not physics. It is **variant boilerplate**: the same radial function appears as a
standard, a linear, an SNR, an operated, a linear-operated, a light-and-mass and a linear
light-and-mass class, each with a spherical twin, and every one of those is a hand-written
`__init__` that re-states the parent's docstring and forwards to it with one argument pinned.

- **131 of the 198 classes have no method but `__init__`** (or no body at all): 4,616 lines, of
  which 1,980 are copied docstrings (`thin_classes.py` walk, §2.1).
- **74 classes are `*Sph` twins**: 4,322 lines. Only 11 carry their own numerics (a spherical
  closed form for deflections or potential); the other 63 pin `ell_comps=(0.0, 0.0)` and nothing else.
- **18 classes are mass–concentration / virial-mass reparameterisations** of NFW-family profiles:
  734 lines, all thin, every one a constructor that calls a `mcr_util` converter and forwards.
- **66 test functions assert that one variant equals another** (27 "lmp matches lp/mp", 39
  "elliptical with zero ellipticity matches spherical"): the same contract, hand-copied per class.

The boilerplate exists for a real reason — PyAutoFit reads a class's **constructor signature** as
its parameter space (`autofit/mapper/prior_model/prior_model.py:153`, `:365`), prior defaults are
keyed by **module path + class name** (`prior_model.py:417`; `config/priors/light/linear/sersic.yaml`
holds `Sersic:`), and `autonerves.dictable` serialises instances by `module.qualname`
(`autonerves/class_path.py:8-13`). A variant *must* be a distinct class with a distinct signature at
a stable import path. What does not follow is that each one must be written by hand.

The design (§4) keeps every public name, module path, constructor signature, prior file, JSON
round-trip and numerical result unchanged, and generates the variants from six factory functions
in one new module. Expected effect on `profiles/` alone: roughly **−4,000 source lines (−20 %)**
and **−1,000 test lines with 66 test functions collapsing to 3**, with the physics code untouched
and a byte-identical public-surface witness recorded before the first edit. A deeper unification
that retires the `lp_linear` / `lp_snr` / `lmp_linear` namespaces in favour of composition-time
variants is possible and sketched in §5, but it is a public-API change spanning PyAutoFit and every
workspace — a feature epic for the human to rule on, not a refactor, and it is *easier* after this
one because the variants will already be data.

## 1. The module as it is

### 1.1 Layout and families

| Family (directory / module) | classes | lines | thin classes | thin lines |
|---|---:|---:|---:|---:|
| `mass/dark` | 29 | 2,970 | 20 | 783 |
| `mass/total` | 19 | 2,929 | 3 | 177 |
| `mass/stellar` | 16 | 1,501 | 11 | 461 |
| `light/standard` | 23 | 1,432 | 12 | 407 |
| `mass/abstract` (`abstract.py`, `mge.py` 801, `deflections_memo.py` 733, `cse.py`) | 4 | 1,158 | 1 | 17 |
| `light/linear` | 19 | 1,047 | 17 | 491 |
| `light_and_mass_profiles.py` (`lmp`) | 17 | 720 | 17 | 720 |
| `light_linear_and_mass_profiles.py` (`lmp_linear`) | 14 | 601 | 14 | 601 |
| `light/snr` | 14 | 518 | 13 | 419 |
| `light/standard/shapelets` | 7 | 501 | 4 | 165 |
| `mass/sheets` | 3 | 459 | 0 | 0 |
| `geometry_profiles.py` | 3 | 435 | 0 | 0 |
| `mass/input` | 4 | 362 | 0 | 0 |
| `basis.py` | 1 | 320 | 0 | 0 |
| `mass/point` | 3 | 277 | 1 | 62 |
| `light/linear/shapelets` | 6 | 218 | 6 | 218 |
| `light/operated` + `light/linear_operated` | 7 | 32 | 7 | 32 |
| other (`validate.py`, `scaling_relations.py`, `point_sources.py`, mocks, `plot/`) | — | ~430 | 5 | 63 |

"Thin" = the class body is empty or holds only `__init__`. The physics lives in the ~65 non-thin
classes and the module-level helpers (`psi_from`, the Tessore–Metcalf omega series, the CSE/MGE
decomposers, `mcr_util`, `nfw_hk24_util`, `ludlow16`).

### 1.2 What one profile costs today

`Sersic` is defined once (`light/standard/sersic.py:106-243`) and then re-declared eleven times with
no new physics:

| Public name | File | Lines | Body |
|---|---|---:|---|
| `lp.SersicSph` | `light/standard/sersic.py:246-275` | 30 | `__init__` pinning `ell_comps=(0,0)` |
| `lp_linear.Sersic` | `light/linear/sersic.py:9-38` | 30 | `__init__` pinning `intensity=1.0`, mixes `LightProfileLinear` |
| `lp_linear.SersicSph` | `light/linear/sersic.py:41-65` | 26 | pins `ell_comps` |
| `lp_snr.Sersic` | `light/snr/sersic.py:7-43` | 37 | prepends `signal_to_noise_ratio`, pins `intensity=0.0` |
| `lp_snr.SersicSph` | `light/snr/sersic.py:46-75` | 30 | both (and its docstring still documents `intensity`) |
| `lp_operated.Sersic` | `light/operated/sersic.py` | 2 | `class Sersic(lp.Sersic, LightProfileOperated): pass` |
| `lp_linear_operated.Sersic` | `light/linear_operated/sersic.py` | 2 | same, on the linear |
| `lmp.Sersic` | `light_and_mass_profiles.py:116-160` | 45 | `__init__` calling `lp.Sersic.__init__` then `mp.Sersic.__init__` |
| `lmp.SersicSph` | `light_and_mass_profiles.py:163-196` | 34 | pins `ell_comps` |
| `lmp_linear.Sersic` | `light_linear_and_mass_profiles.py:106-149` | 44 | same on `lp_linear.Sersic` |
| `lmp_linear.SersicSph` | `light_linear_and_mass_profiles.py:152-185` | 34 | pins `ell_comps` |

314 lines, of which ~190 are the same `Parameters` docstring block repeated. `Exponential` and
`DevVaucouleurs` repeat the whole pattern on top of `Sersic` (they pin `sersic_index`), `SersicCore`,
`Gaussian`, `Chameleon`, `ElsonFreeFall`, `Moffat`, the three shapelet families and the
`*Gradient` stellar-mass profiles do the same.

### 1.3 Why the variants are classes — the framework contract

Every behaviour-preserving design has to satisfy five readers of a profile class, all verified in
the clones:

1. **Parameter space = constructor signature.** `PriorModel.__init__` calls
   `inspect.getfullargspec(cls)` for defaults (`prior_model.py:153`) and
   `constructor_argument_names` does it again for the argument list (`:365`), dropping `self`/`cls`;
   `typing.get_type_hints(cls.__init__, …)` (`:146`) reads annotations. The model identifier hashes
   the same spec (`autofit/mapper/identifier.py:161`). So `lp_linear.Sersic` *is* "a `Sersic` whose
   signature has no `intensity`", and `SersicSph` *is* "one whose signature has no `ell_comps`".
2. **Prior defaults by import path.** `Prior.for_class_and_attribute_name` resolves
   `f"{cls.__module__}.{cls.__name__}"` against `config/priors/**` (`prior_model.py:417`,
   `autofit/mapper/prior/abstract.py:140-158`): `autogalaxy.profiles.light.linear.sersic.Sersic`
   → `priors/light/linear/sersic.yaml` → key `Sersic`. 93 yaml files depend on module path and class
   name being exactly what they are.
3. **JSON round trip by `module.qualname`.** `to_dict` writes `class_path`
   (`autonerves/dictable.py:222`, `class_path.py:8-13`); `from_dict` imports the module and calls
   `cls(**arguments)` (`dictable.py:333-345`). `files/tracer.json` of every fit on disk names these
   paths.
4. **`isinstance` roles.** Downstream code filters by marker class, never by name:
   `LightProfileLinear` (galaxy.py:191, 204, 248, 341; galaxies.py:399-405; to_inversion.py:322-333;
   fit_imaging.py:31; autolens `lens/to_inversion.py`), `LightProfileSNR` (galaxy.py:408),
   `LightProfileOperated` (operate/image.py:247, 351; fit_imaging.py:113; `check_operated_only`),
   `LightMassProfile` (linear/abstract.py:131; `Galaxy` classifies an `lmp` as both light and mass
   because it inherits both bases). MRO order matters: `class Sersic(lp.Sersic, LightProfileLinear)`.
5. **JAX pytree registration walks `type(obj)`** (`autogalaxy/jax/registration.py:72-80`) and
   flattens `__dict__`; any class with ordinary instance attributes works.

Two places sniff the **class name** instead: `geometry_profiles.py:421` and `:442`
(`self.__class__.__name__.endswith("Sph")`) and `light/linear/abstract.py:159` (the same, to find
the standard parent). The linear base also carries a hand-maintained 14-entry dictionary mapping
`lmp_linear.*` → `lmp.*` whose own docstring says "the ugly dictionary used to do this mapping
should be removed for better code" (`abstract.py:118-152`).

### 1.4 Dead and duplicated code found on the way

Not the point of the epic, but free once the files are rewritten:

- `AbstractSersic.elliptical_effective_radius` and `AbstractSersic.image_2d_via_radii_from`
  (`light/standard/sersic.py:62-98`) reference an undefined `xp`; both are shadowed by `Sersic` and
  can never run. `class Sersic(AbstractSersic, LightProfile)` re-lists a base it already has.
- `LightProfileSNR.image_2d_from` (`light/snr/abstract.py:31-49`) is a `NotImplementedError` stub
  under a concrete method of every host class.
- `dPIEMassB0.potential_2d_from` stacks `@to_array @transform @to_array @transform`
  (`mass/total/dual_pseudo_isothermal_mass.py:791-796`). Harmless — `transform` is idempotent via
  the `is_transformed` flag (`autoarray/structures/decorators/transform.py:71`) — but a doubled
  wrap, and the 1,359-line module is five classes that each re-declare deflections, convergence
  and Hessian around the same four `_ci05`/`_pi05` helpers.
- `lp_snr.SersicSph`'s docstring documents an `intensity` argument the class does not take
  (`light/snr/sersic.py:55-66`).

### 1.5 The tests

735 test functions in 89 files. Three shapes dominate:

| Shape | Count | Example |
|---|---:|---|
| pinned numeric value for one profile at one point | ~430 | `test__deflections_yx_2d_from__isothermal_sph_config_1` (`mass/total/test_isothermal.py:13`) |
| cross-variant parity (Ell vs Sph; lmp vs lp/mp) | 66 | `test__gaussian__convergence_2d_from__matches_lmp` (`test_light_and_mass_profiles.py:22`) |
| framework / plumbing (xp forwarding, pytree token, pickling, `lp_instance_from`, model constraints, validation) | ~120 | `light/linear/test_abstract.py`, `test_model_constraint.py`, `test_validate.py` |

The pinned-value tests are the physics witness and stay (as rows of a table rather than functions,
§3 phase 4). The 66 parity tests are one contract written 66 times. Nothing anywhere pins the
*public surface* — argument names, defaults, prior resolution, identifiers, class paths — which is
exactly what a variant refactor could silently change, so the epic's first phase adds that witness
before any file is touched.

## 2. Measurements

### 2.1 Thin classes by area

| Area | thin classes | lines | docstring lines |
|---|---:|---:|---:|
| `light/**` | 59 | 1,732 | 843 |
| `mass/**` | 36 | 1,500 | 546 |
| `lmp` + `lmp_linear` (root) | 36 | 1,384 | 591 |
| **total** | **131** | **4,616** | **1,980** |

### 2.2 Spherical twins

74 `*Sph` classes, 4,322 lines. The 11 with their own methods (kept as hand-written classes; they
are physics, not boilerplate): `IsothermalSph`, `PowerLawSph`, `PowerLawCoreSph`, `NFWSph`,
`NFWTruncatedSph`, `cNFWSph`, `KaplinghatCoredNFWSph`, `YangSIDMSph`, `dPIEMassB0Sph`,
`dPIEMassSph` (a `from_b0` classmethod only), `dPIEPotentialSph`. The remaining 63 are
`ell_comps=(0.0, 0.0)` pins.

### 2.3 Reparameterised dark profiles

18 classes, 734 lines, all thin: `NFWMCRDuffySph`, `NFWMCRLudlow(Sph)`, `NFWMCRScatterLudlow(Sph)`,
`cNFWMCRLudlow(Sph)`, `cNFWMCRScatterLudlow(Sph)`, `gNFWMCRLudlow`, `gNFWVirialMassConcSph`,
`gNFWVirialMassgNFWConcSph`, `NFWVirialMassConcSph`, `NFWTruncatedMCR{Duffy,Ludlow,ScatterLudlow}Sph`,
`KaplinghatCoredNFWMCRLudlowSph`, `YangSIDMMCRLudlowSph` (124 lines). Each is "take
`(mass_at_200, redshift_object, redshift_source[, scatter_sigma|f_c|…])`, call one `mcr_util`
converter, store the inputs, forward `(kappa_s, scale_radius[, core_radius])` to the base".

### 2.4 Consumers that the public surface must keep serving

`test_autolens/` references the namespaces in 78 files (`al.mp.IsothermalSph` 205 times,
`al.lp.Sersic` 193, `al.mp.Isothermal` 104, `al.lp_linear.Sersic` 50, `al.lp.SersicSph` 45, …);
`autogalaxy/fixtures.py` builds `lp.SersicSph`, `lp_linear.Gaussian`, `lp_operated.Gaussian`,
`mp.IsothermalSph`, `lmp.SersicGradient`, `mp.NFWSph`; `analysis/chaining_util.py:430-446`
and `model_util.py:177-210` map between `lp`, `lp_linear`, `lmp`, `lmp_linear` classes by identity;
`galaxy_model_csv.py` resolves profile classes by `getattr(module, name)`; `interop/coolest`
dispatches on `type(profile).__name__`. All of these are preserved by keeping names, modules and
MROs — none by keeping hand-written bodies.

## 3. What a behaviour-preserving refactor may and may not change

**Invariant (the epic's one sentence).** For every public class in `ag.lp`, `ag.lp_linear`,
`ag.lp_snr`, `ag.lp_operated`, `ag.lp_linear_operated`, `ag.lmp`, `ag.lmp_linear` and `ag.mp`:
`f"{cls.__module__}.{cls.__qualname__}"`, `inspect.getfullargspec(cls)` (args, defaults,
annotations), the class MRO restricted to public marker bases, `af.Model(cls).identifier` and
`prior_count`, `to_dict(cls())`, pickling, and the arrays returned by `image_2d_from` /
`convergence_2d_from` / `deflections_yx_2d_from` / `potential_2d_from` on a fixed grid are unchanged.

**May change:** how the class object comes into existence; private helper names; docstring wording
(today's variant docstrings are inconsistent copies, §1.4); which file a *private* helper lives in;
test organisation.

**Must not change (route to `feature/` instead):** any public name or namespace; any constructor
parameter name, order or default; any prior yaml; any numerical result; the `__solved_parameters__`
protocol; the `endswith("Sph")` *behaviour* until its callers are switched to the new attribute in
the same PR.

## 4. Design — variants as data, one module of factories (the refactor track)

### 4.1 Shape

One new private module, `autogalaxy/profiles/variants.py` (~250 lines including a numpydoc
paragraph-dropper), exporting six factories. Each returns a real class object that satisfies the
five readers in §1.3:

```python
# autogalaxy/profiles/light/linear/sersic.py — the whole file after phase 1
from autogalaxy.profiles.light import standard as lp
from autogalaxy.profiles.variants import linear, spherical

Sersic = linear(lp.Sersic, module=__name__)
SersicSph = spherical(Sersic, module=__name__)
```

| Factory | Produces | Today's hand-written equivalent |
|---|---|---|
| `spherical(base, *, module)` | `<Base>Sph`: signature minus `ell_comps`, pinned `(0.0, 0.0)` | 63 classes |
| `linear(base, *, module)` | `Base` with `LightProfileLinear` mixed in after it, signature minus `intensity`, pinned `1.0`; records `_standard_cls = base` | 29 classes + the `standard_lp_parent` dictionary |
| `snr(base, *, module)` | prepends `signal_to_noise_ratio: float = 10.0`, pins `intensity=0.0`, mixes `LightProfileSNR` | 15 classes |
| `operated(base, *, module)` | mixes `LightProfileOperated`, signature unchanged | 6 classes |
| `light_mass(light_cls, mass_cls, *, module)` | `__init__` that calls both parents as today; mixes `LightMassProfile`; records `_standard_cls` for the linear case | 31 classes + the dictionary |
| `reparameterised(base, *, name, module, parameters, converter)` | prepends the physical parameters, stores them, calls `converter(**physical)` and forwards the base parameters | 18 classes |

The generated `__init__` is **source-generated and `exec`'d** (the `dataclasses` technique), not a
`*args, **kwargs` shim, so `inspect.getfullargspec`, `typing.get_type_hints`, `help()`, Sphinx
and the `deflections_memo` introspection (`deflections_memo.py:298`) all see an ordinary function
with real parameter names, defaults and annotations. `__module__`, `__qualname__`, `__name__` and
`__doc__` are set so that import path, prior resolution, pickling and autosummary are unchanged.
This was probed stand-alone in the session (`scratchpad/factory_probe/`): `getfullargspec`,
`get_type_hints`, `pickle` round trip, MRO and `__doc__` all match the hand-written form on
Python 3.12.

Each generated class also carries `_variant_of = base` and `_variant_kind in {"sph", "linear",
"snr", "operated", "light_mass", "reparameterised"}`, which lets the two `endswith("Sph")` checks
and the linear base's parent lookup become attribute reads in the same PR (behaviour identical:
every generated spherical class still ends in `Sph`, and the attribute is only consulted where the
name was).

### 4.2 Docstrings

Variant docstrings are derived from the base: the factory drops the numpydoc paragraph of each
removed parameter and prepends the variant's one-line role sentence (the text today's hand-written
linear/SNR classes carry). Wording changes slightly and becomes consistent; the autosummary pages
in `docs/api/light.rst` / `mass.rst` list the same names and render from the same attributes.
Docstring text is explicitly **outside** the invariant (§3).

### 4.3 What stays hand-written

Everything with physics: the 65 non-thin classes, the 11 numerics-bearing `*Sph` classes, every
module-level helper, `basis.py`, `mge.py`, `cse.py`, `deflections_memo.py`, `geometry_profiles.py`,
`validate.py`. The epic never edits a formula.

### 4.4 Expected effect

| | before | after (estimate) |
|---|---:|---:|
| thin-class source lines | 4,616 | ~650 (factory calls) + ~250 (`variants.py`) |
| `standard_lp_parent` + lmp dictionary | 42 lines | 3 |
| `light/operated`, `light/linear_operated` | 10 files, 32 lines | 2 files, ~12 lines |
| cross-variant parity tests | 66 functions, ~900 lines | 3 parametrised functions, ~120 lines |
| pinned-value tests (phase 4, optional) | ~430 functions | same assertions as table rows, roughly −40 % lines |
| **profiles/ source** | **20,842** | **≈ 16,500 (−20 %)** |
| **profiles/ tests** | **13,468 lines / 735 functions** | **≈ 11,000 lines / ≈ 400 functions** (phase 4 included) |

Reviewer cost drops with it: a new light profile becomes one physics class plus five one-line
factory calls, and the public surface is pinned by a golden file instead of by reading twelve files.

### 4.5 Risks and how each is closed

| Risk | Closed by |
|---|---|
| Any public-surface drift (name, signature, default, prior, identifier, class path) | phase 0 golden file, byte-identical before/after, run on every PR of the epic |
| Numerical drift | the existing 430 pinned-value tests and the golden file's fixed-grid arrays; `autolens_workspace_test/scripts/profiles_jit.py` for the JAX path (unit tests are NumPy-only — `PyAutoGalaxy/AGENTS.md` "JAX & xp") |
| MRO / `isinstance` drift | the golden file records `[c.__name__ for c in cls.__mro__]`; the parity contract tests exercise the `LightProfileLinear` / `LightMassProfile` paths through `Galaxy` |
| Pickling across worker processes (`multiprocessing`, Dask) | classes are bound at module scope under their own name; pickle round trip is in the golden test |
| IDE / static-analysis loss of explicit signatures | ruling D2 (§6): optionally emit a generated `.pyi` beside each variants module, or accept runtime-only signatures |
| Sphinx autosummary of generated classes | `__doc__` and `__init__.__doc__` set; `docs` CI leg builds on every PR |
| `deflections_memo` L2 split for `mp.Gaussian` / `lmp(_linear).Gaussian` (`deflections_memo.py:469-485`) | those classes keep their names and bases; the memo test file (18 tests) is the witness |
| A hand-written `Sph` with real numerics being replaced by a thin one | the 11 are listed in §2.2 and excluded from phase 3 by name |

## 5. The deeper unification (feature track — sketched, not proposed as a refactor)

Once variants are data, the remaining API question is whether they should be *classes* at all.
Two observations from the survey:

- A `Sph` class is, from PyAutoFit's side, exactly `af.Model(lp.Sersic, ell_comps=(0.0, 0.0))`,
  which already works today. The 63 thin `Sph` classes exist for prior-config convenience
  (`IsothermalSph:` blocks in the yaml) and ergonomics, not capability. The 11 numerics-bearing
  ones are different: they are a cheaper spherical code path.
- A `linear` class is "a profile whose `intensity` is solved, not sampled". PyAutoFit already has
  half the protocol (`__solved_parameters__`, read by `graph_spec` for model figures,
  `light/linear/abstract.py:70-76`). A composition-time form — e.g.
  `af.Model(al.lp.Sersic, intensity=al.Solved())` with `Galaxy` filtering on
  `profile.intensity is solved` instead of `isinstance(profile, LightProfileLinear)` — would
  retire `lp_linear`, `lp_linear_operated` and `lmp_linear` (46 classes, 3 namespaces, 14 yaml files).

Both are **public-API changes**: namespaces disappear, `files/tracer.json` class paths change,
prior yaml keys move, `to_inversion.py` and every workspace script, HowTo tutorial, assistant skill
and docs page that writes `lp_linear.` changes (28 references in `galaxy/to_inversion.py` alone;
workspaces not measured — not cloned). They also need a PyAutoFit primitive (a "solved" prior
that removes a parameter from the free set and marks the instance). That is a feature epic with
deprecation shims (the factories make shims one line each), `Consequence: judge`, and it is not
filed here. The refactor track makes it cheaper and reversible; it does not presume it.

## 6. Rulings needed before phase 1 (recorded in the ledger when answered)

- **D1 — Scope of "unified API".** Refactor track only (§4: same public names, generated), or
  also open the §5 feature epic? The refactor is correct under either answer.
- **D2 — Static signatures.** Accept runtime-generated signatures (verified for PyAutoFit, pickle,
  Sphinx), or also ship generated `.pyi` stubs for IDE completion? (Adds ~1 script, ~0 runtime.)
- **D3 — Where the public-surface golden file lives and whether it also covers `ag.ps`
  point-source profiles and `Basis`.** Proposed: `test_autogalaxy/profiles/files/public_surface.json`,
  profiles only.
- **D4 — Keep the 2 `endswith("Sph")` checks and the lmp dictionary alive one release behind the
  attribute, or switch in the same PR?** Proposed: same PR (internal-only; the golden file proves the
  resolved parent is identical for all 46 linear classes).
- **D5 — Phase 4 (table-driven pinned-value tests).** Worth doing, or keep the per-profile test
  files as they are and take only the parity collapse? It is the largest *test-line* reduction but
  touches 60 files.
- **D6 — The `mass_to_light_ratio` naming asymmetry** noted in the spring-clean record
  (`complete/2026/05/mass-profiles-spring-clean.md`) stays out: it is a parameter rename (API).

## 7. Detailed phase bodies

Phase cards, dependencies and status are in the ledger; the bodies here are what each phase's
`/start_dev` prompt is written from.

### Phase 0 — Witness first (test/, PyAutoGalaxy; small; safe)

1. `test_autogalaxy/profiles/test_public_surface.py` with
   `files/public_surface.json`, generated by a `--regenerate` switch on `main` **before** any
   refactor commit. For every public class reachable from the eight namespaces: class path, MRO
   names, `getfullargspec` args/defaults, annotations, `af.Model(cls).prior_count` and
   `.identifier`, `to_dict(cls())`, `pickle` round-trip equality, and `float64` arrays of the four
   quantities on `ag.Grid2DIrregular([[1,1],[2,2],[3,3],[2,4]])` with default parameters (the grid
   every profile test file already uses). One test, parametrised over the registry, asserts
   equality with the file. Regeneration is a deliberate, reviewed act (the PR diff of the JSON is
   the API-change review).
2. Three contract tests replacing nothing yet (they run alongside the 66 until phase 4):
   Ell-with-zero-ellipticity equals Sph for every `(cls, cls_sph)` pair; `lmp.X` equals `lp.X`
   (image) and `mp.X` (convergence, deflections, potential) for every lmp class; every linear class's
   `lp_instance_from` returns its standard parent with the given intensity.
3. Run `autolens_workspace_test/scripts/profiles_jit.py` and record its pass in the PR as the JAX
   witness baseline.

Witness: the new test passes on `main`; the JSON has one entry per public profile class (count
asserted against the `__init__.py` exports so an unexported class is caught).

### Phase 1 — `variants.py` and the light-profile variants (PyAutoGalaxy; medium; safe)

`variants.py` with `spherical`, `linear`, `snr`, `operated` and the docstring deriver; rewrite
`light/linear/**`, `light/snr/**`, `light/operated/**`, `light/linear_operated/**` and the `*Sph`
classes of `light/standard/**` (including shapelets) as factory calls; switch
`geometry_profiles.py:421,442` and `linear/abstract.py:159` to `_variant_kind`. Delete
`AbstractSersic`'s dead methods and the `LightProfileSNR.image_2d_from` stub.
Witness: phase-0 golden file byte-identical; `test_autogalaxy` and `test_autolens` green;
`profiles_jit.py` green; `docs` leg builds. ≈ −1,900 lines.

### Phase 2 — `light_mass` and the two lmp modules (PyAutoGalaxy; medium; safe)

`light_mass()`; rewrite `light_and_mass_profiles.py` and `light_linear_and_mass_profiles.py` as
tables of factory calls; delete the `standard_lp_parent` dictionary in favour of `_standard_cls`.
Witness: as phase 1, plus `chaining_util.mass_light_dark_basis_from` and `model_util.mge_model_from`
tests green (they map between these classes by identity). ≈ −1,300 lines.

### Phase 3 — Mass `Sph` twins and `reparameterised()` (PyAutoGalaxy; medium; safe)

The 63 thin `Sph` classes across `mass/**` not in the §2.2 exclusion list; `reparameterised()` for
the 18 MCR/virial classes with the converter named per class (`kappa_s_and_scale_radius_for_duffy`,
`…_for_ludlow`, `kappa_s_scale_radius_and_core_radius_for_ludlow`, the virial-mass solvers). Stored
attributes (`mass_at_200`, `redshift_object`, …) and the forwarded base arguments are unchanged.
Witness: as phase 1; `mass/dark/test_nfw_mcr.py`, `test_nfw_scatter.py`, `test_yang24.py` and
`test_scaling_relations.py` green. ≈ −1,300 lines.

### Phase 4 — Test consolidation (PyAutoGalaxy; small→medium; safe; ruling D5)

Delete the 66 parity tests (the phase-0 contract tests cover them); convert the per-profile
pinned-value tests to `pytest.mark.parametrize` tables (one table per quantity per profile family);
drop tests that only re-assert what the golden file pins (argument names, defaults). Witness: the
set of `(profile, quantity, point, expected)` tuples before and after is identical (extract both
with a script and diff), test count and line count reported in the PR.

### Phase 5 — Profiles hygiene (PyAutoGalaxy; small; safe)

`dPIEMassB0.potential_2d_from` decorator stack; `dual_pseudo_isothermal_mass.py` shared
`_ci05/_pi05` dispatch between its five classes where bodies are literal copies; `docs/api/light.rst`
and `mass.rst` regenerated from the namespaces' `__all__`-equivalent (optional). Witness: golden file
byte-identical; `test_dual_pseudo_isothermal_mass.py` green.

### Phase 6 — Composition-time variants (feature/, PyAutoFit + PyAutoGalaxy + PyAutoLens +
workspaces; too-large; judge; only if D1 opens it)

Not a refactor. Filed as its own epic from §5 if ruled; its first phase would be the PyAutoFit
"solved parameter" primitive and a one-release deprecation of the three linear namespaces through
the factories.
