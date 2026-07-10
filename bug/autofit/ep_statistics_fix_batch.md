# `@PyAutoFit` EP statistics fix batch — F1/F2/F4/F8 from the #1332 audit

Type: bug
Target: autofit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

The EP statistics audit (PyAutoFit#1332, `ep-statistics-audit`) confirmed
9 findings; its recommended fix batch (F1+F2+F3+F4+F8) was gated on the
priors/messages decision hub #1331. That guidance is now delivered and
shipped (#1345, #1348), and F3 + the F10 guard landed in #1349, F5 in
#1334, F7(c) in #1345. This prompt executes the remainder.

## Scope (all in `autofit/graphical` + `autofit/messages` + `laplace/`)

- **F1** — `MeanField.__truediv__` / `__pow__` pass `log_norm` into the
  `plates` ctor slot: evidence silently dropped, a float lands in
  `_plates`. Fix the ctor calls (and `__pow__`'s meaningless
  `log_norm * other.log_norm` branch). This is F7(a).
- **F2 (+extended)** — `GammaMessage.kl` and `BetaMessage.kl` compute the
  reverse direction vs Normal/TruncatedNormal. Contract:
  `self.kl(other) = KL(self‖other)`, stated once, enforced family-wide
  with a property test (EPHistory sums per-variable KLs — mixed graphs
  currently mix directions).
- **F4** — `AbstractMessage.update_invalid` scalar branch is self-flagged
  broken (`# TODO: Fairly certain this would not work`); it is the
  BAD_PROJECTION recovery path. Fix + unit test both branches.
- **F8** — delete dead/suspect quasi-Newton variants in
  `laplace/newton.py` (`diag_sr1_bfgs_update` returns None,
  `bfgs1_update` sign-disputed, `diag_sr1_update_` unused); only the
  exported `full_*` variants stay.

## Explicitly out of scope

- **F6** (truncated-normal KL uses untruncated formula) — needs
  truncated-moment math; own prompt later.
- **F7(b)** (where sampler per-factor evidence is recorded —
  `MeanField.from_priors` defaults `log_norm=0`) — design decision.
- **F9** (private scipy `_linesearch` import) — robustness chore.

## Validation

Full `test_autofit/` suite; new unit tests per fix (log_norm/plates
round-trip through `__truediv__`/`__pow__`, KL direction property test
across Normal/TruncatedNormal/Gamma/Beta, update_invalid scalar+array);
re-run `autofit_workspace_test/scripts/graphical/ep_*.py` (parity,
deterministic, exact) as integration smoke.

<!-- filed 2026-07-10 by the session executing the #1331 fix batches;
     continues the --auto chain approved in-session -->
