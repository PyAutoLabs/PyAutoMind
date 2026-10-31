## howtogalaxy-chapter2
- issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/94
- completed: 2026-10-31
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/96
- merge-commit: b4a9a429c5067eb51e744d78f5eaf67e1c41c054
- summary: Implemented the full approved Galaxy Chapter 2 restructure: six teaching lessons plus summary, optional searches/speed/historical prior passing, practical output/VRAM/identifier details, visual prior tuning, MGE structural motivation, data-model-Analysis separation and component-based Prodigy-to-Nautilus chaining. Generated notebooks/catalogues and updated navigation. Merged concurrent Chapter 3 PR95 and preserved its source/notebooks exactly.
- validation: Final local smoke 28/28; generation 29/29; completeness 22; notebook code parse/navigation/catalogue/search-memory/whitespace checks pass. Independent review findings resolved. Full-size CPU JAX fixed-linear-neighbour likelihood, gradient and batch finite (4 parameters, 11,304 pixels). All 8 GitHub jobs passed on final head 93cab426; merge state CLEAN.
- limitations: Smoke skips sampling and caps data; bounded JAX check validates computation, not full inference convergence or GPU performance. Heart remains RED; no release or check bypass.
- heart-red-override: Live user authorised full HowToGalaxy implementation and PR despite RED, plus current-turn prm only if required checks and shipping gates pass. Exact authoritative reasons: "PyAutoFit: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)". Authorization and branch evidence recorded on issue, PR, active entry and autonomy log.
- decisions: User approved n_live=14 after current Nautilus rejected 10 for a 13-parameter model. Prior-tuned and reduced-complexity examples retain 75; reference 200; optional thorough run300. Fixed neighbour geometry preserves linear intensity solves; conditional uncertainties explicit. Multi-dataset description has no Python.
- scope: HowToGalaxy only; earlier HowToLens review checkpoint remains for separate implementation.
- checkpoint: /mnt/c/Users/Jammy/Workspace/Science/scratch/howto_chapter2_review_2026-10-31/HOWTOGALAXY_IMPLEMENTATION.txt
- cleanup: User explicitly approved removing the temporary worktree and generated simulated data/test output after merge; validation evidence retained in workspace scratch.

## Original prompt

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
