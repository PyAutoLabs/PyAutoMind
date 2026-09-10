# Scientific workflow through natural language

Type: docs
Issued: 2026-09-09
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1595
Repos: @PyAutoFit @autofit_workspace @HowToFit

## Implementation handoff

- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/scientific-workflow-language`, branch `feature/scientific-workflow-language` in PyAutoFit, autofit_workspace, HowToFit and PyAutoHands.
- RTD page rewritten with prompts, output file table and actual model.json excerpt, visualization/live output, loading and comparison prompts, five-dataset tree. Model alternatives consistently free versus fixed Gaussian width.
- Workspace now runs one real Nautilus fit, saves distinct data/model/residual/combined images and science_summary.json with units, reloads posterior credible intervals and a SQLite query, and demonstrates custom results. Notebook, executed markdown and navigation regenerated.
- HowToFit chapter 2 stubs removed (tracked and recoverable), prose-only chapter 1 tutorial 6 added, all navigation and generated artifacts updated; chapter 3 numbering preserved.
- Necessary PyAutoHands change: inject_colab_setup skips notebooks without nonempty code so prose-only tutorial stays code-free under normal regeneration. 11 focused tests pass; earlier broader 36-test check also passed.
- Necessary PyAutoFit fix found by real notebook execution: Fitness.manage_quick_update must not clear_output when live_visual_update=True; clearing removes the persistent display_id target and silently drops subsequent images. Regression tests added. Real notebook verification now sees initial image plus two updates sharing the same display_id, and exactly one image retained at completion.
- Validation: workspace smoke 8 scripts + 2 notebooks passed; HowToFit smoke 15 scripts passed, 1 skipped; both navigator checks passed; prose-only AST and zero-code notebook validation passed; Sphinx build passed (pre-existing warnings elsewhere on clean build, none on edited page); quick-update tests 34 passed, 1 skipped. Full PyAutoFit suite: 2555 passed, 2 skipped, 76 warnings in 167.49s. Real notebook verification confirms exactly one visible image survives completion after initial display and two refreshes. Final whitespace checks clean.
- Refreshed shipping gate RED at 2026-09-10T02:53:22Z: `PyAutoArray: 2 commit(s) behind origin`; `PyAutoGalaxy: 2 commit(s) behind origin`; `release validation FAILED (stage integrate)`. Unrelated workspace validation and profiling warnings also present. No implementation commits or PRs yet. Requires gate clearance or explicit user instruction overriding it. Workspace now depends on the PyAutoFit display fix and HowToFit generation on the Hands fix; merge those first.

## Approved plan

Rewrite PyAutoFit/docs/overview/scientific_workflow.md in the prompt-led style of natural_language.md, retaining explanations and output examples but no Python. Order: hard disk output, visualization, on-the-fly output, loading results, result customization, model composition as comparison, searches, configs, database, scaling up. Explicitly document saved files using verified output and a model.json excerpt. Demonstrate custom science_summary.json, separate before/during-fit visualization, and working live notebook updates. Finish with an illustrative five-dataset/two-model/two-search tree and an assessment prompt.

Update autofit_workspace/scripts/overview/overview_2_scientific_workflow.py with corresponding runnable examples, current live-output API, distinct residual/fit images and consistent save/reload paths. Regenerate notebook, executed markdown and navigation artifacts. Replace HowToFit's chapter_2_scientific_workflow stub with a prose-only final chapter 1 tutorial linking RTD and the workspace file; update navigation and generated artifacts.

Validate a short real fit, output JSON/images, result reload, live updates, documentation build and relevant workspace checks. No library API changes intended. User approved this plan: "plan looks good, go".

## Original request (verbatim)

I now want us to adapt  overview_2_scientific_workflow.py and its corresponding readthedoc markdown
to the style in natural_language.md, that is I want the readthedocs page to be entirely natural language
prompts to describe the task at hand. However, I also want us to update aspects of the tutorial:

- Begin with the text in "Hard DIsk Output", with the Natural language prompt asking for a descritpion of the contents
of the output folder after inference. The text is good, the natural language prompt should also have a second short 
setense asking PyAutoFit to customize the output folder with a .json file containing informaiton on the results
which are domain specific. This section should also more explicitly list and name what is in the files folder, 
show an excerp of model.json and drive home the point that all of this is key to building a scientific workflow
because it means you can scale inference to multiple datasets and track results easily.

- Visualization section next, for RTD this needs a few prompts that achieve what the Python code (Which the workspace)
version keeps will achieve. Prompt should be clear you can separate specify visualization before fit and during fit.

- NExt section should be on-the-fly output, which now works, so update all the code and scripts to actually use
this successfully. Link back to a scientific workflow -- this allows us to build up intuition for whether inference
is performing optimally or not. Make it clear you can link visualization to do this visualization of the model-fit
becomdes on the fly. Again, RTD needs good natural language prompt.

- I actually think rrom here we can closely follow the exiwting scientific workflow, we jusrt need good natural
language prompts on the RTD and maybe add in python code examples in the python script? Give me your thoughts
and suggestions and we'll make a plan and get this live. I think ending with an example, even if its just an image
or text showing a path folder, with like, 5 datasets, each with multiple model fits, each fitted with different
searches, all of which a user can navigate and inpsect on hard-disk or easily ask the assistant to give an assessment
of is the whole point! 

- The section "Model Composition" is good, but it is covered in the first guide model composition so frame it slightly
more around the point that this means we could fit loads of different models to one dataset and the scientific workflow
is not just about being able to fit different models but doing so in a way we can feasible interpret and comapre them.

- In HowToFit remove chapter_2_scientific_workflow, make it the final tutorial of chapter 1 BUT DONT PUT ANY CODE
have it briefly describe it, then link to the readthedocs page and workspace file.
