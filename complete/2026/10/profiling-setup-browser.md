# Pulse setup browser merged

Completed: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/12 (closed)
PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/13 (MERGED)
Merge: 4b00106c664dafd0ed5f690048cad904b1f96061

Shipped the Pulse setup browser with exact pinned v2 catalogue/shard provenance, shared theme, compact campaigns and interactive configuration navigation. Repaired Playwright vendor link checking by selecting only tracked Markdown, and resolved generated-data conflicts through normal ingestion without changing scientific records.

Validation: 189 Python tests, Ruff, offline board/state, Chromium interactions, independent Sol CLEAN. Every exact-head GitHub CI job passed (lint37310560345 including real lychee, refresh37310560357). User explicitly authorized merge in this turn. Heart RED remains `release validation FAILED (stage integrate)`; no release implied.

Scope is the phase3b Pulse frontpage only. Parent draft/feature/pyautopulse/profiling_setup_browser.md retains unshipped later phases; do not retire the parent. Root review/browser artifacts preserved at tmp/heart-red-20261005/pulse-closeout-evidence before cleanup. No irreplaceable science datasets in the worktree.

## Original prompt

# Make Pulse a compact setup-oriented profiling front page

Type: feature
Target: PyAutoPulse
Repos: PyAutoPulse
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-05
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/12

Primary repo: @PyAutoPulse
Classification: standalone organ/workspace, no library changes.
Branch: feature/profiling-setup-browser
Parent: draft/feature/pyautopulse/profiling_setup_browser.md, approved Phase 3.
Upstream: autolens_profiling#377 MERGED publishes v2. Project UI #378 is separately
in review; this consumer uses the catalogue on main, not an unmerged UI branch.

## Approved high-level plan

1. Apply the shared Heart-family theme, Pulse SVG hero and board width.
2. Add Heart-style copy actions and expandable prompts, concise Profiling Check In,
   integrated review metadata and compact campaigns with separate accessible links.
3. Move tasks inside their campaigns and replace the global evidence wall with
   project/dataset/model disclosures and instrument/configuration selectors.
4. Display exact-scoped runtime, breakdown, compilation, memory, settings and
   evidence with linear charts and explicit unknown/unreviewed states.
5. Switch the registered autolens summary to v2, preserve commit-pinned receipts,
   cached/invalid diagnostics and v1 compatibility, and test real browser behavior.

Tier: judge — merge mode: human /prm.

## Detailed plan

- pulse/board.py: use real PyAutoBrain/board/_theme.py via supported sibling or
  PYAUTO_BRAIN location. Keep machine state semantics, markers and read-contract
  diagnostics; HTML foreground is campaigns then scientific navigation. Historical
  transport/freshness/comparison details remain available in a disclosure.
- pulse/campaigns.py: copy Fix Profiling Systematically and editable Profiling
  Check In prompts through accessible buttons plus full-prompt disclosures. Last
  check-in is compact metadata; reviewed dates never become measurement age.
  Campaign table keeps readable rows at narrow sizes and individually labelled
  evidence/task links; per-campaign disclosure holds tasks, priorities and prompts.
  Never mutate campaigns.yaml merely by rendering, and preserve original task text.
- Add a small setup browser renderer/assets for validated snapshots. Use the
  same v2 contract/conventions as the project: project/dataset/model route,
  instrument/exact-source-row selectors, no automatic latest/fastest acceptance,
  metadata beside results and detailed evidence last. The organ remains generic
  across instances, including inline v2 producers without shards and v1 fallback.
- Embed only each validated captured index. Lazy shard URLs and original evidence
  resolve from Snapshot.commit (the captured source), never moving main or the
  producer-code revision. Verify hashes/counts/setup identities, reject stale
  responses, and retain cache/transport qualification beside the displayed data.
- Deep links include instance/dataset/model/instrument/setup; back/forward and
  keyboard work; no-JS source links and missing-data/error states are explicit.
  Linear bars keep single-call, per-replica batch and batch-wall metrics separate.
  No temporal default plots, ratios, cross-project ranking or baseline promotion.
- registry.yaml lens entry reads dashboard/catalogue.json, profiling-summary@2.
  Fetch main once through the normal ingest, regenerate receipts/snapshots/pages;
  all evidence links bind the resulting commit. Add Brain checkout/env to refresh
  workflows so shared theme works in CI, and actual Chromium tests to lint.
- Test copy success/failure, edits, every campaign task/link, schema fallback,
  empty/unavailable/cached evidence, escaping, multiple instances, selectors,
  corrupt/late shards, keyboard/deep links and responsive dark/light layouts.
  Run full Python suite, Ruff, offline board/state checks and browser harness.

## Branch survey

PyAutoPulse canonical main is clean, no other worktree or open PR; origin/main
advanced only generated dashboard material. Use fresh origin/main after fetch.
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-browser.
Start-dev entry Heart: STALE; authoritative ship gate still reports RED
`release validation FAILED (stage integrate)` and will be evaluated after tests.
No task-specific shipping override is inferred from the project #378 override.

## Authorization and original request

Parent Phase 3 already approved. Current live request explicitly continues into
this phase; no new bulk profiling or scientific acceptance is authorized.

Original request (verbatim):

I authroize, continue and do the next phase

Routing correction: the CLI name heuristic says library; this is the approved standalone organ/workspace phase, no scientific/library API edits. Relevant architecture and prior decisions are already in the parent plan and phase records.

### 2026-10-05 repair continuation in the existing PR

Original user request (verbatim):
can we start fixing stuff? Also can this be fixed: [Pulse \#13](<https://github.com/PyAutoLabs/PyAutoPulse/pull/13>) remains unmerged:

- CI still fails at `lychee (markdown link-rot)` on Playwright’s vendor documentation.
- GitHub now also reports merge conflicts.

Current request authorizes repair of existing Pulse issue12/PR13 in this session. Exact known Heart RED remains `release validation FAILED (stage integrate)`. Development repair, tests and updating the same PR only; no new merge or release authority inferred from the prior-session grant.

Plan: resume clean feature/profiling-setup-browser at3c7bed2, same task claim and retained worktree; merge current origin/main without rewriting history. Resolve generated receipt/snapshot/dashboard conflicts by feature's normal v2 ingest at current project commit, preserving exact captured provenance. Limit lychee inputs to tracked project Markdown using a null-delimited array; keep existing authored-document exclusions. Run Ruff, full pytest, offline state/board verification, browser harness and real lychee scope check as available. Push only tested repair, judge exact-head CI once ready. Tier undeclared, human merge.

Root: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-browser/PyAutoPulse. Same Mind task retained; no independent duplicate issue. Original feature plan remains approved. Brain BugDecision config-error/single-repo; fixing locus .github/workflows/lint.yml plus generated conflict reconciliation.

Pulse PR13 repair is ready at63b212c: merged main, resolved generated conflicts through current coherent v2 ingest, restricted lychee to tracked Markdown.189pytest/Ruff/format/offline/Chromium/whitespace pass; independent Sol CLEAN;31 authored Markdown retained and26 vendor files excluded. Current user repair request recorded above; exact Heart reason `release validation FAILED (stage integrate)` remains. Development PR update only; no new merge/release grant assumed. Live network lychee to be judged in exact-head CI.

Final repair CI: head63b212c, lint37310560345 SUCCESS (live lychee included), dashboard refresh37310560357 SUCCESS; GitHub mergeStateStatus CLEAN. Both requested blockers repaired; no PR merge performed.
