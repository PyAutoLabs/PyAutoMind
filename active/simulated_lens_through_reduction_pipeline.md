# Feasibility: run a simulated image through the full instrument reduction pipeline (HST/JWST/ALMA)

Type: research
Target: pyautoreduce
Repos:
- PyAutoReduce
- PyAutoLens
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised

Research task in the PyAutoReduce repository.

Assess the feasibility of feeding a simulated strong lens through the full instrument reduction pipeline. The idea: take an image of a strong lens — or a model of one built from a Sérsic profile, the way the simulator.py scripts do on the autolens_workspace — and have the option of running it through the full reduction analysis and pipeline for HST, JWST, ALMA, or whatever instrument.

This is more complicated than the normal flow because, rather than downloading real images from (say) the HST archive, the code would almost need to simulate those raw-instrument images itself, which can require many steps. For example, adding cosmic rays is something PyAutoReduce does not currently do, so this may not be feasible without a lot of work.

Do not spend a lot of time building something intricate. A minimal result is fine — e.g. getting a single simulated strong-lens image, at the size of a full tile, to pass through the pipeline. The goal is to assess whether there is a way to do this that is NOT an over-the-top amount of work, and to survey existing open-source repositories that could get us part of the way there.

## Update 2026-07-16 (user re-raised via /intake; merged here instead of filing a duplicate)

The input need not be a strong lens — any image is fine as the input; what
matters is simulating the corresponding image after it is processed by HST,
JWST, ALMA, or whatever instrument.

The user's framing of the feasibility question (verbatim, typos preserved):

> My question is basically, how feasible would this be to implement in
> PyAutoReduce? On the one hand, it feels like after the simulate simulation
> procedures it would just be a metter of running things through PyAutoReduce.
> On the other hand it requires many simulation steps data reduction pielines
> dont natively have (e.g. cosmic rays, noise generation). Assess whether you
> consider this in scope for the project, or whether you consdier this
> something that is too much work or better served using another package? Do
> some deep research against the literature to asssess if we need to write our
> own code or if we can just combine PyAutoReduce with something like GalSim.

So the deliverable now explicitly includes: (a) an in-scope / out-of-scope /
better-served-elsewhere verdict for PyAutoReduce, and (b) a literature / prior-art
deep-research pass (GalSim and peers — e.g. instrument image simulators such as
STScI's tools, ALMA's simobserve) deciding build-vs-combine before any code is
written.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; work-type research confirmed by user; target corrected workspaces->pyautoreduce in review — the classifier matched the autolens_workspace mention rather than the home repo) -->
<!-- updated 2026-07-16: merged the re-raised /intake ask (generic input image, GalSim build-vs-combine literature research); priority normal->high on re-raise -->

