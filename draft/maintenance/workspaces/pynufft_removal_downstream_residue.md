# pynufft removal: unswept downstream residue (1 hard break + stale docs/CI)

Type: maintenance
Target: workspaces
Repos:
- @autolens_workspace_developer
- @autogalaxy_workspace
- @autogalaxy_assistant
- @autolens_assistant
- @PyAutoCTI
- @PyAutoHands
- @PyAutoHeart
Themes:
- hygiene
- interferometer
Difficulty: low-medium
Autonomy: supervised
Priority: normal
Status: split (phases 1-2 SHIPPED 2026-08-23; phase 3 open)
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-08-23

## Provenance

Found 2026-08-23 during `/start_dev draft/bug/autoarray/pynufft_scipy_pinv2_dev_extra.md`.
That bug prompt turned out to be genuinely superseded — verified, not merely
marked — so no dev work was started on it. The sweep run to confirm the
supersession is what surfaced this.

`complete/2026/08/remove-pynufft-legacy-transformer.md`
(Status: shipped) deleted `TransformerNUFFTPyNUFFT` and dropped `pynufft` from
PyAutoArray's `optional`/`dev` extras. Its "Workspace tier" scoped only
`autolens_workspace` and `autolens_workspace_test`, both of which were done
(@autolens_workspace#497, @autolens_workspace_test#261). **The sibling repos
were never swept.** This prompt covers what that left behind.

## Verified state of the shipped removal (2026-08-23)

Independently re-checked, so this prompt does not re-litigate settled work:

- PyAutoArray `main` in sync with `origin` (0 ahead / 0 behind); **zero**
  tracked `pynufft` references.
- `pyproject.toml`: `dev = ["pytest", "black", "numba", "nufftax>=0.6.1,<0.7.0"]`
  — the `pynufft==2022.2.2` pin is gone, as is the `optional` entry.
- `TransformerNUFFTPyNUFFT` absent from all three namespaces (`al`/`ag`/`aa`);
  `TransformerNUFFT` and `TransformerDFT` both present.

## 1. Hard break (confirmed by repro)

`autolens_workspace_developer/jax_profiling/dataset_setup/interferometer.py`

```
:140        "nufft_pynufft": al.TransformerNUFFTPyNUFFT,
```

```
AttributeError: module 'autolens' has no attribute 'TransformerNUFFTPyNUFFT'
```

The dict at `:137` is built **eagerly** inside `simulate()` (`:106`), before the
key lookup — so *every* instrument raises, not only the `alma_high_res` config
at `:76` that selects `"nufft_pynufft"`. Reproduced by calling `simulate('sma')`,
a **DFT** dataset, which still fails. All JAX-profiling dataset setup in that
repo is currently broken.

Note `:65-69`: the `alma_high_res` comment justifies pynufft on grounds that a
dense DFT matrix would be ~20GB/OOM and that nufftax needed Python >= 3.12 on a
3.10 venv. Whoever fixes this must **decide** what that config becomes
(`TransformerNUFFT` via nufftax, or drop the config) rather than mechanically
swapping the symbol — the OOM constraint was real. The
`apply_sparse_operator`/crossover measurements in the shipped removal prompt
(DFT wins below ~1e7 `n_vis * n_pix`; NUFFT is the only feasible path above
~1e8) are the relevant evidence.

This is the **only** executable reference to the deleted class anywhere in the
workspace/assistant repos — everything below is documentation or CI.

## 2. Stale user-facing docs (describe a class that no longer exists)

- **@autogalaxy_workspace — 26 hits.** The direct sibling of the repo that was
  fixed. `scripts/interferometer/{start_here,simulator}.py`,
  `scripts/interferometer/features/linear_light_profiles/modeling.py`,
  `scripts/guides/using_jax.py`, `start_here.py`, the matching `notebooks/*.ipynb`
  and `markdown/*.md`. Describes `TransformerNUFFTPyNUFFT` as an available
  "non-JAX fallback". Mirror the wording @autolens_workspace#497 landed.
- **@autogalaxy_assistant — 8 hits.** `skills/ag_build_interferometer_model.md`,
  `skills/ag_setup_environment.md`, `wiki/core/api/datasets.md`,
  `wiki/core/concepts/interferometer_theory.md`, and
  `wiki/core/operations/installation.md:103`, whose `optional` table still lists
  `pynufft`. Wiki body edits need `--write-provenance`.
- **@autolens_assistant — 2 live hits.** `chat_pack/05_wiki_api_reference.md:178`,
  `wiki/core/api/analysis_objects.md:72` — both still say the legacy backend "is
  still available".
- **@PyAutoCTI** `docs/installation/source.rst:58` — instructs `pip install
  pynufft` as an optional requirement "for unit tests to pass". Confirm CTI's
  suite has no such need before deleting the line.

## 3. Stale CI (installs a dependency the stack no longer uses)

- `@PyAutoHands/.github/workflows/release.yml:296,355,774` —
  `pip install pynufft==2025.1.1`
- `@PyAutoHeart/.github/workflows/workspace-validation.yml:302` — same

These pin **2025.1.1**, not the broken `2022.2.2`, so they are not hitting the
`scipy.linalg.pinv2` failure — this is wasted install time and resolver
surface, not a red build. Worth noting: these recipes are why the local dev
environment still has `pynufft 2025.1.1` installed at all.

## 4. Deliberately out of scope — do NOT touch

- `paper/` directories (@PyAutoGalaxy, @PyAutoLens, @PyAutoCTI,
  @autolens_assistant) — published JOSS records of what the software used at
  time of publication. The shipped removal prompt made this call explicitly.
- Bibliographies: `PyAutoMemory/bibliography/pyautomemory.bib`,
  `admin_jammy/james.bib`.
- `PyAutoMind/complete/**` task history.
- `autolens_workspace_test/scripts/**` and `autolens_profiling/**` — already
  deliberately rewritten as *historical notes* ("pynufft has since been
  removed"), which are accurate and should stay.

## Relationship to other prompts

- **Supersedes the close-out of** `draft/bug/autoarray/pynufft_scipy_pinv2_dev_extra.md`
  — that prompt's own acceptance is met; it needs moving to `complete/`, not dev.
- **Not covered by** `draft/maintenance/autolens_workspace_developer/stale_api_rot_audit.md`
  (Status: formalised). Its alias-aware scan ran 2026-08-04 and found 56 stale
  symbols; `TransformerNUFFTPyNUFFT` only became stale on 2026-08-22, so it is
  absent from that inventory. Same repo, same *class* of rot, different
  instance. That prompt's root-cause note applies here: **this repo has no smoke
  coverage**, which is why the break went unnoticed. If a minimal smoke tier is
  added under that prompt, `dataset_setup/interferometer.py` is a strong
  candidate for it.
- Unrelated to `complete/2026/08/defer-scipy-sparse-import.md` (the real
  import-time win, shipped 2026-08-22 at 281 ms) and to the `nufftax`
  dependency itself.

## Phase split (decided 2026-08-23)

Split along repo seams into three **independent** phases — disjoint repo sets,
no ordering constraint, and **no library-first merge gate** because no PyAuto\*
library source changes are involved:

1. `active/pynufft_removal_downstream_residue_phase_1_developer_break.md`
   — @autolens_workspace_developer; the confirmed `AttributeError`.
   **SHIPPED 2026-08-23** — @autolens_workspace_developer#129, issue #128 closed.
   Record: complete/2026/08/pynufft-removal-residue-phase-1.md
2. `pynufft_removal_downstream_residue_phase_2_workspace_assistant_docs.md`
   — @autogalaxy_workspace, @autogalaxy_assistant, @autolens_assistant; prose.
   **SHIPPED 2026-08-23** — @autogalaxy_workspace#225, @autogalaxy_assistant#19,
   @autolens_assistant#115; issue @autogalaxy_workspace#224 closed.
   Record: complete/2026/08/pynufft-removal-residue-phase-2.md
3. `pynufft_removal_downstream_residue_phase_3_ci_install_docs.md`
   — @PyAutoHands, @PyAutoHeart, @PyAutoCTI; CI recipes + install doc.

The Brain Feature Agent graded the unsplit prompt `too-large` (score 33) and
proposed a 4-phase `design / core_api / workspace_examples / docs` template with
a `start_library -> ship_library -> start_workspace` chain. That template was
rejected: there is **no library API change** to gate on. Its repo count (11) also
came from prose — it counted the four repos this prompt names only to mark them
**out of scope**; the declared surface is 7. Brain has no `maintenance` work-type
agent, so this routed through the Feature Agent; recorded as a follow-up.

## Acceptance

- `simulate()` in `autolens_workspace_developer/jax_profiling/dataset_setup/interferometer.py`
  runs for every instrument, with a recorded decision on what `alma_high_res`
  becomes and why.
- No executable reference to `TransformerNUFFTPyNUFFT` remains in any repo
  (re-run the alias-aware attribute sweep; do not trust this inventory as proof).
- @autogalaxy_workspace prose matches what @autolens_workspace#497 landed,
  across `scripts/`, `notebooks/` and `markdown/` (regenerate notebooks per that
  workspace's own convention, which differs per workspace).
- Both assistants' wiki/skills no longer advertise the backend; installation
  tables no longer list `pynufft` under `optional`.
- Hands/Heart CI recipes no longer install `pynufft`, and the affected workflows
  are confirmed green afterwards — check every run and every matrix leg.
- `paper/` directories and bibliographies are demonstrably untouched.

## Still open after phases 1-2 (2026-08-23)

- **Phase 3** — the only remaining phase of this prompt.
- **autogalaxy_workspace `markdown/`** — three curated pages (`start_here`,
  `interferometer/start_here`, `interferometer/simulator`) still carry the stale
  pynufft text. `generate_markdown.py` executes curated scripts for real and is
  an at-release step, so phase 2 deliberately did not run it.

## Found while shipping, NOT filed anywhere

1. ~~**Both assistant repos have a red `wiki-currency` on `main`.**~~ **FILED AND
   FIXED** (2026-08-29) — it was filed as `wiki-currency-ci-drift` (PyAutoBrain#317)
   and shipped in autolens_assistant#117 + autogalaxy_assistant#21. Both legs are
   green on `main`. Record: `complete/2026/08/wiki-currency-ci-drift.md`.
   *(Original text: symbol audit `--scope all` reported `missing/broken: 2` on main
   (1 after phase 2), the survivor being `al.mesh.RectangularAdaptImage`;
   @autogalaxy_assistant additionally failed `--check-citations` on
   `wiki/core/operations/sandbox.md`, citing the deleted
   `PyAutoGalaxy:autogalaxy/plot/plot_utils.py`.)*
2. **@autolens_workspace_developer committed datasets do not reproduce** from
   their own scripts — regenerating an untouched config (`sma`) yields different
   data plus a differing `SMALLDAT` header stamp.
3. **@autolens_workspace_developer has no test CI** (one Copilot workflow),
   which is why the phase-1 break rotted unnoticed and why #129 merged unchecked.
