- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/491 (one issue, six PRs)
- shipped: 2026-08-20 — all six merged:
  HowToFit#47, HowToGalaxy#70, HowToLens#73, autofit_workspace#145,
  autogalaxy_workspace#218, autolens_workspace#492.
- classification: maintenance (6 workspace repos) — prose-only, no API surface.
- blocked-by (cleared): hands-raw-string-docstring-prefix / PyAutoHands#251.
- summary: prefixed `r` on every LaTeX-carrying docstring across the six workspace repos —
  **41 files, 180 literals, 131 silent corruptions repaired**. 41 files matches the
  2026-08-20 survey exactly, and autolens_workspace's 17 files / 80 warnings match the
  independent 2026-08-09 measurement line for line. Per repo: HowToFit 4/13/7,
  HowToGalaxy 4/20/13, HowToLens 8/32/21, autofit_workspace 2/2/1,
  autogalaxy_workspace 6/30/28, autolens_workspace 17/83/61 (files/literals/repaired).
- the two damage classes: `SyntaxWarning` fires only for escapes Python does NOT recognise
  (`\s`, `\l`, `\[`). The ones it DOES recognise — `\t` in `\theta`, `\f` in `\frac`,
  `\r` in `\rm`, `\b` in `\beta` — corrupt the value with NO diagnostic at all.
  `\theta_E` in HowToLens chapter_4 was literally TAB + "heta_E". Confirmed repaired.
