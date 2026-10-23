# Carry assistant context into every Colab notebook via Gemini Custom Instructions

Type: docs
Target: pyautohands
Repos:
- PyAutoHands
- autolens_assistant
- autofit_assistant
Difficulty: small
Autonomy: supervised
Priority: medium
Filed: 2026-10-23
Status: draft (blocked on a human Colab test)
Consequence: glance

@pyautohands @autolens_assistant @autofit_assistant

## Request (human, 2026-10-23)

> i dont expect the assistant link to be agentic but if it can leverage the assistant repo to make the AI better thats the goal. [...] I am open to all workspace notebooks doing it if its easy to implement and worth it.

## Context

- Colab's Gemini sidebar cannot read a repository. Today only two notebooks leverage the assistant: autofit's experimental Colab notebook clones the assistant at a pinned tag and prints an AGENTS.md excerpt + modes + eight skills for the user to paste into the sidebar (retired by #87); autolens's COSMOS-Web Ring notebook only adds "Ask Gemini:" questions. None of the ~600 generated workspace/HowTo notebooks mention the assistant.
- Colab added per-notebook **Custom Instructions** on 2026-04-08: "stored directly within your notebook", "when you share your notebook ... those instructions travel with it" (https://blog.google/innovation-and-ai/technology/developers-tools/colab-updates/). The `.ipynb` metadata key is undocumented.
- Every generated notebook already passes through `PyAutoHands/autohands/build_util.py::inject_colab_setup`, so a metadata write there covers all workspaces and HowTo repos at the next release.

## Gate (human, ~5 min)

1. Open any notebook in Colab, add a Custom Instruction (e.g. `PYAUTO_TEST please mention the word zebra in every reply`), save to the notebook, confirm a reply says zebra.
2. Download the .ipynb; run `python3 -I <scratch>/colab_diff.py <downloaded> <original>` to find the metadata key and size.
3. Push a copy to a scratch branch and open it via a Colab badge; confirm the instruction still applies (GitHub route).
4. Optional: after the setup cell runs, ask Gemini whether it can see a file in the cloned workspace.

## Scope (if the gate passes)

- `inject_colab_setup` writes the Custom Instructions metadata with a short per-project block: what the assistant is + repo URL, the safety invariants in a few lines, "the reader is in notebook <path> of <project>; explain and help adapt it; do not claim to have run code". No skills embedded.
- The block text lives in PyAutoNerves or Hands beside `COLAB_SETUP_MARKDOWN`, one per project in `COLAB_PROJECTS`.
- autolens_assistant `docs/colab/cosmos_web_ring_colab.ipynb` gets the same metadata (hand-written notebook, not generated).
- Fallback if the key is private or stripped on the GitHub route: a generated markdown cell with the same block and a "paste this into Gemini" line.

## Done when

- Regenerated notebooks carry the instructions; opening one via a README badge yields a Gemini that knows the assistant; AI_OPTIONS.md "Colab notebooks and the assistant" paragraph updated to say so.
