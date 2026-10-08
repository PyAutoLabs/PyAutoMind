# PyAutoDNA: software stacks and compatibility

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
