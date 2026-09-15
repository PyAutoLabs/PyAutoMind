# Experimental Google Colab entry point

Issued: 2026-09-15
Issue: https://github.com/PyAutoLabs/autofit_assistant/issues/44
Type: feature
Repos: @autofit_assistant
Difficulty: small
Autonomy: supervised

## Original request

Can you set up the autofit_assistant with a Google Colab link to experiment with this, put it towards the bottom fo the README.md as for now its experimental

## Scope

Add `notebooks/experimental_colab.ipynb` as an experimental browser entry point
for trying the assistant alongside Colab's Gemini sidebar. Clone the assistant,
install a documented pinned PyAutoFit version, supply curated assistant context
and a copy-to-Gemini bootstrap, and run a small Gaussian inference example.
Explain that cloning does not automatically load assistant instructions into
Gemini, and show how to download results before the runtime expires.

Add an experimental section with an Open in Colab link near the bottom of
`README.md`, directly before License. Validate notebook structure, bootstrap
commands and the small example where the local environment permits; record
browser-only checks explicitly.

## Workflow

Workspace-only task; proposed branch `feature/experimental-colab`. Present the
implementation plan for user approval before editing assistant files. Verify
and reconcile the existing `howtofit-mode` claim before creating a worktree.
