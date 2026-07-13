[SLaM]

- With Claude, no longer any point mainitaing slam_pipeline as a seaprate pckage as the benefits of condensing
all the code are outweighed by the overhead of maintaining a separate package and documentation. So now
make each slam pipeline standalone with documentation explaining their links.
- Also do work to unify lots of tasks via similar things to mge_model_from and work out how to simplify some chaining util use.

[Results]

- Maybe give explicit examples of all key calculations using from_json and the results int he output folders.
- The results folder example is heavily focused on Aggregator, whcih I think is right but we should make result
manipulatgion of the contents of the output folder really clear.
- For linear light profiles we probably want to get the latent variables for the solved for intensitities in.

[Scientific Workflow]

- Build on existing readthedocs with Claude to fully flesh out the scientific workflow API.
- Turn into HowToFit Chapter 2 and single notebook standalone guide.
- Turn single notebook into an example for autolens and autogalaxy, adding to end of chapter 2 of HowTo (or a whole chapter? Wait and see,. prob not.)