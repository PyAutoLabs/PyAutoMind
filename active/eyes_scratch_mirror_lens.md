# Eyes scratch mirror: phase 2 (autolens_visualization)

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
blocked-by: https://github.com/PyAutoLabs/autolens_visualization/pull/7 (task point-image-fit-filename; that PR also edits `_viz_cli.py`)

@autolens_visualization

Phase 1 shipped on 2026-10-21; record `complete/2026/10/eyes-scratch-mirror.md`. Port the same change, exactly as merged in autogalaxy_visualization#5, to lens/autolens_visualization:
- `_viz_cli.py`: `EYES_LIB = "autolens"`, `mirror_to_scratch()`, and the `scratch` entry point
- `gallery/gallery_run.sh`: mirror each producer that succeeds
- `scripts/misc/test/test_eyes_scratch.py`, plus the AGENTS.md and README notes
- Drop the "lens support lands in phase 2" note from PyAutoBrain `skills/eyes/eyes.md`

The result is figures in `$PYAUTO_EYES_SCRATCH/autolens/<dataset_type>/`, e.g. `/mnt/c/Users/Jammy/Science/scratch/eyes/autolens/imaging`.
