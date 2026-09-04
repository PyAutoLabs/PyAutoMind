# Docs follow-up to human-readable-first-docs (#120): drop "also", reinstate paid-plan conversation-assistant framing

Type: docs
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autogalaxy_assistant
- autogalaxy_workspace
- PyAutoLens
- autolens_assistant
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-09-04
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/122
Consequence: glance
Witness: `grep -rn "also useful for new starters"` over the six repos returns nothing; `grep -n "not currently supported\|Only CLI coding agents" autolens_assistant/README.md autogalaxy_assistant/README.md` returns nothing; the new bold note text appears in every file that carried the old one.
Review-minutes: 3
Unattended: ready

# Docs follow-up to human-readable-first-docs (#120): drop "also", reinstate paid-plan conversation-assistant framing

Type: docs
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: high

Follow-up to the merged task human-readable-first-docs (autolens_assistant#120, record complete/2026/09/human-readable-first-docs.md). Three approved changes, one task across six repos: PyAutoLens, PyAutoGalaxy, autolens_workspace, autogalaxy_workspace, autolens_assistant, autogalaxy_assistant.

Original user request (verbatim):
"We dont need "also" here now, are also useful for new starters. Can you also show me the autolens_assistant README.md in particular its conversation assistant section, I think we DO support conversation assistants but both required pair for features: ChatGPT Work needs a full GitHub sync via the GitHub app and Claude Code / Chat needs paid for GitHub integration features."
Then, on the proposed three-part follow-up: "1. yes, make sure oyu sweep workspace and repos 2. yes, do that, 3yes"

1. Drop "also" from the sentence "The following human-readable documentation and examples are also useful for new starters:" → "The following human-readable documentation and examples are useful for new starters:". Sweep every occurrence in all six repos (known: PyAutoLens README.md + docs/index.md, PyAutoGalaxy README.md + docs/index.md, autolens_workspace README.md, autogalaxy_workspace README.md; grep the docs/overview pages and start_here.py / .ipynb / markdown twins too).

2. Reword the "### Choosing Your AI Tool" and "## Conversation Assistants" sections in autolens_assistant/README.md and autogalaxy_assistant/README.md to the accurate paid-plan framing: conversation assistants ARE supported on paid plans — ChatGPT (Plus/Pro/Team) via its GitHub connector / GitHub sync (docs/setup/chatgpt_paid_connector.md), Claude chat (Pro/Max/Team) via Project knowledge (docs/setup/claude_chat_paid.md; its GitHub connector is currently bugged, per that page — do not claim Claude needs a paid GitHub integration). Free routes stay as degraded fallbacks: Claude chat free (claude_chat_free.md), the experimental custom GPT (chatgpt_custom_gpt.md, keep the performance warning). Coding agents unchanged: Claude Code and Codex paid, OpenCode free with encouraging preliminary results and no first-class support (keep the ## Free AI tools section). Link the existing setup pages; reinstate material from docs/archive/ where it is already accurate rather than writing fresh (the archived tables in docs/archive/CHOOSING_YOUR_AI_TOOL.md and README_choosing_your_ai_tool_section.md). Remove the "not currently supported" / "Only CLI coding agents are currently supported" claims. Also fix the assistant sentence in library/workspace docs that lists "conversation agents such as ChatGPT and coding agents such as Claude Code and Codex" only if it now contradicts the note — it should not after step 3.

3. Reword the bold note (currently "**The PyAutoLens AI Assistant currently only supports AI coding agents which require a paid subscription, either Claude Code or Codex. Work is ongoing to support free AI coding agents and conversation agents like ChatGPT.**", and the PyAutoGalaxy equivalent) everywhere it appears — PyAutoLens/PyAutoGalaxy README.md, docs/index.md, docs/overview/overview_1_start_here.md, docs/overview/overview_2_new_user_guide.md; autolens_workspace/autogalaxy_workspace README.md, start_here.py, start_here.ipynb, markdown/start_here.md (regenerate the notebook/markdown twins from the .py per each workspace's convention rather than hand-editing) — to: "**The PyAutoLens AI Assistant currently requires a paid subscription: Claude Code or Codex as a coding agent, or ChatGPT or Claude on a paid plan as a conversation assistant. Free options are being tested.**" (PyAutoGalaxy wording with its own name).

Witness: `grep -rn "also useful for new starters"` over the six repos returns nothing; `grep -n "not currently supported\|Only CLI coding agents" autolens_assistant/README.md autogalaxy_assistant/README.md` returns nothing; the new bold note text appears in every file that carried the old one.

Notes: docs-only, no code. Heart RED reasons unrelated (same set as #120). Library PRs merge first then workspace/assistant PRs; repos independent otherwise. Model split: Fable plans, Opus executes.

<!-- formalised by the Intake (Conception) Agent on 2026-09-04 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/14bf5d2e-d006-4552-abce-b9cf6fdff58f/scratchpad/intake_raw.md -->
