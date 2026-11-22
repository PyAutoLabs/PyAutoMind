# One reader for repos.yaml instead of about ten

Type: refactor
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: notify
Witness: for the real `repos.yaml` and for fixtures with quoted values, trailing comments and a block ended by a new top-level key, every replaced reader returns the same value before and after; `tests/test_repo_paths.py`, `tests/test_public_names.py`, `tests/test_hygiene_conductor.py`, `tests/test_grouped_organ_consumers.py` and `tests/test_docs_conductor.py` pass.
Review-minutes: 0
Unattended: ready
Lane: any

One reader for repos.yaml instead of about ten

Type: refactor
Target: PyAutoBrain
Lane: any

The body map (`PyAutoMind/repos.yaml`) is parsed about ten separate ways in @PyAutoBrain. Five hand-written line scanners of the `repos:` block: `agents/_repo_paths.py` `manifest_paths` and `package_paths`, `bin/project_discovery.py` `manifest_categories`, `agents/conductors/hygiene/_hygiene_repos.py` `parse_minimal`, `bin/public_names.py` `body_map_packages`. Four regex readers: `_docs.known_repos`, `_intake._mind_home`, `_board.repo_homes`, `_hygiene_ci.derive_org` (whose owner vote `_board.derive_org` repeats). One `manifest_field(root, key)` in `agents/_repo_paths.py` could serve them. The scanners differ on quoting, comments and block termination, so each must be matched exactly; some are PyYAML-free on purpose and must stay so. Found in the 2026-11-22 refactor review (PyAutoBrain#700); estimated 60-80 lines.

Witness: for the real `repos.yaml` and for fixtures with quoted values, trailing comments and a block ended by a new top-level key, every replaced reader returns the same value before and after; `tests/test_repo_paths.py`, `tests/test_public_names.py`, `tests/test_hygiene_conductor.py`, `tests/test_grouped_organ_consumers.py` and `tests/test_docs_conductor.py` pass.

<!-- formalised by the Intake (Conception) Agent on 2026-11-22 from file:/tmp/claude-0/-home-user/8f120f5d-ca18-5874-ae34-519506e9751b/scratchpad/prompts/6.txt -->
