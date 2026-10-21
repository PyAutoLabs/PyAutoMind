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
Status: formalised
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

<!-- formalised by the Intake (Conception) Agent on 2026-10-21 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c053631f-5016-452b-a3f0-d983c632651f/scratchpad/intake_weighting.md -->
