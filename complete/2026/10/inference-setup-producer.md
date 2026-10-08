# inference-setup-producer

Completed: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/20
PR: https://github.com/PyAutoLabs/autolens_inference/pull/21
Merge: de37acfe797465205128d45973af5e853c74a684

## Shipped scope

Published inference-summary v2 alongside v1 with 56 original records, preserved record IDs, parent/stage links, archived evidence and historical result/output paths. Defined imaging rectangular/Delaunay instrument setups and simple point-source setup identities; historical unknowns stay explicit and no baseline is promoted. Migrated baseline leaves and HPC/CI callers while retaining original measured wall-rate provenance and explicit current aliases.

Added frozen mass_total[1] manifests: exact dataset, model, priors, executable model/analysis snapshots, content hashes and actual imported library revisions. Portable metadata is retained under tracked prepared/ while bulk snapshots remain local. Baseline likelihood/parameters/posterior evidence is captured independently of scientific acceptance. Added setup-specific Nautilus/Emcee/NUTS/SMC leaves over one shared runner; cold/warm/resume states are distinct from compilation/cache. Warm recipes preserve priors; Emcee resume copies a pinned checkpoint into a new measurement and handles interrupted HDF allocation.

## Validation and decisions

120 tests, Ruff check/format, README/export freshness, all14 wall contracts and six import/setup smokes passed. Real small Imaging frozen-artifact roundtrip and loaded likelihood passed; Emcee/Nautilus validate-only paths passed. Independent review found and closed nine concrete defects before CLEAN, then independently reviewed the setup/sampler navigation follow-up CLEAN. Portable fresh-clone declarations, executable-model tamper refusal, canonical imports, clock immutability and interrupted checkpoint cases have regression coverage.

Exact-head CI run https://github.com/PyAutoLabs/autolens_inference/actions/runs/37751508172 on158710ffd4bd4097c2f011ee0ef3fe49f0cec2e3: lint job and every step succeeded, including lychee and smoke. PR merge state and merge SHA verified; feature HEAD is an ancestor of origin/main. Issue is CLOSED.

Heart STALE: release validation incomplete, no rehearsal for current source. Current explicit human authorization covered implementation and in-turn merge on passed gates; no compute, release or scientific acceptance was performed.

## Limits and handoff

Nautilus baseline warm starts and NUTS/SMC kernel resume are explicitly unsupported rather than fabricated. Frozen reuse requires the same scientific controls and source revisions. No full scientific baseline or HPC jobs ran. Worktree cleanup deferred by explicit root instruction: producer/browser reviewers and symlink consumers still depend on it. Existing committed evidence has zero prepared problems and no accepted baseline; implementation supports future baseline export and reuse without inventing historical artifacts or scientific acceptance. Phase2 complete; browser and assistant adoption remain separate phases.

## Original prompt

# inference-setup-producer

Type: feature
Target: autolens_inference
Repos: autolens_inference
Difficulty: large
Consequence: judge
Autonomy: supervised
Priority: high
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/20
Epic: inference-setup-redesign (phase 2)

## Authorization

Human: "prm, and continue through all phases autonomously to the end".
The approved five-phase design and original request are preserved in
draft/feature/pyautoinsight/inference_setup_redesign.md. Phase1 merged Insight#14.
Explicit current authorization covers implementation and merge/close-out on
green checks of all remaining approved phases. No compute, science acceptance
or release. Tier: judge — merge mode: human-authorized in-turn merge after
independent CLEAN review, required tests and every CI job pass.

## Plan

Publish a v2 setup catalogue alongside the existing v1 summary. Define stable imaging rectangular/delaunay and point-source setup identities, explicitly retain unknown and archived evidence; no promotion. Reorganize runnable leaves into scripts/<dataset>/<model>/baseline_slam.py or baseline.py; update all callers, wall-rate cell identifiers, CI/docs without relabelling old results. Keep shared scientific model builders. Add an explicit prepared-baseline artifact manifest with content hashes, exact dataset/model/prior/stage identity and baseline likelihood/parameter/posterior evidence; implement export/reuse validation and cold/warm/resume distinction separately from JIT/cache state. Provide sampler stage investigation entrypoints for supported samplers only, preserving scientific model/prior/adapt state; inspect installed APIs instead of guessing. Add setup wiki summaries and document reproducible CLI from completed baseline to mass_total[1] experiment. Tests must cover mappings, retained provenance, artifact identity failures, start semantics and shared problem reuse. No full science runs or HPC jobs. Full existing checks and meaningful small smoke only. Coordinate exporter with merged Insight v2 contract; if contract needs a compatible refinement report to root. Do not fake runnable NUTS/SMC support where APIs or artifact resume are unavailable; expose an honest unsupported path and explain remaining work to root.

## Survey

@autolens_inference: canonical main, no active claim at survey. Isolated worktree under
/home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-producer, branch feature/inference-setup-producer.
Preserve all unrelated canonical untracked data. Source setup through start_workspace.

## Original request

prm, and continue through all phases autonomously to the end
