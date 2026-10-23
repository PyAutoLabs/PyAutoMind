## fixed-model-json
- completed: 2026-10-17
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1704
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1708
- head: b4b9e2e0af657ebacbb63394f96d6499361bc951
- validation: Final full serial suite 3704 passed, 120 skipped, 1 xfailed; affected model/graph/aggregator tests 305 passed. Initial five from_instance regressions repaired; legacy instance JSON behavior retained.
- identifier-evidence: Free/fixed/mixed baseline model hashes, search IDs and exact output paths unchanged; converted-instance JSON and hash also unchanged. JSON roundtrip preserves original persistent identifiers.
- witness-detail: GraphSpec comparison excludes process-local obj_id/prior_id counters (pre-existing JSON limitation); all semantic graph fields compared. No identifier algorithm edits.
- merge: 48f1c31beaa7e0c50978646ee14e19511119c4cc
- authorization: Human /prm in this chat, 2026-10-17.
- merge-proof: Remote PR head is an ancestor of origin/main in unshallowed PyAutoFit; zero unmerged commits. GitHub confirms MERGED.
- ci: All head workflows and jobs completed successfully; Python 3.12, 3.13 and no-JAX test legs passed. Applicable docs and generated-search-docs passed. No review objections.
- freeze: pyauto-heart freeze --show returned not frozen. Readiness remains STALE; no release-readiness claim.
- release-link-repair: GitHub pending-release label verified; restored the missing Mind link during close-out.
- shadow-row: Human confirmed merged-unchanged in this chat on 2026-10-17; stage-1 glance row appended to autonomy_log.md.
- release-follow-up: Remove the lens cookbook reload warning after this library fix is released.

## Original prompt

# af.Model.from_json writes zero-free-parameter components back as instances

Issued: 2026-10-17
Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- serialization
- visualization
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: glance
Witness: Dumping and reloading (`output_to_json` / `af.Model.from_json`) a `Collection` holding an all-fixed `Model` and a parameter-less `Model` gives `GraphSpec.from_model(reloaded).to_dict()` equal to the original's (test in `test_autofit/graph_spec`), and the lens cookbook's "reloaded figure differs" sentence is removed once released.
Review-minutes: 3
Filed: 2026-09-11

Found by the model figure while adding it to `autolens_workspace/scripts/guides/modeling/cookbook.py`
(model-figures epic phase 3, PyAutoLens#736). The cookbook's `__JSon Outputs__` stage dumps a model
with `model.output_to_json` and reloads it with `af.Model.from_json`. `model.info` looks unchanged,
but the reloaded model is not the same model: every component with **zero free parameters** comes
back as a plain instance instead of an `af.Model` — in the Solved Parameters model the `Delaunay`
mesh (all-fixed `pixels`/`zeroed_pixels`/`areas_factor`) and the whole `point_source` galaxy
(`PointSolved` has no parameters) collapse to single fixed pills. `af.ModelPlotter` shows it
directly: fixed leaf slots drop 6 → 4 and solved rows 3 → 2 across the round trip, and
`GraphSpec.from_model(...).to_dict()` differs. The galaxy cookbook's model (every component has a
free parameter) round-trips byte-identically, so the trigger is the zero-free-parameter case.

## Ask
- Reproduce with `test_autofit/graph_spec` style: dump/reload a `Collection` holding an all-fixed
  `Model` and a parameter-less `Model`; assert `GraphSpec.from_model(reloaded).to_dict()` equals the
  original's.
- Decide whether `from_json` should preserve `Model`-ness for such components (likely: the JSON
  already records `type: model`? check `autofit/mapper/prior_model/abstract.py` `from_dict`) and fix.
- Until fixed the lens cookbook says the reloaded figure differs; revert that sentence when it no
  longer does.
