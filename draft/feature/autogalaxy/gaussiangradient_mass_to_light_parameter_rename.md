# GaussianGradient mass to light parameter rename

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autogalaxy_workspace
- autolens_workspace
Themes:
- mge
Difficulty: small
Autonomy: human-required
Priority: low
Status: formalised
Filed: 2026-11-09
Consequence: judge
Review-minutes: 10
Unattended: never
Lane: any

Ruling D6 of the profiles-unified-api epic (2026-11-09: "yes, intake it as a parameter rename").
Recorded but not fixed in `complete/2026/05/mass-profiles-spring-clean.md` ("mass_to_light_ratio
naming asymmetry documented but not fixed (breaking change)"). A parameter rename is a public-API
change — constructor kwarg, prior yaml key, notation label, every saved `tracer.json`, every
workspace script — so it is a feature with a deprecation path, not a refactor, and it is kept out
of the refactor epic whose invariant forbids it.

## The asymmetry

`@PyAutoGalaxy/autogalaxy/profiles/mass/stellar/sersic_gradient.py:12-20` (`SersicGradient`) takes
`mass_to_light_ratio` and `mass_to_light_gradient`, with the gradient applied at evaluation time
relative to `effective_radius` (`:64-76`). `profiles/mass/stellar/gaussian_gradient.py:7-15`
(`GaussianGradient`) takes `mass_to_light_ratio_base`, `mass_to_light_gradient` and
`mass_to_light_radius`, and at construction derives the effective ratio
`mass_to_light_ratio = base * ((sigma + 0.01) / mass_to_light_radius) ** gradient` (`:53-62`) and
passes *that* to `mp.Gaussian.__init__` — so a `GaussianGradient` instance already carries a
`mass_to_light_ratio` attribute with a **different meaning** (the per-Gaussian effective ratio) from
the constructor's `_base`. The same three names appear on `lmp.GaussianGradient`
(`profiles/light_and_mass_profiles.py:61-115`) and `lmp_linear.GaussianGradient`
(`profiles/light_linear_and_mass_profiles.py:52-105`).

Other readers of the `_base` name: `autogalaxy/config/priors/mass/stellar/gaussian_gradient.yaml:66`,
`autogalaxy/config/notation.yaml:40` (and the two test-config twins), `analysis/chaining_util.py:542-544,
672-674` (ties the shared ratio across an MGE basis), `test_gaussian_gradient.py`,
`test_deflections_memo.py:132`, `test_light_and_mass_profiles.py`. The deflections memo treats
`GaussianGradient` as not linear in a single scalar (`profiles/mass/abstract/deflections_memo.py`
module docstring) precisely because of the derived ratio.

## Decide, then do

The rename is not a pure find-and-replace because `mass_to_light_ratio` is taken. Two options for
the human:

- **O1** — rename the constructor parameter `mass_to_light_ratio_base` → `mass_to_light_ratio`
  (the value at `mass_to_light_radius`, matching `SersicGradient`'s meaning "the ratio at the
  reference radius") and move the derived per-Gaussian value to a private or clearly named
  attribute (e.g. `mass_to_light_ratio_effective`). Every `mp.Gaussian` method that reads
  `self.mass_to_light_ratio` then needs the derived value instead — audit `profiles/mass/stellar/gaussian.py`
  and the memo's L2 split.
- **O2** — keep `GaussianGradient` as is and rename `SersicGradient.mass_to_light_ratio` →
  `mass_to_light_ratio_base` with a `mass_to_light_radius` defaulting to `effective_radius`
  (symmetry the other way; touches the more-used class).

Either way: accept the old kwarg for one release with a `DeprecationWarning` (the generated
variants from the refactor epic make the shim one place), migrate the prior yaml key and notation
label, add a `tracer.json` argument-name converter in `autonerves.dictable` loading or a
`from_dict` override, grep the workspaces and HowTo repos, and pin identifiers: the model
identifier of `af.Model(ag.mp.GaussianGradient)` *will* change (identifier hashes argument names),
so the record must say so and the release notes must carry it.

## Witness (once the option is ruled)

Numerics unchanged: `convergence_2d_from` and `deflections_yx_2d_from` of `mp.GaussianGradient`,
`lmp.GaussianGradient`, `lmp_linear.GaussianGradient` on the standard grid are bit-identical
before and after for the same physical inputs; the old kwarg still constructs with a warning;
`test_autogalaxy` and `test_autolens` green; prior yaml and notation updated in the same PR.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/d6.md -->
