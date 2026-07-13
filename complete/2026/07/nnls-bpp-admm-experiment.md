## nnls-bpp-admm-experiment
- completed: 2026-07-09
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/370 (closed)
- prs: none (negative result; probes in autolens_profiling scratch/nnls_speedup/, ledger in results/notes/nnls_solver_ledger.md)
- summary: BPP and ADMM prototyped against the real systems as PDIP alternatives; BOTH FAILED gates. BPP: sign-init 95% correct, masked-Cholesky exact, converges rel dObj ~1e-15, but degenerate rect outskirts + collinear MGE force 36-53 factorizations (best magnitude-damped variant) vs PDIP 19-21 — slower. ADMM: plateaus rel dObj ~3e-6 after 3000 iters (needs <=1e-10); sublinear at cond~1e10; preconditioning blocked by positivity geometry. Conclusion: PDIP ~20 iters x fresh Cholesky is near-optimal for this problem class; faster positive-only solves require problem-level changes (n, conditioning, positivity model). Complete dead-end ledger: warm starts, fp32/IR, Gondzio MCC, BPP, ADMM
