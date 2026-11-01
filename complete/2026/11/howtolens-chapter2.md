# HowToLens Chapter 2 reviewed lessons — merged checkpoint

- issue: https://github.com/PyAutoLabs/HowToLens/issues/113
- completed: 2026-11-01
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/115
- merge: 1a8ed8bd56b56b2c18b6c7285c1800f8d1faeffc
- summary: Applied approved tutorials 1–4, optional Prodigy introduction, notebook generation and navigation. Later Chapter 2 lessons remain for separate review.

## Validation
Official isolated Python 3.12 local smoke: 43/43 passed. Canonical Hands notebook generation: 44/44 passed. Notebook structure, navigation, search-memory, 32 tutorial-completeness checks and whitespace checks passed. Independent source review CLEAN. Final combined head d894472d2fe052b1df22404f117c20e544e67b3e passed 3 workflows / 8 jobs including Python 3.12 and 3.13 smoke. All commits proved ancestors of origin/main after merge.

Nautilus requires 21 live points for the actual 20-parameter ordinary model; 10 was rejected by the live guard. Comparisons use 21/75/75/300. MGE retains shear and independent lens/source geometry: 15 free parameters and 30+15 solved linear intensities. Smoke does not establish sampling convergence or runtime claims.

## Integration and next work
Main's Chapter 1 PR #114 was incorporated; Chapter 1 and Chapter 3 source/notebooks match that main exactly. Galaxy Chapter 2 PR #96 and Chapter 3 PR #95 were already merged; Lens Chapter 3 PR #112 was already merged.

Continue five-block human review at proposed Tutorial 5 Data and Likelihoods, then 6 Search Chaining and optional/summaries/navigation restructuring. See draft/docs/howtolens/chapter2_continuation.md. Do not redo approved lessons 1–4 or imply the remaining restructure shipped. Existing later lessons retain numbering 6–11 for now.

Readiness was STALE: release validation incomplete: no rehearsal for current source. This was development shipping only; no release-readiness claim.

User checkpoint: /mnt/c/Users/Jammy/Documents/Codex/2026-11-01/can-x20/outputs/chapter2-checkpoint.txt

## Original prompt

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

