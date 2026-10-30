# autolens_assistant: ingest LEGGOS II (area magnification method) into the literature wiki (arc phase 6d)

Type: docs
Target: autolens_assistant
Repos:
- autolens_assistant
Epic: cluster-strong-lensing
Phase: 6d
Parent: draft/feature/autolens/area_magnification_leggos.md
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Filed: 2026-10-30
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/170
Witness: canonical BibTeX entry for Abedi et al. 2026 (arXiv:2606.20804), a claim-support section in `wiki/literature/sources/cluster-lensing.md` with only claims verified from the paper, concept link, log row, and `python -m autoassistant.literature validate-citations` passes.

## Original request (human, 2026-10-30)

> go

(continuing phase 6 after 6c; phase-6 parent item 4: "Ingest LEGGOS II into autolens_assistant wiki/literature
(bibkey, source entry, magnification-methodology claims) so future cluster work cites it.")

## Verified from the paper (arXiv HTML, 2026-10-30)

Abedi, Sharon, Hutchison, Bayliss, ... (21 authors), submitted 2026-06-18, under review at ApJ, arXiv DOI
10.48550/arXiv.2606.20804, astro-ph.GA. SDSSJ1110+6459 (z=0.659) Lenstool 8.6.4 model with JWST NIRCam/NIRSpec + HST;
arc magnification Eq. 6 μ_arc = A_img/A_src, Eq. 7 A_src = Σ_i A_pix,i/μ_i; clump magnification = map value at the
pixel containing the clump centroid (0.03″ map); arc masks kept on the arc's side of the critical curve (recomputed
per posterior model); uncertainties from 300 posterior models.
