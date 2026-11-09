# Composition time profile variants epic

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
- autogalaxy_workspace
- autolens_workspace
- HowToGalaxy
- HowToLens
- autolens_assistant
- autogalaxy_assistant
Themes:
- mge
- hygiene
Difficulty: too-large
Autonomy: human-required
Priority: normal
Status: formalised
Filed: 2026-11-09
Epic: profiles-composition-time-variants
Consequence: judge
Review-minutes: 30
Unattended: never
Lane: any

Campaign map for the public-API unification the human opened with ruling D1 (2026-11-09: "also
intake the feature 5 epic") of the profiles-unified-api epic
(`draft/refactor/autogalaxy/profiles_unified_api_epic.md`). Evidence and the sketch are
`profiles_unified_api_report.md` §5. This file is never issued itself; phases are filed one at a
time with `Epic: profiles-composition-time-variants` and a `Phase:` once the refactor epic's phases
1–3 are merged (the variants must be data before any namespace is deprecated — the factories make
every deprecation shim one line).

## Why

After the refactor epic a `linear` class is literally "the standard class with `intensity`
removed from its signature and `_intensity = 1.0`", and a `Sph` class is "the elliptical class
with `ell_comps` pinned to `(0.0, 0.0)`". PyAutoFit already expresses the second at composition
time — `af.Model(ag.lp.Sersic, ell_comps=(0.0, 0.0))` — and half of the first: the
`__solved_parameters__` protocol (`@PyAutoGalaxy/autogalaxy/profiles/light/linear/abstract.py:70-76`)
tells `graph_spec` that `intensity` is solved, not sampled. What is missing is a composition-time
way to say "solve this parameter" that removes it from the free set and marks the instance, so
that `Galaxy` / `to_inversion` can filter on the instance rather than on `isinstance(profile,
LightProfileLinear)`. With that, the `ag.lp_linear`, `ag.lp_linear_operated` and `ag.lmp_linear`
namespaces (46 classes, 14 prior yaml files) and most of the 63 thin `*Sph` classes become
redundant and can be deprecated behind one-line shims.

## What changes publicly (the reason this is `judge`)

- Namespaces disappear over a deprecation cycle: `lp_linear`, `lp_linear_operated`, `lmp_linear`;
  possibly the thin `*Sph` names (the eleven numerics-bearing `Sph` classes stay regardless — they
  are a cheaper code path, report §2.2).
- `files/tracer.json` class paths of every past fit name the old classes; `autonerves.dictable`
  resolves by import path, so the shims must survive at least one release and a converter is needed
  for archives.
- Prior yaml keys move (`config/priors/light/linear/*.yaml` → the standard files, with a rule for
  the solved parameter).
- Every workspace script, HowTo tutorial, assistant skill and docs page that writes `lp_linear.`
  changes (28 references in `autogalaxy/galaxy/to_inversion.py` alone; the workspaces were not on
  disk when this was scoped — count them in phase A).
- PyAutoFit gains a primitive (a "solved" prior or parameter marker). Design with the PyAutoFit
  owner; the `Prior/Message` design (#1500) is adjacent and explicitly out of scope.

## Phases (to be filed lazily)

- A — Survey: workspace / HowTo / assistant grep of every `lp_linear`, `lp_snr`, `lmp_linear` and
  `*Sph` use; archive census of `tracer.json` class paths on disk; a decision note on whether `Sph`
  is in scope or only the solved-intensity half. Ruling before B.
- B — PyAutoFit: the solved-parameter primitive (`af.Solved()` or equivalent): removes the
  parameter from `prior_count`, is visible on the instance, round-trips `to_dict`, and keeps
  `identifier` stable for models that do not use it. Witness: identifier pins on the existing
  autofit test models unchanged.
- C — PyAutoGalaxy / PyAutoLens: `Galaxy`, `Galaxies`, `Tracer`, `to_inversion`, `fit_*`,
  `OperateImage` filter on the instance marker; `LightProfileLinear` stays as the shim base; the
  `lp_linear` namespaces become one-line deprecations through the factories with
  `DeprecationWarning`; prior yaml migrated; `tracer.json` converter.
- D — Workspaces, HowTo, assistants, docs migrate; the release notes carry the migration.
- E — Removal one release after D, if the human rules so.

## Rulings needed

- R1 — Is `Sph` in scope, or only the solved-intensity half?
- R2 — The PyAutoFit primitive's name and whether it is a prior type or a model-level marker.
- R3 — Deprecation length (one release, two, or until the next major).

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/epic_ct.md -->
