# PyAutoMind reference

The registry schemas, prompt conventions, and workflow detail for this repo.
Moved verbatim from `README.md` on 2026-07-10 — agent docs that point at
README sections ("Prompt taxonomy", "Prompt file format", the `active.md` /
completion-record schemas) resolve here, one link from the README.

---

## What a prompt looks like

Here's a real prompt — the contents of `autoarray/psf_oversampling.md` — that
became a tracked task. This is the level and style of detail to aim for in
your own GitHub issue: free-form prose, with `@RepoName/path/to/file.py`
references so the tooling knows which repo and files to target. No boilerplate.

````markdown
A point spread function is used to blur images via 2d convolution.

This blurring occurs predominantly in the package @PyAutoArray/autoarray/operators/convolver.py.

The source code currently requires PSF blurring to occur at the same resolution (pixel scale) as the
image, meaning the PSF is always the same resolution as the image.

However, for modeling, convolution can be performed at a higher resolution than the image, which allows for more accurate
blurring and modeling of the image. This requires us to have an oversampled PSF, which is a PSF that has a higher
resolution than the image.

For modeling, where images are generated PSF blurring happens in @PyAutoGalaxy/autogalaxy/operate/image.py.

Modeling can always evaluate images using a hgiher resolition grid, blurring them with the PSF at high
resolution and then downsample to the observed image resolution. Oversampling is implemented in
@PyAutoArray/autoarray/operators/over_sampling.

Note that over sampling often uses an adaptive sub-szie, which means that 2D covnolution with a PSF is not
well defined. for now, we will assume adaptive over sampling is not used.

I want us to be able to append the Convolver class with a convolve_over_sample_size integer, which specifies the over sample size of the PSF.
This will allow us to perform convolution at a higher resolution than the image, which will improve the accuracy of the blurring and modeling of the image.
For example, if convolve_over_sample_size is 2, then the PSF will be oversampled by a factor of 2, meaning it will have a resolution that is 2 times higher than the image.

This, in turn, means out imaging object @PyAutoArray/autoarray/dataset/imaging/dataset.py will need to be
extended to include the convolve_over_sample_size_lp and convolve_over_sample_size_pixelization attributes, which will
specify the over sample size of the PSF for the lensing and pixelization operations, respectively.

class Imaging(AbstractDataset):
    def __init__(
        self,
        data: Array2D,
        noise_map: Optional[Array2D] = None,
        psf: Optional[Convolver] = None,
        psf_setup_state: bool = False,
        noise_covariance_matrix: Optional[np.ndarray] = None,
        over_sample_size_lp: Union[int, Array2D] = 4,
        over_sample_size_pixelization: Union[int, Array2D] = 4,
        use_normalized_psf: Optional[bool] = True,
        check_noise_map: bool = True,
        sparse_operator: Optional[ImagingSparseOperator] = None,
    ):


Also,read through the @PyAutoArray/autoarray/inversion/inversion/imaging package, and parents, to see
how PSF convolution enters this. I think we can get it to work in PyAutoArray/autoarray/inversion/inversion/imaging/mapping.py,
and will leave work in PyAutoArray/autoarray/inversion/inversion/imaging/sparse.py to future work.

This is a complex task, therefore I think we should extend @autolens_workspace_test/scripts/imaging/convolution.py
with a numerical test.

We should then build on this test in a separate test file using a simple over sampled PSF, to get a numerical
result we can test the source code against.

@autolens_workspace/scripts/imaging/simulator.py is a good example we can build on to show how to use
over sampled PSFs in a real simulation. We can extend this script to show how to use over sampled PSFs in a real simulation.

Come up with a plan to implement over sampled PSFs.
````

That prompt becomes a GitHub issue, gets routed to the affected repos
(`PyAutoArray`, `PyAutoGalaxy`, the autolens workspaces), and lands as PRs
against each. Typos, half-finished thoughts, and "I think we should…" are
fine — write naturally, the AI fills in the rest.

---

## How a prompt flows through the workflow

```
  idea               ── you write it in ideas.md
    │
    ▼
  draft prompt       ── you write a markdown file under
    │                   draft/<work-type>/<target>/<name>.md
    ▼
  /start_dev         ── reads the prompt, audits the code, drafts an issue,
    │                   creates the GitHub issue, registers the task in
    │                   active.md, moves the prompt draft/ → active/
    ▼
  active.md entry    ── the task is now tracked across machines and sessions
    │
    ▼
  /start_library     ── creates a worktree, branch, opens dev environment
    or                  (or workspace variant — chosen automatically)
  /start_workspace
    │
    ▼
  development        ── code, tests, run smoke tests, commit
    │
    ▼
  /ship_library      ── runs tests, opens PR, waits for merge
    or
  /ship_workspace
    │
    ▼
  PR merged          ── post-merge cleanup deletes the worktree, drops the
    │                   active.md entry, and writes the dated completion record
    │                   complete/<YYYY>/<MM>/<slug>.md (lifecycle.py record)
    ▼
  done
```

The slash commands above are skills hosted across the organism (Brain, Heart) but
all read/write Mind's registry via workspace-root-anchored paths. One operates
over the registry without starting work:

