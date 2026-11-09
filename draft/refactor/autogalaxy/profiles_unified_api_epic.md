# Profiles unified API epic: generate the light/mass profile variants from one module of factories, pin the public surface first, and collapse the per-variant tests

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
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued; blocked on rulings D1–D5 in the report §6
Consequence: glance
Witness: phase 0 — `test_autogalaxy/profiles/test_public_surface.py` passes on `main` with one golden entry per public profile class; phases 1–3 — the golden file is byte-identical before and after each PR, `test_autogalaxy` + `test_autolens` + the `docs` leg green, `autolens_workspace_test/scripts/profiles_jit.py` passes; phase 4 — the extracted `(profile, quantity, point, expected)` tuple set is identical before and after and the PR reports the test-function and line counts
Lane: any
Review-minutes: 10
Unattended: never
Epic: profiles-unified-api
Filed: 2026-11-09

Human request (verbatim, 2026-11-09): "I want us to plan some major refactors of pyautoarray,
pyautogalaxy and pyautolens. Use the Brain refactor agent to scope out where we could redesign code
that reduces number of lines of python, number of unit tests and generally makes code more readable
and maintainable. I think the profiles module is a good target noting that we also have thoughts on
how to design it with a clear unified API. But also assess what is feasible in general."

Survey, framework constraints, design, risks and the detailed phase bodies:
`profiles_unified_api_report.md` beside this file (written 2026-11-09 by the Refactor Agent
session from read-only clones; no code edited, nothing run). The general feasibility assessment
across the three libraries is `draft/refactor/libraries/line_count_reduction_survey.md`. This
file is the ledger: phase cards, rulings, status.

## Summary

`autogalaxy/profiles/` is 49 % of PyAutoGalaxy's source and 54 % of its tests. 131 of its 198
classes are a hand-written `__init__` that pins one argument of a parent and re-states the parent's
docstring (4,616 lines; 74 `*Sph` twins, 46 linear/SNR/operated variants, 31 light-and-mass
compositions, 18 mass–concentration reparameterisations), and 66 tests assert one variant equals
another. The variants are distinct classes because PyAutoFit reads a class's constructor signature
as its parameter space and resolves priors and JSON by module path + class name — so they stay
distinct classes at the same import paths, but become **generated** by six factories in a new
`autogalaxy/profiles/variants.py`. Public names, signatures, defaults, prior yaml, class paths,
`isinstance` roles and numerics are unchanged; a golden public-surface file recorded before the
first edit is the witness. Expected: ≈ −4,000 source lines in `profiles/` (−20 %) and 66 parity
tests → 3, with the pinned-value physics tests kept as tables. The deeper unification (retiring the
`lp_linear` / `lp_snr` / `lmp_linear` namespaces for composition-time variants) is a public-API
feature across PyAutoFit and every workspace; it is sketched in the report §5 and opened only on
ruling D1.

## Human design notes

(Paste the "clear unified API" thoughts here before phase 1 is issued; the report §4 is then
reconciled against them and D1 ruled.)

## Rulings

- D1 — scope (refactor only, or also open the §5 feature epic): **open**
- D2 — runtime-generated signatures only, or also generated `.pyi` stubs: **open**
- D3 — golden-file location and scope: **open** (proposed `test_autogalaxy/profiles/files/public_surface.json`, profiles only)
- D4 — switch the `endswith("Sph")` checks and the lmp dictionary in the same PR: **open** (proposed yes)
- D5 — phase 4 table-driven pinned-value tests: **open**

## Phases

Epic slug `profiles-unified-api`. PyAutoGalaxy only in phases 0–5; PyAutoLens is a witness (its
suite runs against the branch), not an editing target. One issue per phase; each ships behind
`start_dev` → `start_library` → `ship_library` at the refactor cap (`safe`), so `--auto` runs each
phase to an open PR gated by the four-leg autonomous-ship gate; merge stays human at `glance`.
Phase prompts are filed lazily, one per phase, with `Epic: profiles-unified-api` and an integer
`Phase:`. Issue one phase at a time, never the whole map. Detailed bodies: report §7.

