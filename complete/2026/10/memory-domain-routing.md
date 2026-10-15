- summary: Campaign records now route by information type: inference through Insight, profiling through Pulse, project-owned detailed evidence, Memory pointers and reusable lessons. Replaced Memory's duplicate A5 summary with links to Insight's already-merged wave records and source catalogue/protocol, preserving pinned provenance. Earlier historical benchmark sections were intentionally outside this bounded task.
- merged: PyAutoBrain#525 (9a708305765a51ec3e6878dc86a1e7f704a700e7) and PyAutoMemory#133 (aa33af1215c89fd6ae8b8ca6f0d863a0253cb48b), 2026-10-15, human /prm.
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/524
- validation: All GitHub Actions runs and jobs at both PR heads passed: Brain Python 3.12 and 3.13; Memory validate. Local Brain 1264 pass plus 4/4 grouped tests with PYAUTO_MIND unset after one environment-only failure; Memory 276 pass and make validate; firewall, scoped discovery and five source links pass. Author review had no findings.
- authorization: Live human Heart RED development override "Proceed"; separate human $prm authorized merge and full close-out. No release. Exact Heart reasons retained in the issue and PR bodies.
- evidence: Local full logs preserved under tmp/memory-domain-routing/validation-logs before worktree cleanup.

## Original prompt

# Route campaign information to Insight and Pulse

Issued: 2026-10-15
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/524
Type: docs
Target: brain
Difficulty: medium
Consequence: judge
Autonomy: supervised

## Original request (verbatim)

The following appears on the live feed of pyautolabs / science, but I think the work its describing belongs under PyAutoInsight, so I wonder if we need to work on routing of memory / permanant information to the right organ in certain cases. I suspect a similar thing could happen with profiling / speed up of code not being routed to Pulse? 📚 Memory
docs(methods): sampler-benchmarks points at the autofit inference search catalogue (search-ext A5 consumers)
PR opened
3h ago
PyAutoLabs/PyAutoMemory · open

3h ago PR opened

## Accepted scope

User agreed that project-owned detailed results stay in autofit_inference, Insight owns campaign records and evidence presentation, and Memory retains pointers plus reusable scientific lessons. User: "ok great proceeed". After the exact Heart RED reasons were reported, user: "Proceed" (development and PR opening only; no merge).

Change @PyAutoBrain routing guidance and @PyAutoMemory's duplicate A5 catalogue section. Insight already has the pilot record in tasks/gaussian_x3_search_wave1.md on main, including 223/520 and no-ranking interpretation; retain that destination and link it rather than creating another summary. Pulse owns profiling campaign intent and evidence presentation; project profiling repos retain measurements; library performance implementation stays in its code repo. No feed changes, compute, historical bulk migration or edits to claimed Insight/Pulse repos.

## Implementation plan

1. Brain ORGANISM.md: explicit routing by information type, not permanence, preserving Cortex science records and Mind implementation history.
2. Brain skills/sampler_pipeline/{SKILL.md,reference.md}: replace blanket durable-findings-to-Memory instructions with Insight/inference and Pulse/profiling routes; Memory only reusable lessons and pointers.
3. Memory AGENTS.md: matching write boundary. Replace only the A5 catalogue summary in wiki/methods/concepts/sampler-benchmarks.md with links to Insight wave-1 record and project-owned catalogue/protocol; update index wording and append log provenance. Preserve older historical evidence pending separate provenance migration.
4. Validate Memory with make validate, Brain documentation/skill checks applicable to changed files, verify destination links from GitHub and review the diff. No scientific API changes; downstream smoke n/a.

## Branch survey

Brain: main, clean. Memory: main, unrelated bibliography and lensing edits; use isolated worktrees. Insight and Pulse: main, clean but claimed by search-ext-b5b2-remainder and ral-category-paths respectively; read-only destinations, no claims requested.

Branch: feature/memory-domain-routing
Worktree: .worktrees/memory-domain-routing (inside workspace)
Tier: judge — merge mode: human /prm
