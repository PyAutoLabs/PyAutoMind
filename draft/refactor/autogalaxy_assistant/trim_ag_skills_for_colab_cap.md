# Trim autogalaxy_assistant skills toward their autolens size

Type: refactor
Target: autogalaxy_assistant
Repos:
- autogalaxy_assistant
Difficulty: medium
Autonomy: supervised
Priority: low
Filed: 2026-10-26
Status: formalised
Consequence: judge

@autogalaxy_assistant

## Request (human, 2026-10-26)

Chose a per-assistant Colab cap for autogalaxy ("Per-assistant cap (Recommended)") with the follow-up to
trim the ag skills, after which the cap can drop back.

## Context

- PyAutoHands#324 phase 2: every mappable `ag_*` skill is 21–32k chars (e.g. `ag_build_imaging_model`
  23.5k vs `al_build_imaging_model` 8.3k, `af_compose_model` 5.8k), so autogalaxy's
  `colab/contexts.yaml` runs at `cap: 36000` with one skill per notebook while lens/fit use 20k with 1–2.
- Larger skills also cost every Claude Code / Codex session that loads them.

## Done when

- `ag_*` skills trimmed (de-duplicate shared preamble, move long examples to wiki/core references) with
  no loss of safety invariants or API grounding (`ag_audit_skill_apis` clean);
  `colab/contexts.yaml` `cap:` lowered to 20000 (or removed) with 1–2 skills per entry and the
  `python -m autoassistant.colab_contexts check` green.
