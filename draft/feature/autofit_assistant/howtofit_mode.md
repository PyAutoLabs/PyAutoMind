# autofit_assistant: HowToFit learning mode

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
Themes:
- assistants
Difficulty: small
Autonomy: safe
Priority: medium
Filed: 2026-09-14

## Original request

In autofit_assistant, we recently added start_here and byol models where users hit the README.md, and then paste in a standard prompt to do that. Can you add a "HowToFit" mode to the agent, which points the user to the HowToFit GitHub, explinas they can do the lectures using Jupyter Notebook (recommended if they want to run code) or markdown, and once they are in this how the assistant will answer any questions they have.

## Scope

- Add a HowToFit entry and standard copy-and-paste activation prompt to @autofit_assistant/README.md alongside its existing modes.
- Add a mode document following the existing start_here and byol conventions and register its routing where needed.
- Direct learners to the HowToFit GitHub repository; explain Jupyter Notebook (recommended for running lecture code) and Markdown reading options.
- Explain that the assistant answers lecture questions in this mode, using the learner's current lecture, question, code or error as context.
- Check consistency of mode activation, internal links and the course link; no lecture or library changes are required.