- key traps:
  - **THE DIFF-EMPTY GATE CANNOT CATCH A WRONG EDIT HERE.** The prompt's gate (regenerate,
    assert notebooks/markdown/llms-full.txt/workspace_index.json unchanged) is necessary but
    structurally blind: the generator reads SOURCE TEXT, not runtime values, so a corrupted
    value regenerates byte-identically. The check that actually catches mistakes is comparing
    every changed literal's RUNTIME VALUE HEAD vs worktree and asserting the `r` prefix only
    ever REMOVES corruption. It caught two real errors mid-task: a `print("\nInfo:")` newline
    about to be destroyed, and 12 already-escaped `$\\chi^2$` about to be doubled into LaTeX
    line breaks. Final tally: 131 repaired, 0 unexpected. **Build this check first.**
  - **`\\` is ALWAYS deliberate, whatever the surrounding context.** In a non-raw literal
    `\\` already means one literal backslash — the author got it right; adding `r` doubles it.
    A math-context rule alone lets these through (they sit inside `$...$`).
  - **The warning sweep is interpreter-dependent.** Invalid escapes are a `SyntaxWarning`
    only on Python 3.12+; on 3.11 they are a `DeprecationWarning`. Verified on 3.11.15: a
    docstring with `$\odot$` yields 0 SyntaxWarning and 1 DeprecationWarning — so a
    SyntaxWarning-only sweep returns a VACUOUS zero that looks exactly like "already fixed".
    Collect both. (`compileall` also needs `-f`, or `__pycache__` hides the counts.)
  - **Run the generator BEFORE editing and confirm a no-op.** Otherwise pre-existing
    generator drift is indistinguishable from damage your edit caused.
  - **Preserve line endings.** Several scripts are CRLF; a `write_text` round-trip normalises
    the whole file and turns a 1-character edit into a 549-line diff. Use `newline=""`.
  - Auto-fix only where EVERY backslash sits in a LaTeX context — `$...$`, `\(...\)`,
    `\[...\]`, `\begin{}...\end{}`, or a markdown code span. Four docstrings with malformed
    or unbalanced delimiters were read in full and prefixed by hand; their delimiters were
    left exactly as found (fixing them is a prose change this task excluded).
  - **Gate refinement**: runtime label strings (e.g. HowToFit's four `plt.ylabel`) live in
    CODE cells, which copy source verbatim, so the `r` legitimately appears in the notebook.
    The gate holds exactly as written for every docstring; that one delta is by design.
- residue (deliberate, worth a follow-up): `autolens_workspace/scripts/group/likelihood_function.py`
  keeps 2 warned + 1 silent. Three of its docstrings use the DOUBLE-backslash convention
  (`$\\theta$`, `\\frac`, `\\vec`) mixed with single-backslash macros; adding `r` would double
  the already-correct ones, and fixing it properly means un-doubling 18 backslashes — a prose
  edit this task excluded. Needs a convention decision.
- also left alone: already-escaped `\\` anywhere (two autogalaxy interferometer files,
  autofit `samples.py:410`), real newlines in `print()`, and
  `autolens_workspace/dataset/cluster/a2744/prep.py:38` where `line.split("\t")` is a genuine
  TSV tab.
- **HowToLens#73 was merged with smoke RED, and the red was proven not to be this PR's.**
  Two chapter_3 pixelization scripts fail numba `Pass nopython_type_inference`; neither is in
  the diff and all 8 files that are in it pass. Decisive control: re-running the last GREEN
  `main` build (run 255, commit `dcb67e9`, zero changes from the branch, fresh dependency
  install) now FAILS identically — `main` itself is red. Suspected cause, NOT proven:
  PyAutoArray#453 (in-place Cholesky buffer + new numba kernels for `fnnls_cholesky`) merged
  22:09:30 UTC, minutes before. Two candidate mechanisms were tested under the exact CI
  versions (numba 0.67.0 + scipy 1.17.1) and BOTH passed — a strided `Ubuf` view into
  `_cholupdate`, and the new `np.dot` in `_cho_solve_buffer`. A new numba release was ruled
  out (0.67.0 shipped nine days before the last green run). **Open question for whoever owns
  that solver.**
- follow-up shipped: PyAutoBrain#245 added a `hygiene escapes` mode so this debt is caught
  continuously — it reports both classes, marks files with ONLY silent damage, and handles
  both interpreter traps. Preferred over the originally-proposed
  `-W error::SyntaxWarning` CI guard, which would catch only the warned class and pass
  vacuously on 3.11.

## Original prompt

# Raw-string the LaTeX docstrings across the six workspace repos

Type: maintenance
Target: workspaces
Repos:
- HowToFit
- HowToGalaxy
- HowToLens
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
Difficulty: medium
Autonomy: safe
Priority: low
Status: formalised

Filed 2026-08-06 from the `/cli_noise_clean` audit plus a compile check during
the hygiene-howto-refs-docstrings batch. Non-raw docstrings containing LaTeX
emit `SyntaxWarning: invalid escape sequence` on every compile/import:

- `HowToFit/scripts/chapter_1_introduction/tutorial_1_models.py:100,309`
  (`\sigma`, `\lambda`)
- `HowToLens/scripts/chapter_4_scaling_up_lensing/tutorial_3_scaling_relation.py:71,585`
  (`\sigma`, `\theta_E`)

Fix: make the enclosing docstrings raw (`r"""..."""`) — preferred over
double-backslashes, which would leak into the rendered notebook prose.

## Survey 2026-08-20 — scope and prerequisite both corrected

A full sweep at `/start_dev` time found the original four lines to be a small
corner of the problem, and found a hard dependency the prompt did not know
about. Both sweeps are ~20 lines each and specified below — rebuild them rather
than trusting these counts blind.

### ~~BLOCKED BY~~ — CLEARED 2026-08-20

The PyAutoHands prerequisite **merged**: issue #250 / PR #251 (merge `c887290`), all 3
CI matrix jobs green. Both parsers accept `r`/`R` prefixes now, verified on `main`. This
task is ready to start. History of the block, kept because it explains the gate below:


Two PyAutoHands docstring parsers **silently** mis-handle an `r"""` opener, so
raw-stringing these scripts today would break the generated artefacts rather
than fix them. Both reproduced, neither raises:

- `add_notebook_quotes.py:67` — the `r"""` block is not recognised as a cell
  boundary, so **the tutorial prose ships as a Python code cell**.
- `env_config.py:110` — block parity inverts and `read_env_declaration` returns
  `None` instead of the declared tokens. **Seven `autolens_workspace` scripts
  here carry `__Env__` sections** (3 under `scripts/guides/`, 4 under
  `.../potential_correction/`), so their smoke env profile would be silently
  rerouted.

~~Do not start this task until that Hands fix has merged.~~ It has.

**Re-verified 2026-08-20 (resumed `/start_dev`): still blocked, still unfixed.**
Against PyAutoHands `main` @ `cdea28c`, on a probe pair differing only by an `r`
on the first narrative docstring:

- `_narrative_docstring_ranges` → plain `[(0, 2), (6, 10)]` vs raw `[(6, 10)]`
  — the raw block is dropped, silently, no exception.
- `read_env_declaration` → plain `['jax']` vs raw `None` — silently, no exception.

`add_notebook_quotes.py:67` still reads `lines[start].startswith('"""')` and
`env_config.py:110` still reads `^(?:"""|''')\s*$`; neither accepts an `r`/`R`
prefix. No `feature/hands-raw-string-docstring-prefix` branch exists on the
remote yet, and its own blocker (`feature/hands-hygiene-leftovers`) is still
open. Re-run this two-probe check at the next `/start_dev` rather than trusting
this note.

### Two sweeps are needed, not one

`SyntaxWarning` only fires for escapes Python does **not** recognise. The
escapes it *does* recognise fire silently and corrupt the string with no
diagnostic at all — `\t` in `\theta`, `\f` in `\frac`, `\r` in `\rm`, `\b` in
`\beta`, `\a` in `\alpha`, `\v` in `\vec`. Today `\theta_E` in the
`tutorial_3_scaling_relation.py` prose is literally `TAB + "heta_E"`.

- warning sweep: `compile(src, path, "exec")` under
  `warnings.simplefilter("always")`, collecting `SyntaxWarning` — **171 hits**.
- silent sweep: walk the AST, and for every non-raw `str` constant whose source
  segment contains a backslash, flag any control character (`ord < 32`, `\n`
  excepted) in the *value* — **132 hits**.

**The warning sweep is interpreter-dependent — check this before trusting a
zero.** Invalid escape sequences are a `SyntaxWarning` only on **Python 3.12+**;
on 3.11 and earlier they are a `DeprecationWarning`. A sweep that collects
`SyntaxWarning` on a 3.11 interpreter reports **0 hits** and is
indistinguishable from "already fixed" — verified 2026-08-20 on 3.11.15, where
`compile()` on a docstring containing `$\odot$` yields 0 `SyntaxWarning` and 1
`DeprecationWarning`. Collect **both** categories, or assert the interpreter is
3.12+ before believing the count. (`-m compileall` needs `-f` too, or
`__pycache__` suppresses recompilation and the counts silently drop.) This
already cost one mis-grade on the 2026-08-09 sweep.

`HowToLens/scripts/chapter_4_scaling_up_lensing/tutorial_5_cluster_scale.py`
has **only** silent hits and zero warnings, so a warning-only sweep skips it
entirely. Drive the edit off the union of both.

Notebooks are **not** currently corrupt: the generator reads source text, not
runtime values, so `notebooks/*.ipynb` already carry the correct `\theta_E`.
This is warning noise plus latent breakage, not a shipped-artefact bug.

### Scope — 41 files, 6 repos

**HowToFit** (4 files)
- `scripts/chapter_1_introduction/tutorial_1_models.py` — 2 warned, 2 silent
- `scripts/chapter_1_introduction/tutorial_2_fitting_data.py` — 5 warned, 5 silent
- `scripts/chapter_1_introduction/tutorial_3_non_linear_search.py` — 1 warned, 0 silent
- `scripts/chapter_1_introduction/tutorial_4_why_modeling_is_hard.py` — 5 warned, 0 silent

**HowToGalaxy** (4 files)
- `scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py` — 5 warned, 3 silent
- `scripts/chapter_1_introduction/tutorial_3_fitting.py` — 7 warned, 6 silent
- `scripts/chapter_2_modeling/tutorial_1_non_linear_search.py` — 1 warned, 1 silent
- `scripts/chapter_3_pixelizations/tutorial_5_bayesian_formalism.py` — 7 warned, 3 silent

**HowToLens** (8 files)
- `scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py` — 6 warned, 3 silent
- `scripts/chapter_1_introduction/tutorial_2_ray_tracing.py` — 2 warned, 2 silent
- `scripts/chapter_1_introduction/tutorial_4_point_sources.py` — 1 warned, 2 silent
- `scripts/chapter_1_introduction/tutorial_7_fitting.py` — 7 warned, 6 silent
- `scripts/chapter_2_lens_modeling/tutorial_1_non_linear_search.py` — 1 warned, 1 silent
- `scripts/chapter_3_pixelizations/tutorial_5_bayesian_formalism.py` — 7 warned, 4 silent
- `scripts/chapter_4_scaling_up_lensing/tutorial_3_scaling_relation.py` — 2 warned, 2 silent
- `scripts/chapter_4_scaling_up_lensing/tutorial_5_cluster_scale.py` — 0 warned, 1 silent

**autofit_workspace** (2 files)
- `scripts/cookbooks/configs.py` — 1 warned, 0 silent
- `scripts/overview/overview_1_the_basics.py` — 1 warned, 1 silent

**autogalaxy_workspace** (6 files)
- `scripts/imaging/features/linear_light_profiles/likelihood_function.py` — 4 warned, 4 silent
- `scripts/imaging/features/multi_gaussian_expansion/likelihood_function.py` — 4 warned, 4 silent
- `scripts/imaging/features/pixelization/likelihood_function.py` — 7 warned, 7 silent
- `scripts/imaging/likelihood_function.py` — 4 warned, 3 silent
- `scripts/interferometer/features/pixelization/likelihood_function.py` — 7 warned, 7 silent
- `scripts/interferometer/likelihood_function.py` — 4 warned, 3 silent

**autolens_workspace** (17 files)
- `scripts/group/features/linear_light_profiles/likelihood_function.py` — 1 warned, 1 silent
- `scripts/group/features/multi_gaussian_expansion/likelihood_function.py` — 1 warned, 1 silent
- `scripts/group/likelihood_function.py` — 4 warned, 3 silent
- `scripts/guides/galaxies.py` — 1 warned, 0 silent  *(carries `__Env__`)*
- `scripts/guides/results/aggregator/data_fitting.py` — 1 warned, 0 silent  *(carries `__Env__`)*
- `scripts/guides/tracer.py` — 1 warned, 0 silent  *(carries `__Env__`)*
- `scripts/imaging/features/advanced/potential_correction/likelihood_function.py` — 12 warned, 7 silent  *(carries `__Env__`)*
- `scripts/imaging/features/advanced/potential_correction/start_here.py` — 5 warned, 3 silent  *(carries `__Env__`)*
- `scripts/imaging/features/linear_light_profiles/likelihood_function.py` — 5 warned, 4 silent
- `scripts/imaging/features/multi_gaussian_expansion/likelihood_function.py` — 5 warned, 4 silent
- `scripts/imaging/features/pixelization/likelihood_function.py` — 8 warned, 9 silent
- `scripts/imaging/likelihood_function.py` — 7 warned, 7 silent
- `scripts/interferometer/features/advanced/potential_correction/likelihood_function.py` — 10 warned, 5 silent  *(carries `__Env__`)*
- `scripts/interferometer/features/advanced/potential_correction/start_here.py` — 3 warned, 1 silent  *(carries `__Env__`)*
- `scripts/interferometer/features/pixelization/likelihood_function.py` — 8 warned, 9 silent
- `scripts/interferometer/likelihood_function.py` — 7 warned, 7 silent
- `scripts/point_source/fit.py` — 1 warned, 1 silent

The four matplotlib labels in
`HowToFit/.../tutorial_4_why_modeling_is_hard.py` (`'Normalized Residuals
($\sigma$)'`, lines 437/604/712/820) are runtime strings, not docstrings — same
`r` prefix, same reason.

### Deliberately EXCLUDED

- `autolens_workspace/dataset/cluster/a2744/prep.py:38` — `line.split("\t")` is
  a genuine tab in a TSV parser, not LaTeX. Leave it.
- `PyAutoGalaxy` (4 warnings: `operate/lens_calc.py`, `util/mock/mock_cosmology.py`)
  and `PyAutoCTI` (19 warnings: `extract/two_d/*`, `instruments/acs/array_2d.py`).
  Same defect, but library source — needs `ship_library` and a pending-release
  gate, so it does not belong on a prose-only workspace PR. File separately.
- `autocti_workspace`, every `*_workspace_test` / `*_workspace_developer`, and
  `PyAutoFit` / `PyAutoArray` / `PyAutoLens` source: swept, **zero** hits.

## Constraints

- Docstring content is user-facing tutorial prose. Add the `r` prefix and change
  **nothing else** — do not reword the LaTeX or the surrounding sentences.
  Prose changes belong to a docs task, not this one.
- Notebooks are regenerated, never hand-edited.

## Verification per repo (the diff-empty gate)

1. Both sweeps return zero — on a **3.12+** interpreter, or collecting
   `DeprecationWarning` as well (see the interpreter trap above). A zero from a
   3.11 `SyntaxWarning`-only sweep is vacuous and does not clear this gate.
2. Regenerate:
   `PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py <project>`
   (`howtofit`, `howtogalaxy`, `howtolens`, `autofit`, `autogalaxy`, `autolens`).
3. **`git diff notebooks/ markdown/ llms-full.txt workspace_index.json` must be
   empty.** The generator swaps the delimiter line for `'''` either way, so the
   generated artefacts are byte-identical before and after. A non-empty diff
   means the Hands prerequisite is incomplete — this is the gate, not a
   formality.
4. `read_env_declaration` still returns its tokens for all 7 `__Env__` files.

Ship as six independent PRs, one per repo. Prose-only, no API surface, so no
cross-repo merge ordering.

## Supersedes

`draft/maintenance/autolens_workspace/latex_docstrings_invalid_escape_warnings.md`
(filed 2026-08-09, split from #457) is the same defect measured on
`autolens_workspace` alone — its 80 warnings across 17 files are exactly the 17
files listed above, top-six counts matching. This prompt subsumes it across all
six repos and adds the silent-escape class. Its unique content (the interpreter
trap, now folded in above; the "do not reword the LaTeX or the prose while
fixing the escapes" constraint) is carried here. One task, one prompt — pick up
this file, not that one.

## Follow-up worth filing

A `-W error::SyntaxWarning` compile guard in workspace CI, so this cannot
regress. Note it would catch only the 171-hit class; the silent class needs the
AST sweep above.
