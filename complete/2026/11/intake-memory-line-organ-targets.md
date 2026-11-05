- summary: already shipped — closed as stale draft. The `_with_memory` gate in `agents/conductors/intake/_intake.py` landed in PyAutoBrain 557f8e0 and ba38413: organ targets get no `Memory:` line. The organ set comes from `PyAutoMind/repos.yaml` (`_sizing.ORGANISM_REPOS` = `category: organ`, plus `_intake._ORGANS_DIR_REPOS` for repos under `organs/`, which covers PyAutoScientist). `Target:` is normalised by `_sizing.normalise_repo` (case, leading `@`, path suffix).
- witness: PyAutoBrain branch `ccr-f98d2a4d-92r7rv` commit 906b5dd adds `test_organ_target_spellings_get_no_memory_line` (organ spellings `pyautobrain`, `@PyAutoBrain`, `PYAUTOMIND`, `@PyAutoBrain/agents`, PyAutoScientist get no line; a library target still gets one); tests/test_intake_memory.py 8 passed; Brain suite 1576 passed, 1 skipped (2026-11-05). The test-only commit is unmerged and needs a PR.
- found by: queue check-in 2026-11-05.

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