- `/health status` — dashboard of `active.md`, `planned.md`, `complete/`
  (a PyAutoHeart status view, reached through the single `/health` door).
  Continuity across execution environments needs no special step — any
  environment reads `active.md` and resumes an in-flight task.

---

## Repository layout

```
PyAutoMind/
├── README.md                ← short front page
├── dashboard.md             ← GENERATED task page (picks / in flight / parked / planned / backlog)
│                              `pyauto-brain intake --apply dashboard`; CI self-heals the RENDER on
│                              main — never a shipped prompt nobody retired (that is /prm's close-out
│                              per task, `intake reconcile` across the backlog)
├── REFERENCE.md             ← this file (schemas + conventions)
├── .gitignore
│
├── active.md                ← tasks currently in progress (one ## section per task)
├── ideas.md                 ← raw incubating ideas, no structure required
├── parked.md                ← started/scoped but not in flight (stashes, orphan worktrees, deferred)
├── planned.md               ← issued tasks blocked from starting (created on demand)

│
│   PROMPT-FILE LIFECYCLE (issue #71): draft/ → active/ → complete/YYYY/MM/.
│   Drafts are organised by WORK TYPE (first folder), then TARGET (second).
│   See "Prompt taxonomy" below and ROUTING.md.
├── draft/                   ← NOT STARTED (intaken, pre /start_dev)
│   ├── feature/             ← new user-facing or scientific capabilities
│   │   ├── autoarray/  autofit/  autogalaxy/  autolens/  workspaces/  pyautobrain/  …
│   ├── bug/                 ← incorrect behaviour, crashes, regressions
│   ├── refactor/            ← internal restructuring, no intended behaviour change
│   ├── docs/                ← documentation, tutorials, notebooks, examples
│   ├── test/  release/  maintenance/  research/  experiment/
│   └── triage/              ← classification still unclear; needs manual review
│
├── active/                  ← ISSUED, in flight (moved here by /start_dev)
│
├── complete/                ← SHIPPED — rich completion records (see complete/AGENTS.md)
│   ├── AGENTS.md            ← archive schema + how to look records up
│   └── 2026/07/<slug>.md    ← bucketed by completion date (zero-padded months)
│
│   (complete/archive/ holds retired non-record material — see below)
├── complete/archive/        ← skipped by lifecycle.py check/index
│   ├── epics/               ← retired multi-task epic trackers (former z_features/)
│   └── shelved/             ← deferred prompts + dev notes (former z_vault/)
│
├── scripts/
│   ├── status.sh            ← prompt inventory helper
│   ├── lifecycle.py         ← prompt-file lifecycle engine (move/split/check)
│   └── prompt_sync.sh       ← commit/push helpers sourced by skills
│
└── skills/                  ← Mind-owned skills + the ownership audit
    ├── OWNERSHIP.md          ← where every workflow skill lives, and why
    └── create_issue/         ← convert a prompt into a tracked GitHub issue
```

`PyAutoMind/skills/` now holds **only** the Mind-owned `create_issue` skill (plus
`OWNERSHIP.md`). The development-workflow skills were re-homed to the organs that
own them — **PyAutoBrain** (`start_dev`, `start_dev_for_user`, `plan_branches`,
`start_library`, `start_workspace`, `ship_library`, `ship_workspace`,
`health` [the single health door, with `check` sweep,
`status` dashboard, and `full` release-run legs]), **PyAutoHeart**
(`worktree_status`, and the health-leg procedures `health_sweep/`,
`pyauto-status/`, and `pyauto-status-full/` that `/health` drives), and
**autolens_profiling** (`profile_likelihood`). The
`handoff` skill was retired (PyAutoBrain runs uniformly across execution
environments — see `OWNERSHIP.md`). General PyAuto tooling (release prep,
dependency audits, smoke tests, lint sweeps) lives in `admin_jammy/skills/`.

`scripts/prompt_sync.sh` is sourced by skills that mutate registry files
(`active.md`, `planned.md`, etc.) to commit and push back to origin. It
replaces a now-removed `admin_sync.sh` helper that formerly operated on
`admin_jammy/prompt/`.

---

## Prompt taxonomy

PyAutoMind organises **intent by the kind of thinking required; PyAutoBrain uses
that structure to choose the right reasoning agent.**

