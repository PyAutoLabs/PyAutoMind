# LensTwin phase 4: first identifiability experiment — can a Euclid-like twin recover an injected stellar M/L and NFW κ_s (then a gNFW inner slope)? Run inside a `Science/active` project, local smoke then one RAL array

Type: research
Target: autolens
Repos:
- Science (private; a `Science/active` project — not attached to remote sessions)
Themes:
- mge
- hpc-gpu
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Witness: on the no-misspecification configuration (simulate and fit with MGE stellar `lmp` basis at fixed solved intensities + one free M/L, `NFWSph` with free κ_s and r_s centred on the light, shear free, MGE source), the injected M/L and κ_s lie inside the 3σ posterior intervals for every seed; the `gNFWSph` configuration reports the posterior width on `inner_slope`; every run directory carries `files/twin.json` so truth joins posterior through the aggregator
Review-minutes: 60
Unattended: never
Epic: lenstwin
Phase: 4
Parent: draft/feature/autolens/lenstwin_epic.md
Blocked-by: (1) a PyAutoGalaxy/PyAutoLens release carrying phases 0, 2, 3 and the gNFW speed-up (PyAutoGalaxy#672, #676, #678; PyAutoLens#804, #806) — human `/review_release`; (2) the human names the `Science/active` project and the first real fit (MGE light + SIE + shear + MGE source); (3) a session with that Science checkout (laptop, or a Remote Control folder); (4) an explicit human compute go for the RAL array
Filed: 2026-10-28

Phase 4 of the `lenstwin` epic (ledger `draft/feature/autolens/lenstwin_epic.md`; report `lenstwin_epic_report.md` §3 "Phase 4", §2.5 provenance). Library phases 0, 2, 3 and the gNFW speed-up are merged (records `complete/2026/10/lenstwin-p0-twins-core.md`, `lenstwin-p2-mass-budget.md`, `lenstwin-p3-stellar-dark.md`, `gnfw-convergence-fast.md`). Ruled 2026-10-28: no `Science/twins` project — this runs in an ordinary `Science/active` project chosen by the human, under its existing Cortex row; structure is built out through use, so add only what this experiment needs.

## The experiment (in the chosen `Science/active` project)

1. **Reference and twin.** `al.twins.ReferenceModel.from_fit_directory(<fit>, lens_id=…)`; `twin = al.twins.Twin.baseline(ref).apply(al.twins.transform.ReplaceTotalMassWithStellarPlusDark(galaxy="lens", light="bulge" (verify the attribute name in the fit), scale_radius_kpc=<R4 value — ask the human>, f_dark=0.5))`. Save the reference and the twin's `compare` figure (`aplt.subplot_twin_comparison`) and record Δχ²_image and Δχ²_data before any fitting.
2. **Simulate.** `twin.simulate(seed=s)` for a small seed list (e.g. 5), `output_to` each; `twin.json` carries the flat truth (`record.truth`: Υ, κ_s, r_s, f_dark, θ_E,parent).
3. **Fit (no misspecification).** Build the inference model from the twin: stellar `Basis` of `lmp` Gaussians with intensities fixed to the solved values and one shared free M/L (verify how to tie one M/L across members — `chaining_util.mass_light_dark_basis_from` builds the equivalent `af.Model` from a `Result`; an instance-level route may be needed — if it is a reusable gap, file a small library prompt rather than writing it into the science script), `NFWSph` with free κ_s and r_s, centre tied to the light, shear free, MGE source free (`mge_model_from`). Nautilus through the project's `hpc/` template. Copy `twin.json` to the run's `files/`.
4. **Recover.** Truth-vs-posterior table per seed from `samples_summary.json` (check PyAutoFit for an existing helper first; the epic allows one small PyAutoFit PR only if none exists).
5. **gNFW configuration.** Same with `gNFWSph` and free `inner_slope` (the gNFW speed-up PyAutoGalaxy#678 makes this practical); report the `inner_slope` posterior width.
6. **Run discipline.** `PYAUTO_TEST_MODE=1` smoke locally first; then one RAL CPU array on `--partition=ral` with an explicit human go per batch; never touch other projects' jobs. Cortex `run`/`done`/`result` lines; results are the human's words.

## Open questions for the human (ask before starting)

- Which `Science/active` project hosts this, and which fit directory is the first reference?
- The fixed physical r_s (kpc) for the first halo (R4 says fixed; the value is not ruled).
- Seed count and Nautilus settings for the RAL array.

Out of scope: multi-galaxy budgets (phase 5, R7), misspecified fits (later), workspace/assistant (phase 6).
