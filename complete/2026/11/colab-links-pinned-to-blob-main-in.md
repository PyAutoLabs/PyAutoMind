Pinned the HowToGalaxy / HowToLens Colab links (course notebooks and the library docs that point at them) to the tagged course release instead of blob/main.

- Library: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/751 (MERGED 2026-11-24)
- Library: https://github.com/PyAutoLabs/PyAutoLens/pull/880 (MERGED 2026-11-24)
- Course: https://github.com/PyAutoLabs/HowToGalaxy/pull/108 (MERGED 2026-11-24)
- Course: https://github.com/PyAutoLabs/HowToLens/pull/138 (MERGED 2026-11-24)
- Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/879 (closed)
- Shift: 2026-11-24-am (Codex worker); merged by human /prm.

## Original prompt

# Colab links pinned to /blob/main/ in HowTo READMEs and library howto docs

Type: bug
Target: PyAutoLens
Repos:
- PyAutoGalaxy
- PyAutoLens
- HowToGalaxy
- HowToLens
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: `pyauto-heart url_check` exits 0 on PyAutoGalaxy, PyAutoLens, HowToGalaxy and HowToLens, and `pyauto-heart url_sweep` reports 0 forbidden patterns
Review-minutes: 3
Unattended: ready
Verified: 2026-11-24 7a7fee1d (HowToGalaxy), 1596dd5a (HowToLens), 1ba51f32 (PyAutoGalaxy), dbc63e65 (PyAutoLens)
Lane: any

Source: /health session 2026-11-18 (Heart url_check, swept 2026-11-18T08:31Z: 4 forbidden patterns in 4 repos). Human chose "file a bug prompt".

Heart's forbidden-URL guard (`pyauto-heart url_check <dir>`) reports
`FORBIDDEN: Colab URL pinned to /blob/main/ (use a date-tagged version — the release bumper skips main)` in:

- `HowToGalaxy/README.md` (lines 13, 17) and `HowToGalaxy/scripts/chapter_2_modeling/README.md` (and likely the other chapter READMEs)
- `HowToLens/README.md` (lines 13, 17) and `HowToLens/scripts/chapter_optional/README.md` (and likely the other chapter READMEs)
- `PyAutoGalaxy/docs/howtogalaxy/howtogalaxy.md` (lines 11, 23-26, the Colab column of the chapter table)
- `PyAutoLens/docs/howtolens/howtolens.md` (lines 11, 23-26)

They came in with the 2026-11-10 docs commits "docs: improve public entry points and retire stale guidance" (HowToGalaxy 824fcec, HowToLens dfdb25b) and the 2026-11-12 commits "docs: consolidate HowTo… tutorials and preserve chapter links" (PyAutoGalaxy 8e4a9c35, PyAutoLens a87745e3b).

Fix: point every Colab link at the date-tagged release ref the release bumper rewrites, matching the convention the other workspaces use (the guard is clean on autolens_workspace, autogalaxy_workspace, autofit_workspace and HowToFit — mirror whichever form they use). Leave the plain GitHub `/blob/main/` and `/tree/main/` browse links alone unless the guard flags them. Library docs first (PyAutoGalaxy, PyAutoLens), then HowToGalaxy and HowToLens.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2076909a-d18c-4718-a05e-9afa6642996d/scratchpad/intake/colab.md -->
