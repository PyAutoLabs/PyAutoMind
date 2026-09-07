# Cortex: tasks not phases — one-line summaries, state colours, fewer sections

Type: feature
Target: pyautocortex
Repos:
- PyAutoCortex
- PyAutoBrain
Themes:
- dashboard
- science-workflow
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: no
Filed: 2026-09-07

Make the PyAutoCortex board read like a science project: a project holds
unordered **tasks** (ideas the human runs in whatever order results dictate),
each with a ten-word summary and a coloured state, all visible at once.

## Original request (verbatim)

> More feedback on PyAutoCortex making it suited to doing science. Firstly, I
> think we should do away with the term "phases", which implies that tasks are
> sequential, noting that phaes have numerical numbers. I don't think most
> science analysis goes like that. Rather, it is generally the case that there
> are tasks, representing ideas I have for the project, and I run them, but the
> order may change and adapt based on how results come in or other priorities.
> Secondly, Rathert hen "4 more open phase(s) · plans and issues" being a drop
> down menu, I think that all active tasks for each project should be listed
> and shown on the dashboard by default, however I think it is important that
> the task takes up one line each and is more readable. Thus, for each task, I
> think rather than it being listed like "Inference_programme — phase 11:
> cluster extended-source inference — gradient-based fitting building on JAX
> knowledge — planned" it should have a summary that is up to 10 words so I can
> read is quickly. For conciseness, we dont need the "Inference_programme -
> phase 11:" bit -- its under the inference_programme heasder. So for this one
> I would do somehtig like "Cluster extended source inference testing gradient
> based fitting". So, every task has a summary of up to 10 words, which makes
> the dasboard a lot more readable. Thirdly, more color to indicate state is
> good, for example "planned" could be in green if irts planned and ungdated.
> "active" could be yellow if its going on, green when complete. Use red when a
> run is broken and needs attention. For these, can we make the path font in
> white, so it stands out against pink: Local
> /home/jammy/Code/PyAutoLabs/autolens_profiling  Mirror
> /mnt/c/Users/Jammy/Science/inference_programme  RAL
> /mnt/ral/jnightin/autolens_profiling . Fourthly, think about this and tell me
> if you think I'm wrong, but I think we can remove the "Ready" and "Gated"
> sections, this imformation should come from the projects bit above which we
> are now seeking to improve and make more visible. These sections just mean
> project updates are spread over more places.

Decisions taken with the human on 2026-09-07 (all four points agreed; "yes
full rename lets do it properly", "yes remove as recommended"):

## 1. Full rename: phase → task, and the number goes

In @PyAutoCortex the identity of a task is its slug (the file name), which is
already unique per project — the number carries nothing.

- `phases/<project>/<slug>.md` → `tasks/<project>/<slug>.md` (git mv, every
  file). `scripts/cortex.py` `PHASE_FILE_RE`, `load_phases`, `phase_problems`,
  `new`, `move`, `rule`, `gates`, `retire` and their messages follow.
- Delete the `Phase: N` header outright (no deprecated shadow field). Title
  line becomes `# <Project> — <title>`; ruling titles `# R-… — <verb> <project>
  <slug>`; "revival is a new phase number" becomes "revival is a new slug".
- Rulings: `Phase:` head field → `Task:` pointing at the `tasks/…` path, in all
  29 rulings and in `ruling_problems`. `Supersedes:` logic unchanged.
- `cortex.py new <project> <slug>` loses `--phase`; the template writes
  `Summary:` (see 2) instead.
- Docs follow: `AGENTS.md`, `REFERENCE.md`, `README.md`,
  `docs/schema_decisions.md`, `checkin.yaml` if it names phases; `tests/`.
- Mind side stays: Mind epics really are sequential; `Epic:` on a task file is
  unchanged. Mind intake's "gates a Cortex phase" pill wording → "gates a Cortex
  task".
- In @PyAutoBrain: `agents/conductors/cortex/_cortex.py` (218 mentions), its
  `AGENTS.md`, `skills/cortex/`, `tests/test_cortex_conductor.py`, and the
  intake conductor's Cortex-gate pill. Census keys (`c["phases"]`) rename to
  `tasks`.

## 2. `Summary:` header, one line per task, no fold

- New **required** header `Summary:` — at most ten words, the question the task
  answers, not its method. `cortex.py check` enforces presence and the word
  cap. Write one for every existing task file (~40); this is prose, Opus tier.
- Under `## Projects` every open task of a project is its own tap-to-copy row:
  `Summary` as the link, a state pill, then only the state's facts (run ids,
  wall vs budget, gate refs, ⚠️ failed runs). No project name, no number, no
  "N more open phase(s)" fold. Chips per state as today.

## 3. State colours and the path block

Pill tone map (shared `board/_theme.py` tones, no new CSS):

| state | tone |
|---|---|
| planned, ready | green `g` |
| gated | neutral grey `n` |
| submitted, running, pulled, awaiting-ruling | yellow `y` |
| accepted | green `g` |
| any failed / timeout / void run | red `r`, overrides the state |

Paths (`Local` / `Mirror` / `RAL`): render as a solid accent chip with
`--accent-ink` (white) text instead of the pink-on-tint inline code, so they
read on both themes. Markdown twin unchanged.

## 4. Sections removed

Drop **Ready**, **Gated** and **Running / submitted** sections, their stats
tiles and the Summary table's `Ready` column; the Projects block now carries
that information per task with colour. **Awaiting ruling** stays as the one
cross-project list (a ruling is the human's act). **Recent rulings** stays.

## Acceptance

- `python3 scripts/cortex.py check` clean; PyAutoCortex + PyAutoBrain tests
  green; `pyauto-brain cortex dashboard --check` stable across two renders.
- `grep -ri phase` in PyAutoCortex returns only Mind-epic references and
  history (ruling bodies may keep prose written at the time).
- The rendered board shows every open task per project, one line, coloured.
