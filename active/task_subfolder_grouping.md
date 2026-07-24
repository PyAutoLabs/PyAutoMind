# autolens_workspace_test: task subfolders inside dataset folders + prefix cleanup (Phase 2c)

Type: refactor
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised

User feedback on the merged #212 restructure (2026-07-24): flattening into
dataset folders lost the task-describing second level (jax_likelihood,
jax_grad, visualization...), and dataset prefixes/suffixes are now redundant
("we don't need scripts beginning with imaging_ ... now they are in a named
folder").

**Principles:**
- Within each dataset folder, group by TASK where >=2 related scripts exist:
  `jax_likelihood/` (the former vmap-likelihood family), `jax_grad/`,
  `visualization/` (visualization*.py + modeling_visualization_jit*),
  `simulator/` (consolidate loose simulator*.py into the existing dir),
  `substructure/` (the test_*simulate* trio). Singletons stay at folder root
  (no one-file subfolders).
- Strip prefixes/suffixes made redundant by the containing folders:
  imaging/imaging_lp.py -> imaging/jax_grad/lp.py; the *_datacube suffix
  renames become interferometer/datacube/{delaunay,rectangular,
  shared_preloads}.py; interferometer/interferometer.py ->
  interferometer/jax_grad/gradient.py; point_source/point_source.py ->
  point_source/jax_grad/gradient.py; misc/weak.py -> misc/weak/jax_grad.py
  (also resolves the weak.py-vs-weak/ file/dir coexistence).
- Same machinery + gates as #212: git mv only, zero deletions; smoke/no_run/
  override patterns follow; bootstrap subprocess paths follow (simulators are
  no_run BOOTSTRAP-TARGETs — their no_run entries and every consumer's spawn
  path must update together); jax_grad util-shim depths re-fixed; docs
  updated.

**CRITICAL jax_* subfolder rule:** a `jax_*` path segment re-triggers the
release derive_jax_markers derivation. Only scripts carrying a `jax`
declaration may live under a jax_* subfolder (derivation sets "0", the
declaration's unset applies last -> absent, resolved dict unchanged — verify
per script). A non-JAX script placed under jax_* would flip release
numpy->JAX: the gate must prove zero resolved-env diffs, which catches this.

**Gate:** resolved env + should_skip identical per script (both profiles,
empty base); smoke entries exist; validator all-strict 0; git-mv renames;
bootstrap dry-run for at least one consumer per re-pathed simulator.

Agent must produce the FULL proposed mapping table (old -> new, with the
grouping rationale per subfolder) as the first section of its report so the
human can review the taxonomy at PR time.
