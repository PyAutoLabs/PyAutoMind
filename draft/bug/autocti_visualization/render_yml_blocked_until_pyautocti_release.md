# autocti_visualization render.yml fails on the released stack until PyAutoCTI releases

Type: bug
Target: autocti_visualization
Repos:
- autocti_visualization
- PyAutoCTI
- PyAutoHands
Themes:
- visualization
- infrastructure
Difficulty: small
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: draft
Consequence: judge
Witness: `gh workflow run render -R PyAutoLabs/autocti_visualization` completes green and its last step logs "Dispatched eyes-refresh to PyAutoLabs/PyAutoEyes"
Epic: pyautoeyes-birth
Filed: 2026-09-29

## Task

The first post-merge `workflow_dispatch` of `render.yml`
(run 36626066338, https://github.com/PyAutoLabs/autocti_visualization/actions/runs/36626066338)
failed at "Render figures + rebuild GALLERY.md + gallery/viz_manifest.yaml".
The "Install the released stack from PyPI" step ran
`pip install "autocti[optional]"`, which resolves to `autocti-2024.11.13.2`,
the latest autocti on PyPI. That release is older than autonerves and older
than the `aplt.*` plot-function API the producers call. Both producers fail on
import:

```
File ".../scripts/dataset_1d/visualization.py", line 64, in <module>
    from autonerves import conf
ModuleNotFoundError: No module named 'autonerves'
```

(`scripts/imaging_ci/visualization.py` line 73 fails the same way.) The commit
and `eyes-refresh` steps were skipped, so PyAutoEyes got no dispatch from cti.
The tracked PNGs on main still come from the source-checkout render at birth.
`lint.yml` stays green because it installs the library mains, not PyPI.

For comparison, the autofit_visualization render (run 36626061620) installed
autofit 2026.9.27.2 and autonerves 2026.9.27.2 from PyPI and succeeded.

## Fix (choose one, in this order of preference)

a. **Release PyAutoCTI** on the current cadence. After that,
   `pyautocti-release` and this workflow work as designed. This is the blocker
   to name on the Hands release board: autocti has not published since
   2024-11.
b. **Interim:** when `autocti_version` is empty, have `render.yml` fall back to
   the library mains by mirroring `lint.yml`'s checkout/install step. That
   makes `workflow_dispatch` re-renders work before a release. The
   `rendered_with` stamp must then say it came from a source build.

Found during the `/prm` close-out of `eyes-fit-cti-instances`
(`complete/2026/09/eyes-fit-cti-instances.md`, PyAutoMind#455).
