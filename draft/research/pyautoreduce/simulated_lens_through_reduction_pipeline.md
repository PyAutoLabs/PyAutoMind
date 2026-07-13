# Feasibility: run a simulated strong lens through the full instrument reduction pipeline (HST/JWST/ALMA)

Type: research
Target: pyautoreduce
Repos:
- PyAutoReduce
- PyAutoLens
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Research task in the PyAutoReduce repository.

Assess the feasibility of feeding a simulated strong lens through the full instrument reduction pipeline. The idea: take an image of a strong lens — or a model of one built from a Sérsic profile, the way the simulator.py scripts do on the autolens_workspace — and have the option of running it through the full reduction analysis and pipeline for HST, JWST, ALMA, or whatever instrument.

This is more complicated than the normal flow because, rather than downloading real images from (say) the HST archive, the code would almost need to simulate those raw-instrument images itself, which can require many steps. For example, adding cosmic rays is something PyAutoReduce does not currently do, so this may not be feasible without a lot of work.

Do not spend a lot of time building something intricate. A minimal result is fine — e.g. getting a single simulated strong-lens image, at the size of a full tile, to pass through the pipeline. The goal is to assess whether there is a way to do this that is NOT an over-the-top amount of work, and to survey existing open-source repositories that could get us part of the way there.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; work-type research confirmed by user; target corrected workspaces->pyautoreduce in review — the classifier matched the autolens_workspace mention rather than the home repo) -->
