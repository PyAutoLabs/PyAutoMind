# MassField — external shear, mass sheets and external potentials as their own model object

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Themes:
- cluster
Difficulty: too-large
Autonomy: human-required
Priority: normal
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Review-minutes: 20
Unattended: needs-slicing
Epic: mass-field
Filed: 2026-09-17

## Brief

A `Galaxy` in PyAutoGalaxy is a redshift plus a named bag of profiles; the
tracer only ever asks it for its redshift and its summed fields. `ExternalShear`,
`MassSheet` and `ExternalPotential` describe the tidal field of everything
*outside* the modelled system, so they are not properties of any galaxy, yet the
only redshift-bearing container the stack has is `Galaxy`, and so they ride on
one. In `imaging/` that is harmless (one galaxy, nothing misrepresented). With
several deflectors it is a lie the model tells: `model.info` prints `lens_0`'s
shear, users read γ as something about that galaxy, and `multi_galaxy/`
(autolens_workspace#378) had to invent a shear-only `Galaxy` named
`shear_galaxy` to say what the physics means.

The stack already half-admits the mismatch: the line-of-sight sampler builds a
`Galaxy(redshift=z, mass_sheet=MassSheet(...))` per plane
(`@PyAutoLens/autolens/lens/los.py`), the analysis carries a TODO asking
whether a subhalo should be its own class, and the COOLEST exporter
(`@PyAutoLens/autolens/interop/coolest.py`) peels `ExternalShear` / `MassSheet`
off every galaxy into a separate `MassField` entity on export and folds it back
into a `Galaxy` on import, because the standard treats external fields as a
peer of galaxies, both with a redshift. lenstronomy goes further and has no
galaxy concept at all (a flat `lens_model_list` with a per-component
redshift). COOLEST's middle ground is the right one for PyAutoLens.

**Decision (human, 2026-09-17):** `MassField` is **its own thing** — a
standalone class, *not* a `Galaxy` subclass — holding `ExternalShear`,
`MassSheet` **and** `ExternalPotential` (any `MassProfile` is accepted). It has
its own slot in the model, `fields=`, a collection like `extra_galaxies`, and
its own argument on the tracer, `Tracer(galaxies=..., fields=...)`. Only the
tracer's *planes* merge galaxies and fields at each redshift; `tracer.galaxies`
is unchanged, so nothing that indexes galaxies positionally moves. One field
carries every component at one redshift (shear + sheet + potential is one
`MassField`, as bulge + disk is one `Galaxy`); several fields means several
planes (the LOS sampler's per-plane sheets; line-of-sight shear formalisms with
foreground and background tidal planes), which is why the slot is a collection
and not a single `field=`.

**Backwards compatibility is a hard requirement.** The `Galaxy`-attached form
stays fully supported, undeprecated and unwarned: a user's existing script
composing `af.Model(al.Galaxy, ..., shear=af.Model(al.mp.ExternalShear))` must
keep working and must keep producing the same PyAutoFit result
`unique_identifier`. The identifier hashes the model's class paths and
parameter structure, not source files, so `Galaxy` may be refactored
(behaviour-preserving mixin extraction) provided its import path, constructor,
`dict()` output and prior configs are unchanged; the witness is an
**identifier pin** (same representative model, same identifier on `main` and
on the branch), not "file untouched". A shear-only `Galaxy` in a tracer list
keeps working too. A script that adopts `MassField` composes a different model
and gets a new identifier; that is expected.

`ExternalPotential` has a `centre` (its τ/δ terms have radial dependence about
it); composed in a `MassField` its centre prior is tied to the galaxy mass
centre (`field.potential.centre = lens.mass.centre`), which a `model_util`
helper makes the one-line default.

Rejected, recorded so nobody re-derives them: (a) a `Galaxy` subclass in the
`galaxies` collection — cheapest, but it keeps the false is-a relation, leaves
fields visible to every per-galaxy surface (image dicts, plotters, tables) and
keeps the positional-index hazard in every list-based workspace script; (b)
lifting the field to the model root as a bare profile — needs a redshift for
multi-plane tracing; (c) a single `field=` slot — a second spelling would be
needed the day someone models line-of-sight shear on two planes.

## Phases

Issue ONE at a time, in order, as the predecessor nears shipping — no bulk
issue queues. Phases 1 and 2 are library work (library-first gate); 3 and 5 are
workspace sweeps whose *merge* follows the released libraries (phase 3 was
started early, on the human's ruling, to validate the library before release).

| Phase | Prompt | Repo | What it delivers | Gate |
|---|---|---|---|---|
| 1 | **shipped** — `complete/2026/09/mass-field-class.md` (PyAutoGalaxy#621, merged 2026-09-17) | PyAutoGalaxy | standalone `ag.MassField(redshift, **mass_profiles)`; the mass sums shared with `Galaxy` through a mixin extracted behaviour-preservingly; zero-light interface so a plane can hold it; dict round trip; JAX pytree registration; identifier pin test; API docs. | — |
| 2 | **shipped** — `complete/2026/09/mass-field-integration.md` (PyAutoLens#742, merged 2026-09-17) | PyAutoLens | `Tracer(galaxies, fields=None)`, planes merge, `tracer.fields`, `sliced_tracer_from`, `to_dict`, pytree flatten; analysis folds `instance.fields`; LOS sampler emits fields; COOLEST 1:1 both ways (legacy peel kept); `model_util.mass_field_from` with the `ExternalPotential` centre tie; tests, docs. | phase 1 merged 2026-09-17 (PyAutoGalaxy#621) — **unblocked** |
| 3 | **SHIPPED 2026-09-19** — `complete/2026/09/mass-field-workspace-sweep.md` | autolens_workspace, autolens_workspace_test | External fields moved to the separate fields= slot; one legacy regression remains. | PRs #560 and #322 merged; release hold removed by the human. |
| 4 | *absorbed into phase 3* — prompt `propagate_shear_galaxy_idiom_to_group_cluster.md` retired 2026-09-17 | autolens_workspace | `group/` migrates inside phase 3 (its re-scope survey — 30 loop-idiom + 12 `kwargs["shear"]` sites, `cluster/` clean — is recorded in that prompt's history). | — |
| 5 | **PRs open 2026-09-19** — `active/mass_field_sibling_sweep.md` | HowToLens, autolens_assistant | HowToLens's 28 sites migrated in scripts and generated notebooks; chapter-2 prior passing revised; assistant skill/wiki pages migrated. | HowToLens#90 and autolens_assistant#131 green, awaiting human merge. |
| 6 | **SHIPPED 2026-09-19** — `complete/2026/09/mass-field-flat-sweep.md` | autolens_workspace, autolens_workspace_test | Bare fields=field adoption, readers and guards, identifier pins, regenerated notebooks. | PRs #562 and #322 merged after all checks passed; release hold removed by the human. |
| 7 | **PRs open 2026-09-19** — `active/mass_from_grows_a_fields_argument.md` | PyAutoGalaxy, PyAutoLens | Companion `mass_and_fields_from` carries the top-level field beside mass priors; Lens reexports it. | PyAutoGalaxy#625 and PyAutoLens#745 green, awaiting human merge and release. |
| 8 | **PRs open 2026-09-19** — `active/mass_field_prototypes.md`, `active/mass_field_inference_simulators.md` | PyAutoReduce, autolens_inference | Two Reduce prototypes and two inference simulators use flat fields. | PyAutoReduce#77 and autolens_inference#8 green, awaiting human merge. |
| 9 | **Draft PR open 2026-09-19** — `active/mass_field_flat_adoption_developer.md` | autolens_workspace_developer | Live JAX, search, plotting, LOS and standalone MGL builders migrated; measurement archives preserved. | autolens_workspace_developer#143 awaits phase 7 library release; point-source pin drift and legacy examples are recorded on issue #142. |
| 10 | `draft/maintenance/autolens_inference/mass_field_flat_adoption.md` | autolens_inference | Five-stage SLaM runner field propagation. | Phase 7 release, then phase 8 simulator task claim released. |
| 11 | `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md` to be sliced | autolens_profiling | Live profiling builders; preserve inline witness snapshots. | `hst-gpu-residue-p2` worktree claim currently blocks a separate edit without a recorded human waiver. |

The user confirmed on 2026-09-19 that the local `autolens_jax_joss` checkout was deleted more recently. It is excluded from this local migration sweep. The older four-repo draft remains historical context; its JOSS and already handled Reduce/inference sections are superseded by these rows.

## Decisions

- **BC is a hard invariant** (Brief). No change to `Galaxy`'s import path,
  constructor signature, `dict()`/`to_dict` output or any `config/priors/*.yaml`;
  no deprecation warning on galaxy-attached sheets. Witness for every library
  phase: the identifier pin (a representative galaxy-attached model's
  `unique_identifier` computed on `main` and on the branch, equal).
- **`MassField` is standalone.** It shares the mass-sum implementation with
  `Galaxy` through a mixin (`has`, `cls_list_from`, deflections / convergence /
  potential sums) so nothing is duplicated, and implements the minimal
  zero-light interface a plane needs (`image_2d_list_from` → empty,
  `has(LightProfile)` → False). `isinstance(field, Galaxy)` is False, so
  per-galaxy surfaces never see it.
- **Model slot `fields=`, a collection; tracer argument `fields=`, a list.**
  The analysis folds `list(instance.fields)` into `Tracer(fields=...)` exactly
  as it folds `extra_galaxies` / `scaling_galaxies` into `galaxies`. Planes
  merge galaxies and fields at each redshift; `tracer.galaxies` never contains
  a field. The multi-galaxy `n_main` counting (`lens_` prefix over
  `instance.galaxies`) is untouched.
- **`ExternalPotential` is a field, centre tied to the galaxy mass** via
  `model_util.mass_field_from(lens, potential=True)`; for a multi-deflector
  system the caller names the primary galaxy explicitly.
- **Reversed 2026-09-17 (human ruling) — the user-facing API is `fields=`
  everywhere.** *"other than maybe an autolens_workspace_test integration test
  we shouldn't be using a shear_galaxy or putting shears or any other field in
  galaxies from now on. The user-facing API from here on is fields in the model
  as a separate thing."* The earlier decision kept `imaging/` galaxy-attached to
  spare readers an identifier change; the ruling accepts that change (a migrated
  example is a new model; old `output/` folders are not resumed) in exchange
  for one idiom across every workspace. Library BC is unchanged: `Galaxy`-attached
  fields keep working unwarned for users' own scripts, and exactly one
  workspace script (`autolens_workspace_test/scripts/misc/mass/galaxy_attached_legacy.py`)
  keeps the legacy form as the regression.
- **Naming.** `MassField` follows COOLEST so the interop is 1:1; `fields` is the
  model slot and tracer argument; `field` the conventional single entry.

## Ledger

- 2026-09-17: epic filed from the `/start_dev` plan checkpoint of the group
  shear prompt (Fable session); first draft had `MassField` as a `Galaxy`
  subclass in the `galaxies` collection.
- 2026-09-17 (same day, human ruling): redesigned to a standalone class with
  its own `fields=` model slot and tracer argument — the human's "MassField is
  its own thing"; `fields` is a collection because shear + sheet at one
  redshift is one field, while several fields means several planes. Phase 2
  re-sized medium → large; phase 4 loses its positional-index trap.
- 2026-09-17: phase 1 issued — PyAutoGalaxy#620 (`/start_dev`, web session; prompt now `active/mass_field_class.md`, task `mass-field-class` in `active.md`).
- 2026-09-17: phase 1 merged — PyAutoGalaxy#621 (`/prm`, web session); record `complete/2026/09/mass-field-class.md`; identifier pin held; phase 2 unblocked, `pending-release` on PyAutoGalaxy.
- 2026-09-17: phase 2 issued — PyAutoLens#741 (`/start_dev`, web session; prompt now `active/mass_field_integration.md`, task `mass-field-integration` in `active.md`). Plan notes a gap the prompt assumed away: `Tracer.galaxy_image_2d_dict_from` walks planes, not `tracer.galaxies`, so per-galaxy surfaces need an explicit `MassField` filter.
- 2026-09-17: phase 2 merged — PyAutoLens#742 (merge 7197380; `/prm` from the epic's
  dashboard resume prompt, web session); issue #741 closed; record
  `complete/2026/09/mass-field-integration.md`; identifier pin held, legacy COOLEST
  export byte-identical; `pending-release` on PyAutoLens. Library work (phases 1–2) is
  complete. Phases 3–5 are gated on a **release** of PyAutoGalaxy (#621) and PyAutoLens
  (#742) to the installed stack — phase 3 is not issued until `/release` has published
  both; nothing here is bulk-issued.
- 2026-09-17: phase 2 merged — PyAutoLens#742 (`/prm`, web session); record `complete/2026/09/mass-field-integration.md`.
- 2026-09-17 (evening, Fable session): the human asked to validate the library with real workspace runs *before* the release, then ruled the user-facing API is `fields=` everywhere (quoted in Decisions). Phase 3 re-scoped to both workspaces and every folder (imaging decision reversed), phase 4 absorbed and its prompt retired, `autolens_workspace_test` moved from phase 5 into phase 3; phase 3 started with draft PRs held for the release.
- 2026-09-18: the `fields=` slot learned to accept a **bare `MassField`** — PyAutoLens#743/#744, merged `478213e78` (record `complete/2026/09/mass-field-bare-fields.md`). Additive and capability-only by design: the library keeps collections as its primary example and no workspace source moved in that task, which named `tmp/handoffs/autolens-flat-fields-sweep.md` as the follow-up adoption sweep.
- 2026-09-18: **phase 6 issued** — the flat-form adoption sweep, autolens_workspace#561 (`complete/2026/09/mass-field-flat-sweep.md`, task `mass-field-flat-sweep`). It reuses phase 3's worktree `~/Code/PyAutoLabs-wt/mass-field-workspace-sweep` (the conflict guard exits 1 on both repos for `mass-field-workspace-sweep`; waived as deliberate continuity on the human's plan approval), folding the autolens_workspace_test half onto phase 3's open draft PR #322 so `composition_mge.py`'s pin moves once rather than twice, while autolens_workspace branches `feature/mass-field-flat-sweep` off `main` where #560 already merged at `c79c8d3`. `euclid_strong_lens_modeling_pipeline#90` (merged `9cdee7b`) is the reference implementation. Phase 5 should be amended before it is issued — `mass_field_sibling_sweep.md` is written in the collection era, so HowToLens would migrate twice unless it teaches the flat form directly.
- 2026-09-18: **phase 6's sweep completed** — autolens_workspace#562 and autolens_workspace_test#322, both DRAFT pending the PyAutoGalaxy/PyAutoLens PyPI release. Its follow-up audit filed five drafts: `draft/feature/autogalaxy/mass_from_grows_a_fields_argument.md` (the chaining helper takes no `fields`, so a chained stage silently drops the field — found live on `main` in `multi_dataset/features/one_by_one/modeling.py`, fixed in #562); `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md` (autolens_profiling / autolens_inference / autolens_jax_joss / PyAutoReduce — blocked on the helper); `draft/maintenance/autolens_workspace_developer/mass_field_flat_adoption_developer.md` (72 sites, no CI, archived measurements — opens with a **human scope ruling**, since the 2026-09-17 ruling named only the two workspaces); `draft/maintenance/pyautomind/autolens_jax_joss_manifest_gap.md`; and `draft/test/autolens_workspace_test/latent_smoke_assertion_echoes_search_log.md`. **Phase 5 was amended the same day** so HowToLens migrates once, straight to the flat form, rather than twice.
- 2026-09-18 (web session): **the release the epic waits on was traced to a single blocker.** Phases 1–2 have been `pending-release` since 2026-09-17 and the nightly driver has not shipped since `2026.9.15.1`, so phases 3/5/6 and the three held workspace PRs (autolens_workspace#560 merged, #562 and autolens_workspace_test#322 draft) have all been stalled on it. The nightly is not failing — it is gating, correctly, three nights running: 09-16 and 09-17 stopped at Stage 3 on `verify_install FAILED`, and 09-18 (PyAutoBrain run 35318011061) stopped at Stage 3 on **`1 timeout: autolens multi_galaxy/start_here.py`** (PyAutoHeart run 35319361459), the only failure in that leg. Root cause is unrelated to this epic: autolens_workspace#554 (2026-09-17, issue #549) swapped `scripts/multi_galaxy/start_here.py` off the simulated `simple` dataset onto the real SDSS J1011+0143 ACS/WFC F814W frame without adding the matching entry to `config/build/profile_release.yaml`, leaving it the only real-FITS `start_here` running on the profile defaults. autolens_workspace#563 adds that entry, mirroring `imaging/start_here` (`PYAUTO_SMALL_DATASETS: "0"` + `BUILD_SCRIPT_TIMEOUT: "3600"`, the #547 precedent). Measuring the script's actual release cost and retiring the 3600s override is deferred to `draft/bug/autolens_workspace/multi_galaxy_start_here_release_cost.md`. The mass-field libraries themselves are not implicated in any gate failure.
- 2026-09-18 (web session, later): the release was attempted and **blocked again** — PyAutoBrain nightly run 35371266474, Stage 3 (PyAutoHeart run 35372831809), the same script and the only failure of 53 jobs. autolens_workspace#563's override was the wrong fix: it paired a 3600s per-script timeout with a lifted `PYAUTO_SMALL_DATASETS`, and the script then died at ~1478s on a runner shutdown signal (exit 143) *before either cap could fire*, rather than timing out at 1800s as it had on the profile defaults. #563 was reverted and `scripts/multi_galaxy/start_here.py` SLOW-parked (autolens_workspace#564), the way `cluster/start_here` and `weak/.../a2744` have been since 2026-07-22 — the deterministic unblock, at the stated cost that a script which became a real-data showcase on 2026-09-17 leaves release validation until it is profiled. The evidence and the "do not just raise the timeout again" warning are recorded in `draft/bug/autolens_workspace/multi_galaxy_start_here_release_cost.md`. **Phases 1–2 remain pending-release and the epic remains gated on the next release run**; nothing in the mass-field libraries has been implicated in any gate failure across all three attempts.

- 2026-09-19: phases 3 and 6 fully merged after all CI checks passed; the human lifted their release holds to unblock workspace regrouping. Their shared worktree is retained for ignored data, with claims released.
