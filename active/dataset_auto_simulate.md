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
