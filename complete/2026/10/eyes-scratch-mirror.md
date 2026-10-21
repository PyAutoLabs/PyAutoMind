Shipped phase 1 of the Eyes scratch mirror. It is opt-in through `PYAUTO_EYES_SCRATCH`, and while active image work is under way it copies rendered figures to `$PYAUTO_EYES_SCRATCH/<lib>/<dataset_type>/`. The folder layout follows the PyAutoEyes dashboard.

- autogalaxy/autofit/autocti_visualization `_viz_cli.py`: adds `mirror_to_scratch()` and the `python _viz_cli.py scratch [domain ...]` entry point. Each mirror replaces the domain folder, skips `misc`, and does nothing when the variable is unset. `gallery/gallery_run.sh` mirrors each producer that succeeds, and a failed mirror never fails the run. Adds hermetic tests in `scripts/misc/test/test_eyes_scratch.py`.
- PyAutoBrain `skills/eyes/eyes.md`: adds the "Active image work (on-the-fly)" section.
- Merged 2026-10-21 via a human /prm (judge tier). Every CI leg was green.

Scope recorded is what merged. The autolens_visualization part (phase 2) was re-filed as `draft/feature/autolens_visualization/eyes_scratch_mirror_lens.md`, blocked by autolens_visualization#7 (task point-image-fit-filename).

## Original prompt

# Eyes scratch mirror — on-the-fly figure inspection

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21

@autolens_visualization @autogalaxy_visualization @autofit_visualization @autocti_visualization @PyAutoBrain

## Request (verbatim, 2026-10-21)

> For PYAutoEyes work, I often have to wait for a complete loop of image fix to
> dashboard update to provide feedback, but when im actively working on images it
> needs to be more on-the-fly (e.g. before PRs, CI). Can we make it so such work
> puts images for inspection in Science/scratch/eyes/dataset_type as we go.

Follow-up: "go, mirror the dashboard so its eyes/autolens/<dataset_type>"

## Approved plan

- Opt-in env var `PYAUTO_EYES_SCRATCH` (human sets it to
  `/mnt/c/Users/Jammy/Science/scratch/eyes`); unset = no-op, so CI and other
  machines are unaffected and no Windows path is committed.
- Layout mirrors the PyAutoEyes dashboard: `$PYAUTO_EYES_SCRATCH/<lib>/<dataset_type>/`
  (`autolens/imaging`, `autogalaxy/ellipse`, `autofit/samples`, `autocti/imaging_ci`, …),
  where `<dataset_type>` = the producer domain `scripts/<domain>/`.
- Each `<lib>_visualization/_viz_cli.py` gains a mirror helper + entry point
  `python _viz_cli.py scratch [domain ...]`: replaces the scratch domain folder
  with the current PNGs (no stale figures), prints the path.
- `gallery/gallery_run.sh` calls it after each successful producer, so a
  worktree run of one domain lands figures in scratch immediately.
- Brain `skills/eyes/eyes.md` gains an "active image work" mode: after each fix,
  re-render that domain, mirror, tell the human the scratch path.

## Split (human decision 2026-10-21)

autolens_visualization is claimed by `point-image-fit-filename` (PR #7, also edits
`_viz_cli.py`). Phase 1 = autogalaxy/autofit/autocti_visualization + Brain `eyes.md`
now. Phase 2 = autolens_visualization, same change, after #7 merges via /prm.

Update 2026-10-21: autolens_visualization#7 MERGED and `point-image-fit-filename` closed (claim released) → phase 2 is unblocked; rebase onto the new `_viz_cli.py` (`extra_pngs` keep-list).
