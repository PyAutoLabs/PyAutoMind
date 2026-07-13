# Nautilus NN-training bottleneck: speed-up options for fast likelihoods

Type: research
Target: PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

the biggest bottleneck with Nautilus is that when the likelihood function is very fast (e.g. mge only source on GPU) the time it takes to train the neural networks that inform the nested sampling's next sample is slow, it has overheads, etc. If this supported JAX, it'd be really fast, but JAX-ifying nautilus is probably infeasible (but think about this). Work out if there is any redesign or refactor or work we could do on nautilus to make this bottleneck less problematic or speed it up. Long term we'll probably swap sampler to something JAX native but we haven't found a great one yet, and nested sampling is what we're used to, and recent JAX nested samplers still were not fast enough.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
