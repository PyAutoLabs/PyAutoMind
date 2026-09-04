## docs-followup-paid-plan-assistants
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/122
- completed: 2026-09-04
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/725
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/607
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/531
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/234
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/123
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/23
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/725
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/607
- follow-up-to: human-readable-first-docs (complete/2026/09/human-readable-first-docs.md, #120)
- summary: Dropped the redundant "also" from "The following human-readable documentation and examples are useful for new starters:" in the README and docs index of PyAutoLens, PyAutoGalaxy, autolens_workspace and autogalaxy_workspace (six occurrences; it never appeared in the start_here scripts).
- summary: Reworded the bold AI Assistant note in all 16 files that carried it (library README + docs/index + two overview pages; workspace README + start_here.py/.ipynb/markdown) to "…currently requires a paid subscription: Claude Code or Codex as a coding agent, or ChatGPT or Claude on a paid plan as a conversation assistant. Free options are being tested." The paragraph above it, which lists ChatGPT and the coding agents, is unchanged and now consistent.
- summary: Assistant READMEs: "Choosing Your AI Tool" now says both AI-tool kinds are supported and both need a paid plan (Claude Code / Codex recommended; ChatGPT and Claude chat on paid plans via their GitHub connectors), with a separate bolded "Free options are being tested" paragraph; "Conversation Assistants" reinstates the archived routes table (ChatGPT paid via GitHub sync, Claude paid via its GitHub connector, Claude free via Project + knowledge pack with the free-connector caveat, the experimental custom GPT with its warning, paste-the-bundle) — the "not currently supported" claims are gone. autolens_assistant's claude_chat_paid.md is reframed around the GitHub connector (mirrors chatgpt_paid_connector.md), claude_chat_free.md / troubleshooting.md now describe the Free tier's connector as lacking features rather than an "open bug", and llms.txt's connector row reads "ChatGPT or Claude on a paid plan".
- decision: maintainer-verified 2026-09-04 that the paid-plan Claude GitHub connector works excellently and the Free tier's connector is missing features that hurt performance; the earlier "open connector bug" (claude-code#71542, Free-account repro 2026-08-06) is recorded as a free-tier limitation.
- witness: `grep -rn "also useful for new starters"` over the six repos returns nothing; `grep -n "not currently supported\|Only CLI coding agents"` over both assistant READMEs returns nothing; the new bold note is in all 16 files that carried the old one.
- ci: all six PRs green on every run (library Docs + Tests; workspace Navigator + Smoke + Size Guard; assistant clone-boundary + wiki-currency), all CLEAN at merge; no freeze.
- heart: RED at ship and merge (2026-09-04) for "release validation FAILED (stage integrate)" and "PyAutoArray: open PR 12d old" — both unrelated to this docs-only change; PR-open under a recorded ack, merge authorised by the human typing /prm.
- notes: workspace start_here.ipynb regenerated via the generator's own root-script path (build_util.py_to_notebook + inject_colab_setup), one-line diff each; markdown/start_here.md mirrored by hand because generate_markdown.py executes the scripts and `--only start_here.py` also selects scripts/imaging/start_here.py. autogalaxy_assistant has no docs/setup/, so its README links autolens_assistant's setup guides for step-by-step recipes.
- traps: the Agent-tool delegation of the implementation ran fine, but a bundled merge+close-out delegation is blocked by the auto-mode classifier — run /prm close-outs in-session. The canonical PyAutoLens and autolens_workspace mains still carry another session's uncommitted README.md rewrap, so their ff-pull aborted again (4 and 9 behind); untouched.

## Original prompt

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