Prompts start at `draft/<work-type>/<target>/<name>.md` (and advance
`draft/ → active/ → complete/YYYY/MM/`; issue #71):

- The **first folder** answers *what kind of thinking or agent is needed?* — the
  work type.
- The **second folder** answers *what domain or repository is affected?* — the
  target repo (`autoarray`, `autofit`, `autogalaxy`, `autolens`,
  `autolens_assistant`, `pyautobrain`, …), a workspace bucket (`workspaces`), or
  a topic series (`jax_substructure`, `weak`, `cluster`, `priors`).

### Work types → PyAutoBrain agents

| Folder | Holds | Future PyAutoBrain agent |
|--------|-------|--------------------------|
| `feature/` | new user-facing or scientific capabilities | feature planner |
| `bug/` | incorrect behaviour, crashes, regressions | debugger |
| `refactor/` | internal restructuring, no intended behaviour change | refactor architect |
| `docs/` | documentation, tutorials, notebooks, examples | documentation agent |
| `test/` | test coverage, smoke tests, validation scripts | test engineer |
| `release/` | packaging, versions, deployment, release readiness | release engineer |
| `maintenance/` | dependency updates, hygiene, cleanup, small tech debt | hygiene agent |
| `research/` | exploratory scientific / algorithmic investigation | research analyst |
| `experiment/` | prototypes, spikes, proof-of-concept work | prototype agent |
| `human_review/` | work that already shipped and a human wants to sign off | (none — a person reviews) |

`human_review/` is the one work-type nothing infers. Every other folder answers
*what is this prompt about?*; this one records a human's judgement that a
**completed** task needs their eyes before it counts as done. File one by
declaring `Type: human review` (`human-review`/`human_review` read the same) —
`/intake` will never choose it for you, and no task acquires it by default.
Review is opt-in, not a lifecycle stage, so an empty section means nothing was
flagged, not that nothing shipped. It renders as its own **Human review** section
on `dashboard.md`, directly under *In flight*, and is not counted as backlog: a
review is not work to pick up, it is work waiting on you. Its 📋 hands out a
read-and-report prompt rather than a `/start_dev`. Sign one off by retiring the
prompt the usual way (`lifecycle.py record …`); don't sign it off and the
follow-up is an ordinary `/intake`.

`triage/` holds prompts whose classification is still unclear — file there with a
short note and re-home once the work type is obvious. The full mapping (and the
note that the agents themselves live in PyAutoBrain, not here) is in
[`ROUTING.md`](ROUTING.md).

### Good prompt paths

```
feature/autolens/potential_corrections.md
bug/autoarray/mask_edge_case.md
refactor/autofit/result_object_cleanup.md
docs/workspaces/pixelization_tutorial.md
research/autofit/sbi_design.md
experiment/autoarray/jax_sparse_mapping.md
human_review/autolens/scaling_relation_fit_quality.md
```

### Not work-types

`active/` and `complete/` are **workflow lifecycle** folders, not routed by work
type. `complete/archive/` holds retired non-record material — `epics/` (former
`z_features/` trackers) and `shelved/` (former `z_vault/` deferred prompts + dev
notes) — and is skipped by `lifecycle.py check`/`index`.

### Migration note

The repository previously used the target repo as the first folder
(`autoarray/foo.md`). Those prompts have moved to `<work-type>/autoarray/foo.md`.
Routing always keyed off the `@RepoName` references in a prompt's body, not its
folder, so the skills accept both old and new paths during the transition — but
new prompts should use the work-type layout.

---

## Conventions

### Naming

- Prompt filenames are lowercase `kebab_or_snake_case.md`.
- Numbered series use a leading number: `0_docs.md`, `1_simulator.md`. Skipping a
  number (e.g. `feature/weak/2_*.md` not present) is fine — it usually means a
  step was consolidated or deferred.
- **First folder = work type** (`feature/`, `bug/`, …); **second folder = target**
  repo or domain (lowercased, no `Py` prefix): `feature/autoarray/`,
  `bug/autofit/`, `refactor/autogalaxy/`. Workspace prompts go under
  `<work-type>/workspaces/` regardless of which workspace. See "Prompt taxonomy".

### Prompt file format

Free-form markdown. Strong conventions:

- Reference repos and files with `@RepoName/path/to/file.py` (e.g.
  `@PyAutoFit/autofit/non_linear/search.py`). `/start_dev` parses these to
  identify the primary target repo.
- One prompt = one task = one PR (ideally). If a prompt outlines several
  loosely-related changes, split before issuing.
- No frontmatter required. Title in the first line is helpful but optional.
- **Optional metadata header.** A prompt may carry a light, human-writable header
  near the top so both people and PyAutoBrain can see its type/target at a glance.
  This is a convention, not a schema — never required, no YAML frontmatter:

  ```markdown
  # Short task title

  Type: feature
  Target: PyAutoLens
  Repos:
  - PyAutoLens
  - autolens_workspace
  Themes:                   # optional; vocabulary in themes.md, primary first
  - mge
  - jax-gradient
  Difficulty: medium        # small | medium | large | too-large
  Autonomy: supervised      # safe | supervised | human-required
  Priority: normal          # low | normal | high
  Status: draft
  Consequence: glance       # notify | glance | judge — how much review it needs
  Witness: ids bit-identical, 62 -> 9.7 ms   # what makes it checkable in minutes
  Review-minutes: 3         # a seed, not a measurement
  Unattended: ready         # ready | needs-slicing | never
  Lane: any                 # any | local-dev — where the work can run
  Filed: 2026-07-09         # optional; the day the prompt was written
  Issued: 2026-08-19        # optional; set when the prompt advances to active/
  Blocked-by: PyAutoFit#1436          # optional; see "Declaring a gate" below
  Epic: cluster-strong-lensing        # optional; an entry in epics.md
  Bundle: euclid-pipeline-tidy        # optional; an entry in bundles.md
  ```

  When present, `Type:` should match the work-type folder. The goal is light
  structure, not bureaucracy — prompts stay free-form prose.

  **Declaring a gate — `Closes-when:` / `Blocked-by:`.** Both optional. A prompt
  that waits on something external can say so in a form `lifecycle.py issues
  --drafts` can grade:

  ```markdown
  Closes-when: autolens_profiling#70    # this prompt is DONE when that closes
  Blocked-by: PyAutoArray#431, PyAutoGalaxy#486   # READY TO START when all close
  ```

  The two readings are **opposite**, which is the whole point. Prose cannot be
  graded, so a cited issue could mean either and `--drafts` had to report every
  one as the same ambiguous question. With a declared key the tool reports the
  action instead: a closed `Closes-when:` says *likely shipped, verify and
  retire*; a closed `Blocked-by:` says *ready to start*. Prompts declaring a gate
  drop out of the ambiguous advisory list.

  Notes:
  - Accepts `Repo#123` shorthand (assumed `PyAutoLabs/`) or a full URL, and PRs
    as well as issues. Several refs may be comma-separated.
  - `Blocked-by:` clears only when **every** ref closes; a partly-satisfied gate
    is reported in its own weaker band rather than as ready.
  - Keys inside fenced code blocks are documentation and are ignored, so a prompt
    may show the syntax without declaring a gate.
  - Advisory, never a gate on the exit code: retiring a prompt writes to
    `complete/` and stays a human act.

  Motivated by the 2026-08-09 `draft/` sweep, where five prompts' stated gates
  had closed without anyone noticing — including one whose exit condition was met
  the same day it was written.

  **A Cortex-spawned dev follow-up gets its issue at filing — `Issue:`.** Normally a
  prompt has no GitHub issue until `/start_dev` opens one and moves it `draft/ →
  active/`. There is one exception, adopted 2026-09-01 (Cortex schema decision 55).
  A **PyAutoCortex** phase declares what it waits on in a `Gates:` line that may
  hold **GitHub refs only** — it cannot cite a Mind prompt path. So when a Cortex
  science phase is gated on Mind dev work that has not started, that dev prompt is
  filed as a draft **with its issue opened at the same moment**, so the Cortex phase
  has a ref to name. The prompt stays in `draft/` — an open issue here means
  "there is a ref", not "the work is in flight" — and carries the URL in its body:

  ```markdown
  Issue: https://github.com/PyAutoLabs/<repo>/issues/<n> (opened <YYYY-MM-DD> as a Cortex gate ref; reuse in start_dev — never open a second)
  ```

  `create_issue` and `/start_dev` **reuse that issue** when the prompt is finally
  picked up — they must never open a second one. Two issues for one prompt is the
  failure this rule exists to prevent: the Cortex phase's gate would then be watching
  the wrong one, and would never clear.

  This applies *only* to Cortex-spawned gate refs. An ordinary draft still gets its
  issue at `/start_dev` time and nowhere earlier — filing issues ahead of the work in
  general is the bulk-issue-queue anti-pattern, which stays forbidden.

  **Declaring group membership — `Epic:` / `Bundle:`.** Both optional, both
  naming a slug in the matching registry file, and the two mean opposite things
  about ORDER. `Epic: <slug>` (`epics.md`, plus an optional `Phase: <n>`) says
  this prompt is one phase of an ordered programme: the dashboard pulls it out
  of every pick list and shows it only under its epic, worked in phase order.
  `Bundle: <slug>` (`bundles.md`) says the opposite — this prompt is
  INDEPENDENT, and a human has pinned it to a set worth running in one
  orchestrated session. A bundle member keeps its normal place on the
  dashboard and gains a Bundles card; it leaves only the *auto*-bundle pool,
  since it is already spoken for. A slug naming no registry entry still
  groups, loudly (⚠️ on the page), so a typo is visible rather than silent.

  **Declaring what the work is ABOUT — `Themes:`.** Optional, and the same
  list shape as `Repos:` — a bare `Themes:` line, then one `- keyword` bullet
  each. `Target:` says where the code lives; `Themes:` says what the work is
  about, which is usually the more useful grouping and is routinely cross-repo:

  ```markdown
  Themes:
  - mge
  - jax-gradient
  ```

  The **first** keyword is the primary theme and is what the dashboard's
  auto-bundler groups on, so a card reads "three things about MGE" rather than
  "three things that live in autoarray"; the remaining keywords are affinity,
  deciding which prompts pack together inside that group. One to three keywords
  is the intended shape, primary first. A prompt with no `Themes:` still
  bundles — the bundler falls back to `Target:` — so nothing waits on a theme.

  The vocabulary is [`themes.md`](themes.md), a plain markdown list a human
  edits directly (PyAutoBrain reads that file rather than holding its own
  copy). A keyword that is not in it still groups, loudly: ⚠️ on the bundle
  card and a count in the dashboard's Hygiene section, so the list never rots
  into free-text tags. The **Intake (Conception) Agent** assigns `Themes:` when
  it formalises a prompt.

  The optional `Difficulty:` / `Autonomy:` / `Priority:` keys let both people and
  PyAutoBrain see, at a glance, how hard a task is, whether an agent can safely
  take it on, and how urgent it is. What each `Autonomy:` level *does* at every
  workflow checkpoint is defined once in `PyAutoBrain/AUTONOMY.md` (the autonomy
  contract); levels bind only under an explicit `--auto` launch, and `--auto`
  runs append their outcome to `autonomy_log.md` (the calibration log). The **Intake (Conception) Agent** writes these
  automatically when it formalises a raw idea (`/intake`), sourcing `Difficulty:`
  from the shared sizing faculty the Feature Agent also uses — so the value shown
  up front is the one the Feature Agent later acts on. Still a convention, not a
  schema: all keys remain optional and there is **no YAML frontmatter**.

### The queue and the batch records

Two ledger surfaces the batch workflow adds. Both auto-merge
(`scripts/ledger_merge.py`): an unattended system that cannot record its own
history unattended will not record it.

- **[`queue.md`](queue.md)** — the human's ordered wishlist, and the only file
  they maintain by hand between slots. **Order is priority**; there is no
  `priority:` field, because moving an entry up *is* the act of prioritising it.
  Entries are a `prompt` (one named file), an `epic-slice` (the named epic's
  *next* phase, whatever that turns out to be), or a `theme-sweep` (anything
  `Unattended: ready` on that primary theme). A batch is never composed here —
  `pyauto-brain batch plan` proposes one against a review-minute budget, and the
  human approves or edits it in the slot.
- **`batches/<YYYY-MM-DD>-<am|pm>.md`** — one record per dispatched batch,
  written at dispatch and appended at collection. Schema and the three fields
  that are easy to get wrong are in [`batches/AGENTS.md`](batches/AGENTS.md).

### `Lane:` — where the work can run

```
Lane: any | local-dev
```

Spelled in the environment vocabulary `PyAutoBrain/skills/WORKFLOW.md` already
defines (`local-dev` / `web-github` / `ci-only` / `analysis-only`) rather than a
parallel cloud/laptop one. `local-dev` means the work needs the local dataset and
output trees, an SSH endpoint, or the human at the machine — science runs, most
of the Euclid programme's execution half. Default `any`.

**A session detects its own lane and refuses to plan the other**, reporting the
count rather than silently dropping it: *"4 local-dev tasks are ready — run this
from the laptop."* Detection is probed from the environment, never declared: a
session that could be *told* where it is could plan `local-dev` work it cannot
run. One queue holds both lanes; the planner filters.

Not to be confused with `active.md`'s `location:`, which is live per-task
handoff state. `Lane:` is a static fact about the work.

### The review-cost model

`Difficulty:` measures blast radius — how far a change reaches. It cannot answer
the question a batch has to be planned against, which is what the task will cost
**the human** once it lands. Four keys answer that, all derived by the sizing
faculty at conception and all overridable by declaring them:

- **`Consequence:`** `notify` | `glance` | `judge` — how much review the work
  needs. `notify` is work nobody outside this workshop consumes (docs,
  notebooks, profiling scripts, organ-repo tooling, test-only, a refactor with a
  byte-equality witness). `glance` is a witnessed change to a consumed repo: you
  read the witness, not the diff. `judge` is a PI's call — a public API, a
  default, an error contract, a science-policy question, an external reporter's
  request.
- **`Witness:`** free text: the machine-checkable claim that will make this
  reviewable in minutes rather than by reading the diff. Look at what the fast
  completion records carry — "ids bit-identical, 62 → 9.7 ms", "31-rule
  byte-equality", "0.068″ parity vs the published model". The slow ones carry
  prose.

  **No `Witness:` means `Consequence: judge`,** however small the task looks.
  That default is the point: choosing a cheap tier means committing, at
  conception, to producing evidence — which is what actually makes work
  reviewable quickly. It is also the one key nothing derives or backfills. An
  invented witness is plausible prose with nothing behind it, which is worse
  than none, because the value of the field is that its absence is informative.
  So `intake formalise` will never write one, and neither should you unless you
  mean it.
- **`Review-minutes:`** an integer **seed**, not a measurement — tier-driven,
  with one nudge for size. The honest numbers come from what the human actually
  spent, recorded per batch. Never cite a value here as evidence about how long
  something took.
- **`Unattended:`** `ready` | `needs-slicing` | `never` — can it finish without
  a human. Deliberately not `Difficulty:` renamed: `needs-slicing` keys off the
  **compaction rule** — a task that would need context compaction to finish is
  too big to run unattended — so a single-repo `large` task is still `ready`
  while a `large` one across four repos is not.

Measured over the 153 backlog prompts the day this shipped: **151 grade `judge`,
because three carry a witness.** Given one, the same backlog grades 33 `notify` /
104 `glance` / 16 `judge`. The whole distance between "everything costs a PI's
hour" and "a fifth of it costs nothing" is whether prompts say what will make
them checkable.

Read `pyauto-brain sizing <prompt>` for any prompt's grades, and
`PyAutoBrain/agents/faculties/sizing/AGENTS.md` for the rules and their known
limits.

### `active.md` schema

Each task is an H2 section:

```markdown
## <task-name-kebab-case>
- issue: https://github.com/<owner>/<repo>/issues/<n>
- issued: YYYY-MM-DD                              # the day the task was issued
- session: claude --resume <session-id>           # optional
- status: <library-dev | workspace-dev | ready-to-ship | awaiting-input | …>
- library-pr: <url>               # optional until the PR exists; repeatable —
- library-pr: <url>               # one line per PR, or one line of `<url>, <url>`
- workspace-pr: <url>             # same shape, for the workspace half
- pending-release: <lib>@<pr-url> # optional; a merged library PR not yet on PyPI
- release-gate: <lib>             # optional; this task waits on <lib>'s release
- location: <cli-in-progress | ready-for-mobile | …>   # optional, used by /handoff
- question: <issue-comment-url>   # optional; set when status is awaiting-input
                                  # (checkpoint-and-continue — PyAutoBrain/AUTONOMY.md)
- heart-ack:                      # optional; --auto launches: the exact YELLOW
  - <reason line acknowledged at launch>   # reason set the human acknowledged
- corrective-red:                 # optional; set when shipping under the
  reason: <exact Heart RED reason string>  # human-authorized corrective-PR
  authorization: <issue-comment-url>       # exception (PyAutoBrain/AUTONOMY.md
                                           # "Corrective-PR exception for Heart
                                           # RED"): names the one RED reason the
                                           # PR repairs + the human's live
                                           # authorization comment
- worktree: ~/Code/PyAutoLabs-wt/<task-name>
- repos:
  - <RepoName>: feature/<branch-name>
- summary: |
    Free-form summary of progress and next steps.
```

#### The PR keys (`library-pr:` / `workspace-pr:`)

`ship_library` and `ship_workspace` write them; `/prm` reads them to find the
PRs it must merge; the dashboard links them. They were doing all three before
they were written down here, which is why nothing validated them and the
dashboard could only render the free-text `status:`.

- **Repeatable.** A task may ship several PRs of one kind (phase 2 of the
  `mind-post-cortex` epic opened three library PRs). Repeat the key on its own
  line, one URL each. The older single-line form — `- library-pr: <url>, <url>`
  — stays valid and is read the same way; nothing needs rewriting.
- **`library-pr:` means "a PR against a library or organ repo"** and
  `workspace-pr:` "a PR against a workspace, HowTo or assistant repo". The
  distinction is the merge order `/prm` enforces (library first), not the
  diff's contents.
- **The rule `lifecycle.py check` enforces:** a row whose `status:` says
  `awaiting-merge`, `PR open` or `shipped` must carry at least one `*-pr:`.
  A row that declares its PRs are open, and then does not say where they are,
  is a task `/prm` cannot close and a human cannot find.

**This one is drift, not a warning** — `check` exits 1 on it. A row that says
its PRs are open and then does not say where they are contradicts itself, which
is the class of thing this check exists to catch; there is nothing for a human
to weigh. The live ledger passed the day it shipped, so the first failure can
only be a new row.

The escalation ladder for the *other* new check is the opposite way round: an
uncleared `pending-release:` is reported and `check` still exits 0 (below), and
it stays that way. It is not a contradiction — the key's whole meaning is "not
released yet" — so it must never become a gate on the Mind's CI. If it ever
looks like it should escalate, the thing to fix is the release, not the check.

#### The pending-release chain (`pending-release:` / `release-gate:`)

A merged library PR is not a released library. Between the merge and the PyPI
publish, workspace work that depends on the new API is blocked, and until this
shipped the only machine view of that state was the Brain board's live `gh`
search over the `pending-release` label.

The division of labour is deliberate and this is the whole of it:

| Who | Holds |
|-----|-------|
| **GitHub** | the `pending-release` label on the merged library PR — the source of truth for "merged, not yet published" |
| **PyAutoHands** | the release that publishes it |
| **Mind** | the *link* (`pending-release: <lib>@<pr-url>`) and the *gate* (`release-gate: <lib>`) — nothing else |

- `ship_library` writes `pending-release: <lib>@<pr-url>` on the task's
  `active.md` row when it opens a PR carrying the `pending-release` label.
  `<lib>` is the library repo's name (`PyAutoArray`), the URL its PR.
- `ship_workspace` writes `release-gate: <lib>` on a workspace task that is
  blocked behind that library's release. One line per library.
- `/prm` close-out carries any uncleared `pending-release:` from the
  `active.md` row into the completion record, so the obligation outlives the
  row.
- **`/review_release` step 5, the "Live run" branch, clears it** — that is the
  one step in the organism that establishes a release actually published. It
  drops the `pending-release` label from the named PRs and deletes the
  `pending-release:` lines from the `active.md` rows and `complete/` records
  that name them. Nothing else may clear the key: a release that was dispatched
  is not a release that published.
- `lifecycle.py check` warns (never errors) on a `complete/` record whose
  `pending-release:` is still uncleared after 30 days. A stale link is a
  bookkeeping miss, not drift — the library may legitimately not have been
  released yet.

The dashboard's **Pending release** section renders this **from the ledger
only** — it never calls `gh` at render time, and it says so in its own blurb.
The Brain board's live query stays the fresh view; the dashboard section is the
view that works offline, in CI, and on a phone, and that says what the Mind
*believes* rather than what GitHub *currently reports*. When the two disagree,
GitHub is right and the ledger needs a `/review_release` pass.

### Task dates

The Mind used to date only what it **finished** — every completion record
carries `completed:` — so it could answer "what shipped in July?" but not "what
did we start?". Every task now carries a machine-readable date from the moment
it leaves the backlog:

| Where | Field | The event it dates |
|-------|-------|--------------------|
| `active.md` | `- issued: YYYY-MM-DD` | the day the task got its GitHub issue |
| `planned.md` | `- filed: YYYY-MM-DD` | the day it was scoped |
| `parked.md` | `- parked: YYYY-MM-DD` | the day it stopped |
| `draft/**/<name>.md` | `Filed: YYYY-MM-DD` | the day the prompt was written |
| `active/<name>.md` | `Issued: YYYY-MM-DD` | the day it got its issue, in its light header |
| `complete/<YYYY>/<MM>/<slug>.md` | `- completed: YYYY-MM-DD` | unchanged — the ledger already did this |

The backlog is the **largest** pool of tasks the Mind holds — 150 prompts
against a handful of live rows — so `draft/` carrying a date is what lets the
dashboard's Recent feed see most of the work at all. A prompt keeps its
`Filed:` when it advances to `active/` and gains an `Issued:`; the later, more
specific event is the one that dates the task.

The **key names the event**, so a merged feed can say what each date means
rather than showing a bare timestamp. Reading is tolerant: `registered:`,
`started:`, `planned:`, `found:` and `shipped:` are all read as dates too (the
registries are hand-edited by many sessions, and an entry that says when it
happened should count however it said it) — the table is what a *writer*
should use. The most specific event wins when an entry carries several, so a
task that was filed and later issued dates from its issue.

A date inside another field's prose (`- issue: …/1501 (issued 2026-08-19)`) is
deliberately **not** read — that is the un-parseable habit this convention
replaces. The prompt's `Issued:` header is its own copy of the registry date,
so an issued prompt stays dated even if its registry row goes missing.

`scripts/lifecycle.py dates` reports every entry and issued prompt carrying no
date; `dates --write` backfills them retroactively from the evidence the repo
already holds, annotating each inferred date with where it came from:

```
Issued: 2026-08-18 (backfilled from parked.md `parked:`)
```

The sources, in order: git — the commit that introduced the entry, wrote the
draft, or moved the prompt into `active/`; the prompt's own Intake trailer
(`<!-- formalised by the Intake (Conception) Agent on … -->`); the dated
registry entry that claims the prompt; a date the entry already stated in its
own prose.

The two states want **opposite** readings of the same history, and the switch is
`--follow`. An `active/` prompt dates from the day it *arrived* there (being
issued is a `git mv`, so following the rename back would report the wrong day);
a `draft/` prompt dates from the day it was *written*, wherever it lived then —
the 2026-07-13 lifecycle migration `git mv`-ed 42 prompts in one commit, and
without `--follow` all 42 would date from the migration rather than from
themselves. Nothing is guessed — an entry with no
evidence is reported for a human to date by hand. A **shallow** clone (CI, a
cloud session) cannot see past its boundary commit, so git dates at or before
it are discarded rather than stamping every task with the day the clone was
made.

The dashboard's [Recent](dashboard.md#recent) table is the payoff: it holds the
50 newest events on the work in hand — issued, parked, filed — and shows 10,
opening the next 10 on each tap of `…`. Shipped work stays out of it;
`complete/index.md` is where the ledger is read.

### Completion record (`complete/<YYYY>/<MM>/<slug>.md`) schema

The dated records are the completion ledger (`complete/AGENTS.md`; the
monolithic `complete.md` was retired 2026-07-16, issue #81). Each record opens
with the same fields the old ledger entries carried, then the rich narrative
and, appended by `lifecycle.py record`, the original prompt:

```markdown
## <task-name>
- issue: https://github.com/<owner>/<repo>/issues/<n>
- completed: YYYY-MM-DD
- library-pr: <url> [, <url>]
- workspace-pr: <url> [, <url>]
- pending-release: <lib>@<pr-url>   # optional; carried from the active.md row by
                                    # /prm, cleared by /review_release on a live
                                    # run (see "The pending-release chain")
- summary: <what landed, gotchas, follow-ups — free-form bullets>

## Original prompt

<the active/ prompt the task started from>
```

### Epic trackers (retired 2026-07-13)

Multi-task **epic trackers** (umbrella markdown files listing a sequence of
sub-prompts) formerly lived in `z_features/`. That folder was retired into
`complete/archive/epics/` once the `draft/ → active/ → complete/` lifecycle made
its `z_`-prefixed home redundant. The per-task completion records live in
`complete/<YYYY>/<MM>/`; the archived trackers keep the epic-level narrative.

---

## How the ledger lands (`mind_ledger_merge.yml`)

A branch-scoped session — the phone, claude.ai/code, any `claude/**` flow —
pushes its Mind changes to a feature branch, never to `main`
(`prompt_sync.sh` pushes HEAD deliberately, so a cloud session cannot bypass
review). Nothing downstream used to move that branch on: no workflow so much as
*looks* at a `claude/**` push, because `lifecycle_drift`, `dashboard_refresh`,
`firewall_gate` and `spawn_drift` all trigger on `push: main` or
`pull_request` only. A filed prompt, a task moved to `complete/`, a regenerated
dashboard — all of it waited for a human to write an explicit "merge that
branch" prompt, and the dashboard rendered a stale backlog until they did.

`.github/workflows/mind_ledger_merge.yml` closes that seam. On every push to
`claude/**` it classifies the branch's diff against `main` and, when the whole
diff is **ledger**, merges it and deletes the branch. No session step, no PR,
no prompt.

**Ledger** is drawn by `scripts/ledger_merge.py`, and it is **default deny**:

| Ledger — merged automatically | Code — always a human |
|---|---|
| `draft/**`, `active/**`, `complete/**` | `scripts/`, `tests/`, `.github/`, `skills/`, `policy/`, `docs/` |
| `active.md`, `planned.md`, `parked.md`, `condemned.md`, `epics.md`, `bundles.md`, `ideas.md`, `autonomy_log.md` | `repos.yaml`, `themes.md`, `README.md`, `AGENTS.md`, `REFERENCE.md`, `ROUTING.md`, … |
| `dashboard.md`, `dashboard.html` | anything unclassified — a new root file, a new top-level folder |

Two exceptions inside the ledger dirs: a **dot-path** anywhere, and a file
pytest would **collect** (`conftest.py`, `test_*.py`, `*_test.py`) — inert
prompt assets like `draft/bug/autofit/*_assets/run_once.py` ride along, a file
CI would execute does not. The workflow's own file and the gate script are on
the code side of the line, so neither can auto-merge a change to itself.

Predict the verdict before you push:

```bash
python3 scripts/ledger_merge.py classify --base origin/main   # exit 0 = will auto-merge
```

What blocks, and what does not:

- **`lifecycle.py check` blocks.** Structural drift — a prompt in `active/`
  with no `active.md` entry — is a real contradiction and nothing heals it.
- **Stale renders do not block.** `complete/index.md`, the registry contents
  blocks and the dashboard pages all self-heal on `main`, so the workflow
  merges and then dispatches `dashboard_refresh.yml` and `lifecycle_drift.yml`
  (a `GITHUB_TOKEN` push triggers no workflows, so they must be asked).
- **A conflict blocks**, and the branch is left untouched.

An open PR on the branch is merged **through** the PR, so it records as
`MERGED`; a branch with no PR gets a direct merge commit and is then deleted on
the same proof `branch_sweep.yml` uses — `main` must actually contain the head
sha. `workflow_dispatch` runs the same gate in `audit` mode by default, so a
manual look never merges by accident.

## Tracking and inspection

### Quick inventory

```bash
bash scripts/status.sh
```

Prints counts per category, lists the active and recently-completed tasks, and
and lists the recently-completed tasks.

### From inside Claude Code

- `/health status` — dashboard of registry state (active, planned, recent complete; PyAutoHeart, via the `/health` door)
- `/start_dev draft/<work-type>/<target>/<name>.md` — read a prompt and route it (PyAutoBrain)
- `/worktree_status` — cross-references registry with task worktrees (PyAutoHeart)

---

## How this repo integrates with the rest

The PyAuto workflow has three repos with distinct roles:

| Repo | Purpose |
|------|---------|
| **PyAutoMind** (this repo) | The Mind: ideas, intent, goals, priorities, the prompt registry and prompt-coupled skills. The starting point. |
| **admin_jammy** | Personal admin notes only (`euclid.md`, `grants.md`, `week.md`, `travel.md`, …). Formerly also held PyAuto tooling under `software/`; that has moved out (worktree/label scripts → `PyAutoBrain/bin/`, generic skills → Brain/Heart). |
| **PyAutoMemory** | The Memory organ: topical LLM wikis (`wiki/lensing/`, `wiki/smbh/`, `wiki/cti/`, `wiki/methods/`, `wiki/galaxies/`) and a reading queue (`reading-queue.md`, moved from `admin_jammy/papers.md`). |
| **`PyAuto*` libraries and `*_workspace*` repos** | Where the actual code work happens. Each task gets a feature branch + worktree under `~/Code/PyAutoLabs-wt/<task-name>/`. |

Helper scripts that this repo's skills source:

- `PyAutoBrain/bin/worktree.sh` — task worktree management (create, remove, conflict check).

These live in `PyAutoBrain/bin/` because they're general organism-wide tooling,
not prompt-specific. The skills that need them source by absolute path.

---

## Bootstrap on a new machine

```bash
cd ~/Code/PyAutoLabs
git clone git@github.com:PyAutoLabs/PyAutoMind.git    # the Mind (this repo)
git clone git@github.com:PyAutoLabs/PyAutoBrain.git   # dev-workflow skills
git clone git@github.com:PyAutoLabs/PyAutoHeart.git   # status / readiness skills
git clone git@github.com:Jammy2211/admin_jammy.git    # general tooling (optional)
bash PyAutoBrain/bin/install.sh                        # symlinks skills + commands
```

> **The local checkout directory must be named `PyAutoMind`.** The skills and
> scripts reference `PyAutoMind/...` paths directly — e.g.
> `source PyAutoMind/scripts/prompt_sync.sh` and `git -C PyAutoMind …` — so a
> differently-named directory breaks those commands.

`install.sh` auto-discovers skills from every present discovery root
(`admin_jammy/skills/`, `PyAutoMind/skills/`, `PyAutoBrain/skills/`,
`PyAutoHeart/skills/`, `autolens_profiling/skills/`) and creates symlinks under
`~/.claude/skills/` and `~/.claude/commands/`. Roots that aren't checked out are
skipped. Re-run any time after pulling new skills from any of those repos.
