# Linear-solver programme phase 3: GPU/vmap/A100 timing and parity rows for the solver corpus

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: too-large
Autonomy: supervised
Priority: medium
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Filed: 2026-09-24, retargeted: 2026-09-30 (epic linear-solver-programme)
Blocked-by: a release shipping the phase-2 fix (draft/bug/autoarray/raw_pdip_forward_amplitude_bias_fix.md) AND the RAL mirror synced via HPCPullPyAuto
Witness: `scripts/lens/solver/timing.py` rows plus `accuracy.py --device gpu` rows on the phase-1 corpus (`results/lens/solver/corpus/`: slam_fixture_571, slam48_hst, slam_spread_hst, euclid_vis_lp — 81 systems) record, for the SLaM source_lp[1] 60-column model and the captured euclid system, single / vmap16 / vmap50 per-evaluation cost on the RTX 2060 and RAL A100 fp64 for jacobi vs raw (released phase-2 solver), the NNLS share of each batch, and GPU-vs-CPU parity (max |dlogL| and amplitude/`flux_inactive_rel` agreement) on the 48 near-truth vectors — appended to `results/notes/linear_solver_accuracy_2026_09.md` and `wiki/campaigns/linear_solver_accuracy.md`.
Review-minutes: 3
Consequence: glance
Unattended: needs-slicing

Epic `linear-solver-programme`, phase 3. Contract: `complete/2026/09/linear-solver-accuracy-study.md` (phase-1 record with the original programme prompt folded in).

This prompt was filed on 2026-09-24 as a standalone PyAutoArray#571 follow-up (SLaM 60-column GPU
timing and parity, single and vmap). The original ask below now lives in the phase-1
`scripts/lens/solver/` package and its corpus rather than in a fresh
`scripts/imaging/hazards/` script: the SLaM model recipe, the 48 near-truth vectors and the
euclid capture are already corpus systems, so phase 3 adds GPU/A100 cells to that package and
appends rows to the shared ledger. Phase 1 found the released raw stop leaves spurious
amplitude on reference-inactive columns while logL barely moves, so GPU parity must be scored
with `flux_inactive_rel` (and amplitude agreement), not logL alone.

## Context

Context: the 2026-09-24 audit measured only CPU timing for the fix (neutral: 27.3 -> 25.8 ms single, 31.3 -> 30.3 ms/eval vmap16). On GPU the pre-fix behaviour made every Nautilus vmap batch run all 50 PDIP iterations whenever one lane failed (NNLS ~28% of a 2060 batch, ~44% of a single A100 evaluation), so the fix should cut batch cost; that is unmeasured. GPU parity of the raw-forward PDIP is also unmeasured (the audit saw CPU/GPU/vmap divergence on the failing vectors pre-fix).

## Ask

1. Add a new cell to `scripts/lens/solver/timing.py` following the package's `_driver`
   pattern, loading the SLaM source_lp[1] 60-column system and the euclid capture from
   `results/lens/solver/corpus/`; time single, vmap16 and vmap50 per-evaluation cost on the
   RTX 2060 and RAL A100, fp64, with `nnls_preconditioning_no_mapper` forced to jacobi and to
   raw (the released phase-2 solver), interleaved minima.
2. Record NNLS share per config via the existing solve ablation pattern (unconstrained solve
   swap) or `stats["iterations"]`.
3. GPU parity: run `accuracy.py --device gpu` over the corpus (at minimum the 48 near-truth
   vectors); report max |logL_gpu - logL_cpu|, amplitude agreement and `flux_inactive_rel`
   against the CPU fnnls reference, and iterations per lane.
4. Append the rows and a verdict to `results/notes/linear_solver_accuracy_2026_09.md` and
   `wiki/campaigns/linear_solver_accuracy.md` (regenerate README dashboards,
   `build_readme.py --check`); route any regression to /intake as a bug.

<!-- formalised by the Intake (Conception) Agent on 2026-09-24; retargeted into epic linear-solver-programme phase 3 on 2026-09-30 -->
