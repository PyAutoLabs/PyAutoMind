# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; on shipping,
write the dated `complete/<YYYY>/<MM>/<slug>.md` record instead.

<!-- toc:start -->

**Contents**

- [single-source-density-design](#single-source-density-design)
- [prior-message-collapse-design](#prior-message-collapse-design)
- [fixed-light-numba-s7](#fixed-light-numba-s7)
- [bootstrap-smoke-codex](#bootstrap-smoke-codex)
- [colab-refinement-throughout](#colab-refinement-throughout)

<!-- toc:end -->

## single-source-density-design
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1500 (open — the parked design hub)
- prompt: draft/bug/priors/12_single_source_density_refactor.md
- parked: 2026-08-18 — **human-confirmed deferral** of the design decision (census wrap-up chat).
  The bundled 12+13 design issue is filed with full evidence and four decision asks
  (one-hierarchy-vs-two, #1498 logpdf contract, EP-mixin scope, prompt-14 sequencing); nothing is
  blocked by deferring — bugs are fixed and the #1497/#1499 property sweep (134 tests, merged
  `21288bb`) guards current behaviour regardless.
- classification: refactor design (PyAutoFit); DESIGN ONLY — no code until #1500 is answered.
- resume: answer the decisions on #1500, move this back to active.md, cut stage-1 as its own task
  (Distribution sibling layer, Gaussian family first, property tests as the safety net).
- note: bug/priors/15 (#1498 — TransformedMessage.logpdf missing Jacobian) is a LIVE wrong answer,
  not part of this deferral; it can be fixed standalone once the contract is picked.
- repos-none-claimed: claims no repos while parked.

## prior-message-collapse-design
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1500 (shared — bundled with single-source-density-design)
- prompt: draft/bug/priors/13_collapse_prior_and_message.md
- parked: 2026-08-18 — same human-confirmed deferral; prompt 13 is the hierarchy-collapse half of
  the #1500 bundle. Resume and retire together with single-source-density-design.
- repos-none-claimed: claims no repos while parked.

## fixed-light-numba-s7
- archived-proposal: complete/archive/shelved/fixed_light_numba_s7_cpu_verdict.md
- parked: 2026-09-18 — user explicitly shelved phase7 before implementation.
- decision: Assume no usable memo benefit and changing sampler order for current planning. Further memo-policy and sampler-order/history research out of scope; production defaults unchanged.
- evidence: Phase5/5b/6 findings remain in completed records and merged profiling results.
- resume: Only on explicit user request; rescope before issue/worktree/compute creation.
- repos-none-claimed: No issue, worktree, source changes or jobs created for phase7.

## bootstrap-smoke-codex
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/144
- parked: 2026-10-02
- status: queued (human-deferred) — requested quicker wrap after inference PR
- prompt: active/bootstrap_smoke_codex_and_bench_pr.md
- classification: workspace
- suggested-branch: feature/bootstrap-smoke-codex
- bundle: assistant
- affected-repos:
  - autolens_assistant
- resume: Plan approved and issue created; implementation not started. Reuse approved issue plan, survey current claims, and resume through start_workspace. No branch or PR created for this member.
- carry-forward: Preserve bench/bootstrap-smoke-stage-b; approved plan carries 7ca904b, add0556, ca19325 to fresh member branch before one Codex v2 run.

## colab-refinement-throughout
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/145
- parked: 2026-10-02
- status: queued (human-deferred) — requested quicker wrap after inference PR
- prompt: active/colab_refinement_throughout.md
- classification: workspace
- suggested-branch: feature/colab-refinement-throughout
- bundle: assistant
- affected-repos:
  - autolens_assistant
- resume: Plan approved and issue created; implementation not started. Reuse approved issue plan, survey current claims, and resume through start_workspace. No branch or PR created for this member.
- scope: Existing Colab skills/setup/Ring notebook only; extra Teacher/SLACS notebook twins deferred.

