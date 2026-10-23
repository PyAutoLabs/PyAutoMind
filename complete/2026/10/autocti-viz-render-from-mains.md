- summary: `autocti_visualization/.github/workflows/render.yml` could never pass. It installed `autocti[optional]` from PyPI, whose newest release is `2024.11.13.2` (autocti is not on the Hands release train), and that predates `autonerves`, which the producers import. Human decision 2026-10-23: render from the mains.
  - Default (blank version) now checks out the PyAutoNerves/Fit/Array/CTI mains into gitignored `_libs/` and installs them as `lint.yml` does.
  - An explicit `autocti_version` or a `pyautocti-release` dispatch keeps the PyPI install.
  - A "Report where the stack came from" step was added, and the bot commit names the library SHAs.
  - `AGENTS.md` Testing / Eyes contracts and `.gitignore` were updated.
- evidence: PR lint green. Post-merge render 40032877406 on main passed every step, the first green render since the repo was born:
  - bot commit c4a9752 `re-render gallery with PyAutoCTI main@2a91ff5` (Nerves f116f70, Fit 919ebd4, Array d99ec2b);
  - App mint, then `eyes-refresh`;
  - PyAutoEyes Dashboard Refresh 40033172516 success.
  This also closes the GitHub-token phase 3 proof for this repo, so phase 3 is 7/7 proven.
- follow-up: the manifest's `rendered_with:` still shows the source checkout's stale stamps (`autocti: 2024.11.13.2`, `autoarray`/`autofit: 2026.8.17.1`), which PyAutoEyes displays. See draft/bug/autocti_visualization/manifest_rendered_with_stale_in_mains_mode.md.
- heart: YELLOW acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale), unrelated.

## Original prompt

# autocti_visualization render.yml fails: No module named 'autonerves' under the released stack

Type: bug
Target: autocti_visualization
Repos:
- autocti_visualization
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Filed: 2026-10-23
Issued: 2026-10-23

`render.yml` on main (run 39996567008, 2026-10-23, dispatched as the GitHub-token
phase 3 proof) fails in "Render figures + rebuild GALLERY.md": both producers
(`scripts/dataset_1d/visualization.py`, `scripts/imaging_ci/visualization.py`)
raise `ModuleNotFoundError: No module named 'autonerves'` right after
"Install the released stack from PyPI". The previous render (36626066338,
2026-09-29) also failed. Find whether the released autocti wheel lacks an
`autonerves` dependency (library packaging, PyAutoCTI) or the workflow's install
step omits it (workspace fix), fix at the right layer, then re-dispatch
`render.yml` — that run also proves the phase 3 PyAutoEyes App-token leg for this
repo (record complete/2026/10/github-token-p3-dispatchers-app.md), which is still
unproven.

## Decision (human, 2026-10-23): render from the library mains

Cause: `render.yml` installs `autocti[optional]` from PyPI, whose newest release is
`2024.11.13.2` (autocti is not in the Hands release train — `release.yml` says
"the CTI release train is not yet wired"). That wheel predates `autonerves`; the
producers import `from autonerves import conf`. So the render cannot pass from PyPI.

Fix in `cti/autocti_visualization/.github/workflows/render.yml`, mirroring `lint.yml`:
when no version is given (manual dispatch with blank input — the default), check out
PyAutoNerves, PyAutoFit, PyAutoArray and PyAutoCTI mains into sub-folders, install
each `./<repo>[optional]` in dependency order and put them on `PYTHONPATH`; keep the
PyPI path for an explicit `autocti_version` input or a `pyautocti-release` dispatch
(for when the CTI train is wired). The bot commit message names the source
(`PyAutoCTI main@<sha>`, not `autocti.__version__`, which is a stale stamp from a
source checkout). Update the header comment and the `AGENTS.md` Testing paragraph.
Out of scope: changing `gallery_build.py`'s `rendered_with:` (PR notes it).

Witness (post-merge): one `render.yml` dispatch on main succeeds end to end — render,
bot commit, App mint, `eyes-refresh` dispatch — and a PyAutoEyes Dashboard Refresh run
appears. That also closes the GitHub-token phase 3 proof for this repo.
Consequence: judge (CI behaviour change; proof is post-merge).
