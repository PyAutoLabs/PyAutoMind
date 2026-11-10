# PyAutoFit compact corner array adapter

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_profiling
Classification: Both (library plus experimental benchmark workspace)
Consequence: judge
Autonomy: supervised
Epic: nautilus-fast-likelihoods
Phase: experimental phase1 output optimization

## Scope and authority

Original request (verbatim): "ok this sounds like a worth while thing to do, can we do this and also start some of the other CPU sampler speed up work?"

Experimental continuation of nautilus-fast-likelihoods. Outside Pulse; no campaign registration, HPC submission or release. Full phase0b remains incomplete. Tier: judge — merge mode: human /prm. Status: proposed, awaiting plan approval and extension of the development Heart RED override to this new library-optimization scope. Current authoritative RED reasons: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure" (2026-11-10T15:48:37.310808+00:00).

The existing diagnostic PR autofit_profiling#13 is open and green at2c3c0aa. Keep it unmerged and retain every old worktree/raw archive. These are new bounded implementation members, not additional changes slipped into that diagnostic PR. Register one issue/implementation PR per member after approval. Use isolated feature branches and serialize coding claims for PyAutoFit/autofit_profiling under the same session; explicitly transfer only this session's profiling claim, recording the pending diagnostic PR/retained worktree. Use a profiling branch based on the diagnostic head where its helpers are needed, label that dependency, and never merge its base automatically. No source edits in canonical main or pinned dependency archives. Library-first merge gates remain human.

Library survey: canonical PyAutoFit main clean atbdb7af0e9, no other active PyAutoFit coding claim in Mind. Existing plotting fixes already defer shared-axis handling and avoid duplicate pyplot draw. Profiling claim belongs to nautilus-30d-diagnostics; resolve its same-session handoff explicitly during setup. Recheck refs/claims before creating worktrees. Pin the baseline and candidate dependencies; never update the retained environment in place.

Implementation owner: @PyAutoFit. Experimental benchmark owner: @autofit_profiling.

## High-level plan

1. Add an opt-in compact-corner adapter in PyAutoFit, without modifying installed anesthetic code or globally patching its functions.
2. Prepare arrays once, reuse eligible per-column weighted quantiles, and call lower-level plotting functions instead of the per-panel dataframe dispatcher.
3. Preserve scientific and visual semantics on the supported path; use the existing backend for unsupported options/data.
4. Validate equivalence, then compare baseline/candidate in repeated, interleaved runs. Keep output attribution separate from sampler speed.

## Detailed implementation

- Proposed branch feature/nautilus-compact-plot-adapter in a new claimed PyAutoFit worktree.
- Add autofit/non_linear/plot/compact_corner.py and route from nest_plotters.corner_anesthetic. Add compact_backend setting in autofit/config/visualize/plots_settings.yaml, default anesthetic; explicit array selects candidate. Resolve backend setting before generic kwarg forwarding. Existing public style/error/parameter-subset behavior remains.
- First supported fast path: compact lower hist_2d, diagonal kde_1d, upper disabled, linear axes and finite float64 samples with supported weights/options. Prepare sample matrix/weights once; retain all points and original weights. Cache quantiles only within the current figure and for equivalent column/weight/q inputs. Preserve bins, density/levels, colors/alpha, legend, axis labels/ranges, twin axes and existing deferred shared-axis pass.
- anesthetic.hist_plot_2d computes quantiles before consuming its range kwarg, so merely passing ranges does not remove that cost. Implement a small PyAutoFit-owned histogram helper for the narrowly supported compact path using precomputed bounds, NumPy histogram2d and Matplotlib pcolormesh. Keep lower-level anesthetic KDE for diagonal semantics. Document the supported behavior instead of copying a whole plotting library.
- Unsupported styles, nonfinite/pair-dependent masks, custom unhandled options, incompatible dependency versions or weight forms use the original path before partial plotting starts. Do not silently swallow caller errors or cache across plots. Extend keyword validation/tests accordingly.
- No tick suppression, changed typography, sample thinning, altered bins, lost cross-parameter panels, KDE approximation, sampler/configuration change or global monkeypatch. Rendering time may remain substantial.

## Validation and compute

Extend test_autofit/non_linear/plot/test_nest_plotters.py plus focused adapter tests. Real-runtime tests cover weighted/unequal/zero weights, repeated labels, subset order, constant columns, supported quantile options, explicit options, fallback/error cases and no persistent global state. Compare numerical densities/bin edges/weights/limits/twin alignment and same-runtime rendered pixels (exact where deterministic; any tolerance must be declared before benchmarking and justified). A fallback must produce the established output, not a blank success.

Run required PyAutoFit suite and applicable smoke, both supported Python CI versions, and profiling tooling checks. Preserve existing default backend. Freeze code before measurement.

One bounded pilot: three paired full wrapped-output replays from the same original30D checkpoint, baseline versus candidate, interleaved AB/BA/AB. Same33984samples/weights,12x12in/100dpi compact output and warm font-cache policy; zero native sampling, at most one scoped final-summary timing evaluation per case (required on completed success). Six children maximum,240s/4096MiB per child,1800s aggregate including preflight. The240s cap is an explicit new allowance for matched full-finalization witnesses, not a relabelled prior120s run. One worker/native threads1; existing host/memory guards. Stop on correctness failure, cap or unexpected error; no automatic retry or cap escalation. Use new experiment directories and retain unrun cases.

Report per-pair ratios, median/range, plot stages, full-wrapper/process time, memory and all failures. Three repeats are exploratory; no statistical or production-default claim. If equivalence fails or benefit is not convincing, leave default unchanged and report the candidate as unproven. No prescribed speedup invented after results.

## Execution phases within this approval

Brain feature routing classified this as large library work. Keep three sequential gates: (A) compatibility/design and deterministic correctness tests; (B) opt-in implementation plus parity or interruption/resume witnesses; (C) the stated bounded paired pilot and development PR. Do not start C if B fails. Approval covers these stated phases only; changing scientific semantics, defaults, resource caps or external-library source requires a new decision. No independent agent delegation requested; execute sequentially.
