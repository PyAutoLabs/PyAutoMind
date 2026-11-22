# Agent --help text is rotted in feature, build and bug

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: notify
Witness: a test runs each of the three with `--help` and asserts no line starts with `set ` and that build's output names `--rehearsal-run-id` and the exit codes.
Review-minutes: 0
Unattended: ready
Lane: any

Agent --help text is rotted in feature, build and bug

Type: bug
Target: PyAutoBrain
Lane: any

Three shell agents print rotted `--help` text because they slice their own header with hardcoded `sed` line ranges. In @PyAutoBrain: `agents/conductors/feature/feature.sh:49` leaks `set -uo pipefail` into `--help`; `agents/conductors/build/build.sh:97` truncates the help before `--rehearsal-run-id`, `--dry-run`, `--json` and the exit codes; `agents/conductors/bug/bug.sh:50` leaks an internal comment. `health.sh`, `rehearse.sh`, `validate.sh` and `nightly.sh` already use a header-help `awk` that stops at the first non-comment line; use the same in these three. Found in the 2026-11-22 refactor review (PyAutoBrain#700).

Witness: a test runs each of the three with `--help` and asserts no line starts with `set ` and that build's output names `--rehearsal-run-id` and the exit codes.

<!-- formalised by the Intake (Conception) Agent on 2026-11-22 from file:/tmp/claude-0/-home-user/8f120f5d-ca18-5874-ae34-519506e9751b/scratchpad/prompts/1.txt -->
