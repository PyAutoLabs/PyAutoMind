# Unify AI assistant guidance in getting-started documentation

Align the assistant-facing guidance across the relevant library Read the Docs
pages, library READMEs, and workspace READMEs. Survey the existing copies before
finalising scope so the wording remains concise and consistent.

Likely repositories: @PyAutoLens, @PyAutoGalaxy, @autolens_workspace,
@autogalaxy_workspace. Include any other PyAuto documentation surface found to
contain the same split between chat and fully agentic AI.

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
