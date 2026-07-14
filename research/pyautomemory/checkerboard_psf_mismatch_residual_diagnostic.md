# Checkerboard PSF-mismatch residual diagnostic — research + document + ingest papers

Type: research
Target: PyAutoMemory
Repos:
- autolens_assistant
- PyAutoMemory
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Checkerboard PSF-mismatch residual diagnostic: research and document the central checkerboard/aliasing residual pattern that indicates an incorrect or mismatched PSF model in lens/galaxy fits (wrong sub-pixel centering, wrong oversampling/pixel scale, or an undersampled/resampled library STDPSF that does not match drizzled data). Seen in PJ011646 stdpsf_baseline (new drizzled mosaic + legacy library STDPSF) but absent with STARRED. Deliverables: (1) find 2-4 authoritative papers (e.g. Anderson & King ePSF, drizzle/interpolation aliasing, PSF sub-sampling/centering artifacts); (2) ingest them into PyAutoMemory (methods_wiki/lensing_wiki) and the autolens_assistant literature wiki (wiki/literature/sources via al_ingest_paper); (3) add a concise autolens_assistant wiki concept reference for the checkerboard-PSF-residual diagnostic (appearance, causes, fixes: better-centered/known PSF, correct oversampling, STARRED/empirical ePSF over library STDPSF), cross-linked to the ingested papers.

<!-- formalised by the Intake (Conception) Agent on 2026-07-14 from user-intake -->
