## positions-source-jacobian-default
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/791
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/792
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/593
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/346

- **Library:** `al.FitPositionsSource` now defaults to `weighting = "jacobian"`, with Bᵢ = Aᵢ⁻ᵀΘᵢAᵢ⁻¹ (Gravity.jl, Lombardi 2024 Eq. 46; the Solved class is Eq. 58). `"magnification"` (Jullo 2007 Eq. 10, scalar μ²/σ²) is kept as an opt-in. Its normalisation was changed from the 1-D, μ-dependent Σ log(2πσ²/μ²) to the model-independent Σ log((2π)²σ⁴), i.e. Eq. 46 with B ≈ μ²Θ.
- **Human decisions:**
  - Two weightings × two centres. There is no plain-barycentre option, because Solved already gives the optimal centre and a Lenstool-only reproduction was not wanted.
  - `jacobian` is the default because it is the more robust statistic.
- **Lenstool check:** Lenstool 8.10.1 `o_chi.c`, read from a personal mirror, not the official repo.
  - Lenstool's default is image-plane (`forme -1`).
  - `forme 8/13` is the tensor form and equals our jacobian.
  - Its scalar modes weight by |μ|, not μ².
  - Our old `"magnification"` matched the paper's Eq. 10 but no Lenstool code path.
  - The Mahler SMACS0723 input is `forme -1`, so the workspace Lenstool example now uses `FitPositionsImagePairRepeat`.
- **Workspace:** the full explanation of the default lives in the new "Source-plane weighting" section of `guides/point_source_pairing.py`. The `cluster/likelihood_function.py` walkthrough was rewritten to the jacobian form.
- **Workspace_test:** `source_plane.py` was re-pinned from −331481.26 to −104.67. The change is fully accounted for: the normalisation contributes +2.11, and χ² dropped from 662,993 to 244 (one image has μ ≈ 82).
- **Re-filed:**
  - `draft/docs/autolens_profiling/positions_source_jacobian_default_rerun_note.md` (the profiling scope, deferred because of the claim conflict);
  - `draft/bug/autolens_workspace/cluster_likelihood_scripts_preexisting_mismatches.md` (two pre-existing script problems).
- **Mind traps:** prompt_sync_push hit non-fast-forward pushes repeatedly. A plain `pull --rebase` on a clean tree fixed each one.

## Original prompt

# FitPositionsSource default "magnification" weighting mis-maps near-critical noise: check against Gravity.jl, consider defaulting…

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_profiling
- autolens_visualization
- autolens_workspace
- HowToLens
Difficulty: too-large
Autonomy: human-required
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/lens-modeling-methods.md; wiki/lensing/sources/dark-matter-substructure.md
Status: issued
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/791
Consequence: judge
Review-minutes: 25
Unattended: never

@PyAutoLens @autolens_workspace @autolens_profiling

## Request (human, 2026-10-21)

> intake an issue on the bug thing, have the issue check against the gravity.jl paper

## Finding (2026-10-21, while prototyping the source-plane fit panel)

`FitPositionsSource` (`autolens/point/fit/positions/source/separations.py:174-177`) defaults to `weighting = "magnification"`:
- χ²ᵢ = |β̂ᵢ − c|² · μᵢ² / σᵢ², i.e. an isotropic source-plane noise radius of σ/|μ|.
- The true source-plane footprint of image-plane noise σ is the ellipse σ·AAᵀ. For an isothermal lens its radial semi-axis stays σ, so the scalar convention under-states radial noise by ~|μ| on near-critical images.

Numbers on the autolens_visualization point_source true model (σ = 5 mas, μ = 6.7/69/47/102):

| Model | Image-pair χ² | Default source χ² (σ/\|μ\|) | Source χ², weighting="jacobian" |
|---|---|---|---|
| True model | 4.25 | **10,023** | 5.41 |
| R_E + 0.01″ | 53 | 167,321 | 120 |
| Lens centre x + 0.005″ | 6,243 | 20,364 | 6,012 |

On the multi-plane cluster true model, point_0's default source χ² is 81.8 (jacobian 4.46).

The jacobian weighting tracks the image-plane χ² ordering; the default does not.

## Prior work (do not redo)

