## assistant-docs-hierarchy
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/647
- completed: 2026-07-24
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/648, https://github.com/PyAutoLabs/PyAutoGalaxy/pull/522
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/330, https://github.com/PyAutoLabs/autogalaxy_workspace/pull/156
- summary: Added distinct AI Assistant and Human-Readable Documentation sections across the PyAutoLens and PyAutoGalaxy READMEs, RTD landing pages, Start Here pages, New User Guides, and workspace READMEs. Repaired the flattened workspace installation and Colab layout. All library tests, Sphinx builds, workspace smoke tests, and GitHub checks passed; no API, scripts, or notebooks changed.

## Original prompt

# Clarify AI Assistant and human-readable documentation options

## Original request

On the README.md page can you use smaller subsection heading to spit PyAutoLens AI Assistant and Human readable docs, or bold font, or something to make them appear a bit more separate and distinct as two options? The PyAutoLens AI Assistant supports conversation agents such as ChatGPT and coding agents such as Claude Code and Codex. You can get started simply by asking it a question about gravitational lensing or describing the task you would like to perform with PyAutoLens. See the assistant for its full scope and instructions.

The following human-readable documentation and examples are also useful for new starters:               The formatting and strucutre on autolens_workspace is flat out broken: The following human-readable documentation and examples are also useful for new starters:

You can get set up on your personal computer by following the installation guide on our readthedocs.

Alternatively, you can try PyAutoLens out in a web browser by going to the autolens workspace on Colab.   Also for formatting split on readthedocs lensing or describing the task you would like to perform with PyAutoLens. See the assistant for its full scope and instructions.

The rest of this human-readable guide begins with two simple questions to help you find the most appropriate example notebook for your science case. and also have the AI assistant section at the top of the "Start Here" page of each readthedocs

## Scope

Improve the visual hierarchy between the AI Assistant route and the human-readable documentation route across the PyAutoLens and PyAutoGalaxy library READMEs, Read the Docs landing/Start Here pages, and matching workspace READMEs. Repair the flattened autolens_workspace Getting Started structure while retaining installation and Colab guidance. Put the AI Assistant section at the top of each Read the Docs Start Here page.

Affected repositories: @PyAutoLens, @PyAutoGalaxy, @autolens_workspace, and @autogalaxy_workspace.
