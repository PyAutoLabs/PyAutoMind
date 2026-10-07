# Retire nested CLAUDE.md pointers and remove the temporary firewall-gate skip

Type: maintenance
Target: pyautomind
Repos:
- @PyAutoMind
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-10-07
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/484

## Request (verbatim, 2026-10-07)

> do theese:
> - Remove the temporary firewall-gate skip and its tests in PyAutoMind, now that the leg is green on main.
> - Re-spawn the Mind and Memory templates so the spawn drift check stops flagging the old template file.
> - The 17 nested pointers and the Brain legacy-pattern remainder draft, both filed in Mind.

(The re-spawn runs through `/spawn`; the Brain remainder is its own draft. This
prompt covers the two PyAutoMind items.)

## Context

PyAutoMind#483 (merged 4d63b637) inverted the `"CLAUDE.md → AGENTS.md pointers"`
lint and the `session_hook_propagate` wave (run 37627261984) removed the 44
repo-root pointers; euclid_assistant was hand-cleaned (a39e35c). The leg is now
OK on main. Two things remain in this repo:

1. `.github/workflows/firewall_gate.yml` still carries the TEMPORARY skip of
   that leg, the replacement "Assert PyAutoMind carries no CLAUDE.md" step, and
   the matching TEMPORARY tests in `tests/test_session_hook_sync.py`
   (`test_the_skipping_step_composes_both_decisions` and the three added ones).
2. The lint and the removal leg look only at each repo's ROOT. 17 tracked
   content-free pointers sit below repo roots and are untouched:
   `autogalaxy_assistant/scripts`, `autolens_assistant/scripts`,
   `autocti_assistant/scripts`, `autolens_workspace_test/scripts`,
   `autolens_workspace_test/scripts/misc/database/scrape`,
   `PyAutoMemory/wiki` and `wiki/{lensing,smbh,galaxies,methods,cti}`,
   `autogalaxy_assistant/wiki/literature`, `autofit_assistant/wiki/literature`,
   `autocti_assistant/wiki/literature`, `autolens_assistant/wiki/literature`,
   `autolens_assistant/wiki/euclid`. Measured: a pointer below the cwd suppresses
   nothing for a root-started session, but a session started INSIDE such a
   folder loses every ancestor AGENTS.md. Each is the same `@AGENTS.md`
   pointer shape (some 87 B, some ~255-330 B with the boilerplate paragraph,
   one 11 B) with a sibling AGENTS.md.

## Scope (this repo only)

1. Remove the TEMPORARY skip, its banner, the replacement step and the
   TEMPORARY tests; restore the gate's structure test to its pre-#483 shape
   (the pointer leg runs normally on PR and push).
2. `scripts/repos_sync.py`: extend `check_claude_md_pointers` and
   `remove_claude_md_pointers` from the repo root to every tracked `CLAUDE.md`
   in the repo tree (`git ls-files` — never walk untracked/ignored dirs such as
   `tmp/`, `output/`, `.worktrees/`). Rule unchanged: a CLAUDE.md with a
   sibling AGENTS.md must not exist; content-free pointers are removable,
   content-bearing ones are reported (`KEPT`) and never deleted. Keep the leg
   name byte-identical (Heart's parser). A CLAUDE.md with NO sibling AGENTS.md
   is out of scope: leave it, do not report it.
3. `.github/workflows/session_hook_propagate.yml`: the dispatch-only removal
   already stages `git rm --cached CLAUDE.md` at the root; make it stage every
   tracked CLAUDE.md the removal deleted (use the removal's own output or
   `git ls-files --deleted`), still dispatch-only, still honouring `dry_run`,
   nothing else widened. Update the header comment and the hand-cleanup list
   (euclid_assistant is done; drop it).
4. Tests: nested fixtures for check + removal + idempotence + KEPT; the
   workflow staging test if one exists. Mind suite green.
5. Verify on the real workspace with `--check` only (expect the leg to fail
   naming the 17 nested pointers across 6 repos); `--write` only on scratch
   fixtures.

## Done when

`--check` lists the nested pointers; after the next human-dispatched wave it
is OK; the gate has no TEMPORARY text; Mind suite green.
