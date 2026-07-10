# Multi-dataset shared-state — Phase 1: design lock-in

Phase 1 of 4 of `feature/autolens/multi_shared_state_examples.md` (read the
parent prompt first — it carries the user's request verbatim, the PyAutoReduce
registration semantics, and the use-case table). Deliverable: a **design note +
locked API sketch** recorded on the GitHub issue (no source edits), the pattern
of `oversampling_phase_1_design.md` / `kxs_phase_1_design.md`.

## Questions the design must resolve

1. **What is shareable for imaging?** Unlike the datacube (channel-invariant
   `uv`/`noise` → share `F = LᵀW̃L` + mapper), imaging exposures have
   per-dataset PSFs and pixel offsets → neither `F` nor the mapping matrix `L`
   is invariant. Candidate shared object: the **source-plane Delaunay mesh
   geometry** (image-mesh sparse grid traced once from the lead dataset), with
   each dataset building its own `L_i` by tracing its offset grid onto that
   shared mesh. Quantify what this actually saves (mesh construction +
   triangulation vs per-dataset L/F builds) before committing — if the
   shareable fraction is small, the honest answer may be "share the mesh for
   *consistency*, not speed" and the design should say so explicitly.
2. **Same-wavelength "one reconstruction" semantics.** The user wants one
   source reconstruction for all same-λ exposures. A genuinely joint solve
   (`F = Σᵢ LᵢᵀWᵢLᵢ`, `D = Σᵢ Lᵢᵀdᵢ`, one `s`) does **not** decompose into the
   per-factor likelihood sum that `FactorGraphModel` computes — decide between:
   (a) a joint-inversion Analysis that owns all N same-λ datasets (one factor),
   (b) per-factor reconstructions with the mesh shared (N reconstructions that
   happen to live on the same mesh — not literally one source), or
   (c) shared-state carrying the joint solve with per-factor likelihood
   contributions derived from it. Option (a) may be the truthful model; the
   design must pick one and justify it against the FactorGraph contract
   (sub-task A's "shared object computed once, forwarded to factors").
3. **Different-wavelength semantics** are cleaner: shared shifted mesh,
   independent per-dataset reconstructions (colour) — confirm this is just
   "share mesh geometry only" and falls out of whichever mechanism Q1 picks.
4. **Shift mechanism.** `aa.DatasetModel` already provides per-dataset (y,x)
   offset (+ rotation) as optional free parameters (see
   `multi/features/dataset_offsets/`). Design how DatasetModel offsets compose
   with the shared mesh: the mesh is built once in the source plane; each
   dataset's offset applies to its image-plane grid before tracing. Default =
   shifts known/fixed (from PyAutoReduce `target_pixel` differences); optional
   free (dy,dx) with Gaussian priors of width = registration residuals
   (floor ~0.1–0.3 px). Simulator support: per-dataset shifts in the relevant
   `simulator.py` scripts, default 0.
5. **imaging_and_interferometer**: how the shared mesh crosses the two dataset
   types (imaging preloads vs the existing `PreloadsInterferometer`).
6. **Preloads API shape**: `PreloadsImaging` fields (mesh/mapper geometry vs
   `mapper_galaxy_dict` reuse), what `AnalysisImaging.shared_state_from`
   returns, and JAX pytree registration (recompute inside the jitted region
   each eval — no instance memoisation; see `feedback_jax_closure_cache_busts`).

## Grounding (verified 2026-07-10)

- Only the interferometer consumer exists (`aa.PreloadsInterferometer`,
  `AnalysisInterferometer.shared_preloads`/`shared_state_from`); no
  `PreloadsImaging`, nothing on `AnalysisImaging`.
- The `multi/` examples already use `af.FactorGraphModel(*factors, use_jax=True)`
  — the sub-task A mechanism (`shared_state_from` + `shared=`) applies directly.
- `aa.DatasetModel` (PyAutoArray `dataset/dataset_model.py`) is the existing
  offset/rotation surface, demonstrated in `multi/features/dataset_offsets/`.

## Process

- Consult `autolens_assistant/` (AGENTS.md → relevant `skills/`/`wiki/core/`
  pages) before locking the source-reconstruction design; PyAutoMemory
  `lensing_wiki`/`methods_wiki` for source-reconstruction + likelihood context.
- Output: design note on the issue (options weighed, decision + rationale per
  question above, locked API sketch for Phase 2, example-script outline for
  Phase 3). Phases 2–4 prompts get updated with the locked decisions.
