# Polish RTD and workspace Start Here introductions

Type: docs
Target: PyAutoLens
Repos: @PyAutoLens @PyAutoGalaxy @autolens_workspace @autogalaxy_workspace
Status: active
Issued: 2026-11-12
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/834
Consequence: judge
Autonomy: supervised

## Original request

Ok, I happyu with that, I think that the starting of both is too text heavy and description, it preches the Natural language stuff too much, and I think we should use my 2D schematic for the cosmos web ring in PyAutoLens. Stuf like "**Python is not going anywhere.**   " does not belong in the intro to PyAutoLens. The GitHub has a good quick style of explaining theres two ways to explore and use the software, but I think the RTD can have a bit more info. But lets polish this, note also that the same criticism applies to the start_here.ipynb workspace ntoebook. PyAutoBrain has good agents for docs writing.

## Approved scope

- Short science-led opening on both docs/overview/overview_1_start_here.md pages. Keep current README scientific framing in view; README changes are outside this request.
- Replace the natural-language advocacy and defensive Python paragraphs with Explore It Yourself / Explore with AI, a practical sentence on each route, one existing assistant starting prompt and an AI Options link.
- Use autolens_assistant/docs/images/strong_lens_schematic.png in Lens RTD and workspace introductions. Describe it as a schematic, not an observation. Retain provenance.
- Mirror approved prose in each workspace root start_here.py; regenerate start_here.ipynb and applicable markdown outputs with PyAutoHands. Preserve executable code and later walkthrough sections.
- Check links, image loading, prompt copy rendering, focused Sphinx build, notebook validity and unchanged executable content.
- Suggested branch: feature/start-here-intro-polish, isolated bundle inside .worktrees/start-here-intro-polish. Recheck live claims before setup.
- Tier: judge — merge mode: human /prm. Implementation approved 2026-11-12; user review required before raising PRs. No merge approved.

## Survey

2026-11-12: Brain docs and workspace conductors consulted; WRITING_STYLE.md and applicable tutorial prose guidance read. Heart YELLOW permits planning. All four canonical repositories are on main. Lens has unrelated paper_jax/paper.md edits; autolens_workspace has untracked dataset.fits. Preserve both. Other sessions are active: refresh claims at implementation. three-autos-public-framing has released Lens/Galaxy claims after their PR merges; PyAutoFit remains claimed.

## Authorization

Looks good, go ahead and apply these to both RTD pages and the workspace start_here notebooks, using my 2D schematic for PyAutoLens. ask me to review the new text before we raise PR

## Applied checkpoint — 2026-11-12

- Approved text applied in .worktrees/start-here-intro-polish/{PyAutoLens,PyAutoGalaxy,autolens_workspace,autogalaxy_workspace}, all on feature/start-here-intro-polish. Changes remain uncommitted for human text review.
- Libraries: docs/overview/overview_1_start_here.md. Lens also has byte-identical schematic PNG plus provenance TXT in docs/overview/images/overview_1/. Old natural-language-or-python fragment retained as a label.
- Workspaces: root start_here.py, regenerated start_here.ipynb via Hands py_to_notebook + inject_colab_setup + inject_gemini_instructions, and markdown/start_here.md prose prefix regenerated from canonical source; executed remainder preserved.
- Validation: both focused Sphinx introduction builds passed with warnings treated as errors using actual theme/CSS/MyST/copybutton presentation settings. Full API documentation build not run. Notebook schemas valid; executable script AST, all notebook code cells and metadata unchanged; all RTD content from Imports onward and markdown from Google Colab Setup onward byte-identical. git diff --check passed.
- Live introduction links checked: all eight returned HTTP 200; prompt containers, legacy fragments and local schematic references verified in rendered HTML.
- Brain docs audits: 79/100 each; Lens intro heuristic counts caption plus intro as five sentences; other findings concern unchanged later sections. Approved prose retained.
- Logs: bundle autolens_preview_build.log, autogalaxy_preview_build.log, autolens_docs_audit.log, autogalaxy_docs_audit.log. Isolated .docs-venv is tooling only.
- Review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/start_here_intro_polish_20261112/applied_review/index.html (four rendered openings and full regenerated notebooks).
- Next action: human reviews applied text. Do not raise PRs until that review is complete and authorized; no merge authorization.

## Revision 2 — approved and applied 2026-11-12

User approved replacing Explore It Yourself / Explore with AI with one Exploring PyAutoLens / Exploring PyAutoGalaxy section, embedded Google Colab and assistant links, and a short interactive-walkthrough prompt cue. Applied to both RTD sources and both workspace sources; regenerated notebooks and markdown prose. Removed redundant introductory walkthrough paragraph. HowTo links moved to RTD Wrap Up; existing later notebook lecture sections retained.

Updated the same applied_review previews and full notebook copies. Both focused Sphinx builds pass with -W. Notebook schemas valid, executable AST/code cells and metadata unchanged; embedded links, legacy fragment and prompt markup verified; diff checks pass. Aside from the approved HowTo link relocation, later RTD and workspace teaching content is unchanged. Changes remain uncommitted; no PRs raised. Next action remains human text review.
