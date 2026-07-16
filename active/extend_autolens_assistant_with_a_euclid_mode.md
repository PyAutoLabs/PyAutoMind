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
