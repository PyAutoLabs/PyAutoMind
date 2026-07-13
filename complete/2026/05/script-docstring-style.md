## script-docstring-style
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/6
- completed: 2026-05-28
- library-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/7
- repos: autolens_assistant
- notes: Documented the PyAutoLens workspace script style (title + __Contents__ header, """__Section__""" narrative docstrings, source citations woven into prose) as the standard for all assistant-generated code — in CLAUDE.md "Conventions" + skills/_style.md; converted scripts/template.py and skills/al_chain_searches.md as exemplars. Follow-up queued at autolens_assistant/script_to_notebook.md (script→notebook converter). Shipped a follow-on cleanup PR #8 stripping personal content (work scratch scripts, filled profile.md, SLACS personal metadata) and genericizing personal identifiers (activate.sh→pip venv, HPC mail-user/host/path placeholders) to make autolens_assistant a generic template; demo datasets kept.
