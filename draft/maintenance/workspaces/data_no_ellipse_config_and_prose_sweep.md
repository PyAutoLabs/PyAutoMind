# Sweep the retired `data_no_ellipse` toggle from configs and prose

Type: maintenance
Target: workspaces
Repos:
- autogalaxy_workspace
- autogalaxy_workspace_test
- autogalaxy_visualization
- HowToGalaxy
- autogalaxy_assistant
- PyAutoLens
- HowToLens
- autolens_workspace
- autolens_workspace_test
- autolens_visualization
- autolens_assistant
- euclid_strong_lens_modeling_pipeline
Themes:
- hygiene
- visualization
Difficulty: small
Autonomy: safe
Priority: low
Status: draft
Consequence: glance
Witness: after the sweep, `grep -rn data_no_ellipse` over the listed repos returns nothing, and `autogalaxy_visualization` re-rendered on the release containing PyAutoGalaxy#698 has `ellipse_fit.png` + `ellipse_fit_log10.png` per ellipse scenario in its manifest and GALLERY.md.
Review-minutes: 5
Unattended: ready
Lane: any
Filed: 2026-11-10

## Why

PyAutoGalaxy#698 (`feature/ellipse-fit-filenames`) removed the `fit_ellipse.data_no_ellipse` toggle and the dead
`disable_data_contours` flag. Its outputs were byte-identical duplicates of the `data` images. The library no longer
reads the key, so the copies left behind are inert, but they mislead readers.

**Gate:** start only after PyAutoGalaxy#698 is merged and released (library-first).

## Work

1. Delete the `data_no_ellipse:` line from every `config/visualize/plots.yaml` that has it. At filing that was the
   workspace, workspace_test (including `scripts/ellipse/config` and the autolens_workspace_test
   `scripts/{imaging,interferometer}/config{,_source}` copies), visualization, HowTo, assistant and Euclid pipeline
   configs, plus `PyAutoLens/autolens/config/visualize/plots.yaml`.
2. Prose: `autogalaxy_workspace/scripts/ellipse/plot.py:176` (and regenerate its notebook);
   `autogalaxy_visualization/scripts/ellipse/visualization.py:216` "(+ data_no_ellipse variants)";
   `autogalaxy_visualization/AGENTS.md:102-104`, which describes the old filename collision.
3. Re-render `autogalaxy_visualization` on the release. `ellipse_fit.png` changes content (it was the log10 image,
   the last write on main; it is now linear) and `ellipse_fit_log10.png` is new.
4. Side note from review: the `multipole` and `multipole_scaled` ellipse scenarios render byte-identical figures. Check
   whether the producer parameters make the two models coincide. If so, file it as an Eyes critique rather than
   fixing it here.
