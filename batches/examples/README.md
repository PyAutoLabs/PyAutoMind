# Shift brief examples

Validator fixtures for `bin/pyauto-brain batch brief --check`
(autonomous-orchestrators phase 2). **Nothing here is a batch record**: none of
it was dispatched, and `scripts/lifecycle.py` reads only `batches/*.md`, never
this folder. The schema they follow is `../AGENTS.md`, "Shift brief
(2026-11-03)". The named task paths are placeholders, so `--check` warns that
they resolve to no prompt; that warning is expected.
