## What shipped (2026-10-23)

One PyAutoLabs-level page, `PyAutoScientist/AI_OPTIONS.md`, now describes every AI route for the science assistants: Claude Code and Codex (recommended, paid), GitHub Copilot CLI and OpenCode (free, documented not benchmarked), troubleshooting, Colab notebooks as the "see the code" route, and Claude.ai / ChatGPT chat with the GitHub connector at the bottom. Every quota is dated October 2026 with sources.

autogalaxy_assistant, autofit_assistant and autocti_assistant READMEs are shorter: one paragraph, the link, the clone snippet and the starting prompt. Each gained an `AI_OPTIONS.md` stub beside `AI_POLICY.md` (same pattern) and lost `.gemini/settings.json`, the chat archives, the OpenCode setup pages and (autofit) the Colab + Gemini notebook and script. `AGENTS.md`, `llms.txt`, `modes/maintainer.md` and `skills/start-new-project.md` no longer mention Gemini CLI or chat support; the "other harness" sentence names Copilot CLI and OpenCode. `llms.txt` itself stays everywhere: it is the agent routing front door, not chat legacy. pyautolabs.github.io's "Ask an AI assistant" card and the three workspace READMEs point at the page.

## Not shipped here (re-filed)

The autolens_assistant leg (README three-step block, Colab badge move, deletion of `docs/setup/opencode_cli.md`, `docs/evaluation/agent_evaluation.md`, `docs/archive/`, `.gemini/settings.json`) was blocked by the cosmos-web-ring-notebook claim (autolens_assistant#161) and is re-filed as `draft/docs/autolens_assistant/ai_options_page_autolens_leg.md`.

## Decisions and learnings

- Gemini CLI's free tier ended 2026-06-18; the `.gemini/settings.json` stubs pointed at a retired product.
- Free pick is two routes, not one (human, 2026-10-23): Copilot CLI (many have it via Education / institutions) and OpenCode (everyone else).
- Heart was YELLOW at ship (manifest drift mismatch; stale PyAutoLens release rehearsal), unrelated to docs; recorded on each PR.
- autogalaxy_assistant#36 went red on `wiki-currency` because PyAutoArray 2026.10.22.1 was released after the assistant's audit baseline was pinned; the 2026.10.23.1 release regen on main fixed it and a re-run went green. Lesson: an assistant docs PR opened across a stack release reads red on version drift until the release's baseline commit lands; re-run, do not re-pin by hand.
- The Colab question (can Colab's Gemini leverage the assistant repo?) is answered by Colab Custom Instructions (2026-04-08, stored in the notebook); follow-up `draft/docs/pyautohands/colab_custom_instructions_assistant_context.md` is gated on a human Colab test.

## Original prompt

# One PyAutoLabs-level "AI options" page for every assistant; simplify the assistant READMEs; retire chat/OpenCode/Gemini legacy

Type: docs
Target: pyautoscientist
Repos:
- PyAutoScientist
- autolens_assistant
- autogalaxy_assistant
- autofit_assistant
- autocti_assistant
- pyautolabs.github.io
Difficulty: medium
Autonomy: supervised
Priority: high
Filed: 2026-10-23
Issued: 2026-10-23
Status: formalised
Consequence: glance

@pyautoscientist @autolens_assistant @autogalaxy_assistant @autofit_assistant @autocti_assistant @pyautolabs.github.io

## Request (verbatim from the human, 2026-10-23)

> I want us to sort out the options recommended for users for the autolens_assistant and other assistants. Currently, we know they work brilliantly for agentic AI subs codex and claude, and the github README.md says such. We mention (hopefully near the end) that they can be used in Claude Chat of ChatGPT with subs, but this does not work well for a free option. [...] The only thing we need is a viable free agentic AI option [...] We should then make a unified page summarising all AI options for each assistant which each assistant links too, but we should prioritize this being simple, so I think 3 AI agents: claude (paid sub), codex (paid sub) and the best free options and then towards the bottom a description of the chat option with claude and chatgpt, making it clear their GitHub sync is very good. Also, in the past we introduce stuff like llms.txt which I think was to have chat support but I think we are retiring that so for each assistant check if there is legacy stuff we can retire. [...] the goal should also be to ensure the github readme is simpler.

Follow-up decisions (same day): "lets make the de facto PyAutoLabs level, as its weird for cti to link to lens"; "use opencode and copilot for free, documenting both, I agree many will have copilot access and many wont. I agree with rest."

## Context (review done 2026-10-23, Fable session)

- All four library assistants (autolens, autogalaxy, autofit, autocti) say "Choose Claude Code or Codex", retired browser-chat routes on 2026-09-10 (archived under `docs/archive/chat/` in autolens + autofit), and call OpenCode an "experimental alternative — compatible, not tested". autogalaxy and autocti link to autolens's `docs/setup/*.md` pages: that cross-link is the thing to remove.
- `llms.txt` is NOT chat legacy: it is the agent routing front door, referenced by each `AGENTS.md` and the wiki. Keep it.
- Every assistant already carries a one-line `AI_POLICY.md` stub pointing at `PyAutoScientist/AI_POLICY.md`. Reuse that pattern for the new page.
- Free landscape 2026-10-23 (sources in the Fable review): Gemini CLI free tier ended 2026-06-18 (replaced by closed-source Antigravity CLI, tiny weekly quota) so the `.gemini/settings.json` stubs point at a dead product; GitHub Copilot CLI is on Copilot Free (unpublished AI-credit allowance, auto model only) and free for verified students; OpenCode's client is free with 13 limited-time free Zen models (vision unclear, billing details may be needed for the key); Codex is listed on ChatGPT Free for "quick tasks" but CLI access on Free is unconfirmed. Claude.ai Free officially includes the GitHub connector (reads file contents only); ChatGPT's GitHub connector is paid-only.
- Colab: no agentic mode. The autolens COSMOS-Web Ring notebook is a no-AI tutorial mirror of the greeting; autofit's "Colab + Gemini" notebook pastes assistant context into the sidebar by hand. A separate follow-up prompt will cover Colab Custom Instructions injection once the human's Colab test is done; this task only retires the autofit experiment and moves the autolens badge out of the getting-started block.

## Scope

1. **New page `PyAutoScientist/AI_OPTIONS.md`** (name negotiable; the one canonical page). Order: (a) Claude Code — paid; (b) Codex — paid; (c) free options: GitHub Copilot CLI (note the Copilot Student plan) and OpenCode (client free, bring-your-own model; name the Zen free models as limited-time, warn that free models often lack vision so figure checks degrade); (d) a short "Chat instead of an agent" section at the bottom: Claude.ai and ChatGPT with the GitHub connector read the assistant repo well for questions, planning and learning, but cannot run code or look at data, so they are for discussion, not fits; note Claude's connector is on Free, ChatGPT's is paid. One sentence that every free tier is "try it, not sustained science". One paragraph that Colab notebooks are the "see the code" route and the assistant the "do it in conversation" route. Keep it short: a reader should pick in under a minute. Move the useful content of autolens's `docs/setup/{claude_code,codex_cli,opencode_cli,troubleshooting}.md` into (or under) this page so every assistant links to one place; starting prompts stay per-assistant.
2. **Each assistant README (four repos)**: replace the per-repo "Choose Claude Code or Codex" paragraph, the "Experimental alternatives" section and the chat-retired text with one short block: "Runs inside an AI coding agent. Claude Code and Codex are recommended; free options and chat use are on the PyAutoLabs AI options page" + link + the three-line clone/`claude`/`codex` snippet + the starting prompt. Add an `AI_OPTIONS.md` stub next to `AI_POLICY.md` mirroring its pattern. Replace cross-links from autogalaxy/autocti into autolens's docs/setup with the new page. autofit: delete the "Experimental: Google Colab + Gemini" section, `notebooks/experimental_colab.ipynb` and `scripts/experimental_colab.py`. autolens: move the Colab badge out of the three-step getting-started block into the "learning PyAutoLens" context (keep the notebook).
3. **Legacy retirement** (all four): delete `docs/setup/opencode_cli.md` (autolens, autofit) once folded into the page; delete `docs/evaluation/agent_evaluation.md` (autolens) or reduce it to the evaluation protocol only; delete `.gemini/settings.json` and the AGENTS.md line that mentions it; after folding the still-true chat facts into the page, delete `docs/archive/` in autolens + autofit (the git history keeps it) and `docs/archive/README_ai_chat_assistant_section.md` in autogalaxy; update `modes/maintainer.md` and `docs/setup/troubleshooting.md` references; update `AGENTS.md` wording "On any other harness (OpenCode, Gemini CLI, ...)" to name Copilot CLI and OpenCode.
4. **pyautolabs.github.io**: point the "Ask an AI assistant" card at the new page.
5. **Workspace READMEs** (autolens/autogalaxy/autofit workspace) carry a copy of the "Claude Code or Codex ... paid access" paragraph: replace with one sentence + link. HowTo* READMEs' "Study with the assistant" blocks stay as they are.

## Out of scope

- Colab Custom Instructions injection into generated notebooks (follow-up prompt after the human's Colab test).
- euclid_assistant (no AI-option story).
- Validating Copilot CLI or OpenCode against the assistant benchmarks; the page says they are supported routes, documented not benchmarked.

## Done when

- One page, four READMEs each shorter than today and linking to it, no assistant links into another assistant's docs, listed legacy removed, site card updated, PRs open (library-first does not apply; all repos are docs).
