## science-project-api-gate
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/47 (closed)
- pr: https://github.com/PyAutoLabs/autolens_assistant/pull/48 (merged 65f9598, squash)
- completed: 2026-07-10
- summary: task 2 of the autolens_assistant batch — Create scaffold generates a thin .claude/settings.json wiring the PyAuto* PreToolUse code-gate to the referenced assistant via runtime resolution ($AUTOLENS_ASSISTANT → sibling → sources/ clone; exec of the assistant's validate_pyauto_code.py, which resolves audit_skill_apis.py relative to itself — zero vendoring, no baked paths); DEFAULT-ON + fail-open (user decision); generated AGENTS.md gains Code gate section w/ cross-tool caveat (hooks Claude Code-only; others self-enforce --code/--file). Validated: deny via env-var + sibling resolution, allow valid symbol, silent fail-open absent assistant; NOTE hook test payloads need "tool_name":"Bash" or the hook allows unconditionally.
- followups: batch continues — per_project_literature (core hybrid) next

## Original prompt

# The assistant protects generated code with a PreToolUse hook that

Type: feature
Target: autolens_assistant
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

The assistant protects generated code with a PreToolUse hook that blocks PyAuto* symbols
written from memory that don't exist in the installed stack — @autolens_assistant/.claude/hooks/validate_pyauto_code.py,
backed by @autolens_assistant/autoassistant/audit_skill_apis.py and wired in
@autolens_assistant/.claude/settings.json.

A spun-off science project (created by @autolens_assistant/skills/start-new-project.md) refers
back to the assistant and deliberately does **not** copy `autoassistant/` or the rest of the
copilot machinery. But a user will still generate and run PyAutoLens code inside the project,
so the project should get the same API code-gate.

Decision + implementation (lean: do it via refer-back, don't copy `autoassistant/`):

- `start-new-project` generates a thin `.claude/settings.json` in the project that wires the
  PreToolUse code-gate to the **referenced** assistant's `audit_skill_apis.py`, resolved
  through the same assistant-ref mechanism the project already uses (see
  `science_project_assistant_ref.md`). The validator stays in one place (the assistant);
  the project just points its hook at it.
- The hook command must resolve the assistant path at runtime (env var -> sibling ->
  cloned `sources/autolens_assistant/`), not bake in an absolute path.
- Cross-tool caveat: only Claude Code runs `.claude/` hooks. Codex/Gemini in the project rely
  on the prose "ground against the live API, don't guess" rule inherited from the assistant's
  `AGENTS.md` via refer-back — state this in the generated project docs so it isn't a silent gap.

Decide whether the gate is on by default in generated projects or opt-in during setup.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
