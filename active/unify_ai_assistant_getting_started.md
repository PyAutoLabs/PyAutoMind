# Phase 1: Unify AI assistant guidance in library documentation

Update the library READMEs and Read the Docs sources for @PyAutoLens and
@PyAutoGalaxy. Present one concise **AI Assistant** route covering conversation
agents (for example ChatGPT) and coding agents (for example Claude Code and
Codex), then direct readers to the relevant assistant repository for its full
scope.

Put the assistant first in each Getting Started section. Introduce the remaining
links as human-readable documentation and examples. Remove the duplicated
**AI chat assistant**, **Fully agentic AI**, and **Three Ways to Learn
PyAutoLens** framing from the scoped library and Read the Docs pages.

The intended PyAutoGalaxy assistant URL must resolve before its links are
published. Phase 2 is tracked separately in
`draft/docs/workspaces/unify_ai_assistant_workspace_readmes.md`.

## Original request

- All readthedocs / README.md explaining the assistant should not have two separate splits for **AI chat assistant** 
and **Fully agentic AI**, but instead just say AI assistant. They should concisely say conversation agents (e.g. ChatGPT)
and coding agents (e.g Claude, codex) and then point to the assistant URL, which is where the user gets the full scope.
- 
- PyAutoLens and PyAutoGalaxy README.md should point to their assistant in the "Getting Started" section, and
then have the bit The following links are useful for new starters but say they are human readable docs.
- It feels like we are oging to get rid fo this section "## Three Ways to Learn PyAutoLens", and these style changes
will also hapepen on readthedocs and the workspace README.md files.

- the worksapce readme should keep the colab stuff, but point to the assistant in Getting Started first. Again
I think "## Three Ways to Learn PyAutoLens" will thus go.
