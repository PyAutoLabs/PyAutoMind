# Inference task ownership

PyAutoInsight owns inference campaign intent and pending domain tasks. Its
campaigns.yaml, tasks/, CHECKIN.md and migration.yaml provide one entry point.
Cortex retains scientific runs, observations and human conclusions. Projects
retain results and execution; Mind retains bounded implementation PR lifecycle,
repository claims and mixed library/production epics.

## Migration landed 2026-10-04

Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/1
Source commit: 8dd1edc7e04c960daae3663513c61395823eddb0.
Five complete prompts and one NUTS/HMC idea fragment are preserved byte-for-byte
with SHA256 mappings in Insight/migration.yaml. Audit dispositions cover 99
candidates from 249 current draft/active/registry files.

- prior-centering after Galaxy fix: remains blocked until release verified;
- Cortex documentation reconciliation: completed by merged inference PR18; preserved original task remains available in Insight;
- EP campaign, EP scoping and graphical scoping: preserve phased/decision gates;
- NUTS/HMC trial on validated likelihoods: needs human decision.

Mixed library implementation epics and scientific run ledgers remain in their
own repositories; the audit explains each retained candidate. Eight campaign
rows link authoritative Cortex/project evidence. Historical job ids are not
proof of jobs running today.

## Landing evidence and source removal

Destination [PyAutoInsight PR #2](https://github.com/PyAutoLabs/PyAutoInsight/pull/2)
merged at `aabc4869410824a62cf1816925cda7f88994b95a` before any source deletion.
Producer [autolens_inference PR #18](https://github.com/PyAutoLabs/autolens_inference/pull/18)
merged at `26778b158538711a5a79acbadb0699a103446bd7`.

The cleanup verifies the destination merge is an ancestor of fetched Insight
main and checks each destination file directly at that merge commit against
its migration SHA256. All five source files match the recorded original bytes;
the NUTS/HMC idea fragment matches exactly. These originals have now been
removed from Mind's pending queue, with the campaign/scoping ledger references
repointed to Insight. The remaining ideas about library implementation retain
Mind ownership and link the migrated scoping contracts as dependencies.

Mind's graphical-ep and autolens-inference epic entries preserve implementation
history and links, without independently scheduling domain campaigns. All
Cortex run records, observations and human conclusions remain untouched.
The original migration audit retains pinned source revisions and dispositions;
resolve historical Mind paths through Insight `migration.yaml`. Immutable
completion history is not rewritten. The organ-development lifecycle remains
open until deployment verification and normal close-out finish.
