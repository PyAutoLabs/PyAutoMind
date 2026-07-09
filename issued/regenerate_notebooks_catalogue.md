# Regenerate autolens_workspace notebooks + catalogue (global drift)

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Discovered during PyAutoLens#592 (release-docs polish). Running the sanctioned
`PyAutoBuild/autobuild/generate.py autolens` from `autolens_workspace/` rebuilt/added ~30
notebooks and refreshed `llms-full.txt` / `workspace_index.json` — i.e. the workspace's
generated artifacts are **globally stale** vs the `scripts/` source of truth. Missing/added
notebooks included `weak/` (modeling, likelihood_function, real_data/a2744, features/strong_lensing/*),
`cluster/lenstool/*`, `guides/point_source_pairing`, plus content drift in `imaging/`, `group/`.

Under #592 only the two notebooks matching the two edited scripts were committed; all other
regeneration was discarded to keep that docs PR clean. This prompt is the dedicated cleanup:

- From `autolens_workspace/` run the generate step (see AGENTS.md "Generating notebooks"):
  `PYTHONPATH=../PyAutoBuild/autobuild python3 ../PyAutoBuild/autobuild/generate.py autolens`.
- Commit **all** regenerated notebooks + `llms-full.txt` + `workspace_index.json` in one
  "regenerate notebooks + catalogue" PR (no script/source changes — purely generated artifacts).
- Confirm `navigator_check` (catalogue == notebook set) and `run_smoke.py` pass.
- Watch the `.script_sizes.json` guard; this is generated-artifact only, no `scripts/` edits.