### Phase 0 — Witness first (test/, PyAutoGalaxy; small; safe) — no dependencies
- `test_autogalaxy/profiles/test_public_surface.py` + `files/public_surface.json` generated on
  `main` before any refactor commit: class path, MRO, `getfullargspec` args/defaults/annotations,
  `af.Model(cls).prior_count` + `.identifier`, `to_dict(cls())`, pickle round trip, and the four
  lensing/light quantities on the standard 4-point grid, for every public class in the eight
  namespaces. Three parametrised contract tests (Ell≡Sph at zero ellipticity; lmp≡lp+mp;
  linear `lp_instance_from` round trip). Record a `profiles_jit.py` pass.
- Witness: the header's phase-0 witness. Size: small. Compute: none.

### Phase 1 — `variants.py` and the light-profile variants (PyAutoGalaxy; medium; safe) — depends on 0, D2, D4
- `spherical`, `linear`, `snr`, `operated` factories + docstring deriver; rewrite `light/linear`,
  `light/snr`, `light/operated`, `light/linear_operated` and the light `*Sph` classes as factory
  calls; `_variant_kind` replaces the two name checks; dead `AbstractSersic` methods and the SNR
  stub removed. ≈ −1,900 lines.
- Witness: golden file byte-identical; both suites, docs leg and `profiles_jit.py` green.

### Phase 2 — `light_mass` and the lmp modules (PyAutoGalaxy; medium; safe) — depends on 1
- `light_mass()`; `light_and_mass_profiles.py` and `light_linear_and_mass_profiles.py` as tables;
  the `standard_lp_parent` dictionary deleted. ≈ −1,300 lines.
- Witness: as phase 1, plus the `chaining_util` / `model_util` tests that map between these
  classes by identity.

### Phase 3 — Mass `Sph` twins and `reparameterised()` (PyAutoGalaxy; medium; safe) — depends on 1
- 63 thin `Sph` classes (the 11 numerics-bearing ones listed in report §2.2 stay hand-written);
  18 MCR/virial classes through `reparameterised()`. ≈ −1,300 lines.
- Witness: as phase 1, plus `test_nfw_mcr.py`, `test_nfw_scatter.py`, `test_yang24.py`,
  `test_scaling_relations.py`.

### Phase 4 — Test consolidation (PyAutoGalaxy; small→medium; safe) — depends on 0–3, D5
- Delete the 66 parity tests; pinned-value tests → parametrised tables; drop tests the golden
  file subsumes.
- Witness: identical `(profile, quantity, point, expected)` tuple set before/after; counts in the PR.

### Phase 5 — Profiles hygiene (PyAutoGalaxy; small; safe) — depends on 3
- dPIE decorator stack and shared `_ci05/_pi05` dispatch; optional regeneration of
  `docs/api/light.rst` / `mass.rst` from the namespaces.
- Witness: golden file byte-identical; `test_dual_pseudo_isothermal_mass.py` green.

### Phase 6 — Composition-time variants (feature/; PyAutoFit, PyAutoGalaxy, PyAutoLens, workspaces; too-large; judge) — only if D1 opens it
- Not a refactor; filed as its own feature epic from report §5. First phase: the PyAutoFit
  "solved parameter" primitive, then a one-release deprecation of the three linear namespaces via
  the factories.

## Log

- 2026-11-09 — FILED by the Refactor Agent session with the report and the cross-library survey.
  Nothing issued. Next: the human pastes the unified-API notes, rules D1–D5, then
  `/start_dev draft/refactor/autogalaxy/profiles_unified_api_p0_witness.md` (to be filed via
  `/intake` from report §7 phase 0 once D3 is ruled).
