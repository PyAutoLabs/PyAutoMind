# Profiling research wiki for autolens_profiling

- Work type: docs
- Target: @autolens_profiling (workspace-type repo; no library change), @PyAutoMind (epics.md ledger pointers)
- Epic: profiling-research-wiki (new)
- Autonomy: human-required
- Filed: 2026-09-27 from a review session
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/337
Issued: 2026-09-27

## Original prompt

I have been chugging away with a lot of autolens_profiling work, on all the different likelihod
functions. I think its going well, but at times I am unsure if its improving or speeding up the
code and a few tasks I lost track of quite why they were being done. [...] Also be sure we are
building the research wiki of all this work so the profiling work we do is kept and tracked.

[after the review] I agree the situation with the wiki is a problem and we need to be building it
as we go, so action that.

## Review findings that motivate this (2026-09-27)

- There is no wiki. `results/notes/` holds 74 files / 28,474 lines; 38 % is committed `.out` job
  logs and JSON sidecars. The only index, `results/notes/profiling_campaign_status_2026_09.md`,
  covers fixed-light + HST GPU residue only (0 mentions of point-source or interferometer).
- Mind `epics.md` lists 2 profiling epics; September `complete/` records tag 9. The other 7
  ledgers were archived to `complete/archive/epics/` or never existed.
- The "why" of each phase (question + pre-registered go/no-go rule) lives in 10–14k-character
  GitHub issue bodies and Mind `## Original prompt` sections, not in the profiling repo.
- Stale release labels: PyAutoArray #553–555 are in 2026.9.19.1 and #576/#578 in 2026.9.27.1
  but `profiling_campaign_status_2026_09.md` / `results/README.md` still say pending.
- The README dashboard (`build_readme.py`) renders only the sweep matrix; campaign findings are
  21 hand-written bullets under "JAX gradients and compile time" and skip point-source 4a–4c,
  HST residue p2/p4, certified solver, Delaunay-NN series, numba-interferometer, numpy-deflections,
  gaussian-precompute.

## Scope

1. `wiki/index.md` — one row per campaign. Columns: Campaign | Question | Status | Headline
   (host + job) | Verdict | Library PRs (release state) | Profiling PRs | Ledger note | Mind
   epic/contract | Next / open drafts | Superseded-by | Last updated. Backfill every campaign
   present today (~22): point-source image-plane CPU p1–4c; point-source source-plane p1–2e;
   cluster PointSolver (filed, not started); point-source GPU breakdown (draft); fixed lens light
   p0–5; fixed-light numba CPU s4–s6/levers/memo; HST GPU residue p1–4; certified positive solver;
   post-certified breakdown (draft); interferometer likelihood campaign (MGE / W~ route / mesh
   A100 / mesh CPU + open p3/p4 and drafts); numba interferometer revisit; Delaunay/DelaunayNN
   A100 series; A100 pixelized baseline; matrix-free pixelized (no-go); numpy deflections CPU;
   gaussian deflections precompute; image-source mappings; compile time (XLA autotune / Prodigy
   census / multiband pyloop); PreOptimizationTimes baseline; reference notes (NNLS ledger,
   sparse vs dense, VRAM); imaging over-sampling (draft); mass-field profiling.
2. `wiki/campaigns/<slug>.md`, one page per campaign, fixed header: Status / Question /
   Pre-registered rule / Verdict / Headline / Library PRs / Next. Move the "why" out of issue
   bodies and Mind `## Original prompt` sections into the page. Link to the existing
   `results/notes/` ledgers; do NOT move or rewrite the ledgers.
3. Correct the stale release labels above in `profiling_campaign_status_2026_09.md` and
   `results/README.md`.
4. Wire in: link `wiki/index.md` from `README.md` and `results/README.md`; point Mind `epics.md`
   `ledger:` fields for profiling epics at the campaign pages; add a check (in `lint.yml` or
   `build_readme.py --check`) that every `results/notes/*.md` ledger is referenced from a
   `wiki/campaigns/` page so the wiki cannot drift.
5. Follow the `autolens_inference/wiki/project/state.md` pattern (Status / Where we are / dated
   journal, `_template.md`).

## Out of scope (file as separate drafts)

- Moving `.out` logs / JSON sidecars out of `results/notes/`.
- The run-time-over-time dashboard and any profiling organ birth.
- Changing any library or profiling script.
