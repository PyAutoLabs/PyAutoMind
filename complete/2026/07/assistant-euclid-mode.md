# Assistant euclid mode — pipeline-paired skills + dedicated euclid wiki

## Outcome

Euclid mode shipped end-to-end on 2026-07-16; issue
https://github.com/PyAutoLabs/autolens_assistant/issues/73 closed, both PRs MERGED:

- euclid_strong_lens_modeling_pipeline#27 (Phase 0) — removed `profiling/` and
  `skills/` (nothing referenced either); fixed stale `scripts/README.md` file
  list and `initial_lens_model.py` docstring (`pipelines/` → `scripts/`,
  Jammy2211 → PyAutoLabs URL).
- autolens_assistant#74 (Phases 1+2, two commits on one branch since they
  cross-reference) —
  - Five `euclid_*` skills pairing the pipeline: `euclid_setup_pipeline`
    (install, dataset layout, black-box `start_here.py`), `euclid_prepare_data`
    (segmentation validation + GUI mask/centre tools), `euclid_model_lens`
    (staged progression: initial MGE+SIE → Sersic photometry → lens-only
    subtraction → multi-waveband → full SLaM, with a goal→stage table),
    `euclid_workflow_products` (csv/fits/png aggregator products),
    `euclid_hpc_runs` (`hpc/sync` + SLURM arrays). New `euclid_<task>`
    domain-mode naming convention registered in `skills/README.md`; routing
    note in AGENTS.md; pipeline added to `sources.yaml`.
  - `wiki/euclid/` — fourth sub-wiki on the literature schema: 7 entities
    (euclid-mission, vis, nisp, euclid-wide-survey, ext-surveys, q1-dr1-releases,
    ou-phz), 4 concepts (euclid-psf, zero-point-corrections, psf-homogenisation,
    euclid-photo-z), 4 sources pages (strong-lensing Discovery Engines A–F +
    ERO/NGC 6505, mission-data, forecasts, dr1-image-processing), bibliography.

## Key decisions

- "Mode" = skills family + sub-wiki, NOT a `modes/` interaction preset
  (modes stay teacher/assistant only) — user-approved at plan time.
- Bibliography keys are the Euclid Collaboration's own (`Q1-SP048`,
  `EuclidSkyOverview`, `Q1-TP004`…), 21 entries copied VERBATIM from
  euclid_assistant's shared `euclid.bib`; 9 pre-Euclid classics (Ma06,
  Huterer06, Amara&Réfrégier07, Kitching08, HSC Miyazaki18, CFIS Ibata17,
  Pan-STARRS Chambers16, DES Abbott21, Boucaud16) verified against public
  arXiv/Crossref metadata (every DOI resolved + title-matched) before entry.
  `bibkey_aliases.yaml` maps author-year names and the two overlapping
  `autolens_literature.bib` keys (EuclidCollaboration2025→Q1-SP048,
  2025b→Q1-SP052).
- `Euclid_DR1_impact_image_processing.pdf` (Fogliardi et al. 2026 draft, values
  preliminary) ingested as content only into
  `wiki/euclid/sources/euclid-dr1-image-processing.md`; PDF NOT committed to
  the public repo; NO bib entries for in-prep DR1 papers (Aussel/Lines/
  Holloway/Nightingale/Nersesian/Vincken/Kümmel/McCracken/Polenta 2026) until
  public metadata exists.
- Shipped through an unrelated Heart RED ("PyAutoLens: 1 uncommitted source
  change(s)") on explicit user ack; no scripts changed (markdown/deletions/
  docstrings), pipeline python compileall-verified, citation validator green.

## Traps / notes for future sessions

- `autolens_assistant` has NO `pending-release` label — assistant PRs ship
  unlabelled (the label guard covers workspace repos only).
- The Q1 Discovery Engine key mapping (papers ↔ collab bib keys): A=Q1-SP048
  Walmsley, B=Q1-SP052 Rojas, C=Q1-SP053 Lines, D=Q1-SP054 Li (double source
  plane), E=Q1-SP059 Holloway, F=Q1-Ecker; SP085=Lines sims-to-sky ML;
  Q1-Vincken=AstroVink ViT; TP002=McCracken VIS, TP003=Polenta NIR,
  TP004=Romelli MER (Kümmel 2nd author — "Kümmel 2026" is the in-prep DR1 MER
  update), TP005=Tucci PHZ.
- This same session fixed the intake conductor + sizing faculty for the Mind#71
  lifecycle layout (draft/ prefix, census/reconcile against active/ +
  complete/) and re-homed two root-level stray prompts.

## Follow-up

User will model a small fraction of lenses through euclid mode and iterate on
features/functionality the Euclid science paper needs (new tasks as they arise).

