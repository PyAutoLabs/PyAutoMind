# Dependency-cap refresh 2026-08: safe bumps, astropy 8 decision, two dead deps

Type: maintenance
Target: libraries
Repos:
- PyAutoFit
- PyAutoArray
- PyAutoGalaxy
Themes:
- release
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-06 (backfilled from git)

Filed 2026-08-06 from a full `/dep_audit` (38 capped/pinned specifiers across
8 pyprojects vs PyPI latest; no cross-repo conflicts — every duplicated
constraint is byte-identical). Follows the floors-not-pins doctrine
(version-pinning redesign).

**Tier 1 — safe cap bumps:** scipy `<=1.17.1` → 1.18.0 (Fit+Array),
scikit-learn `<=1.8.0` → 1.9.0 (Array), xxhash `<=3.4.1` → 3.8.1 (Fit),
corner `==2.2.2` → 2.3.0 (Fit).

**Dead deps (verify then remove from PyAutoFit):** `astunparse==1.6.3` (zero
references; `requires-python>=3.12` has `ast.unparse` built in) and
`gprof2dot==2021.2.21` (no import site or invocation found; CLI tool, so
confirm no doc/script references before dropping).

**astropy `<=7.2.0` (Array+Galaxy) — decision needed:** blocks astropy 8.x
and the dev venv already runs 8.0.1 (exceeds the repos' own cap — env drift).
Broad FITS/units/coords usage → needs a verification pass, not a drive-by
bump. Note the in-flight astropy-cap-bump task (PyAutoArray#435 /
PyAutoGalaxy#558) — check what range those PRs land before scoping.

**Suspicious pin:** `pynufft==2022.2.2` in PyAutoArray's `dev` extra only,
unannotated, while the `optional` extra has pynufft uncapped — looks
accidental; investigate and align.

**Deliberately excluded from this task:** jax/jaxlib `<0.11.0` (Nerves) now
blocks the released 0.11.0 — base layer of the whole differentiable path;
needs its own dedicated migration task with the JAX 0.4→0.5-style
verification pass. Samplers stay pinned by doctrine (dynesty, nautilus, zeus,
getdist); tfp-nightly and nufftax pins are annotated and deliberate.

PyPI-tooling caveat for the executor: the PyPI JSON API returns stale data for
some packages (jax, tfp-nightly) — resolve latest via `pip index versions`
cross-checked against `pypi.org/simple/<pkg>/`.
