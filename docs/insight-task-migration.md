# Inference task ownership

PyAutoInsight owns inference campaign intent and pending domain tasks. Its
campaigns.yaml, tasks/, CHECKIN.md and migration.yaml provide one entry point.
Cortex retains scientific runs, observations and human conclusions. Projects
retain results and execution; Mind retains bounded implementation PR lifecycle,
repository claims and mixed library/production epics.

## Migration prepared 2026-10-04

Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/1
Source commit: 8dd1edc7e04c960daae3663513c61395823eddb0.
Five complete prompts and one NUTS/HMC idea fragment are preserved byte-for-byte
with SHA256 mappings in Insight/migration.yaml. Audit dispositions cover 99
candidates from 249 current draft/active/registry files.

- prior-centering after Galaxy fix: remains blocked until release verified;
- Cortex documentation reconciliation: implementation in inference PR18;
- EP campaign, EP scoping and graphical scoping: preserve phased/decision gates;
- NUTS/HMC trial on validated likelihoods: needs human decision.

Mixed library implementation epics and scientific run ledgers remain in their
own repositories; the audit explains each retained candidate. Eight campaign
rows link authoritative Cortex/project evidence. Historical job ids are not
proof of jobs running today.

## Landing order and current status

Producer PR18 and Insight destination must merge before source deletion. The
initial registration PR deliberately leaves all Mind originals intact. Once
Insight destination merge is verified, run its migration cleanup, regenerate
Mind registry contents/dashboard, and validate lifecycle/ledger round trips.
Until then, migration is prepared, not complete. No completed record or claim
release may assert otherwise. Immutable completion history is not rewritten.
