# Colab link rot: fix stale/wrong URLs + purge allowlists (phase 2 of colab-maturity)

Autonomy: safe
Difficulty: medium
Status: launched 2026-07-09 --auto (human-directed in-session after merging phase 1).
Phase 1 merged 2026-07-09 (PyAutoConf#120, PyAutoBuild#125, PyAutoHeart#44); the new
Heart forbidden-URL patterns turn the Monday sweep red until this phase lands.

SCOPE SPLIT at launch: PyAutoLens + PyAutoGalaxy are claimed by
release-docs-polish-learn-paths (awaiting-input, uncommitted) — their docs/howto*
dead-link fixes + allowlist purges are DEFERRED to a follow-up leg blocked on that
task. This run covers the unclaimed repos: HowToFit, HowToGalaxy, HowToLens,
euclid_strong_lens_modeling_pipeline.

## Context

Census 2026-07-09 (see `issued/colab_maturity.md` for the full census). Phase 1
made every generated notebook Colab-runnable by construction and hardened the
guards. This phase fixes the accumulated link rot the guards now flag.

Notebook regeneration is NOT part of this phase — the next release regenerates
all notebooks through PyAutoBuild's new injection path automatically.

## The work

1. **HowToLens** — chapter READMEs (`scripts/*/README.md`, mirrored into
   `notebooks/*/README.md` by generate.py): 71 unpinned `blob/main` Colab URLs →
   pin to the current release tag (the bumper maintains them thereafter). Fix
   dead filenames: `tutorial_11_adapt_regularization.py.ipynb` → actual
   `tutorial_11_adaptive_regularization.ipynb`; `tutorial_3_pixelizations` →
   actual name; `tutorial_6_modeling` → `tutorial_6_lens_modeling`; verify every
   link target exists at the pinned tag.
2. **HowToGalaxy** — chapter READMEs: 28 Colab URLs point at the WRONG repo
   (`autogalaxy_workspace/.../notebooks/chapter_*` — chapters live in
   HowToGalaxy). Repoint to `PyAutoLabs/HowToGalaxy/blob/<tag>/...`.
3. **HowToFit** — chapter READMEs are tag-pinned + right repo; verify link
   targets (allowlist shows two moved/renamed tutorials frozen at 2026.5.14.2).
4. **PyAutoLens / PyAutoGalaxy docs** — fix or remove dead Colab links
   (`chapter_optional` tutorials, renamed pixelization tutorials) in
   `docs/howtolens/` / `docs/howtogalaxy/`.
5. **euclid_strong_lens_modeling_pipeline/README.md** — forbidden
   `Jammy2211` Colab URL → PyAutoLabs (or drop).
6. **Allowlist purge** — remove the now-fixed Colab entries from every
   `.url_check_allowlist.txt` (PyAutoLens, PyAutoGalaxy, HowToLens, HowToGalaxy,
   HowToFit); several entries are themselves stale (frozen 2026.5.14.2 forms).
7. **Verify** — run `PyAutoHeart/heart/checks/url_check.sh` (offline) per repo
   and the live sweep locally; Monday cron should go green.

## Conflicts to check at issue time

At census time, `release-docs-polish-learn-paths` claimed PyAutoLens,
PyAutoGalaxy, autolens_workspace; `ep-examples-tests` claimed autofit_workspace.
Re-run `worktree_check_conflict` before starting.
