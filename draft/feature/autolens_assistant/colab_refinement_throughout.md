# Refine the assistant for Google Colab, here and throughout

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- assistant
- colab
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 15
Unattended: needs-input
Blocked-by: PyAutoMind/active/cosmos_web_ring_greeting.md (autolens_assistant#136)
Filed: 2026-09-26

## Request

User (2026-09-26, verbatim from the COSMOS-Web Ring greeting request): "A follow up issue
will further refine the assistant in the context of Google colab here and throughout."

## Scope

The COSMOS-Web Ring greeting (#136) adds one dedicated Colab notebook
(`docs/colab/cosmos_web_ring_colab.ipynb`) and promotes it as a recommended route for
people learning PyAutoLens who want to see the API. This follow-up makes Colab a
first-class surface across the assistant: how the skills phrase "run this" when the user
is in a notebook rather than a shell (`al_to_notebook`, `al_setup_environment`,
`al_run_search` output-folder tours), how `wiki/core/operations/installation.md` and the
setup docs present Colab next to Claude Code/Codex, whether other worked examples
(Teacher-mode simulate/fit, SLACS0946) deserve notebook twins, and how the assistant's
prose invites the user to ask Colab's Gemini as the natural-language hook. Decide with the
human which of these ship; no new library API.
