# EP framework review — statistics, docs, diagnostics, deterministic variables

Type: research
Target: graphical_ep
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: execution-complete (2026-07-08) — all 8 phases done; shipped or
parked on human review (see the per-phase annotations below and the
wrap-up on PyAutoFit#1330)

## Original request (verbatim)

So, we used Opus to do a review of messages and priors in autofit, which led to all the issues in bug/priors. I want us reassess this using Fable, and for us to go on to do a wider review of the Expectation propagation framework (source code PyAutoFit/autofit/graphical, with examples giving a run through of the graphical / EP modeling in HowToFit/scripts/chapter_3_graphical_models, and the cancer use case in /mnt/c/Users/Jammy/Science/ic50_workspace, and cosmology in /mnt/c/Users/Jammy/Science/concr/scripts/cosmology . Tasks include: (i) assessing if priors, messages and the underlying statistics of EP in autofit has bugs we should fix; (ii) documentation of the graphical package (including formal bayesian equations which ensure an AI agent knows exactly what bayes statistics are being used) and more thorough integration tests in autofit_workspace_test (see autofit_workspace_test/scripts/graphical) and more thorough end-to-end example scripts, written in the style of eamples in autofit_workspace/scripts, which explain the EP framework, its stats and allow for step-by-step run trhoughs of th eEP framework, e.g. something written in the style of something like autolens_workspace/scripts/imaging/likelihood_function.py which allows a user to run EP at the lower level API step-by-step and follow what is happening; (iii) currently there are not many built in tools for analysing the results of an EP fit or monitoring how the fit is progress, can we add more of these (could be funciton calls at end of examples, visuals output during EP and text file metadata in the output folder; (iv) deterministic variables in the cancer use case use inbuilt aspects of the EP composition (find an old PR by rhayes777 on this) but do not use the determinitic_variable API in the low level EP code, should we do anything about that?; (v) scope out analytic likelihood updates in the EP source code; (vi) What other features can we plan? This is obviously a huge prompt, so use your fable magic to plan everything out thoroughly

## Scope and relationship to existing backlog

This is the **correctness / documentation / diagnostics / feature** umbrella
for the EP framework. It complements — does not duplicate — the two
performance-focused companions in this folder:

- `ep_scoping.md` — EP scale-up / per-fit overhead (performance).
- `graphical_scoping.md` — joint-graph scale-up (performance).

It directly supersedes-or-revalidates two existing artefacts:

- `bug/priors/01–14` — the Opus-era review findings. Phase 0 reassesses
  every one on clean `main` before any fixing (clusters age out; verify
  reproduction first).
- `research/autofit/priors_and_messages_math_audit.md` — the parked Opus
  census that spawned `bug/priors`. Phase 0 folds its confirmed-bug list
  into the reassessment; retire or update it once the Fable verdicts land.

Grounding material for the review (read, don't bulk-load):

- Source: `PyAutoFit/autofit/graphical/`, `PyAutoFit/autofit/messages/`,
  `PyAutoFit/autofit/mapper/prior/`.
- Tutorial walk-through: `HowToFit/scripts/chapter_3_graphical_models/`.
- Real use cases: cancer IC50 — `/mnt/c/Users/Jammy/Science/ic50_workspace`
  (non-standard z_projects layout); cosmology —
  `/mnt/c/Users/Jammy/Science/concr/scripts/cosmology`.
- Existing integration tests: `autofit_workspace_test/scripts/graphical/`.

## Phases (split into separate issues/PRs at start_dev time — issue each as its predecessor nears shipping, not upfront)

### Phase 0 — Fable reassessment of the Opus priors/messages findings
**Issued:** PyAutoFit#1330 (2026-07-08) — task `ep-priors-fable-reassess`.
**Complete (2026-07-08):** all 9 reproducible findings confirmed on main @
`0f26ff2d8`; verdicts in `bug/priors/*.md`; decision hub for fixes:
PyAutoFit#1331 (awaiting maintainer + contributor guidance).
Re-verify each of `bug/priors/01–14` and the confirmed-bug list in
`priors_and_messages_math_audit.md` against clean PyAutoFit `main`:
reproduce, confirm/refute the math, re-rank severity. Output: updated
per-bug verdicts (fix / park / close), written back into the `bug/priors`
prompts, and a retirement decision on the old audit census.

### Phase 1 — EP statistics correctness review (the wider Fable review)
**Issued:** PyAutoFit#1332 (2026-07-08) — task `ep-statistics-audit`.
**Complete (2026-07-08):** findings F1–F9 on #1332 (2 confirmed EP-layer
bugs w/ repro: MeanField log_norm→plates ctor slip; Gamma+Beta KL reversed
vs Normal; truncated-KL error quantified 1.5%→140%; evidence bookkeeping
broken in 3 legs; dead quasi-Newton code). Core EP update algebra verified
correct. Wiki write-up shipped:
`PyAutoMemory/methods_wiki/concepts/expectation-propagation.md`.
Recommended EP fix batch F1+F2+F3+F4+F8 pends #1331 guidance.
Audit the statistics of `autofit/graphical`: message algebra
(natural/canonical parameterisations, sufficient statistics, log-normalisers),
cavity distribution computation, tilted-distribution moment matching / KL
projection direction, damping, the mean-field approximation, EPHistory
convergence criteria (KL divergence evaluation), and the Laplace optimiser
step. Validate against the three grounded use cases (HowToFit ch3, IC50,
cosmology). Output: a findings census in the style of the priors audit,
each finding with a minimal reproduction.

The statistical write-up from this review also lands in the PyAutoMemory
wiki: a new `PyAutoMemory/methods_wiki/concepts/expectation-propagation.md`
concept page (the EP algorithm as PyAutoFit implements it — formal
equations, approximating family, moment matching, damping, known
pitfalls/findings), linked from `concepts/bayesian-inference.md` and the
wiki index. PyAutoMemory is personal: the public Phase 2 docs in PyAutoFit
must carry their own equations and never reference PyAutoMemory.

### Phase 2 — Formal documentation of the graphical package
**Issued:** PyAutoFit#1333 (2026-07-08) — task `ep-graphical-docs`
(--auto, supervised; worktree ep-graphical-docs).
**Shipped at PR-open (2026-07-08):** PyAutoFit#1334 — new
`autofit/graphical/README.md` (formal spec, 16 numbered equations,
code-anchored) + statistical docstrings (damped update, KL contract,
transform composition convention incl. bug/priors/11 doc half, project
moment matching, F5 fix). Full suite 1422 pass/14 skip; no API changes;
workspace impact none. Merge is human.
Package-level documentation stating the exact Bayesian machinery in formal
equations — factor graph definition, the approximating family
q(θ) = Π q_i, cavity q^{\i}, tilted distribution, moment-matching KL
projection, message update and damping rule, deterministic-variable
handling — written so an AI agent (or human) can verify code against the
stated math line-by-line. Lives with the source (module docstrings and/or
`autofit/graphical/README` + docs pages).

### Phase 3 — End-to-end examples + integration tests
**Issued:** autofit_workspace#81 (2026-07-08) — task `ep-examples-tests`
(--auto, supervised, plan approved in-session; worktree ep-examples-tests).
- New `autofit_workspace/scripts` examples in house style, including a
  step-by-step low-level-API EP run-through in the mould of
  `autolens_workspace/scripts/imaging/likelihood_function.py` (build the
  factor graph by hand, run one EP update per cell, inspect messages).
- Thicken `autofit_workspace_test/scripts/graphical/` integration coverage
  (deterministic variables, EP vs joint-fit parity, convergence on known
  posteriors). Library unit tests stay numpy-only.

### Phase 4 — EP diagnostics and monitoring tooling
**Issued:** PyAutoFit#1335 (2026-07-08) — task `ep-diagnostics`
(--auto, supervised; worktree ep-diagnostics, parallel to the parked
ep-graphical-docs claim, disjoint files).
Built-in tools for analysing a finished EP fit and monitoring a running
one: end-of-example analysis function calls, visuals emitted during EP
(message-field evolution, per-factor KL history), and text/metadata files
in the output folder (iteration log, convergence table, per-factor status).
Design should coordinate with the inspection/aggregation ideas already in
`graphical_scoping.md` (its limitation 3).

### Phase 5 — Deterministic variables reconciliation
**Issued:** PyAutoFit#1336 (2026-07-08) — task `ep-deterministic-reconcile`
(--auto, supervised, read-only).
**Complete (2026-07-08), decision pending:** rhayes777 PR located (#1153,
declarative deterministic via compound priors — its test is commented out);
census: factor_out unreachable from declarative API, compound priors
invisible to EP. Key analysis: compound/shared-variable patterns are
statistically TIGHTER (relation exact inside factors); factor_out trades
exactness for modularity (z gets messages, q(z) factorised from parents).
Recommendation A on #1336: keep both, document trade-off, resurrect the
#1153 test. IC50 needs no migration.
The IC50 cancer use case composes deterministic quantities via the EP
composition machinery (locate the old rhayes777 PR that added this) but
does not use the low-level `deterministic_variable` API in
`autofit/graphical`. Decide: unify on one path, document both, or deprecate
one. Output: a recommendation with migration cost estimate.

### Phase 6 — Analytic likelihood updates (scoping)
**Issued:** PyAutoFit#1337 (2026-07-08) — task `ep-analytic-updates-scope`
(--auto, supervised, read-only).
**Complete (2026-07-08), prioritisation pending:** exact machinery exists +
an undocumented duck-typed analytic-projection contract (ProbitModel /
LinearModel in regression tests). Gap: declarative path never uses it —
PriorFactor wraps the bound method and strips the hooks (in-code TODO at
declarative/factor/prior.py:22), so every declarative EP fit pays one
optimiser run per free parameter per cycle for closed-form updates.
Ranked candidates on #1337: (1) exact PriorFactors ~1 day; (2) document
the contract; (3) first-class linear-Gaussian factor (IC50's global factor
is exactly this shape); (4)/(5) blocked by fix batches.
**Plan filed (2026-07-08):** PyAutoFit#1338 — self-contained 4-WP
implementation plan (plan-only per user; pick-up possibly by Opus).
Backlog anchor: feature/autofit/ep_analytic_updates.md.
Scope exact/conjugate factor updates in the EP source — factors whose
tilted-distribution moments are available in closed form should skip the
sampler entirely. Map which message families and likelihood forms admit
analytic updates, what the API would look like, and expected speed-up
(ties into `ep_scoping.md` performance work).

### Phase 7 — Feature ideation
**Complete (2026-07-08):** 11 provenance-tagged ideas appended to
`PyAutoMind/ideas.md` (`[from: ep-review*]`) — adaptive damping,
block-Gaussian mean field, power EP, EP health report, warm-started
factor searches, StochasticEPOptimiser audit, evidence-correct model
comparison, hierarchical exact updates, resumable EP, JAX-native Laplace,
HowToFit ch3 refresh. No prompts bulk-issued (intake sweeps ideas.md).
From everything learned above, propose further EP features (e.g. richer
message families, structured/correlated approximations, convergence
guarantees/diagnostics, parallel factor updates). Output: provenance-tagged
`ideas.md` bullets or new prompts, not code.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/3589268b-e5c9-4b32-b655-d07f732ea300/scratchpad/ep_review_intake.md; header and phase plan hand-fixed post-apply (title, docs→research, PyAutoFit→graphical_ep, re-homed from docs/autofit/) -->
