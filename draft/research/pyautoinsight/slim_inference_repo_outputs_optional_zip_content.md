# Slim inference-repo outputs: optional zip contents, visualize config, samples weights

Type: research
Target: PyAutoInsight
Repos:
- autofit_inference
- autolens_inference
- PyAutoInsight
Difficulty: medium
Autonomy: safe
Priority: normal
Memory: wiki/methods/concepts/aggregator-performance.md; reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md
Status: formalised
Consequence: glance
Witness: one source_lp[1] search output (zip + unzipped files) measured before/after the config change, with the exported result row unchanged
Review-minutes: 3
Unattended: ready

# Slim inference-repo outputs: optional zip contents, visualize config, samples weights

Human request (2026-10-20, verbatim): "intake an issue which for PyAutoInsight has us go over the files in the .zip folders that are optional (mostly images) and updated the config files of these repos to visualize or output a lot less. This would also include samples weights maybe being tweak to save space."

Type: research
Target: PyAutoInsight
Witness: one source_lp[1] search output (zip + unzipped files) measured before/after the config change, with the exported result row unchanged

## Evidence (measured 2026-10-20, autolens_inference)

- One `source_lp[1]` search zip, 26.2 MB uncompressed: `files/*.csv` 18.9 MB (72%, samples.csv and
  friends), `image/*.fits` 3.6 MB, `image/*.png` 2.8 MB, `files/*.fits` 0.5 MB, json 0.3 MB.
- Whole RAL output tree (excluding prepared/ pickles, see the sibling prepared-without-pickles task):
  samples.csv 290 MB (58 files), *.fits 248 MB (426), *.png 208 MB (398), zips 5-39 MB each.

## Do (assessment first, across the inference repos Insight aggregates: autolens_inference, autofit_inference)

1. Inventory every file in a search output/zip; mark which ones the Insight read contract, the
   exporters (result rows) and a human review actually use, and which are optional (mostly images).
2. Propose per-repo config changes (config/visualize/*, output.yaml) to stop writing the optional
   images/fits for inference runs.
3. Samples: assess raising the samples weight threshold (drop negligible-weight samples from
   samples.csv) and what that changes for evidence/posterior summaries the rows record; quantify the
   saving.
4. Report expected size per search before/after; config edits ship via start_dev.

<!-- formalised by the Intake (Conception) Agent on 2026-10-20 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/88d3fcba-c2d1-4816-8ba3-b341960a2cf7/scratchpad/intake_insight_output_slimming.md -->
