## keck-ao-acceptance-checks (Keck-AO checks 3–4 — plate-scale finding delivered — INTERIM, retired)
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/13 (STAYS OPEN — real finding + resumable fit)
- completed: interim 2026-07-09; active.md entry retired 2026-07-14 (/morning, human-directed — no longer actively tracked)
- summary: Check 3 delivered a concrete result — the adapter's narrow-camera `native_scale` (9.942 mas) is wrong for both epochs; truth is 9.952 mas pre-2015 (Yelda 2010; B1938 raw PIXSCALE 0.009952 agrees) / 9.971 mas post-2015 (Service 2016), so shipped phase-4 mosaics read θ_E ~0.10% low. Proposed fix (gated on review): epoch-aware `native_scale` selected with the distortion solution. Check 4 lens fit (SIE+shear+Sersic, Nautilus) ran ~1h CPU, not converged, 94MB checkpoint.
- residual (not blocking retirement): the epoch-aware `native_scale` fix + the check-4 θ_E-vs-0.45″ convergence are documented on #13 with resume commands; #13 stays OPEN as the backlog anchor. The 94MB checkpoint was on a laptop that reset — may need re-running from scratch on a quiet machine.

## Original prompt

# Keck-AO acceptance checks 3-4 — astrometry + Einstein-radius invariance

Type: test
Target: PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Original request: "do those checks" (follow-up to PyAutoReduce#11 / PR #12,
2026-07-09).

Complete the keck_ao.md validation-anchor acceptance checks left open at the
phase-4 merge:

3. **Astrometric parity vs HST** — compare the B1938+666 nirc2_native
   reduction's astrometry against HST imaging of the same system (own-pipeline
   WFC3 reduction if archival data exists, else published positions), and
   audit the narrow-camera plate-scale question (header PIXSCALE 9.952 vs
   adapter native_scale 9.942 mas; literature spread 9.942/9.952/9.971 —
   direct multiplicative bias on any measured Einstein radius).
4. **Science invariance** — fit the reduced dataset with PyAutoLens
   (SIE + shear, Sersic lens light/source) and compare the inferred Einstein
   radius with the published ~0.45" (Lagattuta et al. 2012 / Vegetti et al.
   2012).

Deliverables: results on a tracking issue; a parity appendix in
docs/design/keck_ao.md (+ any plate-scale correction to the adapter that the
audit demands). Analysis runs in prototypes/ on main (read-only until the
doc/source edit is user-approved — no --auto on this invocation).