## Original prompt

# Extend autolens_assistant with a euclid mode

Type: feature
Target: workspaces
Repos:
- autolens_assistant
- euclid_assistant
- euclid_strong_lens_modeling_pipeline
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

In the project euclid_strong_lens_modeling_pipeline, we have all the examples used for modeling euclid data.
This is the github project I put standard pipelines out there to the collaobration so they can perform the
modeling themselves.

However, science was done at the path /mnt/c/Users/Jammy/Science/euclid, but this accumulated a lot of extra
scripts and code which is not really important for general Eulcid science.

I want to consoliate euclid_strong_lens_modeling_pipeline as a repo which has all the necessary code and infrastructure
to reproduce the resutls of the euclid paper. For now, lets assume euclid_strong_lens_modeling_pipeline is complete,
what I will do is I will gradually do a series of tasks in order to validate I get the results I want.

First remove the "profiling" and "skills" folders, which are no longer required.

The real task, is to extend the autolens_assistant with a "euclid" mode, which has the following aims:

1) It uses the euclid_strong_lens_modeling_pipeline to model euclid data, which means it will need its own wiki of skills which
pair the euclid modeling scripts to the assistant.

2) For the literature have a dediciaged euclid_wiki which contains all the strong lensing euclid papers for reference
but also non lensing euclid papers describing the instrument and other parts of the data.

Look in euclid_assistant/*/euclid.bib and use these papers:

Amara & Réfrégier 2007;
Euclid Collaboration: Mellier et al. 2025;
Ma et al. 2006; Huterer et al. 2006;
Kitching et al. 2008;
Euclid Collaboration: Tucci et al. 2025;
Euclid Collaboration: Cropper et al. 2025;
Euclid Collaboration: Jahnke et al. 2025;
Euclid Collaboration: Walmsley et al. 2025a;
Euclid Collaboration: Rojas et al. 2025;
Euclid Collaboration: Lines et al. 2025;
Euclid Collaboration: Li et al. 2025;
Euclid Collaboration: Holloway et al. 2025;
Euclid Collaboration: Ecker et al. 2026;
Euclid Collaboration: Romelli et al. 2025;
Euclid Collaboration: Kümmel et al. 2026

These papers describe EXT data which is part of Euclid Data:

Combining data from the Subaru Hyper Suprime Camera (HSC; Miyazaki et al. 2018) for the g and z bands; the
Canada–France Imaging Survey (CFIS; Ibata et al. 2017) for the u and r bands; and the Panoramic Survey
Telescope and Rapid Response System (Chambers et al. 2016, Pan-STARRS) for the i band. In the Southern
Hemisphere, we use imaging from the Dark Energy Survey (DES; Abbott et al. 2021) in the griz bands.

The PSF of a particular band is unique to the target depending on its tile and sky coordinates
(Euclid Collaboration: McCracken et al. 2025, 2026; Euclid Collaboration: Polenta et al. 2025, 2026).

The ZPCs were calculated by the Euclid Photometric-Redshift Organisation Unit (OU-PHZ; Euclid Collaboration:
Desprez et al. 2020).

Also put PyAutoLabs/Euclid_DR1_impact_image_processing.pdf in there.

The standard approach to calculate aperture photometry across multiple wavebands is to first homogenise the
PSFs by generating convolution kernels that match higher-resolution images to the lowest-resolution band.
For example, Euclid Collaboration: Romelli et al. (2025) employed the kernel creation algorithm of
Boucaud et al. (2016), which builds convolution kernels based on Wiener filtering with a tunable
regularisation parameter.

The Euclid satellite will detect 1.5 billion galaxies over the Euclid Wide Survey (EWS, Euclid Collaboration:
Mellier et al. 2025; Euclid Collaboration: Scaramella et al. 2022). With an area of 14 000 deg2 (Euclid
Collaboration: Mellier et al. 2025), a IE PSF of 0.16" (Euclid Collaboration: McCracken et al. 2026; Euclid
Collaboration: Cropper et al. 2025), as well as three near-infrared bands providing crucial colour
information (Euclid Collaboration: Jahnke et al. 2025), the survey will revolutionise strong lensing.

(Acevedo Barroso et al. 2025; O'Riordan et al. 2025)

There are lots of papers above with key context on euclid strong lensing but also the instruments, data,
photo-zs etc.

Look at the euclid_assistant but note that, for now, the goal is not to have its type setting and editing
tools for papers to make it into autolens_assistant — this is just to help euclid strong lens modeling.

Once euclid mode is in place, I will then start modeling a small fraction of lenses and we can iterate
on what features and functionality need adding given the science paper.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/e54ae416-6430-4a1c-a39b-f6d17c43de25/scratchpad/intake_raw.md -->
