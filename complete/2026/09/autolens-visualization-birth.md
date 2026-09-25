- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/436 (closed as pivoted 2026-09-25)
- shipped: 2026-09-25 — the repo only: `PyAutoLabs/autolens_visualization` created by the human on github.com and PR https://github.com/PyAutoLabs/autolens_visualization/pull/1 (`fd846dba`) merged 2026-09-25 (skeleton, tracked HST-scale imaging `hst` + SMA interferometer datasets, `scripts/{imaging,interferometer}/visualization.py` producers, 40 PNGs, `GALLERY.md`, gallery builder + hermetic tests + lint/render workflows).
- classification: feature (autolens_visualization) — **superseded by a pivot, not completed as planned.**
- pivot: the human decided (2026-09-25) to promote the repo from a per-library project repo to the organ **PyAutoEyes** — one library-neutral home for every library's rendered figures (per-library instance subtrees, one harness, an instance registry, a Pages board that is the single point of contact for visual behaviour). New epic `pyautoeyes-birth` (epics.md), phases 0–5 under `draft/feature/pyautoeyes/`; phase 0 = `eyes_birth_organ_row.md` (organ row, boundary prose, local move). The GitHub repo is renamed (not re-created) so history and PR #1 carry over.
- discarded: the three organ registration branches `feature/autolens-visualization-birth` — PyAutoMind `2265a122`, PyAutoBrain `9829c67`, PyAutoHeart `1c9a532` — verified green 2026-09-25 (`repos_sync.py --check` all legs OK except the pre-existing hub-blurb leg), **never pushed**, superseded by the phase-0 organ-row work. Their three follow-up drafts were carried over onto main retargeted to PyAutoEyes (`draft/feature/pyautoeyes/multi_galaxy_gallery.md`, `draft/feature/pyautoeyes/group_cluster_gallery.md`, `draft/bug/pyautobrain/eyes_survey_recursive_producers.md`, all `Epic: pyautoeyes-birth`).
- carried over: the plot critiques recorded on #436 (e⁻/s colourbar labels on convergence/potential/deflection/magnification and inversion count panels; masked region filled green in normalized-residual panels; white holes in log10 reconstructed image; dense edge contours on Data (log10); interferometer "Normalized Residual Map 1σ" saturated at ±1) move to the `pyautoeyes-birth` epic for a later `/eyes` pass.
- next: phase-0 issue — see the `pyautoeyes-birth` epic entry (PHASE0_ISSUE).
- session: claude-code-cli, Fable architect, Opus execution, 2026-09-25.

## Original prompt

# Birth `autolens_visualization`: the repo where every figure is rendered, stored and improved

Type: feature
Target: autolens_visualization
Repos:
- @autolens_visualization
- @PyAutoMind
- @PyAutoBrain
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: human-required
Priority: high
Lane: local-dev
Filed: 2026-09-25
Issued: 2026-09-25

## Request (verbatim)

Make the repo autolens_visualization, which is where all images are made for inspection and improvements.
This will link close to the existing PyAutoBrain eyes agent, or over ride it, your call. The idea is basically before
we would output all images to autolens_workspace in a special run, but instead we can just permnenantly store what they
look like (most up to date) in the repo, which will have script which call the method to output them in the repo via
the visualizer I think. This should include a markdown page we navgiate on GitHub or a dashboard
and then we can improve visualization using this more open forum.

The main goal is a single project where I can manage visualization and have AI chats to improve it in
the source code, as currently I have to run things in autolens_workspace to get an output folder which I inspect
or use science project.

Given this is for visualization which is used in scientific analysis, it should use a realistic sized image and
instrument setup, I think for now it should use the same HST setup as the autolens_profiling workspace for
imaging and I guess a similar dataset for visibilities. Future work will be to then do this on multi_galaxy,
group, cluster etc which require a lot of visualization work, but lets get the core infrastructure setup
for just imaging and interferometer which I guess means well end up with a autolens_visualization/scripts/imaging,
autolens_visualization/scripts/interferometer folder and follow the same structure as other repos.

## Scope

Core infrastructure only: imaging + interferometer galleries, a GitHub-navigable
gallery page, registration in the body map, and the Eyes agent pointed at the
new repo. multi_galaxy / group / cluster galleries are follow-up prompts.
