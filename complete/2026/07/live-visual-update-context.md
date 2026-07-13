## live-visual-update-context
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/53 (closed)
- pr: https://github.com/PyAutoLabs/autolens_assistant/pull/54 (merged, squash)
- completed: 2026-07-10
- summary: task 5 of the autolens_assistant batch — al_configure_search ask-once Live visual updates branch (script viewer / notebook in-place / HPC keep-False; fit.png always written; iterations_per_quick_update cadence); al_run_search no-re-ask reminder; wiki/core/api/searches.md Shared knobs documents live_visual_update grounded on installed abstract_search.py (common-base param via **kwargs, default False); config/general.yaml updates:/hpc: synced w/ workspace (quick_update_background + live_visual_update, all false). Stale 'too-large' difficulty label confirmed wrong — contained change.
- followups: batch finale — portable_user_defaults (discovery-half) next

## Original prompt

# Surface live visual updates in assistant search guidance

Type: feature
Target: autolens_assistant
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

The `live_visual_update` capability is already implemented in PyAutoFit and documented broadly
throughout `autolens_workspace`. This task is only about making `autolens_assistant` aware of the
existing option at the point where it configures or launches a search. Do not reimplement the
library feature and do not add it to the root `AGENTS.md` constitution.

What to change in @autolens_assistant:

- Add a concise **Live visual updates** branch to `skills/al_configure_search.md`. When preparing
  an interactive production fit, ask once whether the user wants to watch the fit update live.
- Explain the environment-sensitive recommendation:
  - foreground Python script: `live_visual_update=True` opens and refreshes a matplotlib viewer;
  - Jupyter / Colab: the running cell refreshes one image in place;
  - HPC, headless, background, or unattended execution: keep it `False`.
- State that `fit.png` continues to be written on every quick update regardless of the live flag,
  and explain that `iterations_per_quick_update` controls the refresh cadence.
- Add a short operational reminder to `skills/al_run_search.md`, without asking repeatedly when
  the search configuration already records the choice.
- Update `wiki/core/api/searches.md` through the repository's approved wiki-refresh workflow so
  the shared search options include `iterations_per_quick_update` and `live_visual_update` with
  their current Nautilus scope and defaults.
- Synchronize `config/general.yaml` with the corresponding `autolens_workspace` defaults under
  both `updates:` and `hpc:`. Live display must remain disabled by default and explicitly disabled
  in HPC mode.
- Check the installed PyAutoFit API and current workspace examples rather than copying stale
  parameter names from assistant documentation.

Acceptance checks:

- A user configuring a local foreground or notebook fit is offered the option contextually.
- A user configuring an HPC/headless fit is not encouraged to enable a display surface.
- Generated Nautilus examples use the current quick-update parameter names and show the live flag
  only where useful.
- The assistant makes clear that live display is optional and disk output is unaffected.
- No new mode, standalone skill, or root-instruction section is introduced.

## Original request

> ok whgat about this feature: Live visualization mode, this is already documented and implemented throughout the autolens_workspace (e.g. __Live Visual Update__
>
> By default the quick-update image is only written to disk. Set `live_visual_update=True` to also push it to a
> live display surface:
>
> - **Python script** — a matplotlib window opens automatically and refreshes with each quick update, so you can
>   watch the fit converge without leaving your terminal.
> - **Jupyter / Colab notebook** — the cell that ran `search.fit(...)` shows a single self-updating image that
>   refreshes in place every `iterations_per_quick_update`.
>
> The disk write (`fit.png`) always happens regardless of this flag. Set it to `False` (the default) if you just
> want the on-disk output, or if you are running in a headless environment (e.g. an HPC cluster).
> """
> search = af.Nautilus(
>     path_prefix=Path("imaging"),  # The path where results and output are stored.
>     name="start_here",  # The name of the fit and folder results are output to.
>     unique_tag=dataset_name,  # A unique tag which also defines the folder.
>     n_live=100,  # The number of Nautilus "live" points, increase for more complex models.
>     n_batch=50,  # GPU lens model fits are batched and run simultaneously, see modeling examples for details.
>     iterations_per_quick_update=1000,  # Every N iterations the max likelihood model is visualized and output to hard-disk.
>     live_visual_update=True,  # Set True to open a live matplotlib window (script) or refresh a Jupyter cell (notebook).
> )), I think this is probably just something I want to make sure the assistant has in a good context point to ask or remind the user, but maybe not in AGENT.md given we are trying to keep its length down
>
> go

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
