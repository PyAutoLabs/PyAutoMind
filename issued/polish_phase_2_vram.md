# polish phase 2 — vram-first validation sweep

Type: maintenance
Target: autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of 4 of `polish.md` (see parent for full intent). Depends on phase 1
(design locked).

Profiling runs have historically flagged memory/VRAM issues that side-tracked
the campaign into source fixes. To avoid that, run the `vram` package **first**,
across the imaging, interferometer and datacube configs that phase 3 will
profile, so memory issues and other bugs surface now rather than mid-campaign.

Deliverables:
- vram results for the phase-3 config matrix, saved per the phase-1 results
  conventions (`.json` + `.md`).
- The computed vmap batch sizes per config — phase 3's `likelihood_runtime`
  sweeps are vmap-only and consume these batch sizes.
- Any memory/VRAM bugs found are triaged: fix here only if small and in-repo;
  otherwise file as separate `bug/` prompts and do not side-track the campaign.

Out of scope: runtime/breakdown sweeps (phases 3–4); searches; point_source;
laptop GPU.
