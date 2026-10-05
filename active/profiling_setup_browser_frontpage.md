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
