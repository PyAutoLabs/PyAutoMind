# autolens_assistant leg of the PyAutoLabs AI-options page (deferred from #87)

Type: docs
Target: autolens_assistant
Repos:
- autolens_assistant
Difficulty: small
Autonomy: supervised
Priority: high
Filed: 2026-10-23
Status: formalised
Consequence: glance

@autolens_assistant

## Context

PyAutoScientist#87 (record `complete/2026/10/assistant-ai-options-page.md`) shipped `PyAutoScientist/AI_OPTIONS.md` and simplified the autogalaxy, autofit and autocti assistant READMEs. The autolens_assistant leg was deferred because the repo was claimed by cosmos-web-ring-notebook (autolens_assistant#161). Start this once #161 has merged and its claim is released.

## Scope (mirror the merged autogalaxy_assistant#36 diff)

- README: replace the "Choose Claude Code or Codex …" three-step block, the "If you cannot use either agent, OpenCode …" line and the "Experimental alternatives" section with the shared one-paragraph block + link + clone snippet + starting prompt. Move the Colab badge paragraph out of the getting-started block into the "Using PyAutoLens Assistant" learning context (keep `docs/colab/`).
- Add `AI_OPTIONS.md` stub beside `AI_POLICY.md`.
- Delete `docs/setup/opencode_cli.md`, `docs/evaluation/agent_evaluation.md`, `docs/archive/`, `.gemini/settings.json`; fold anything still unique in `docs/setup/{claude_code,codex_cli,troubleshooting,first_prompts}.md` into the shared page or keep `first_prompts.md` only.
- `AGENTS.md` line ~6 (drop CLAUDE.md/.gemini sentence), the "On any other harness (OpenCode, Gemini CLI, …)" sentence → Copilot CLI and OpenCode; `llms.txt`, `modes/maintainer.md`, `docs/setup/troubleshooting.md`, `skills/start-new-project.md` references.
- Grep for dangling links (`wiki-currency` checks them); `paper/paper.md` keeps its llms.txt mention.

## Done when

README shorter and linking to the shared page; listed legacy gone; wiki-currency and boundary CI green.
