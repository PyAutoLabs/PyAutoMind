# autofit_visualization — seed every sampler so re-renders are byte-stable

Type: maintenance
Target: autofit_visualization
Repos:
- autofit_visualization
Themes:
- visualization
Difficulty: small
Autonomy: safe
Priority: normal
Lane: local-dev
Status: draft
Consequence: notify
Witness: two consecutive `gallery_run.sh --all` runs leave `git status` clean (identical sha256s in `gallery/viz_manifest.yaml`)
Epic: pyautoeyes-birth
Filed: 2026-09-29

## Task

The first post-merge `render.yml` dispatch
(run 36626061620, https://github.com/PyAutoLabs/autofit_visualization/actions/runs/36626061620)
committed `b72fb4a` ("chore: re-render gallery with autofit 2026.9.27.2").
It changed 51 files: 49 PNGs, `GALLERY.md` and the manifest. The PNGs changed
only because dynesty, emcee, zeus and nautilus run unseeded. As a result:

- every release re-render rewrites about 50 tracked PNGs, so the repo history
  grows each time with no real figure change;
- the Eyes staleness and diff signal cannot tell a real figure change from
  sampler noise.

## Fix

Seed every search in the producers. Use PyAutoFit's `seed` / `rstate` kwargs
where the search takes one, or seed the numpy RNG where it takes none. Seed
MultiStartAdam's starting points as well. Then run `gallery_run.sh --all` twice
in a row and confirm the manifest sha256s are identical.

Found during the `/prm` close-out of `eyes-fit-cti-instances`
(`complete/2026/09/eyes-fit-cti-instances.md`, PyAutoMind#455).
