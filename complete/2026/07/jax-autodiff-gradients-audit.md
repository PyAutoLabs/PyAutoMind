## jax-autodiff-gradients-audit
- completed: 2026-07-09
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/87 (closed)
- prs: https://github.com/PyAutoLabs/autolens_workspace_test/pull/157 (merged 1f34925) + https://github.com/PyAutoLabs/autolens_workspace_developer/pull/88 (merged 6c41fa8)
- summary: 3-phase JAX autodiff gradients audit complete in one supervised session — every smooth likelihood FD-certified (Sérsic, linear Sérsic through NNLS, MGE, point-source source-plane χ² incl. Hessian magnifications, FitWeak plain+z-scaled, RectangularUniform AD=FD 7 s.f.). Headline: RectangularAdaptDensity at os_pix=1 likelihood is exactly piecewise-constant in mass/shear (empirical-rank CDF invariance; AD-zero correct, FD staircase artifacts); user-requested extension certified BOTH adaptive meshes at production os_pix=4 incl. RectangularAdaptImage full production shape (reg.Adapt+AdaptImages+border relocator, ≤~1% mass). Delaunay re-confirmed hard-undifferentiable (pure_callback no JVP; custom_jvp zero rule = the unblock and correct a.e. derivative; PR#281 moot post-refactor). jax_grad suite upgraded finiteness→FD-correctness (util.py + 4 new scripts; stale dataset pointers fixed); audit README in jax_profiling/gradient/; methods_wiki autodiff-implicit-diff page filled. Heart YELLOW acked at ship; merge+close human-authorized in-conversation
- followups: 5 bullets in ideas.md (Delaunay custom_jvp; differentiable adaptive mesh via smooth-density CDF per arXiv:2606.30620; Grid2DIrregular xp gap; interferometer MGE FD test; NUTS/HMC trial on certified likelihoods)
- post-close extension (user-requested, same session): interferometer gradients — LP standard+linear FD-certified ≤~1e-6 through TransformerDFT; production sparse path (apply_sparse_operator + RectangularAdaptDensity + reg.Adapt) hits the staircase with NO over-sampling escape hatch (all gradients correctly zero — unusable); RectangularUniform on sparse path FD-certified = the interferometer gradient mesh. PRs: workspace_test#158 + workspace_developer#89 MERGED 2026-07-09 (human-authorized); branches deleted, mains fast-forwarded

## Original prompt

# JAX autodiff audit: light profiles, pixelized-source gradients, and likelihood gradients

Type: research
Target: autolens_profiling
Repos:
- PyAutoLens
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

You're working in the PyAutoLens or PyAutoArray codebase, using the usual profiling workspace, profiling agent, and PyAutoBrain flow. First, investigate the state of JAX autodiff support for Sérsic light profiles, linear Sérsic light profiles, and Multi-Gaussian Expansion light profiles. Profile what's there, identify what breaks tracing or differentiation, and add or refine automated tests comparing autodiff against finite differences. Second, investigate gradients for pixelized source reconstructions, starting with the Delaunay mesh. We expect that full gradients may not be feasible there. Confirm why and document where it fails. Then move to the rectangular mesh, where we think gradients might be possible. Before starting that part, ask me for the relevant paper if you don't already have it. Third, validate gradients for the source plane chi-squared used for point sources, and for the weak lensing likelihood.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; work-type & target corrected in review: research / autolens_profiling) -->
