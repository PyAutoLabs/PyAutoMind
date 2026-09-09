# Scientific workflow through natural language

Type: docs
Repos: @PyAutoFit @autofit_workspace @HowToFit

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
