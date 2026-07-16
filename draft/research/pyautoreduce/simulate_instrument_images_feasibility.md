# PyAutoReduce can currently download and reduce real datasets

Type: research
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised

PyAutoReduce can currently download and reduce real datasets. However, I would like for it to have the option
to input an image (this could be of a strong lens, but really any kind of image is fine as the input is not important)
and then simulate the corresponding image of it after its processed by HST, JWST, ALMA, or whatever.

My question is basically, how feasible would this be to implement in PyAutoReduce? On the one hand, it feels like
after the simulate simulation procedures it would just be a metter of running things through PyAutoReduce. On the
other hand it requires many simulation steps data reduction pielines dont natively have (e.g. cosmic rays, noise generation).
Assess whether you consider this in scope for the project, or whether you consdier this something that is too
much work or better served using another package? Do some deep research against the literature to asssess if we
need to write our own code or if we can just combine PyAutoReduce with something like GalSim.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/59a19942-c45f-4f2a-ad18-6bcc3dd8a7ba/scratchpad/chunk2_research.md -->
