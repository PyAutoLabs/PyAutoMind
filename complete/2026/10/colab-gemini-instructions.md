## What shipped (2026-10-26)

Colab's Gemini sidebar cannot read a repository, but Colab stores per-notebook Gemini instructions in notebook metadata (`metadata.colab.aiContexts` + `selectedAiContext`; key recovered from Google's Learn Mode example notebooks, undocumented). Every PyAuto workspace and HowTo notebook now carries its folder's assistant skills plus that assistant's safety rules as the active Gemini instruction, so a Colab user gets the assistant's knowledge with zero setup.

- **PyAutoHands** (#325, #326): `build_util` assembles preface + rules + mapped skill text from each assistant's `colab/contexts.yaml` and stamps every generated notebook (deterministic uuid5 id per project, idempotent, metadata-only, validated before the `notebooks/` rmtree); `autohands gemini_context {apply,report}`; release.yml checks out the matching assistant for autolens_workspace, HowToLens, autofit_workspace, HowToFit, autogalaxy_workspace, HowToGalaxy; per-assistant `cap:` (default 20,000, ceiling 50,000). Repo names live in `autohands/config/workspaces.yaml` `colab_gemini:` (tenant firewall).
- **Assistants**: `colab/contexts.yaml` (folder glob → skills, first match wins, never_map) + `autoassistant/colab_contexts.py` check/apply + CI `colab-contexts.yml` in autolens (#165), autofit (#59), autogalaxy (#39, cap 36000), autocti (#39); upkeep skill `{al,af,ag,ac}_refresh_colab_contexts` (#166, #60, #40, #39): check + Hands coverage report, AI scan, minimal mapping edits, PR.
- **autocti_workspace** (#38): 79 notebooks stamped once with `apply` (CTI is outside the Hands release generate) + README re-apply note.
- **PyAutoBrain** (#541): clone boundary classifies assistant `colab/*` as mixed.
- autolens_assistant COSMOS-Web Ring notebook stamped (live now); generated workspace notebooks pick it up at the next release.

## Human-verified in Colab (2026-10-26)

Hand-written metadata honoured on upload ("zebra" probe); 18.7k- and 52.4k-char contexts honoured; GitHub-URL route (cosmos notebook from the PR branch) honoured.

## Decisions and learnings

- Skills stay single-sourced in the assistants; notebooks carry a release-time snapshot. Users see only a named, toggleable instruction in the Gemini chat box.
- 20k default cap (human); autogalaxy at 36k because ag_* skills are 21–32k each (~3× their autolens twins) — trim follow-up `draft/refactor/autogalaxy_assistant/trim_ag_skills_for_colab_cap.md`.
- Merge order rule: an assistant's mapping must be on main before Hands enables `assistant:` for its workspace in release.yml.
- Hands organ code may not name satellite repos/owners (tenant-firewall CI leg) — config only.
- Agent `gh pr merge` is classifier-blocked: the human merged every PR; GitHub 504s split two merge chains (re-check each PR).
- Heart RED throughout (release integrate / workspace smoke / drift, unrelated): human development overrides per phase, recorded in the four sinks; `--auto` was requested for phases 3+4 but parks on RED, so they ran supervised.
- Broca: the Hands `report` is the upkeep evidence; Broca ingestion stays in `draft/feature/pyautobroca/broca_communication_pilot.md`.

## Follow-ups (not shipped)

- Full CTI-on-Colab (setup cell, arctic install, Nerves `_PROJECTS`, release matrix).
- autocti_assistant AGENTS.md real-data invariant: lensing wording + dead link `skills/ac_prepare_imaging_data.md`; autocti_workspace AGENTS.md says notebooks regenerate at release (they don't).
- autofit_assistant clone profile misses `AI_OPTIONS.md` (pre-existing).
- AI_OPTIONS.md "Colab notebooks and the assistant" paragraph after the next release.

## Original prompt

# Carry assistant context into every Colab notebook via Gemini Custom Instructions

Type: docs
Target: pyautohands
Repos:
- PyAutoHands
- autolens_assistant
- autofit_assistant
- autogalaxy_assistant
- autocti_assistant
- autocti_workspace
Difficulty: medium
Autonomy: supervised
Priority: medium
Filed: 2026-10-23
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/324
Status: formalised
Blocked-by: none (upload + size gates passed 2026-10-26; GitHub-route gate verified on the PR branch)
Consequence: glance

@pyautohands @autolens_assistant @autogalaxy_assistant @autofit_assistant @autocti_assistant

## Request (human, 2026-10-23)

> i dont expect the assistant link to be agentic but if it can leverage the assistant repo to make the AI better thats the goal. [...] I am open to all workspace notebooks doing it if its easy to implement and worth it.

## Context

- Colab's Gemini sidebar cannot read a repository. Today only two notebooks leverage the assistant: autofit's experimental Colab notebook clones the assistant at a pinned tag and prints an AGENTS.md excerpt + modes + eight skills for the user to paste into the sidebar (retired by #87); autolens's COSMOS-Web Ring notebook only adds "Ask Gemini:" questions. None of the ~600 generated workspace/HowTo notebooks mention the assistant.
- Colab added per-notebook **Custom Instructions** on 2026-04-08: "stored directly within your notebook", "when you share your notebook ... those instructions travel with it" (https://blog.google/innovation-and-ai/technology/developers-tools/colab-updates/). The `.ipynb` metadata key is undocumented.
- Every generated notebook already passes through `PyAutoHands/autohands/build_util.py::inject_colab_setup`, so a metadata write there covers all workspaces and HowTo repos at the next release.

## Finding (2026-10-26): metadata key recovered without the UI

Human's first Colab attempt found no "Custom Instructions" input. Google's own Learn Mode
example notebooks (linked from the colab-updates blog post; Drive ids
1Tes-C6WNL99HKx4Ghg9ckGYSWRLxn-CA and 1Y39sN0zqWvFDY3o6EPu1J0BcTiqPUhp4) carry the key:

```json
"metadata": {"colab": {
  "selectedAiContext": "<uuid>",            // or the built-in "learn_mode"
  "aiContexts": {"<uuid>": {"id": "<uuid>", "name": "Pirate Mode", "context": "Talk like a pirate"}}
}}
```

So `inject_colab_setup` can write the instructions directly; the UI is not needed to author them.
The gate is now: does Colab apply a hand-written `aiContexts` entry (a) on File > Upload and
(b) via a GitHub badge? Test notebook built in session scratch (colab_ci_test.ipynb, "zebra" probe).
The UI control is a toggle/selector in the Gemini chat box, not a settings page.

**Gate (a) PASSED 2026-10-26** (human): uploaded colab_ci_test.ipynb, Gemini replied with "zebra" —
Colab honours a hand-written `aiContexts` entry. Remaining: (b) GitHub-badge route.

## Gate (human, ~5 min)

1. Open any notebook in Colab, add a Custom Instruction (e.g. `PYAUTO_TEST please mention the word zebra in every reply`), save to the notebook, confirm a reply says zebra.
2. Download the .ipynb; run `python3 -I <scratch>/colab_diff.py <downloaded> <original>` to find the metadata key and size.
3. Push a copy to a scratch branch and open it via a Colab badge; confirm the instruction still applies (GitHub route).
4. Optional: after the setup cell runs, ask Gemini whether it can see a file in the cloned workspace.

**Size gate PASSED 2026-10-26** (human): 2,254-word (18.7k chars) and 6,349-word (52.4k chars) contexts
both honoured, end-of-text probe word returned → Colab accepts large instructions.

## Scope (human-approved 2026-10-26, supersedes the short-block plan)

- **Skills stay in the assistants** (single source). Generated `.ipynb` metadata carries a release-time
  snapshot; workspace `.py` scripts and skill files are untouched.
- Each assistant owns `colab/contexts.yaml`: workspace/HowTo path glob → ordered skill list (most specific
  wins, default entry), plus a Colab preface ("written for a coding agent with the repo; in Colab ignore
  repo-file/hook/terminal steps") and the core rules (stay with the notebook's API, real-data gate for
  lens/galaxy, never claim code ran, one focused question, point to the assistant for heavy work).
  The assistant's CI checks every mapped skill exists.
- Hands `build_util` assembles preface + rules + mapped skills and writes `metadata.colab.aiContexts` /
  `selectedAiContext` (deterministic uuid5 per project, idempotent), for every generated notebook incl.
  prose-only ones. **Cap 20k chars per notebook** (human choice): over-cap fails generation naming the
  mapping entry — never truncates. Missing assistant mapping fails loudly.
- `release.yml` generate job adds a read-only checkout of the matching assistant; local `generate.py`
  resolves it via Brain's repo-path resolver or an explicit argument/env var.
- autolens_assistant `docs/colab/cosmos_web_ring_colab.ipynb` gets the cosmos greeting skill the same way
  (build step + metadata-only patch of the committed notebook, no re-execution).
- Human 2026-10-26: "done across PyAutoLens, galaxy, fit and CTI". CTI is outside the Hands release
  generate (not in COLAB_PROJECTS / Nerves _PROJECTS, no setup cell), so Hands also exposes the injector as a
  standalone CLI over any notebooks tree; CTI's 79 notebooks get it via an autocti_workspace PR. Full
  CTI-on-Colab (setup cell, arctic install, release matrix) = separate follow-up.
- Phase 1: Hands + autolens_assistant (gate (b) = human opens the cosmos notebook via a Colab GitHub URL
  on the PR branch). Phase 2: autogalaxy_assistant + autofit_assistant mappings.
  Phase 3: autocti_assistant mapping + autocti_workspace notebooks via the Hands CLI.
  Phase 4 (human 2026-10-26: "skill building assistant maintenance ... tools or features which link
  assistant skills to workspace ... routinely ... refresh and AI scan"): a maintainer skill in each
  assistant (`al_/ag_/af_/ac_refresh_colab_contexts`) that AI-scans the workspace folder tree against
  the skill catalogue, proposes `colab/contexts.yaml` updates when skills or folders change, and opens a
  PR; plus a deterministic coverage report (folders with only the default match, dead skill refs,
  per-notebook size vs cap) the skill and Broca both read. Broca records linkage freshness as upkeep
  evidence (see draft/feature/pyautobroca/broca_communication_pilot.md) — Broca never runs the scan.
- Merge: human /prm (declared glance overridden by the human-gate need). Heart RED: human dev-only
  override 2026-10-26.
- Follow-up after release: AI_OPTIONS.md "Colab notebooks and the assistant" paragraph.

## Done when

- Regenerated notebooks carry folder-matched assistant skills (≤20k chars) as active Gemini instructions;
  the cosmos notebook opened via a GitHub Colab URL yields a Gemini that follows them; phase 2 mappings
  merged for galaxy and fit; phase 3 CTI notebooks carry autocti_assistant skills.
