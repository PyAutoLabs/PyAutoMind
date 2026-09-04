## human-readable-first-docs
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/120
- completed: 2026-09-04
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/723
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/606
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/529
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/233
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/121
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/22
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/723
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/606
- summary: Swapped every user-facing doc (PyAutoLens / PyAutoGalaxy README + docs/, autolens_workspace / autogalaxy_workspace README + `start_here.py` with regenerated notebook and markdown twins) back to human-readable docs first and the AI Assistant second, text unchanged, plus a bold note under each assistant section that only paid AI coding agents (Claude Code, Codex) are supported and free/conversation agents are in progress.
- summary: Reworked both assistant READMEs: "Choosing Your AI Tool" trimmed to the coding-vs-conversation distinction with only paid coding agents supported (OpenCode and the free-tools section mentioned); "AI Chat Assistant" section removed; `CHOOSING_YOUR_AI_TOOL.md` moved to `docs/archive/` with relative links repaired; all Antigravity references removed (its CLI setup page deleted, inbound links repointed to OpenCode); new `## Conversation Assistants` (links the experimental custom GPT with a performance warning) and `## Free AI tools` (OpenCode named, encouraging preliminary results, no first-class support) sections after "How does … actually work?".
- summary: Backups for later reinstatement live in each assistant repo under `docs/archive/` (Choosing Your AI Tool section, AI Chat Assistant section, the moved guide).
- witness: `grep -ril antigravity autolens_assistant/README.md autogalaxy_assistant/README.md` returns nothing; in every touched README the human-readable docs section precedes the AI Assistant section.
- ci: all six PRs green on every run and leg (PyAutoLens/PyAutoGalaxy docs + unittest 3.12/3.13/nojax; workspaces navigator + smoke 3.12/3.13 + size-guard; assistants clone-boundary + wiki-currency). autolens_assistant's chat-bundle check fails identically on main — pre-existing API-surface staleness, unrelated.
- heart: RED at ship (2026-09-03) and merge (2026-09-04) for "release validation FAILED (stage integrate)" and "PyAutoArray: open PR 12d old" — both unrelated to this docs-only change; PR-open under a recorded ack, merge authorised by the human on 2026-09-04 (same reason set acknowledged for gaussian-precompute-p3 on 2026-09-03).
- residue: the pre-existing assistant sentences that still say ChatGPT is supported sit directly above the new bold note saying it is not (left verbatim by request). The bridge sentence "The rest of this guide is human-readable documentation…" was dropped from both `start_here.py` since the assistant block now closes the tutorial. autogalaxy_assistant's Supported Coding Agents table now marks Gemini CLI and OpenCode "Not first-class supported". Regenerated `markdown/start_here.md` pages were a month stale and picked up unrelated script drift (full render, noted in the workspace PR bodies).
- traps: the canonical PyAutoLens and autolens_workspace mains each carry an uncommitted README.md line-rewrap from another session, so `git pull --ff-only` aborted there ("Aborting … M README.md"); left un-pulled and untouched — pull once that rewrap is committed or discarded.
- traps: the Agent-tool delegation of this close-out was blocked by the auto-mode classifier (bundled merge/close-out prompt), so the close-out ran in-session.
- parallel-claim: autolens_workspace was also claimed by gaussian-precompute-p3 (#530, merged first on 2026-09-04); file sets were disjoint and #529 merged CLEAN with no rebase needed.

## Original prompt

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
