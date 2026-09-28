# PyAutoEyes phase 1a — re-birth autolens_visualization as the lens project repo

Type: feature
Target: autolens_visualization
Repos:
- autolens_visualization
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
Themes:
- visualization
- infrastructure
Difficulty: medium
Autonomy: supervised
Priority: high
Lane: local-dev
Status: draft
Consequence: judge
Witness: `bash gallery/gallery_run.sh --all` in `lens/autolens_visualization` reproduces the 40 PNGs (byte-diff acceptable only in the version string) and writes the tracked `gallery/viz_manifest.yaml`; `python3 organs/PyAutoMind/scripts/repos_sync.py --check` clean (bar the pre-existing hub-blurb leg, if still red); `pyauto-brain eyes survey lens/autolens_visualization` reports no gaps and no orphans
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 1a
Filed: 2026-09-28
Issued: 2026-09-28

Blocked on: human repo creation (`gh repo create PyAutoLabs/autolens_visualization --public` — the agent is denied `gh repo create`).

## Layering (human decision 2026-09-28)

Two layers, the same shape as `autolens_profiling` / `autolens_inference`
under the Brain board. **Project repos** `<lib>_visualization` make, store and
track the figures of one library. **The organ PyAutoEyes** is the cross-project
dashboard that reads every project repo's tracked manifest and links to its
PNGs; it renders nothing and copies no figures. This phase puts the lens
content back into its own project repo; phase 1b strips the organ to its
skeleton.

## Task

Human first, quoted verbatim for the session:

1. `gh repo create PyAutoLabs/autolens_visualization --public`

Agent, after the human confirms the empty repo exists:

1. **History carries over.** From the current `organs/PyAutoEyes` checkout
   (clean, in sync with `origin/main`), add the new repo as a remote and push
   the *current* main history to it — `git remote add autolens_visualization
   https://github.com/PyAutoLabs/autolens_visualization.git && git push
   autolens_visualization main` — so every PNG keeps its provenance (PR #1,
   the phase-0 commits). Then clone it to `lens/autolens_visualization`
   (origin = the new repo). PyAutoEyes main is left untouched here; phase 1b
   strips it.
2. **In `lens/autolens_visualization`** (task worktree, one PR):
   - README.md / AGENTS.md (+ CLAUDE.md stub) retitled to
     `autolens_visualization`, the layering stated: a *project* repo that owns
     the lens figures — producers, simulators, datasets, `plots.yaml`,
     instruments, tracked PNGs, `GALLERY.md`, the render harness — while the
     organ PyAutoEyes only aggregates it on its dashboard. Remove organ prose
     inherited from phase 0 (registry, board, "every library").
   - **Tracked manifest.** `gallery/gallery_build.py` writes
     `viz_manifest.yaml` to a tracked path (`gallery/viz_manifest.yaml`),
     carrying every figure it holds (producer, domain, relative PNG path,
     size, mtime-free content hash) plus the rendered stack version;
     `output/gallery/gallery.html` stays gitignored. `render.yml` commits the
     manifest alongside the PNGs and `GALLERY.md`. `--check` fails on a stale
     manifest. This is the organ's read contract (phase 1b reads it).
   - `render.yml`: keep the `pyautolens-release` `repository_dispatch` (plain
     git PNGs, no LFS); add a final step that fires a `repository_dispatch`
     (`eyes-refresh`) at PyAutoEyes so its dashboard refreshes (Cortex
     pattern; token as the other cross-repo dispatches use).
   - `_viz_cli.py` kept; `activate.sh`, lint.yml unchanged except names.
     Keep `dataset/imaging/hst` byte-identical to profiling (never
     re-simulate).
3. **PyAutoMind** — mirror the #436 registration set
   (`complete/2026/09/autolens-visualization-birth.md`): `repos.yaml` row
   after `autolens_inference`, template the `autolens_profiling` row —

   ```yaml
   autolens_visualization:
     path: lens/autolens_visualization
     github: PyAutoLabs/autolens_visualization
     category: project
     role: "Rendered PyAutoLens figures — every visualizer output on realistic HST-scale imaging and SMA interferometer data, the producers and harness that render them, re-rendered on each release; aggregated by the PyAutoEyes dashboard."
   ```

   and the PyAutoEyes `role` rewritten to the layered wording (the
   cross-project visualization dashboard over the `<lib>_visualization`
   project repos: registry, manifest contract, Pages board; renders nothing,
   never judges, never edits plot code). `ROUTING.md` target list gains
   `autolens_visualization`. Then `python3 scripts/repos_sync.py --write`
   and propagate the generated map blocks / organ tables to their repos
   (watch the `--write`-from-bundle spill into canonical checkouts).
4. **PyAutoBrain** — Eyes conductor prose
   (`agents/conductors/eyes/AGENTS.md`, `skills/eyes/eyes.md`): default
   instance → `lens/autolens_visualization`, with the layering in one
   paragraph (project repos hold the figures; the organ PyAutoEyes is the
   dashboard; the registry that lists instances arrives in phase 2);
   `bin/clean_slate.sh` dataset-wipe exclusion for the new path. `_eyes.py`
   stays repo-name-free.
5. **PyAutoHeart** — `config/repos.yaml` drift exclusion / organism list entry
   for `autolens_visualization`, as #436 had it.

## Ship policy

PR order Mind → Brain → Heart → autolens_visualization. While Heart is RED the
PRs ship only under a contemporaneous human RED override. Merge stays human
(`/prm`). Phase 1b must not start deleting organ content until this phase is
merged and the history is confirmed on the new repo (`git ls-remote`).
