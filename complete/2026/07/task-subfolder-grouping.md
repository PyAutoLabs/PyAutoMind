## Outcome — SHIPPED + MERGED 2026-07-24 (PR #217)

Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/216
(closed). Task subfolders restored inside dataset folders (jax_likelihood/
jax_grad/ visualization/ simulator/ substructure/ datacube/; singletons at
root); redundant prefixes stripped; weak/ promoted out of misc/ to mirror
autolens_workspace's top-level weak/ (misc/weak.py -> weak/jax_grad.py also
resolved the file/dir coexistence). 65+ git-mv renames, zero deletions.

## Design decisions
- jax_likelihood vs jax_grad split by PROVENANCE (recovered from the #212
  rename map), not name-guessing.
- visualization/ filenames kept where stripping would silently DEMARK
  _jax/_jit name markers; multi/visualization/ stripped (marker-safe).
- Simulators consolidated ONLY into existing simulator/ dirs
  (simulator_* -> simulator/{simple,dspl}); multi/ and cluster/ simulators
  stayed (no existing dir -> zero consumer churn).
- jax_* SEGMENT RULE enforced: only jax-declared scripts under jax_*
  subfolders (release derivation re-fires there; declarations applied last
  keep the resolved dict identical — verified per script).

## Gotchas
- 41 consumer spawn paths + BOOTSTRAP-TARGET no_run entries must move
  together; one false positive caught (a prose ref to the autolens_workspace
  repo's simulator — different repo, restored).
- util shims re-depth on every level change; misc/weak.py's bare
  `import util` relied on script-dir and needed a shim when moved.
- gallery_run.sh hard-codes visualization script paths — 8 rewritten.

## Follow-ups
Same recipe for autogalaxy_workspace_test (mirror + subfolders in one pass —
cheaper than two); profiling/ move (blackjax claim); eyes_gallery_repoint;
test_results_relayout (Phase 3); potential_correction asymmetry bug (drafted).

## Original prompt

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
