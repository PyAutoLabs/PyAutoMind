# repos_sync.py check mode now checks the root AGENTS.md routing table and WORKFLOW owner map

Completed: 2026-10-07
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/480
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/481

Merged 2026-10-07 under a human `/prm`.

- `repos_sync.py --write` regenerates two `required=True` blocks (workspace-root `AGENTS.md` routing table, `PyAutoBrain/skills/WORKFLOW.md` owner map) but check mode had no leg for either, so it reported OK while the root table was missing PyAutoEars and PyAutoInsight.
- Added check legs `root AGENTS.md routing table (generated)` and `WORKFLOW.md owner map (generated)` (`check_routing_table`, `check_owner_map`): absent file skipped (partial/web checkouts), missing markers reported, stale block reported with the `--write` remedy.
- New `tests/test_repos_sync_routing_blocks.py` (6 tests); full Mind suite 668 passed. Pre-existing unrelated `shared-standards: 2 mismatches` left untouched.

## Original prompt

# repos_sync.py check mode never checks the workspace-root AGENTS.md routing table

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- ci
- robustness
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Filed: 2026-10-07
Issued: 2026-10-07

Original request (verbatim, from the parent session):

> PyAutoMind scripts/repos_sync.py: check mode never checks the workspace-root AGENTS.md routing table.
> `--write` regenerates it (write_block(root/"AGENTS.md", routing_table(categories, repos), required=True) near line 2314), but there is no corresponding drift check, so check mode reported OK while the root table was missing PyAutoEars and PyAutoInsight and had stale Pulse text (the parent already regenerated the root file; it is currently in sync). Add a check (mirror the existing organism-map block check style and its registration in the check list near line 2237) that compares the root AGENTS.md repos_sync:begin/end block to routing_table(...), skipping gracefully if the root AGENTS.md is absent (partial/web checkouts). Also check whether the WORKFLOW.md owner_map block written alongside it has a check; if not, add one the same way. Add/extend tests if repos_sync has a test suite. Verify: check passes now; temporarily corrupt a copy (use --root on a scratch copy) to prove it fails. Note the pre-existing unrelated "shared-standards: 2 mismatches" — do not fix them.
