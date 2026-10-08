# Simplify the PyAutoEyes dashboard and browse one figure at a time

Target: @PyAutoEyes
Type: feature

Retain a compact overview, use library → dataset → figure navigation, and display
one selected figure prominently inside the dashboard with its critique actions.
Use PyAutoPulse and PyAutoInsight Results sections as read-only navigation references;
only PyAutoEyes implementation is in scope.

## Original user request (verbatim)

PyAutoEyes dashboard: lens - PyAutoLens -> PyAutoLens, same for Galaxy

The table at the top is good but its a bit cluttered or too much informaiton or hard to read, can we simplify?
In "Rendered with" we only need version numbers so for example "	autolens " is removed. Freshness can be more
concise (I think it dusplicates inform with Rendered with?) Survey feels like it could be removeD?

I thikn we should click "lens PyAutoLEns" to get a drop down menu of datasets (E.g. imaigng, interferometer),
which we rthen click to reveal all images. This will reduce information being over the top at beginning and user
navigates based on their choices ot know whats happening. Similar design in PyAutoPulse and PyAutoInight Results tabs.

Stuff like this is too much info and I wont read it "Rendered with autolens 2026.8.17.1, autogalaxy 2026.8.17.1, autoarray 2026.8.17.1, autofit 2026.8.17.1; generated 2026-09-28."

at the moment clicking an image takes you to raw githubcontent which then takes a while to load and moves you off the dashboard.
I want to be able to click an image to bring it up but can it be more seamless and integrated in the dashboard set up?
I can imagine that after clikcing imaging as a drop down, instead of seeing all images at oncde its a drop down menu
and we choose one at a time which then displays in the dashboard large (with its suggest an improvement) prompt
also there. I Will really look at one image at a time so why display them all in a grid?

Remove this: Figures from PyAutoLabs/autolens_visualization, manifest gallery/viz_manifest.yaml, re-rendered on pyautolens-release.

Survey (Brain Eyes conductor, local checkout): 40 PNGs on disk (imaging 22, interferometer 18); gaps none; orphans none; stale renders none.