- `complete/2026/07/point-source-chi-squared-variants.md` implemented the Lombardi 2024 (arXiv:2406.15280, *Gravity.jl: Fast and accurate gravitational lens modeling in Julia*, A&A 690, A346) solved likelihoods and added `weighting = "jacobian"|"magnification"`.
- Its benchmark (profiling#99) already found the scalar-μ² source plane "catastrophically biased" (truth −33788 vs wrong models −110 on a μ=367 image), with the tensor weighting as the fix.
- `FitPositionsSourceSolved` defaults to "jacobian". `FitPositionsSource` kept "magnification", apparently for Lenstool-style comparability.

## Scope

1. **Check against the Gravity.jl paper (full text):** its source-plane χ² definition, weighting, and normalisation / log-det terms. Confirm exactly what our "jacobian" implements (precision Wᵢ = Aᵢ⁻ᵀΘᵢAᵢ⁻¹, observed-plane normalisation) and whether "magnification" corresponds to any convention the paper endorses. Quote the equations.
2. **Decide the default** (human decision): switch `FitPositionsSource` to "jacobian", keep "magnification" with a loud docstring/warning, or deprecate it. Weigh backwards compatibility: existing results, the Lenstool comparisons, and the workspace/HowToLens text that describes the μ² weighting.
3. **If switching:**
   - library change plus tests (truth ranks first on an anisotropic mock)
   - workspace and tutorial prose updates
   - an autolens_profiling/inference rerun note
   - a changelog/release-note line, since this changes source-χ² modelling results
4. **Cross-check** with the new source-plane fit panel, which draws both the σ/|μ| circle and the A·σ ellipse. Prototypes are in `/mnt/c/Users/Jammy/Science/scratch/eyes/autolens/source_plane_prototype/`.

## Findings (2026-10-21, start_dev session: paper + Lenstool source check)

**Gravity.jl** (Lombardi 2024, arXiv:2406.15280, §5.1):
- Eq. 46: log P = Σ[½ log|Θᵢ/2π| − ½ (β̂ᵢ−β)ᵀ Bᵢ (β̂ᵢ−β)], with Bᵢ = Aᵢ⁻ᵀ Θᵢ Aᵢ⁻¹. The normalisation is image-plane only and model-independent.
- Eqs. 49, 54–58: precision-weighted β̄ and analytic marginalisation of the source, adding −½ log|B/2π|.
- No scalar-μ² approximation is discussed. Lenstool is mentioned only for timing and for agreement on lensing quantities.
- Our `"jacobian"` equals Eq. 46 for the free centre. `FitPositionsSourceSolved` equals Eq. 58.

**Lenstool:**
- **Paper.** Jullo et al. 2007 (arXiv:0706.0048), Eq. 10, writes the scalar form |β−⟨β⟩|² μ²/σ². It gives no source-plane normalisation.
- **Code.** Lenstool 8.10.1 `src/o_chi.c` `chi2_src()`, read from the mirror github.com/tomresseguier/lenstool-perso (not the official CRAL repo). The source-plane mode is selected by `image.forme`:
  - `forme 8/13` ("the proper way"): (A⁻¹δ)ᵀ W (A⁻¹δ). This is the same as Gravity.jl Bᵢ and Keeton 2001 Eq. 10.
  - Scalar modes: weight by |μ|/σ², or by a system-averaged det A. These are not μ²/σ².
  - Default `forme -1`: an image-plane fit.
  - Every source-plane mode adds log(4π²/det W). This is model-independent only in `forme 8/13`.
  - The centre is a plain or √μ-weighted mean, and the source is never marginalised.
- **Gravity.jl vs Lenstool.** The two codes do not disagree: our `"jacobian"` with its normalisation equals Lenstool `forme 8` for circular errors.
- **Our `"magnification"`.** It matches Jullo's Eq. 10 chi² but no Lenstool code path. Its normalisation Σ log(2πσ²/μ²) is 1-D and model-dependent (it rewards high μ) and matches no Lenstool mode.
- **The workspace Lenstool example is mislabelled.** The Mahler SMACS0723 ICLv2 `input.par` uses `forme -1`, an image-plane fit. So `autolens_workspace/scripts/cluster/lenstool/modeling.py:34-37` is wrong to map it to `FitPositionsSource` with the "scalar μ² convention".

## Decisions (human, 2026-10-21)

- **Keep two weightings × two centres.** Weighting is `"jacobian"` or `"magnification"`. Centre is free (`FitPositionsSource`) or solved (`FitPositionsSourceSolved`). There is no separate barycentre option: Solved already gives the optimal centre, and a Lenstool-only reproduction is not wanted.
- **Default to `"jacobian"` in both classes.** For `FitPositionsSource` this is a new default; `FitPositionsSourceSolved` already uses it.
- **Fix `"magnification"`.** Make it Eq. 46 with B ≈ μ²Θ, i.e. give it the model-independent 2-D normalisation log((2π)²σ⁴) in both classes. Document its radial-direction bias near critical curves.
- **Fix the workspace Lenstool example** and its README: point them at the image-plane fit.
- **Defer the autolens_profiling rerun note** until the `cluster-pointsolver-robust-settings` claim is released.
- Tier judge → human /prm.

<!-- formalised by the Intake (Conception) Agent on 2026-10-21 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c053631f-5016-452b-a3f0-d983c632651f/scratchpad/intake_weighting.md -->
