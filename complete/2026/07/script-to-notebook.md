## script-to-notebook
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/51 (closed)
- pr: https://github.com/PyAutoLabs/autolens_assistant/pull/52 (merged b4e73f7, squash)
- completed: 2026-07-10
- summary: task 4 of the autolens_assistant batch — stdlib-only autoassistant/to_notebook.py (adapts PyAutoBuild py_to_notebook/add_notebook_quotes, cited; no ipynb-py-convert dep) + al_to_notebook skill + README/symlink + 2 unit tests (suite 16 pass). E2E vs pipeline on start_here.py: 25/26 byte-identical; 26th = PIPELINE artifact (back-to-back docstrings -> code cell w/ literal '# %%' markers, live in the published start_here.ipynb) — filed bug/pyautobuild/back_to_back_docstrings_notebook.md.
- followups: PyAutoBuild artifact prompt queued; batch continues — live_visual_update_context next

## Original prompt

# Now that `autolens_assistant` generates scripts in the PyAutoLens narrative-docstring

Type: feature
Target: autolens_assistant
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Now that `autolens_assistant` generates scripts in the PyAutoLens narrative-docstring
style (title + `__Contents__` header, per-section `"""__Section__"""` docstrings — see
issue PyAutoLabs/autolens_assistant#6), we should add a **script -> notebook converter**
to the assistant.

The style was adopted precisely because it makes conversion mechanical:

- Each top-level `"""..."""` docstring block becomes a **markdown cell** (the title block,
  the `__Contents__` list, and every `__Section__` narrative).
- The Python code *between* docstring blocks becomes a **code cell**.

This mirrors how `autolens_workspace` converts its `start_here.py` scripts to the matching
`start_here.ipynb` notebooks. Look at how the workspace already does this before writing
anything new — there is very likely an existing converter in `autolens_workspace` (or its
build tooling) we can reuse or adapt rather than re-implement (@autolens_workspace).

What I want:

- A converter (a `work/`-style tool or a small module) that takes a generated `.py` in the
  narrative-docstring style and emits a `.ipynb` with the cell split above.
- A skill (e.g. `al_to_notebook.md`) wrapping it, so a user can say "turn this into a
  notebook" after the assistant produces a script.
- End-to-end verification on a real generated script (e.g. an imaging start-here style
  script the assistant produces).

Cite the workspace converter as the reference if one exists; only build from scratch if it
genuinely doesn't.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
