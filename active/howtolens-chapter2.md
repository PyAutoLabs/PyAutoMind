Issue: https://github.com/PyAutoLabs/HowToLens/issues/113
Issued: 2026-11-01

## Overview
Implement the human-reviewed HowToLens Chapter 2 tutorials 1–4 from the 2026-10-31 review. HowToGalaxy Chapter 2 and both Chapter 3 checkpoints are already merged.

## Plan
- Apply the exact approved wording and subsequent corrections to Nautilus introduction, practicalities, why modeling is hard, and linear profiles/MGE.
- Consolidate superseded early lessons and repair references; retain later lessons pending their separate prose review.
- Regenerate notebooks/catalogue, validate scripts and scientific API details, and run repository smoke and CI.
- Create the PR and merge only after required checks pass, as requested in this chat.

## Detailed implementation
Repository: PyAutoLabs/HowToLens, clean main at 5249e06. Branch: feature/howtolens-chapter2.
Edit canonical scripts/chapter_2_lens_modeling sources; preserve Chapter 3. Retain VRAM Use and Unique Identifier sections and corrected output tree. Validate low-live-point Nautilus settings instead of claiming guaranteed failure. Retain shear in the 15-parameter, 45-linear-intensity MGE model. Use source-generated notebooks and catalogue. Tutorial 5/6 redesigned prose is not yet reviewed; do not silently implement it.

## Authorization and gates
User: “Can you PR, prm and merge our chapter 2 and 3 work on HowToLens and Galaxy which wasnt measured from yesterday”; after the outstanding approved Lens material was identified: “yeah get chapter 2 up to date”. Approved wording recovered from the original chat. Heart entry: STALE (exit 1), development only; fresh shipping gate required. No release or failed-check bypass.

