# Swap docs back to human-readable-first; assistant README rework (paid coding agents only)

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
Issued: 2026-09-03
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/120
Consequence: glance
Witness: `grep -ril antigravity autolens_assistant/README.md autogalaxy_assistant/README.md` returns nothing, and in every touched README the human-readable docs section precedes the AI Assistant section.
Review-minutes: 3
Unattended: ready

# Swap docs back to human-readable-first; assistant README rework (paid coding agents only)

Type: docs
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: high
Witness: `grep -ril antigravity autolens_assistant/README.md autogalaxy_assistant/README.md` returns nothing, and in every touched README the human-readable docs section precedes the AI Assistant section.

We fairly recently swapped all docs (E.g. README.md, workspace, readthedocs) to point users to the PyAutoLens / PyAutoGalaxy
AI assistant first and human readable docs second.

I want us to swap them back. Do not change the text or description for each, just swap the order so human readable is
first.

Also in the sections ### PyAutoLens AI Assistant (or wherever the text on the AI Assistant is) state in bold font in a
sentence under the existing text:
"The PyAutoLens AI Assistant currently only supports AI coding agents which require a paid subscription, either Claude code or codex.
Work is on going to support free AI coding agents and conversation agents like ChatGPT".

In the autolens_assistant (and autogalaxy_assistant) README.md file can you:

- Backup the text on ### Choosing Your AI Tool so that I can reuse it once we get conversation assistants back.
- Remove the text in ### Choosing Your AI Tool, keep the text which explains the difference between a coding agent and conversation agent (but then say only coding agents are supported) and make it clear up front on paid for subscription AI coding agents, claude or codex, work (but mention open code and the free AI agent section at the bottom of the README).
- Backup all text in #### AI Chat Assistant for when I fix support.
- Remove this text, `autolens_assistant` has first-class support for AI coding agents such as **Claude Code**, **Codex**,
**Antigravity** and **OpenCode**. The [setup guide](CHOOSING_YOUR_AI_TOOL.md) covers each one, including which is
currently the best free option., and dont link to CHOOSING_YOUR_AI_TOOL.md (and back up and move somewhere out the way) as for now we support two simple choices.
- Remove all reference throughout to antigravity, it sucks.
- After the section ## How does PyAutoLens-Assistant actually work?, add a section ## Conversation Assistants explaining we are working on getting these to work
and link to the GPT prototype but warn its not got great performance
- Add a section ## Free AI tools saying we are actively testing free AI tools but cannot provide first class support for any,
however mention opencode here and say preliminary testing shows encouraging results.

Repos touched: PyAutoLens, PyAutoGalaxy (README + docs/), autolens_workspace, autogalaxy_workspace, autolens_assistant, autogalaxy_assistant.

<!-- formalised by the Intake (Conception) Agent on 2026-09-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4f224c80-877b-46c3-b605-137e7eb2e2b1/scratchpad/intake_raw.md -->
