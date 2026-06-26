The refer-back model (see @autolens_assistant/skills/start-new-project.md) means a spun-off
science project is reproducible **standalone**: `config/`, `scripts/`, `data/` and `results/`
are copied into the project, so cloning it is enough to re-run the analysis. The AI copilot is
the only thing that lives elsewhere, and a collaborator who wants it triggers clone-on-demand
of the assistant via the project's thin `AGENTS.md`.

This is mostly resolved by the model; it just needs to be made obvious to a collaborator who
clones only the project repo.

What to implement:

- Add one clear line to the generated project's `README` template stating: this repo runs
  standalone for reproducing the analysis (env via `activate.sh`, code in `scripts/`,
  provenance in `results/manifests/`); to drive it with the PyAutoLens AI assistant, point
  `AUTOLENS_ASSISTANT` at a local `autolens_assistant` clone (or let the agent clone it on
  demand) — see `AGENTS.md`.
- Keep it to a sentence or two; the detail already lives in the thin `AGENTS.md`.

Small task — depends on the assistant-ref env var name being settled
(`science_project_assistant_ref.md`).
