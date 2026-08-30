# Remove the dead EDEN packaging tooling from PyAutoFit

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoNerves
Themes:
- hygiene
- release
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: PARTIALLY SHIPPED — the module is gone, `eden.yaml` is not (2026-08-09)
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-07-13 (backfilled from git)

## 2026-08-09 — half the primary scope has already landed

Checked by the draft/ sweep against PyAutoFit main (`3b960609`):

- **`autofit/tools/edenise` — GONE.** `autofit/tools/` now holds only
  `__init__.py`, `add_notebook_quotes.py`, `namer.py`, `util.py`. A repo-wide
  grep for `edenise` returns zero Python hits, so the § Guardrails
  "confirm nothing imports it" check is settled by the removal itself.
- **Root `eden.yaml` — STILL PRESENT.** The second half of the § Scope
  PyAutoFit bullet is outstanding.

Also note the § Scope follow-up targets **PyAutoNerves** — the repo formerly
named PyAutoConf (now the `autonerves` package). The references throughout this
prompt were updated to the current name on 2026-08-26; `scripts/edenise.py` has
not been re-checked since, so confirm it survived the rename rather than
assuming the path.

What is left is deleting one dead config file plus the PyAutoNerves driver, so
`Difficulty:` drops `medium` → `small`. The guardrail about re-scoping if a live
consumer surfaces no longer applies to the PyAutoFit leg.

---

## Why

The Euclid **EDEN** packaging path is dormant dead code. Its per-repo `eden.ini`
configs were removed across the org on 2026-07-13, and its only driver —
`PyAutoNerves/scripts/edenise.py` (`from autofit.tools import edenise`) — was last
touched in 2023 and is wired into no CI or build. With the configs gone, the
tooling is orphaned.

## Scope

- **PyAutoFit** (primary): remove the `autofit.tools.edenise` tooling module and
  the root `eden.yaml`.
- **PyAutoNerves** (follow-up): remove the orphaned `scripts/edenise.py` driver.

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
