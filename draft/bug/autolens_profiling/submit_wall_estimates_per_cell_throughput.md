# Submit scripts quote an MGE step rate for pixelized cells and get…

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Filed: 2026-08-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/176 (issued 2026-08-26)
Blocked: registered in planned.md — autolens_profiling is claimed by log-det-multistart-tag (#175)

# Submit scripts quote an MGE step rate for pixelized cells and get killed

`autolens_profiling/hpc/batch_gpu/submit_phase8b_bijector_a100` set
`--time=0:30:00`, justified in its own comment as "16 starts x 3000 steps at
the #117-validated pixelized throughput is ~5 min including compile per task
(matches the diagnostic_theta_e submit's citation); --time below gives it 6x
headroom."

That citation is an MGE-cell throughput and does not transfer. Measured on
RAL 2026-08-25:

  mge                  0.117 s/step   (3000 steps ~ 350 s)  — matches the citation
  knn                  2.23  s/step   (3000 steps ~ 1.9 h)  — 19x
  delaunay_adapt_split 4.83  s/step   (3000 steps ~ 4.0 h)  — 41x

So the "6x headroom" was ~8x short for knn and ~16x short for delaunay. 35 of
39 arms in job 340576 were killed at roughly 12% of budget, losing an entire
overnight A100 block. Only the 4 mge control arms — the ones the citation
actually described — completed.

FIX: a per-cell throughput reference that submit scripts must cite, and/or a
guard, so an MGE step rate can never be quoted as the basis for a pixelized
cell's wall clock. The numbers above are the first measured rows.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p3.md -->
