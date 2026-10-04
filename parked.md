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
- [catalogue-inspection-before-vis-pix](#catalogue-inspection-before-vis-pix)
- [bootstrap-smoke-codex](#bootstrap-smoke-codex)
- [colab-refinement-throughout](#colab-refinement-throughout)
- [heart-dashboard-remaining](#heart-dashboard-remaining)

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

## catalogue-inspection-before-vis-pix
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/92
- issued: 2026-09-19
- parked: 2026-09-19 — issued but not in flight; registry placement reconciled with human approval.
- repos-none-claimed: No worktree claimed by this entry; resume through start-dev.
- prompt: active/catalogue_inspection_before_vis_pix.md
- classification: workspace
- suggested-branch: feature/catalogue-before-vis-pix
- affected-repos:
  - euclid_strong_lens_modeling_pipeline

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

## heart-dashboard-remaining
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/274
- parked: 2026-10-04 — human requested “wrap up well contnue heart work elsehwere another time”.
- repos-none-claimed: no active repo claims; all eight compatibility branches are merged.
- issued: 2026-10-04
- prompt: active/restore_dashboard_green.md
- status: parked by human; compatibility repair merged; remaining Heart work deferred to another chat
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/restore-dashboard-green
- coordination: Human approved isolated Galaxy dependency-metadata change alongside evaluation-grid-cap-field (merged library PR646; retained workspace release gate); no changes to its files or task.
- heart-red-override:
  - authorization: I authorize development investigation and repair despite the current RED reason above. Follow start-dev and record the task-specific authorization wherever required.
  - reasons: "release validation FAILED (stage integrate)"
  - scope: Heart dashboard repair #274 and bounded timeout investigation; applicable tests and independent review remain required; human /prm only.
  - passed-gates: 9255 full-suite tests (2 skips,5 xfails) across8 repos; independent Sol CLEAN; 25 resolver cases and fresh normal resolution PASS; CPU/CUDA endpoint witnesses PASS; hosted compatibility37210342253 and Heart unit37210342215 PASS at8721c2e. Original comparison inconclusive; broader point-gradient timeout both versions; not release clearance.
- authorization: Human approved phased dashboard repair plan on 2026-10-04; tier undeclared, merge via human /prm. Preserve unfinished work and scientific evidence.
- diagnostic-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/280
- diagnostic-head: 8721c2e3e747561d4cf010fb2a1a6e431224cbb4
- diagnostic-validation: 1222 Heart tests; independent review CLEAN; native LAPACK capture37205459198; original comparison37206724174 remains inconclusive; final-head unit37210342215 and two-endpoint compatibility37210342253 PASS. Original failed release preserved.
- completed-phase: PR279 merged at3d86fd8; complete/2026/10/retired-repo-sidecars.md. Both CI legs passed, issue278 closed.
- validation: Heart1222/Nerves237/Hands472/Fit2959/Array1959/Galaxy1315/Lens820/CTI271 tests PASS; independent Sol CLEAN; package/CPU/CUDA/hosted endpoint checks PASS. All28 current-head CI jobs passed before merges.
- resume: All8 PRs merged after28/28 exact-head CI jobs passed; freeze clear. Completion phase record complete/2026/10/jax-lapack-compatibility-repair.md. Protected Nerves must publish first; release not authorized. Keep #274 and retained worktree open for remaining dashboard scope, original validation failure and point-gradient timeout. Anthropic blocker handed to separate chat at human request; untouched here.
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/184
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/184
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/297
- pending-release: PyAutoHands@https://github.com/PyAutoLabs/PyAutoHands/pull/297
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1659
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1659
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/647
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/647
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/280
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/280
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/612
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/612
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/766
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/766
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/112
- pending-release: PyAutoCTI@https://github.com/PyAutoLabs/PyAutoCTI/pull/112
- retention: Keep the existing worktree and all science/dataset/diagnostic products. Do not remove or reset it as close-out cleanup.
