# Profiles public surface witness

Type: test
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace_test
Themes:
- hygiene
- mge
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Filed: 2026-11-09
Epic: profiles-unified-api
Phase: 0
Consequence: notify
Witness: `pytest test_autogalaxy/profiles/test_public_surface.py` passes on `main` with exactly one golden entry per class exported by the eight profile namespaces (count asserted against the `__init__.py` exports), the three contract tests pass for every (Ell, Sph) pair, every lmp class and every linear class, and the PR records a green `autolens_workspace_test/scripts/profiles_jit.py` run as the JAX baseline
Review-minutes: 1
Unattended: ready
Lane: any

Phase 0 of the profiles-unified-api epic (`draft/refactor/autogalaxy/profiles_unified_api_epic.md`;
design and evidence in `profiles_unified_api_report.md` §3, §7). Witness first: nothing in
`test_autogalaxy/profiles/` pins the *public surface* of the profile classes — argument names,
defaults, prior resolution, model identifiers, class paths — which is exactly what the factory
refactor in phases 1–3 could silently change. This prompt records that surface on `main` before
any refactor commit. No source file under `@PyAutoGalaxy/autogalaxy/` changes.

## Deliverables

1. `@PyAutoGalaxy/test_autogalaxy/profiles/test_public_surface.py` with
   `test_autogalaxy/profiles/files/public_surface.json` (ruling D3: profiles only — `ag.ps` and
   `Basis` excluded). A `--regenerate` switch (a pytest option or a `python -m` entry in the test
   module) writes the file; the committed file is generated on `main` in this PR. For every public
   class reachable from `ag.lp`, `ag.lp_linear`, `ag.lp_snr`, `ag.lp_operated`,
   `ag.lp_linear_operated`, `ag.lmp`, `ag.lmp_linear`, `ag.mp` record:
   - `f"{cls.__module__}.{cls.__qualname__}"` and `[c.__name__ for c in cls.__mro__]`;
   - `inspect.getfullargspec(cls)` args, defaults and the `typing.get_type_hints(cls.__init__)`
     annotation names — the exact calls PyAutoFit makes (`autofit/mapper/prior_model/prior_model.py:146-153, :365`);
   - `af.Model(cls).prior_count` and `af.Model(cls).identifier`;
   - `ag.to_dict(cls())` (default construction) and `pickle.loads(pickle.dumps(cls())) == cls()`;
   - `float64` arrays of `image_2d_from` (light), `convergence_2d_from`, `deflections_yx_2d_from`,
     `potential_2d_from` (mass) on `ag.Grid2DIrregular([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])`
     with default parameters, stored to full precision; a class whose default parameters raise
     records the exception type instead.
   One test, parametrised over the registry, asserts equality with the file; one test asserts the
   registry size equals the number of classes the eight `__init__.py` modules export.
2. Three parametrised contract tests in the same directory, replacing nothing yet (the 66
   hand-written parity tests they generalise stay until phase 4): for every `(cls, cls_sph)` pair,
   `cls(ell_comps=(0.0, 0.0), **kwargs)` equals `cls_sph(**kwargs)` on the standard grid for each
   quantity the class defines; for every `ag.lmp` / `ag.lmp_linear` class, `image_2d_from` equals
   the `ag.lp` / `ag.lp_linear` parent and `convergence_2d_from` / `deflections_yx_2d_from` /
   `potential_2d_from` equal the `ag.mp` parent; for every linear class, `lp_instance_from` returns
   its standard parent with the given intensity (today's `standard_lp_parent`,
   `@PyAutoGalaxy/autogalaxy/profiles/light/linear/abstract.py:118-166`).
3. Run `@autolens_workspace_test/scripts/profiles_jit.py` and paste its pass into the PR as the
   JAX-parity baseline (unit tests are NumPy-only — `PyAutoGalaxy/AGENTS.md` "JAX & xp").

## Acceptance

The header `Witness:`; `pytest test_autogalaxy -q` green; `git diff` touches nothing under
`autogalaxy/` and no `autogalaxy/config/priors/` file. Regeneration of the JSON is a reviewed act:
from phase 1 on, a diff of this file in a PR *is* the public-API review.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/p0.md -->
