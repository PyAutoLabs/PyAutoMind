# PyAutoDNA: software stacks and compatibility

Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/509
Issued: 2026-10-08

Type: feature
Target: pyautodna
Difficulty: large
Priority: high
Consequence: judge
Autonomy: human-required

## Original request (verbatim)

We had to recently do a JAX versioning investigation where CI broke against local or something (look it up October 4 2026).

I now realise we should have software and project stack versioning properly, as part of the PyAutoScientist dashboard.
This could go under PyAutoNerves, its similar to config but would be probably the main high level thing it now
manages. However, it does feels a bit higher level and distinct from Nerves, so could maybe warrant its own organ?
Do some research and give me your recommendaiton.

I am picturing a world where this ensures I am frequently on my local stack on the latest version of libraries
and that RAL is too. Furthermore, it should give me a good overview of what version were on, whats supported,
sometimes maybe why we have certiaon version supported and the general tools required to do update campgins and check
dependencies and make sure we are not supporting unsupported. OH and also remember that CI oten has its own
versions to get stuff through, and Python 3.12 vs 3.13 is also a thing. So yeah, high level dashboard management
of the entire versioning stack.

This should also coordiunate the different versions we have, we have like the latest but that doesnt correspond
to whats in the source code? I'm still not sure about that design but the dashboard should make it more manageable.

## Subsequent user instructions (verbatim)

This sounds excellent, make sure the format and structure follows the now standard design implemented throughout all dashboards. Thoughts on organ name?

What about DNA? I like both that and Skeleton

DNA it is! go

## Accepted design and authorization

User approved the research recommendation and named the new organ PyAutoDNA.
Implement the three proposed phases: inventory/dashboard; support policy/shared
profiles; upgrade campaigns/adoption. This is ordinary development, not --auto;
merge remains human /prm. Existing environments are observed, not upgraded as a
side effect of collection or dashboard refresh. No scheduler is armed by this run.

DNA owns environment registry, immutable stack specifications, support rationale,
inventory receipts, campaign/adoption history and board. @PyAutoBrain coordinates
upgrades; @PyAutoHeart retains validation/readiness authority; @PyAutoHands retains
release provenance/execution; @PyAutoNerves retains runtime compatibility/config;
@PyAutoMind owns implementation tasks and identity; @PyAutoScientist is the entry.
Package pyprojects remain authoritative requirements, not manually copied policy.

Distinguish upstream available, declared compatible, tested, recommended and
observed. Identify source checkouts by SHA/dirty state/import path, distributions
by metadata/origin, releases by wheel/source mapping and workspaces by API floor.
Never compare frozen source __version__ stamps to wheels as an equality gate.
Capture Python/platform/backend, packages, git identities, relevant flags and
GPU runtime metadata; remote/missing evidence is unknown, never green.

## Implementation plan

1. New PyAutoDNA repository: dna/{schema,inventory,policy,campaigns,board,cli}.py,
   schemas/, environments.yaml, stacks/, decisions/, campaigns/, docs/, tests/;
   CLI supports collect, compare, audit, campaign inspection and board rendering.
   Inventory is captured in the actual interpreter after installation; validate
   input schemas, timestamps and stable identities. Public output excludes local
   paths/host/user data; private raw receipts stay outside published artifacts.
2. Reuse Brain board/_theme.py hero/navigation/orchestration_panel/JS and validate
   state.json with board/_state.py. Responsive environment, compatibility,
   decisions and campaign views; standard copy-preview/work-links/refresh footer.
   Add CI and Pages workflow, tests for degraded evidence, escaping, comparisons,
   constraints, provenance, campaign transition gates and public projections.
3. Register DNA in Mind repos.yaml; update Brain ORGANISM.md, config/policy.yaml,
   shared theme organ/heading/navigation definitions and Scientist integration.
   Generate only claimed consumers using repos_sync; keep remaining adoption
   explicit. Brain is currently claimed by board-one-click-update: permission to
   coordinate requested; do not edit overlapping repository pending response.
4. Policy records link October 4 JAX incident and existing floors-not-stamps
   decision; preserve reproduced versus source-inferred exclusions and partial
   test coverage. Named profiles separate Python 3.12/3.13 and CPU/CUDA; no
   invented current versions or certifications. Audit resolved installs against
   repository declarations and recorded baseline; report CI overrides/rationale.
5. Campaigns record target stack, linked Heart validation, environment adoption,
   retained rollback stack, owner and review date. Produce reviewable upgrade
   proposals; promotion needs matching successful evidence and explicit action.
   Existing scientific runs retain recorded environments. Document local/RAL/CI
   collection and adoption procedure and proposed cadence without enabling cron.

## Evidence and validation

