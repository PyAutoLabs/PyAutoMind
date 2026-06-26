A science project created by `start-new-project` is a separate, self-contained repo that
**refers back** to the `autolens_assistant` copilot for its `skills/` and `wiki/` rather than
vendoring a copy. The model is already locked and partly implemented in
@autolens_assistant/skills/start-new-project.md (see the "Locating the assistant from a
project" section and the Create scaffold). This task finishes the resolution + provenance
mechanics — it is implementation detail, not a fresh decision.

What to implement:

- **Resolution order** when the copilot is invoked inside a project: an environment variable
  pointing at a local assistant clone -> a sibling directory (`../autolens_assistant`) ->
  clone-on-demand of the recorded URL into a gitignored path (`sources/autolens_assistant/`),
  mirroring the source-of-truth `sources/` clone pattern in @autolens_assistant/AGENTS.md.
- **Pick the env var name** (proposed: `AUTOLENS_ASSISTANT`) and document it in the thin
  `AGENTS.md` that `start-new-project` generates for each project.
- **Provenance pin (record, not enforced checkout).** The project records the assistant repo
  URL + commit in `project.yaml` (`assistant_ref`), and every run manifest already records
  `assistant: {repo, commit}`. Day-to-day operation uses the resolved current clone; the
  manifest captures what was actually used.
- **Mismatch warning (non-blocking).** If the resolved assistant clone's commit differs from
  `project.yaml`'s `assistant_ref.commit`, warn the user about provenance drift and offer to
  re-pin; never hard-block or force a checkout.

Touches the generated scaffold + thin `AGENTS.md` produced by
@autolens_assistant/skills/start-new-project.md. No change to the assistant's own constitution
beyond what the source-of-truth section already establishes.
