# euclid_dr1: every dataset rgb.jpg is upside down relative to the VIS FITS — flip them all, locally and on RAL

Type: bug
Target: euclid
Repos:
- euclid_dr1 (science project, /mnt/c/Users/Jammy/Science/euclid_dr1; RAL /mnt/ral/jnightin/euclid_dr1)
Themes:
- euclid
- hpc
Autonomy: supervised
Witness: for Tile102007000RA0642357198143DECNEG0666711522747, after the flip `plt.imread("rgb.jpg")` shown with `origin="upper"` puts the blue arc top-left and the companion galaxy bottom-left, matching the VIS_BGSUB HDU shown the same way (before the flip the arc is bottom-left).

## Problem
The `rgb.jpg` in each tile of `dataset/dr1_sep1_rest/<tile>/` (written 2026-09-20; 101–102 px square, not the 100 px of the FITS) is flipped vertically relative to the VIS/NIR FITS cut-outs. Drawn row 0 at the top, the VIS image and the segmentation binaries match each other but the RGB is mirrored top-to-bottom. There is no left–right mirroring. I found this on 2026-09-24 while building the artefact-fix before/after panels (`scratchpad/artefact_fix_first100/make_panels.py` has to use `rgb[::-1]` to line them up).

The pipeline reads the file as-is: `util.py:421-456` (`_open_rgb("rgb")` → `al.Array2DRGB`, no flip). So the RGB panel in every vis_lp `image/rgb.png` subplot is upside down relative to the fit panels, and so is the `rgb.png` in the inspect bundles (`scripts/tools/build_inspect.py`).

## Task
Write a script (e.g. `preprocess/flip_rgb.py`) that flips every dataset `rgb.jpg` vertically, then run it:
1. **Locally** on `dataset/dr1_sep1_rest/` (14,032 tiles) and any other `dataset/` folder with the same problem. Check `q1_walsmley` and the legacy `rgb_0`/`rgb_1` thumbnails against their FITS before deciding whether to include them; don't assume.
2. **On RAL** on `/mnt/ral/jnightin/euclid_dr1/dataset/...`, running the script there over SSH (`euclid_jump`). Don't re-upload: RAL uploads from the laptop run at ~95 KB/s.

Requirements:
- **Idempotent.** Running it twice must not flip the file back. Record the flip somehow (e.g. a `rgb_flipped` marker file per tile or a manifest), and check the marker, not the image.
- **Lossless where possible.** Re-saving a JPEG with PIL recompresses it. Prefer `jpegtran -flip vertical -perfect` and fall back to a high-quality re-encode only for the tiles where `-perfect` fails (101/102 px isn't a multiple of the MCU size). Alternatively, write a PNG and point `_open_rgb` at it. Say which approach you picked.
- Keep originals recoverable until the flip is verified (e.g. `rgb_raw.jpg`, or a tarball of the originals).
- Check the upstream writer. If whatever produced `rgb.jpg` on 2026-09-20 lives in this repo or the pipeline repo, fix it there too so that newly delivered tiles (the 15 sep1 remainder upload batches) aren't upside down. Otherwise flip them before submission.
- Any in-flight or queued RAL runs read `rgb.jpg` only for the visualisation subplot, so the flip doesn't change any likelihood. Still, don't rewrite files under a running array task's dataset while it's being read.

## Verification
- The witness above, plus a 3-panel by-eye grid (RGB | VIS | lens+source binary contours) for ~20 random tiles, locally and on RAL.
- Count of flipped / skipped (marker already present) / failed tiles, locally and on RAL. The two totals should match the tile counts.
- Record the result in the euclid_dr1 Cortex ledger.
