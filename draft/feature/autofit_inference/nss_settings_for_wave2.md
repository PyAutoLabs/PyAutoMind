# NSS settings for the wave-2 inference run: at least 50 MCMC steps, not the n_live_200 default

Type: feature
Target: autofit_inference
Repos:
- autofit_inference
Difficulty: trivial
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Epic: search-extensibility
Blocked-by: NSS deferral in autofit_inference being lifted (B5 wave 2)
Witness: the NSS settings entry the wave-2 run uses sets at least 50 MCMC steps (about 5×ndim for the 10-parameter `gaussian_x3_blend`); a pilot of 3 seeds on `gaussian_x3_blend` recovers all ordered centres, with ln Z inside the reference spread.
Unattended: ready
Filed: 2026-10-08

Found by the A3b witness (PyAutoFit#1678 / PR #1681, record `complete/2026/10/search-ext-a3b-nss-preflight.md`). NSS fitted `gaussian_x3_blend` under JAX on CPU at fp64.

**Default settings (n_live 200, 5 MCMC steps):**
- seed 0: ln Z 133.98, correct;
- seed 1: converged to the wrong mode;
- seed 2: ln Z about 27 nats low.

**n_live 200 with 50 MCMC steps:**
- seeds 0–2: ln Z 135.35, 137.62 and 135.67, with all centres correct;
- that is inside the reference spread (Nautilus 137.06/137.07, Dynesty 134–139.7).

**Why it matters:** NSS is deferred from the B3 pilot. When B5 wave 2 lifts that deferral, the obvious settings entry (`n_live_200`, sampler defaults) would score NSS as unreliable. That would be a settings artefact, not the sampler. Fix it before the scored run, not after.

**Completion criterion:** the Witness above. The settings rationale (steps ≈ 5×ndim) is recorded next to the entry, and this note is cited from the B5 plan.
