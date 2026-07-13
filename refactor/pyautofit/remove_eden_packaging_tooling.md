# Remove the dead EDEN packaging tooling from PyAutoFit

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoConf
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Why

The Euclid **EDEN** packaging path is dormant dead code. Its per-repo `eden.ini`
configs were removed across the org on 2026-07-13, and its only driver —
`PyAutoConf/scripts/edenise.py` (`from autofit.tools import edenise`) — was last
touched in 2023 and is wired into no CI or build. With the configs gone, the
tooling is orphaned.

## Scope

- **PyAutoFit** (primary): remove the `autofit.tools.edenise` tooling module and
  the root `eden.yaml`.
- **PyAutoConf** (follow-up): remove the orphaned `scripts/edenise.py` driver.

## Guardrails

- This is **dead-code removal with no behaviour change** to the shipped library
  API — but `autofit.tools.edenise` is an import surface, so first confirm
  nothing in the installed library, tests, or any workspace imports it
  (`grep -rn "tools.edenise\|import edenise"`), and that `edenise.py` is the sole
  consumer, before deleting.
- If any live consumer surfaces, re-scope (this would become a `feature/`-style
  API change, not a clean removal).
- Ship library-first per the workflow; no downstream workspace impact expected.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake; re-homed triage/ -> refactor/pyautofit/ and Target corrected PyAutoConf -> PyAutoFit by hand (classifier low-confidence) -->
