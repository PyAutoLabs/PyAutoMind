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
