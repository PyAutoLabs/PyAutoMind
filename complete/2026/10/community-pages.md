Community pages and a merged "Community & Contributing" README section across PyAutoLabs,
triggered by Discussion #32 (SiriusFzh's PyAutoLens Visual Workbench).

## What shipped

- `docs/general/community.md` in PyAutoLens, PyAutoGalaxy and PyAutoFit, in each
  `docs/index.md` General toctree; the PyAutoLens page lists the SiriusFzh Visual Workbench
  (repo URL, labelled as a community project).
- One `## Community & Contributing` section replacing `Community & Support` / `Contributing`
  across 16 public repos plus PyAutoScientist, each linking the per-library RTD community page.
- PyAutoLabs front page: the community section moved to the bottom, linking every project page.

## PRs (all MERGED 2026-10-07)

Wave 1 (libraries): PyAutoLens#774, PyAutoGalaxy#649, PyAutoFit#1663, PyAutoArray#618.
Wave 2 (READMEs): autolens_workspace#585, autogalaxy_workspace#256, autofit_workspace#167,
autoreduce_workspace#5, HowToLens#96, HowToGalaxy#85, HowToFit#71, autolens_visualization#3,
autogalaxy_visualization#3, autofit_visualization#3, autocti_visualization#3,
autolens_profiling#391 (after corrective #392), pyautolabs.github.io#30, PyAutoScientist#48.

## Notes

- Five PRs (autolens_profiling#391 and the four *_visualization#3) were held by human decision
  until release 2026.10.7.1: their lychee lint 404'd on the new RTD community page because RTD
  had been red since 2026-10-04 on the `autonerves>2026.10.4.1` floor. Lints re-ran clean once
  RTD rebuilt; #391 additionally needed autolens_profiling main's dashboard re-rendered against
  the current PyAutoBrain theme (0022385) and a branch update.
- Heart acknowledged at ship: manifest drift (2 undeclared checkouts) and stale release
  validation; both unrelated to this task.

## Original prompt

# Community pages + merged "Community & Contributing" sections across PyAutoLabs

Type: docs
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoFit
- PyAutoArray
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autoreduce_workspace
- HowToLens
- HowToGalaxy
- HowToFit
- autolens_visualization
- autogalaxy_visualization
- autofit_visualization
- autocti_visualization
- autolens_profiling
- PyAutoScientist
- pyautolabs.github.io
Themes:
- docs-hub
- community
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `docs/general/community.md` exists in PyAutoLens, PyAutoGalaxy and PyAutoFit, is in each `docs/index.md` General toctree, builds with no new Sphinx warnings vs `sphinx_warning_baseline.txt`, and the PyAutoLens page lists the PyAutoLens Visual Workbench (repo URL, not release zips); every README in the 16 public repos plus PyAutoScientist has exactly one `## Community & Contributing` section and no `Community & Support` / `## Contributing` / `## Contribution` heading; the PyAutoLabs front page `#community` section is the last section before the footer and links the three per-project community pages.
Review-minutes: 6
Unattended: ready
Filed: 2026-10-07
Issued: 2026-10-07

## Original request (verbatim, 2026-10-07)

> That all sounds good, dont bother with the PSF noise map thing. I want to encourage
> community contributions and ensure they are visible, so I would put this in a community
> section at the bottom of the PyAutoLabs front page, I would put it on the PyAutoLens
> GitHub repo and autolens_workspace repo in a new community section, actually use the
> Community & Support section but dont list projects but link to a readthedocs page with
> all individual things (PyautoLabs should also use this URL). I think we can probably
> merge community * Support and Contributing. Lets do this across all repos in a more
> systematic way then
>
> I think PyAutoLens RTD should have it like oyu suggest, but we should also in
> PyAutoScientist (mirroring the PyAutoLabs front page) have URLS that go to individual
> projects community pages

## Context

Triggered by PyAutoLabs Discussion #32 (SiriusFzh, 2026-10-06): an independent
MIT-licensed PyAutoLens Visual Workbench (https://github.com/SiriusFzh/PyAutoLens-Workbench)
asking where a documentation link belongs. A read-only security audit (Opus, 2026-10-07)
found it safe: no prompt injection, telemetry, exec paths; localhost-only server with
Host/Origin checks; exemplary attribution. Caveats: link the repo not the release zips,
keep it labelled as a community project.

## Plan (approved in-session 2026-10-07)

1. Per-library MyST page `docs/general/community.md` in PyAutoLens (canonical), PyAutoGalaxy,
   PyAutoFit, label `(community)=`, added to the General toctree after `general/credits`.
   Sections: Get help & talk to us (Discussions / issues with reproducer / invite-only Slack);
   Contributing (repo CONTRIBUTING.md, org-wide PyAutoLabs/.github CONTRIBUTING.md, Code of
   Conduct, PyAutoScientist AI_POLICY.md, workspace notebook-editing note); Community
   contributions (intro: independent tools/tutorials/teaching material/papers' code, not
   maintained or endorsed by PyAutoLabs; how to get listed: Discussions post or PR this page;
   the list — PyAutoLens first entry = PyAutoLens Visual Workbench, SiriusFzh, MIT: local
   browser app for Mac/Windows, draggable 3D lens/source geometry, 31 forward-simulation
   products, PNG/FITS/CSV export, teaching quick fits, English/Chinese UI; Galaxy/Fit lists
   empty); See also (sibling community pages).
2. Every README in the 16 public repos: replace `## Community & Support` (+ `## Contributing`
   / `## Contribution`) with one `## Community & Contributing` (~6 lines): existing
   Discussions/issues/Slack wording + "Community-built tools, tutorials and how to
   contribute: the <Project> community page (<RTD URL>)" + per-repo CONTRIBUTING.md link
   where present. Family routing: lens repos (+autocti_visualization, autoreduce_workspace)
   → PyAutoLens page; galaxy repos → PyAutoGalaxy page; fit repos + PyAutoArray → PyAutoFit
   page. Keep trailing Spotify `<sub>` lines; drop the duplicated "Hands on support… Slack"
   sentence. Organs, *_test, *_developer and assistant repos untouched.
3. PyAutoScientist README: merge `## Contributing` + `## Community` into
   `## Community & Contributing` keeping org .github / CoC / AI policy links, add the three
   per-project community page links. pyautolabs.github.io/index.html: rename `#community`
   to "Community & Contributing", move it to the last section before the footer, add the
   same three links + org CONTRIBUTING link; nav anchor text stays "Community".
4. Discussion #32 reply drafted via /community for human approval and posting after wave 1
   merges and RTD builds.

Execution: wave 1 = the three library PRs (library-first, ship_library); wave 2 = bundle of
the remaining 15 repos, one PR each. Fable plans, Opus executes.
