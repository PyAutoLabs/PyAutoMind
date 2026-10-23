The four science-assistant READMEs were rewritten for a human arriving cold, and the style was codified in PyAutoBrain.

- autolens_assistant#163: README rewritten to the maintainer's spec (short Getting Started, one-line Colab pointer, strong-lens schematic, Teacher Mode subsection, advanced prompts in docs/advanced_examples.md, Scientific Context before Science Project, Conversational Assistants, Benchmarks near the end, AI-agent note collapsed at the bottom); plain-English Claude Code and Codex setup pages.
- autogalaxy_assistant#37: restyled; roadmap moved to docs/whats_available.md.
- autofit_assistant#58: restyled (465 → 228 lines); API tour → docs/tour.md, own-project steps → docs/your_own_project.md.
- autocti_assistant#37: restyled; Teacher Mode and collapsed agent note added.
- PyAutoBrain#538: skills/WRITING_STYLE.md (house style for people-facing pages), linked from /docs and the review faculty rubric. Root workspace AGENTS.md (untracked, local) gained an on-demand pointer.

Heart was STALE at ship (Release STALE; PyAutoHands release workflow failure; manifest_drift workspace checkouts red); the maintainer approved shipping. Tier judge, human /prm.

Follow-ups: draft/feature/pyautobrain/docs_conductor.md (dedicated Documentation conductor); draft/docs/autolens_assistant/ai_options_page_autolens_leg.md still holds the legacy deletions (opencode_cli.md, docs/archive/, .gemini/, agent_evaluation.md, AGENTS.md wording) — its README part is now done. Pre-existing test failures seen: autolens forward-model truth version pin; autofit hard_sne_cosmology README-parity; autocti benchmarks/prompts and test_mcp_tools.

## Original prompt

# Human-readable READMEs across the four science assistants

Type: docs
Target: autolens_assistant
Repos:
- autolens_assistant
- autogalaxy_assistant
- autofit_assistant
- autocti_assistant
Difficulty: small
Autonomy: supervised
Priority: high
Filed: 2026-10-23
Issued: 2026-10-23
Status: issued
Consequence: judge

@autolens_assistant @autogalaxy_assistant @autofit_assistant @autocti_assistant

## Context

The human found the autolens_assistant README "went far from being a good starting point for a human" and gave a
detailed rewrite spec (verbatim below). The rewrite was done in-session on 2026-10-23 and the human approved its tone
and style, then asked for (1) the style codified in PyAutoBrain (`skills/WRITING_STYLE.md`, shipped as a separate
Brain PR) and (2) the same style applied across the other three assistants.

Overlaps `draft/docs/autolens_assistant/ai_options_page_autolens_leg.md`: this task covers its README block (Getting
Started now links the shared AI options page; Colab moved to a one-line pointer above Getting Started). The leg's
remaining items (delete `docs/setup/opencode_cli.md`, `docs/archive/`, `.gemini/`, `docs/evaluation/agent_evaluation.md`,
AGENTS.md wording) stay in that draft.

## Scope

- autolens_assistant: README rewrite per the human's spec; new `docs/advanced_examples.md` (old Example Prompts 2–3);
  plain-English `docs/setup/claude_code.md` and `docs/setup/codex_cli.md`; link fixes in `first_prompts.md` and
  `skills/al_to_notebook.md`.
- autogalaxy_assistant, autofit_assistant, autocti_assistant: README (and any setup pages) restyled to Brain
  `skills/WRITING_STYLE.md`, mirroring the autolens structure; long material (autofit tour, roadmaps) moved to
  `docs/` pages linked from short bullets.

## Done when

Four PRs open with human-readable READMEs, tests green, no dangling links; human reviews (with an AI) and /prm.

## Original request (verbatim, 2026-10-23)

> 1. do it, 2. do it 3. yes but I also want this same change in style applied across the other 3 assistants

(3 = "ship the autolens_assistant changes with /ship_workspace once reviewed". The original autolens spec was a long
pasted list in the same session: move the AI-agent note to the bottom, two-sentence Getting Started, one-paragraph
start, strong-lens schematic, new starting-prompt intro, Teacher Mode subsection, Example Prompts 2/3 to a separate
page, Scientific Context above Science Project, Benchmarks to the bottom, Conversational Assistants replacing
Experimental alternatives, setup pages more human readable.)
