# EP guide crashes: strict NormalMessage built from a negative-variance EP message

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

The nightly PyAutoHeart `workspace-validation.yml` run is RED on a single cell,
`run_scripts (3.12, autolens, guides)`, because
`autolens_workspace/scripts/guides/modeling/advanced/expectation_propagation.py`
crashes during expectation propagation with:

```
autofit.exc.MessageException: NormalMessage sigma cannot be negative, got sigma=-0.016...
```

It is **stochastic / unseeded**: `sigma=-0.016` on 2026-07-13, `sigma=-0.17` on
2026-07-11 (the 2026-07-10 red was a different, earlier step). Different negative
values across runs ⇒ the negative width is produced inside the EP message-passing
algebra, not from a fixed model mistake.

Root cause (grounded, not the stale hint in the error string):

- The guard `assert_sigma_non_negative` (`autofit/messages/normal.py:45`) rejects
  `sigma < 0` at strict `NormalMessage.__init__` (`normal.py:110`). It was added
  deliberately for the *prior-passing* misuse case and is load-bearing there —
  do not simply delete it.
- Its error hint blames `RelativeWidthModifier`, but that hint is **stale for this
  path**: `RelativeWidthModifier.__call__` already returns `value * abs(mean)`
  (`autofit/mapper/prior/width_modifier.py:110`, #1331 D5), so it cannot emit a
  negative sigma. The EP crash does not come from prior passing.
- EP legitimately produces intermediate messages with negative / infinite
  variance (cavity division of Gaussians). The codebase already has the correct
  vehicle for this: `NaturalNormal` (`normal.py:508`), which permits
  `eta2 ∈ (-inf, 0)` and bypasses the guard by calling `AbstractMessage.__init__`
  directly. The bug is that somewhere on the EP / declarative path a **strict
  `NormalMessage`** (guard-enforced) is being constructed from a negative-variance
  state where a `NaturalNormal` should be used (or the projection/inversion that
  yields the passed `sigma` has a sign/validity bug), so a legitimate transient
  EP message is hard-crashing instead of being handled/damped.

Fix locus is the **PyAutoFit library** (`autofit/graphical/expectation_propagation`
and/or `autofit/messages/normal.py`), NOT the workspace guide. Per no-autoimmunity:
do **not** seed the guide script, constrain its priors, or otherwise mask the
symptom — the guide is documentation and must keep exercising the real EP path.

Scope of a fix should include: identify the exact construction site turning a
negative-variance EP message into a strict `NormalMessage`; route it through
`NaturalNormal` / the invalid-message handling (`AbstractMessage.update_invalid`,
`normal.py:346`) so transient negative-variance cavities are tolerated or damped
rather than raised; keep the strict guard intact for the genuine prior-passing
case; correct the now-misleading `RelativeWidthModifier` hint in the exception;
add a regression test in `test_autofit/graphical/` that drives an EP update
through a negative-variance cavity without raising; confirm the EP guide script
runs green in workspace-validation.

Evidence: PyAutoHeart workspace-validation runs 29227574734 (2026-07-13) and
29153442364 (2026-07-11). Related history: #1331 / #1348 (sigma<=0 semantics,
point-mass idiom), EP inherent-randomness work.
