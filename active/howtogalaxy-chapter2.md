# HowToGalaxy Chapter 2 restructure

Target: @HowToGalaxy
Issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/94
Issued: 2026-10-31
Type: docs
Consequence: judge

## Original implementation request (verbatim)
Yes, proceed with the full HowToGalaxy implementation despite Heart RED, validate it and get the PR up. Do prm if the required checks and shipping gates pass.

## Approved scope
Adapt the approved HowToLens Chapter 2 prose to galaxy modeling without further block reviews. Use six tutorials: non_linear_search (Nautilus only), practicalities (merge realism and concise results), why_modeling_is_hard, linear_profiles, data_and_likelihoods, search_chaining. Move speed and historical prior passing to optional; replace optional LBFGS with MultiStartProdigy alongside MCMC. Preserve observational narrative, practical output tree/identifier/VRAM details and scientific distinctions. Link results and multi_dataset as advanced follow-up. Use neighbouring-galaxy component separation for Galaxy chaining. Regenerate notebooks and navigation; smoke and API validate. Do not edit Lens or Chapter 3 content owned by another chat.

## Plan
- Apply approved Chapter 1–4 lesson adaptations to Chapter 2 tutorials 1–4.
- Implement data/likelihood and component-chaining lessons using current Galaxy examples.
- Update optional material, numbering, references, build configuration and generated artefacts.
- Validate, open PR, and merge only if all required shipping gates/checks pass.
Tier: judge — merge mode: explicit current user /prm conditional on green checks.

Detailed review checkpoint: /mnt/c/Users/Jammy/Workspace/Science/scratch/howto_chapter2_review_2026-10-31/RESUME.txt (approved exact prose in current chat).

## Branch survey
HowToGalaxy main clean at ead53e6; task branch feature/howtogalaxy-chapter2.
Chapter3 merged separately in HowToGalaxy#95 (06876fe); checkpoint: complete/2026/10/howto-chapter3.md. Integrate current main and regenerate shared catalogues while keeping Chapter3 content intact.
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtogalaxy-chapter2/HowToGalaxy

## Validation plan
AST/compile and API grounding; smoke changed scripts, full required smoke as feasible; regenerate with Hands and validate catalogue/notebook/link paths. Real fits needed to substantiate convergence/runtime; no fabricated timings. Heart RED override above permits this implementation and PR, no release or failed-check bypass.
