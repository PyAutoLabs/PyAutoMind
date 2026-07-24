## Outcome — SHIPPED + MERGED 2026-07-24 (PR #89)

Issue #88 closed. The auto-simulate recipe applied with per-dataset BYTE-
identity as the gate — and it discriminated hard: only 4 of 11 dirs are
byte-reproducible (imaging/{euclid,jwst,ao}, interferometer/sma — cmp-
verified) and left the tip (20 files, ~8.5 MiB). KEPT: imaging/hst is
STALE (regen differs every pixel; pinned log_evidence=29110.92 calibrated
to committed bytes — the gate prevented silent corruption of the flagship
benchmark); alma/alma_high (NUFFT float non-determinism — the 46MB/229MB
files CANNOT be uncommitted); source_complex/alma_high_res/hannah (no
producing preset); point_source/simple (autolens precedent). 5
quick_update scripts gained the canonical hook (the only ad-hoc loaders).

## Lessons
- Byte-identity is PER-DATASET empirical, never per-family: same simulator,
  same seed, different instruments -> different verdicts (hst stale vs
  euclid/jwst/ao clean; DFT reproducible vs NUFFT drift).
- should_simulate gates on the DIRECTORY -> removal must be whole-dir.
- tracer.json key-order is non-deterministic everywhere but only
  point_source consumes it.

## Verification
Bootstrap dry-runs (euclid 58.8s, sma 230.9s; regenerated == removed
blobs); build_readme --check unchanged before AND after; ls-files == the
29 kept. RAL submits target only kept datasets — zero walltime risk.
alma_high non-repro is INFERRED (5M-vis regen infeasible locally) — one-
line confirm on real hardware if full closure wanted; stays committed
regardless.

## Original prompt

# autolens_profiling: uncommit regenerable datasets, auto-simulate everywhere

Type: refactor
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised
Blocked-by: profiling-mirror-taxonomy (#84, in flight — paths change; land that first)

User request 2026-07-24 (follow-on to the restructure): the repo should use
the auto-simulate dataset pattern throughout, like the workspaces.

STATE (audited 2026-07-24): the central mechanism ALREADY exists and is
canonical — `_profile_cli.auto_simulate_if_missing` gates on
`al.util.dataset.should_simulate` — but 49 dataset files are still COMMITTED
(per-instrument sets: imaging/{ao,euclid,hst,...}, interferometer/...).

The task (the autolens_workspace_test#213 recipe, post-restructure paths):
1. Classify all 49 committed dataset files: which simulator produces each
   (simulators/ by instrument preset), seed-fixed?, byte-reproducible?
   (verify by regeneration against any consumer assertions/baselines —
   NOTE: results/baselines and runtime comparisons may be calibrated against
   the committed bytes; a changed dataset silently shifts every profiling
   baseline, so byte-identity is REQUIRED, not just statistical equivalence.
   Non-reproducible => stays committed + protective no-standalone-run note).
2. Verify every dataset-consuming script routes through
   auto_simulate_if_missing (most do via _profile_cli); convert any ad-hoc
   dataset exists-checks (distinguish from results-dir exists-checks in
   sweep/aggregate, which are fine).
3. git rm regenerable datasets + gitignore (tip-removal ONLY).
4. Gates: clean-bootstrap dry-run per instrument family; build_readme
   --check idempotent; baseline comparison values unchanged.
5. RAL note: the cluster mirror's dataset/ will regenerate on first run
   after sync — confirm the A100 submit scripts tolerate first-run
   simulation time or pre-provision.
