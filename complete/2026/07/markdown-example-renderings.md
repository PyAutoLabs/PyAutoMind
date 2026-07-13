## markdown-example-renderings
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/134 (closed)
- completed: 2026-07-10
- prs: PyAutoBuild#137 (generator) + autolens_workspace#263 (9 executed pages) — both MERGED same day (700042de / 49277d04), human-authorized in-session
- summary: executed-markdown example pages, GitHub-browsable with real output images. generate_markdown.py (curated config/build/markdown_examples.yaml; never TEST_MODE; features/ refused; tracked-file restore; local-path redaction; stale *_files cleanup; 22 tests) + autolens pilot: root start_here, imaging five, guides trio (83 PNGs ~19M, README links). Both Nautilus fits ran real (2h05m + 1h55m, once); resume cache proven 122s and copied to canonical output/ before worktree cleanup. Review found+fixed path leakage + orphan PNGs pre-ship. Calibration: merged-unchanged. Phase 2 rollout prompt filed (docs/pyautobuild/markdown_example_renderings_rollout.md) — run on Opus per user; cluster runtime + HowTo curated list are human calls.

## Original prompt

# Markdown renderings (with images) of curated workspace + HowTo examples

Type: docs
Target: PyAutoBuild
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Generate markdown (.md) renderings of a small curated subset of flagship examples across the workspaces (autofit/autogalaxy/autolens_workspace) AND the HowTo tutorials (HowToFit/HowToGalaxy/HowToLens), executed with real output images, so new users browsing GitHub can read them cleanly formatted with plots visible. Scope decided at intake: curated subset ONLY (skip a blanket no-image .md mirror — GitHub already renders the output-stripped .ipynb files natively, so no-image .md adds little); images committed in each workspace/HowTo repo next to its .md (PNGs at fixed dpi, .gitignore must not swallow them), not hosted externally. Generator slots into the PyAutoBuild pipeline alongside the existing py->ipynb generation: execute flagged scripts, nbconvert to markdown, write .md + image dir, plus an index page linked prominently from workspace and HowTo READMEs ('Browse the examples with output'). Regeneration is manual/at-release (real runs, not TEST_MODE), only when a flagged script changes.

Curated list (user-decided 2026-07-10): each workspace's start_here.py plus, per dataset type, simulator.py, likelihood_function.py, fit.py and modeling.py; NOTHING from any features/ folder; autolens_workspace guides/galaxies, guides/lens_calc and guides/tracer.py; and the base workspace start_here.py. Execution-time constraint: the image build must NOT spend ages sampling, but PYAUTO_TEST_MODE truncates the search and would produce WRONG images — think carefully here (e.g. run modeling searches once to completion and cache/load results for regeneration, or use fast-but-real search settings validated to give correct plots; TEST_MODE output images are unacceptable). Original motivation verbatim: 'we could also make markdown (.md) files from the .py files... on github when a user browses the github webpages they can literally read every example there in a way that is more cleanly formatted than .py files... could do for a small subset of examples (e.g. to entice new users).'

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from user-intake -->