Historical evidence: complete/2026/10/jax-lapack-compatibility-repair.md;
complete/2026/10/restore-dashboard-green.md; complete/2026/08/release-version-sync-back-to-main.md.
Shared standards: Brain docs/standards.md and board-{sizing,navigation,orchestration}.md.
Run focused and full DNA tests, relevant shared theme/Scientist integration tests,
schema/feed validation, real local inventory and comparison, static HTML and
browser interaction checks where available. Never substitute fixtures for live
RAL/CI observations; label uncollected surfaces. Obtain Heart verdict at ship.

Suggested branch: feature/pyautodna-stack-management
Tier: judge — merge mode: human /prm

## Coordination and execution

Human explicitly allowed coordinated Brain changes on 2026-10-08. Preserve board-one-click-update changes and use a separate worktree. Bootstrap source changes are confined to DNA, Brain, Mind identity, Scientist; the other organs supply evidence, not source edits. Feature classifier recommended workspace flow based on mixed organ references; use generic worktree/library source mechanics for these infrastructure repositories (no scientific workspace scripts).

## Implementation checkpoint — 2026-10-08

- Implemented locally on feature/pyautodna-stack-management in .worktrees/pyautodna-stack-management (DNA, Brain, Mind, Scientist). Source edits remain uncommitted pending ship gate; new DNA canonical repo has only empty bootstrap commit 8a6ae0c and no GitHub remote yet.
- DNA includes immutable inventory/spec/audit/campaign records, explicit promotion/adoption/rollback evidence gates, upstream lookup, two-inventory diff, public export, standard board/feed and manual CI/Pages workflows. Shared theme, body map and Scientist integration are prepared. User explicitly authorized coordinated Brain changes; preserve board-one-click-update.
- Real local inventory: Python 3.12.10, JAX/JAXlib 0.10.2. RAL shared venv login observation: Python 3.12.4, JAX/JAXlib 0.10.2. Audits against current canonical declarations expose both environments' excluded JAX/JAXlib plus RAL anesthetic 2.8.14. No environment upgraded; RAL CPU/GPU compute-node and CI observations remain unknown.
- Tests: DNA 18 unittest cases; Brain 1251; Mind 696; Scientist 14. Brain/Mind suites require clearing inherited PYAUTO_ROOT/PYAUTO_MIND/PYAUTO_BRAIN for fixtures, after sourcing activate.sh; initial environment-contaminated failures reproduced on baseline. Independent Sol review CLEAN for core and board after fixes. Twelve browser viewport/light-dark cases pass, including copy/preview/keyboard/Unicode/anchors; source/feed/YAML checks pass.
- Logs: worktree dna-{brain,mind}-cleanenv.log, dna-scientist-final.log, dna-browser-final/results.json; DNA .scratch/final-tests.log and raw private receipts. Public allowlisted projection inventories/public.json omits paths/account names/install origins/runtime flags.
- Preview: PyAutoDNA/_site/index.html. Live publication has not occurred. Generated maps updated only in claimed consumers using isolated generation scope; remaining global propagation belongs to merge close-out.
- Ship gate from Brain vitals: YELLOW85. Exact yellow reason: "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml". Evidence names unregistered COWLS_COSMOS_Web_Lens_Survey checkout, unrelated to this feature. Stale reason: "release validation incomplete: no rehearsal for current source". Human acknowledgement requested via async question; no answer received yet. No source push/PR or merge authorized through this gate yet.
- Next: obtain acknowledgement of that exact YELLOW reason (or refreshed permissible verdict), create public PyAutoLabs/PyAutoDNA with empty main bootstrap preserving history, commit/push the four feature branches and open dependent review PRs. Merge order Mind identity → Brain shared component → DNA → Scientist; human /prm remains required. Configure Pages only with the appropriate merge/publication step. Do not close #509 before all consumer work lands.

## PR-open checkpoint — 2026-10-08

Human acknowledged the recorded Heart YELLOW warning with “yes proceed”. Re-read readiness returned the same YELLOW85 receipt and exact reasons above; development shipping only, no release or merge. Created public PyAutoLabs/PyAutoDNA with preserved empty bootstrap main and pushed feature branches.

- https://github.com/PyAutoLabs/PyAutoMind/pull/494
- https://github.com/PyAutoLabs/PyAutoBrain/pull/510
- https://github.com/PyAutoLabs/PyAutoDNA/pull/1
- https://github.com/PyAutoLabs/PyAutoScientist/pull/51

Source commits: Mind 1de20993; Brain b83a616; DNA 69642c3; Scientist a17a009. Saved validation: 1,979 tests plus 12 browser cases; source whitespace normalized during staged diff check. Applicable live CLI/render/feed smoke passed; scientific workspace migration/smoke is not applicable because scientific APIs/scripts are unchanged.

Status: library-shipped, awaiting-merge. Merge via human /prm in Mind → Brain → DNA → Scientist order. DNA CI consumes Brain main and requires its shared-theme change. Pages configuration/publication and remaining generated-map propagation belong to post-merge close-out. Do not close #509 until all consumers land. No environment upgrades, scheduled jobs or compute submissions performed.
