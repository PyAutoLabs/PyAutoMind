# Priors & Messages cleanup — tracker

## Why this folder exists

After fixing the `LogUniformPrior` sign-convention bug in PyAutoFit commit
`e95295b83` ("fix: log_prior_from_value sign convention — density form
across Prior subclasses"), we audited every prior and message in PyAutoFit
for similar latent math bugs.

Full audit lives at:
`PyAutoMind/research/autofit/priors_and_messages_math_audit.md`

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
| 01 | [log_gaussian_with_limits_crash](01_log_gaussian_with_limits_crash.md) | `LogGaussianPrior.with_limits` will `TypeError` on first call | pending | — | — |
| 02 | [uniform_logpdf_array_handling](02_uniform_logpdf_array_handling.md) | `UniformPrior.logpdf(np.array(...))` raises ambiguous-truth error | pending | — | — |
| 03 | [gamma_from_mode_wrong_formula](03_gamma_from_mode_wrong_formula.md) | `GammaMessage.from_mode` formula is dimensionally wrong | pending | — | — |
| 04 | [truncated_normal_log_partition_incomplete](04_truncated_normal_log_partition_incomplete.md) | `TruncatedNormalMessage` pdf does not integrate to 1 via generic interface | pending | — | — |
| 05 | [inv_beta_suffstats_clamp_noop](05_inv_beta_suffstats_clamp_noop.md) | `inv_beta_suffstats` negative-clamp branch is a no-op | pending | — | — |
| 06 | [normal_message_sigma_negative_unchecked](06_normal_message_sigma_negative_unchecked.md) | `NormalMessage` silently accepts negative sigma | pending | — | — |

## Phase 2 — Convention / safety (require design input)

These are not pure bugs — they require a *choice* about the desired
behaviour. The reproducers expose the inconsistency; the fix needs an
expert to ratify the convention before code changes.

| # | Prompt | Concern | Status | Issue | PR |
|---|--------|---------|--------|-------|----|
| 07 | [log_prior_normalisation_convention](07_log_prior_normalisation_convention.md) | `log_prior_from_value` drops constants inconsistently across priors | pending | — | — |
| 08 | [relative_width_modifier_safety](08_relative_width_modifier_safety.md) | `RelativeWidthModifier` collapses to 0 / goes negative near zero means | pending | — | — |

## Phase 3 — Testing infrastructure (would have caught everything above)

| # | Prompt | Scope | Status | Issue | PR |
|---|--------|-------|--------|-------|----|
| 09 | [prior_property_tests](09_prior_property_tests.md) | Add property-based correctness sweep over every `Prior` subclass | pending | — | — |

## Phase 4 — Refactors (only after Phases 1-3)

Bigger structural changes. Should not begin until the underlying bugs
are fixed and locked in by tests, otherwise the refactor will paper
over them.

| # | Prompt | Scope | Status | Issue | PR |
|---|--------|-------|--------|-------|----|
| 10 | [fixed_message_cache_growth](10_fixed_message_cache_growth.md) | `FixedMessage.logpdf_cache` is an unbounded class-level dict | pending | — | — |
| 11 | [transformed_message_semantics_doc](11_transformed_message_semantics_doc.md) | `TransformedMessage` reversal convention is undocumented foot-gun | pending | — | — |
| 12 | [single_source_density_refactor](12_single_source_density_refactor.md) | Each density is encoded in three places (`value_for` / `logpdf` / `log_prior_from_value`) | pending | — | — |
| 13 | [collapse_prior_and_message](13_collapse_prior_and_message.md) | `Prior` and `Message` carry duplicated responsibility | pending | — | — |
| 14 | [replace_transform_stack_with_bijectors](14_replace_transform_stack_with_bijectors.md) | Replace hand-rolled `AbstractDensityTransform` with `tfp.bijectors` / `numpyro.transforms` | pending | — | — |

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
