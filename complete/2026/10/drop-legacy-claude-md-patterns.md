## drop-legacy-claude-md-patterns
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/494
- completed: 2026-10-07
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/495

- Merged as `766c0063` (2026-10-07). Remainder split out of `absorb-claude-notes-agents-md` (`complete/2026/10/absorb-claude-notes-agents-md.md`, PyAutoBrain#493); this closes that record's "no file in PyAutoBrain names CLAUDE.md" done-when (PyAutoBrain#492).
- `agents/conductors/clone/_clone.py`: `CLAUDE.md` / `scripts/CLAUDE.md` removed from the framework patterns, so a reference assistant tracking either now fails the clone boundary as unclassified (intended; none tracks one today).
- `bin/regroup_workspace.py`: root `CLAUDE.md` dropped from the rewritten local config files; bare-repo-name rewrite narrowed to `AGENTS.md`.
- `tests/test_memory_surfaces.py`: the "adapter never displaces `wiki/AGENTS.md`" guard plants a generic `wiki/GEMINI.md`.
- Unblocked by the PyAutoMind#482 `session_hook_propagate` removal waves (root run 37627261984, nested run 37631942996). Brain suite 1291 passed (clean shell); `check_boundary.py` exit 0 on autolens/autofit assistants; control clone with a committed `scripts/CLAUDE.md` exits 1; `git grep -in "claude\.md"` empty.

## Original prompt

# Drop the tolerated-legacy CLAUDE.md patterns in _clone.py and regroup_workspace.py

Type: maintenance
Target: pyautobrain
Repos:
- @PyAutoBrain
Difficulty: small
Autonomy: supervised
Consequence: judge
Priority: low
Status: active — issued #494 (PyAutoMind#482 removal wave blocker cleared: root run 37627261984 + nested run 37631942996)
Filed: 2026-10-07
Issued: 2026-10-07

- Split out of `absorb-claude-notes-agents-md` at close-out — the rest shipped in
  `complete/2026/10/absorb-claude-notes-agents-md.md`
  (https://github.com/PyAutoLabs/PyAutoBrain/pull/493); this is what remains of
  its "no file in PyAutoBrain names CLAUDE.md" done-when.

## Scope

PyAutoBrain#493 kept `CLAUDE.md` as a tolerated-legacy file pattern in
`agents/conductors/clone/_clone.py` and `bin/regroup_workspace.py`, because the
assistants' `scripts/CLAUDE.md` pointers still exist and their
`clone-boundary.yml` CI would fail on unclassified files. Once the PyAutoMind#482
propagation wave (and the nested-pointer follow-up) has removed those files,
drop the legacy patterns and their tests.

## Done when

No file in PyAutoBrain names `CLAUDE.md` as a thing that exists; Brain suite
green; the assistants' `clone-boundary.yml` still passes.
