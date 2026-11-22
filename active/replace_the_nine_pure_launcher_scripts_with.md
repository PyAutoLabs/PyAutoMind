# Replace the nine pure launcher scripts with a registry entry

Type: refactor
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-11-22
Consequence: notify
Witness: every verb's output is byte-identical before and after for `--help` and one real invocation; `tests/test_skill_install.py` and `tests/test_conductor_discovery.py` pass; `repos_sync.py --check` passes.
Review-minutes: 0
Unattended: ready
Lane: any

Replace the nine pure launcher scripts with a registry entry

Type: refactor
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Lane: any

Nine agent wrappers in @PyAutoBrain only `exec python3 "$HERE/_<verb>.py" "$@"` after sourcing `_common.sh`: `docs.sh`, `clone.sh`, `workspace.sh`, `profiling.sh`, `eyes.sh`, `community.sh`, `cortex.sh`, `batch.sh`, `review.sh` (265 lines, 36 of them code; `board/board.sh` is the same shape). Let a registry value in `bin/pyauto-brain` name `_<verb>.py` and add one `exec python3` branch in `main()`; the dispatcher already exports `PYAUTO_ROOT`. Check each script's header usage text against its `AGENTS.md` before deleting it. @PyAutoMind `scripts/repos_sync.py` (around lines 1860 and 1884) lists `clone.sh` and `profiling.sh` in allow-lists and needs the matching edit. Leave `sizing`, `memory`, `samplers`, `refactor`, `feature`, `bug`, `intake`, `vitals`, `release`: they resolve sibling checkouts or reorder arguments. Found in the 2026-11-22 refactor review (PyAutoBrain#700).

Witness: every verb's output is byte-identical before and after for `--help` and one real invocation; `tests/test_skill_install.py` and `tests/test_conductor_discovery.py` pass; `repos_sync.py --check` passes.

<!-- formalised by the Intake (Conception) Agent on 2026-11-22 from file:/tmp/claude-0/-home-user/8f120f5d-ca18-5874-ae34-519506e9751b/scratchpad/prompts/5.txt -->
