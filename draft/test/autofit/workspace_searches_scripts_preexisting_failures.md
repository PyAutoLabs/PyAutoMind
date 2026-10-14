# `@autofit_workspace` six `searches/` scripts fail on main at TEST_MODE 1/2 (NUTS divergences, MultiStart `n_resurrections`, NSS `log_evidence_error`)

Type: test
Target: autofit
Repos:
- autofit_workspace
- PyAutoFit
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Witness: all 19 `scripts/searches/` scripts in autofit_workspace pass at TEST_MODE 1 and TEST_MODE 2 against PyAutoFit main (A5 PR4 measured 14/19 and 13/19, the same pass set as main df6d218f1), and the workspace CI anchors in the A5 consumers task cover them.
Filed: 2026-10-14

Measured by the A5 library worker on PyAutoFit#1692 and identically on main df6d218f1, so none of these are A5 regressions. Failing scripts: BlackJAXNUTS ("unexpected divergences" in test mode), MultiStartAdam, MultiStartProdigy, MultiStartResumeNaNCounters, MultiStartResurrect (e.g. `KeyError: 'n_resurrections'`), and NSS at TEST_MODE 2 (`KeyError: 'log_evidence_error'`). Each is either a library test-mode gap (the key the script reads is not written under test mode) or a stale script; decide per script, fix library-side where the key is a documented output, and land the script changes after `draft/refactor/autofit/search_ext_a5_consumers.md` (which re-anchors workspace CI on the template). Evidence: session 51fca711 scratchpad `a5/` workspace-script logs.
