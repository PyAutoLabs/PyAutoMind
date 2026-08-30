# Priors & Messages cleanup — tracker

Type: bug
Target: priors
Themes:
- graphical-ep
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: phases 1-3 SHIPPED; phase 4 = design (#1500) + parked 14 + findings 15-16
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-05-18 (backfilled from git)

> **2026-08-18 wrap-up sweep.** All nine confirmed bugs (01-08, 10) are fixed
> and merged on PyAutoFit main — Phase 1 batch via #1344/PR#1345 (merged
> `c0b6c94b8`), Phase 2 width-modifier pair via #1346/PR#1348 (merged
> `cf0cc4bbb`), verified live 2026-07-14. All five decisions on hub #1331 are
> taken (see its 2026-07-14 resolution comment). Completion records:
> [[priors-messages-fixes]], [[prior-width-safety]], [[ep-priors-fable-reassess]].
> Regression suites `test_priors_messages_fixes_1331.py` (12 tests) and
> `test_prior_width_safety.py` (11 tests) are on main.
> 2026-08-18 update: 09+11 SHIPPED (PR#1499 merged `21288bb`); 12+13 filed as
> design issue #1500 (decisions pending); 14 parked behind #1500; new finding
> 15 (#1498) awaiting adjudication.
> 2026-08-19 update: the 15 caller analysis is done (adjudication brief in
> the prompt file) and turned up finding 16 (`factor_gradient` dead-on-call),
> drafted but not yet issued.

## Why this folder exists

After fixing the `LogUniformPrior` sign-convention bug in PyAutoFit commit
`e95295b83` ("fix: log_prior_from_value sign convention — density form
across Prior subclasses"), we audited every prior and message in PyAutoFit
for similar latent math bugs.

Full audit lives at:
`complete/2026/08/priors-and-messages-math-audit.md` (retired 2026-08-18 —
fully graduated; was `draft/research/autofit/priors_and_messages_math_audit.md`)

This folder breaks that audit into a logical, dependency-ordered sequence
of standalone GitHub issues. The intent is to land them one by one so
each can be externally validated before the next begins.

## Verification philosophy

**The audit was AI-generated. Some findings may be wrong.**

Each prompt below instructs the agent to:

1. Read the relevant code (paths in the prompt).
2. Run a short Python reproducer that *numerically* demonstrates the bug.
3. Open a GitHub issue in `@PyAutoFit` via `/create_issue`.
4. Explicitly request external verification in the issue body — from a
   collaborator with stats / probabilistic-programming background, and
   optionally a second AI tool (Claude / GPT / Gemini cross-check).
5. **Stop. Do not implement the fix until the verification ack lands.**

The reason for the strict stop: I am not the expert here. Some of these
findings (especially the math-heavy ones in Phase 2) hinge on convention
choices where the "bug" may turn out to be intentional. Independent
review before any code change.

## How to use

When ready to action one of these issues, run:

```
/create_issue bug/priors/<file>.md
```

That files the issue. The agent should NOT call `/start_dev` against
these prompts until the issue has been ack'd by an external reviewer.

Update this tracker after each issue lands and again when the PR merges.

---

## Phase 1 — Standalone numerical bugs (easy reproducers)

These are concrete, isolated bugs with self-contained Python reproducers.
Each can be filed independently and verified in minutes.

| # | Prompt | Bug | Status | Issue | PR |
|---|--------|-----|--------|-------|----|
| 01 | log_gaussian_with_limits_crash (prompt retired) | `LogGaussianPrior.with_limits` will `TypeError` on first call | **shipped 2026-07-10** | #1344 (hub #1331) | #1345 |
| 02 | uniform_logpdf_array_handling (prompt retired) | `UniformPrior.logpdf(np.array(...))` raises ambiguous-truth error | **shipped 2026-07-10** | #1344 (hub #1331) | #1345 |
| 03 | gamma_from_mode_wrong_formula (prompt retired) | `GammaMessage.from_mode` formula is dimensionally wrong | **shipped 2026-07-10** (D3: match mean+variance, α=m²/V) | #1344 (hub #1331) | #1345 |
| 04 | truncated_normal_log_partition_incomplete (prompt retired) | `TruncatedNormalMessage` pdf does not integrate to 1 via generic interface | **shipped 2026-07-10** (integral 2.27 → 1.0) | #1344 (hub #1331) | #1345 |
| 05 | inv_beta_suffstats_clamp_noop (prompt retired) | `inv_beta_suffstats` negative-clamp branch is a no-op | **shipped 2026-07-10** (D1: raises `ValueError`) | #1344 (hub #1331) | #1345 |
| 06 | normal_message_sigma_negative_unchecked (prompt retired) | `NormalMessage` silently accepts negative sigma | **shipped 2026-07-10** (D2: σ<0 rejected, σ=0 point-mass kept) | #1346 (hub #1331) | #1348 |

## Phase 2 — Convention / safety (require design input)

These are not pure bugs — they require a *choice* about the desired
behaviour. The reproducers expose the inconsistency; the fix needs an
expert to ratify the convention before code changes.

| # | Prompt | Concern | Status | Issue | PR |
|---|--------|---------|--------|-------|----|
| 07 | log_prior_normalisation_convention (prompt retired) | `log_prior_from_value` drops constants inconsistently across priors | **shipped 2026-07-10** (D4: Option A — drop constants everywhere + `Prior.log_normalisation()` hook) | #1344 (hub #1331) | #1345 |
| 08 | relative_width_modifier_safety (prompt retired) | `RelativeWidthModifier` collapses to 0 / goes negative near zero means | **shipped 2026-07-10** (D5: `abs(mean)` + opt-in `absolute_floor` + `PriorException` guard) | #1346 (hub #1331) | #1348 |

## Phase 3 — Testing infrastructure (would have caught everything above)

| # | Prompt | Scope | Status | Issue | PR |
|---|--------|-------|--------|-------|----|
| 09 | prior_property_tests (→ complete/, [[prior-property-tests]]) | Add property-based correctness sweep over every `Prior` subclass | **SHIPPED 2026-08-18** (merged `21288bb`, 134 tests; folds in 11 §2) | #1497 | #1499 |

## Phase 4 — Refactors (only after Phases 1-3)

Bigger structural changes. Should not begin until the underlying bugs
are fixed and locked in by tests, otherwise the refactor will paper
over them.

| # | Prompt | Scope | Status | Issue | PR |
|---|--------|-------|--------|-------|----|
| 10 | fixed_message_cache_growth (prompt retired) | `FixedMessage.logpdf_cache` is an unbounded class-level dict | **shipped 2026-07-10** (cache removed, aliasing fixed) | #1344 (hub #1331) | #1345 |
| 11 | transformed_message_semantics_doc (→ complete/, [[transformed-message-semantics-doc]]) | `TransformedMessage` reversal convention is undocumented foot-gun | **SHIPPED** — §1 via #1333/PR#1334 (2026-07-10), §2 via PR#1499 (2026-08-18) | #1333, #1497 | #1334, #1499 |
| 12 | single_source_density_refactor (→ active/) | Each density is encoded in three places (`value_for` / `logpdf` / `log_prior_from_value`) | **design issue FILED 2026-08-18** (bundled with 13) | #1500 | — |
| 13 | collapse_prior_and_message (→ active/) | `Prior` and `Message` carry duplicated responsibility | **design issue FILED 2026-08-18** (bundled with 12) | #1500 | — |
| 14 | [replace_transform_stack_with_bijectors](14_replace_transform_stack_with_bijectors.md) | Replace hand-rolled `AbstractDensityTransform` with `tfp.bijectors` / `numpyro.transforms` | parked — go/no-go hangs off the #1500 design decision | — | — |
| 15 | [transformed_message_logpdf_jacobian](15_transformed_message_logpdf_jacobian.md) | `TransformedMessage.logpdf`/`pdf` omit the transform Jacobian (new finding from the 09 sweep) | **caller analysis complete + posted to #1498 2026-08-19** (EP loop is coherently base-space; `PriorFactor` is the one hybrid seam; public `Prior.logpdf` mis-promises physical) — awaiting external verification + contract adjudication with #1500 | #1498 | — |
| 16 | transformed_message_factor_gradient_unpack (→ complete/2026/08/) | `TransformedMessage.factor_gradient` crashes on first call (unpacks 4 from a 3-tuple; dead code, found by the 15 caller analysis) | **SHIPPED 2026-08-27** — repaired (option 1), independent of #1498; community PR #1502 merged `ae37ea817`, gradient verified vs finite differences | #1501 (closed) | #1502 |

---

## Ordering rationale

**Why Phase 1 before Phase 2?** Phase 1 bugs have unambiguous correct
answers (a function should not crash, a pdf should integrate to 1).
Phase 2 questions ("which constants do we keep?") need a convention
that's easier to choose *after* the unambiguous cases are settled.

**Why Phase 3 before Phase 4?** Without the property tests, any
refactor in Phase 4 risks regressing the Phase 1/2 fixes silently.
The tests are the safety net.

**Why 12-14 are last?** They are the right long-term direction (single
source of truth, fewer classes, replace the hand-rolled transform stack
with a library) but each is a multi-week effort and would be disruptive
to land without the bugfix + test infrastructure underneath.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
