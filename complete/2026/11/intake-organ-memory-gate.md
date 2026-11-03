- summary: intake no longer writes a `Memory:` line on organ-targeted prompts. `_cites_memory()` gates on ORGANISM_REPOS (`category: organ`) and, by human decision 2026-11-03, any body-map repo whose `path` sits under `organs/` (the PyAutoScientist landing repo); both read from repos.yaml, so no repo name enters organ code (tenant firewall). `write_prompt` skips the Memory query for those targets. Item 1 of the original prompt (header pass-through) had already shipped in PyAutoBrain#554.
- pr: PyAutoBrain#564 (shared with board-phase2-legs, rtd-organism-currency, project-discovery-argparse-ordering — one PR by human decision); issue PyAutoBrain#561.
- witness: PASS — test_organ_target_gets_no_memory_line (fails on the pre-fix `_intake.py`) + test_library_target_with_hits_still_gets_memory_line; Brain suite 1477 passed; CI pytest 3.12 + 3.13 + docs-build green.
- trap: the first test version named a library repo literally and tripped the tenant firewall; the test now reads the library from repos.yaml.

## Original prompt

# intake classify --file injects an unrelated Memory: line on organ-targeted prompts

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-11-03
Issued: 2026-11-03
Consequence: glance
Witness: a new test asserts `_with_memory` adds no `Memory:` line when the prompt's `Target:` is an organ repo (PyAutoBrain, PyAutoMind, PyAutoCortex, PyAutoHeart, PyAutoHands, PyAutoNerves, PyAutoEyes, PyAutoPulse, PyAutoInsight, PyAutoMemory, PyAutoBroca, PyAutoGut, PyAutoDNA, PyAutoScientist, PyAutoEars) and still adds one for a library target with digest hits; `pytest PyAutoBrain/tests -q` green
Review-minutes: 3
Unattended: ready
Lane: any

Measured 2026-11-03 while filing the autonomous-orchestrators epic and its phase 1
(`@PyAutoMind/draft/feature/pyautobrain/autonomous_orchestrators_epic.md`,
`..._p1_policy_and_formats.md`) with `bin/pyauto-brain intake --apply classify --file`:

1. The input declared `Epic: autonomous-orchestrators`, `Phase: 1` and `Filed: 2026-11-03`.
   The written file carried none of them. Cause: `_render_header()` in
   `@PyAutoBrain/agents/conductors/intake/_intake.py` takes only the classification fields
   (type, target, repos, difficulty, autonomy, priority, themes, consequence, witness,
   review-minutes, unattended). `_split_header()` reads the optional keys in
   `_HEADER_BLOCK_KEYS` (`epic`, `phase`, `filed`, `blocked-by`, `closes-when`, `lane`) into
   `declared`, and they are then dropped on the floor. Without `Epic:`/`Phase:` the
   dashboard shows an epic member as a standalone pick, which is exactly what epics.md says
   must not happen; without `Filed:` the prompt's date is the file mtime.
2. Both files received `Memory: wiki/galaxy/...` lines citing PyAutoGalaxy wiki pages. The
   prompts are about Brain orchestration doctrine; the citations matched on vocabulary
   ("profile", "model") only. `memory_citations()` is unconditional, and the comment above
   it says the line answers "what does the science say" — for an organ-targeted prompt there
   is no science question, so the line should not be written. Suggested rule: skip
   PyAutoMemory citation when `Target:` resolves to an organ repo, or when the best digest
   score is below a floor; keep the "no hits → no line" behaviour.

Both were fixed by hand in the two prompt files. **Reproduced on this very filing** (2026-11-03): the raw input declared `Lane: any`, which the written header dropped, and a `Memory:` line citing massive-ellipticals and dark-matter-substructure wiki pages was injected; both hand-fixed again. Fix: pass the declared optional keys
through `_render_header` (after `Priority:`, before `Consequence:`, in `_HEADER_BLOCK_KEYS`
order), and gate `_with_memory` as above. Phase 2 of the autonomous-orchestrators epic
(`draft/feature/pyautobrain/autonomous_orchestrators_p2_lane_schema_census.md`) names the
same pass-through; whichever lands first closes the other.

**Re-scoped 2026-11-03 (human-approved):** item 1, the header pass-through, shipped in
autonomous-orchestrators phase 2 (PyAutoBrain#554, record
`complete/2026/11/autonomous-orchestrators-p2.md`; its test
`test_declared_optional_headers_survive_apply_unchanged`). This prompt is now **item 2 only**:
gate `_with_memory` so organ-targeted prompts get no `Memory:` line.

<!-- formalised by the Intake (Conception) Agent on 2026-11-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/da64305f-c750-425e-b845-c95ca4a765c8/scratchpad/intake_header_bug.md -->

Reproduced again 2026-11-03 filing the phase-3 prompt (later 3a, now `complete/2026/11/autonomous-orchestrators-p3a.md`): `Memory: wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md` on a PyAutoBrain-targeted prompt; hand-removed. (The declared headers survived, confirming the phase-2 half.)
