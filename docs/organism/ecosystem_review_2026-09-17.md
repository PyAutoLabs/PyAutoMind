# PyAutoScientist ecosystem review — 2026-09-17

An evidence-based review of the four organs a remote session can hold — **Mind**
(PyAutoMind), **Brain** (PyAutoBrain), **Memory** (PyAutoMemory), **Cortex**
(PyAutoCortex) — asking one question: *given how the organism is actually
used, what are the obvious improvements?* Every number below was measured in the
checkouts at their 2026-09-17 tips (Mind `90db62e3`, Brain `9f09bbc`, Memory
`7df1213`, Cortex `851450e`) or read from GitHub through the MCP tools. Heart,
Hands, Nerves and Gut were not attached and are only seen from the Mind's side.

The short version: **the organism works, and works hard** — about 100 tasks a
week ship through it, three quarters of them science. The improvements are
not about capability. They are about (1) a ledger design that silently loses
records under its own traffic, (2) gates and faculties that are documented as
load-bearing but measured as decorative, (3) an organ (Memory) whose machinery
has outgrown its content, and (4) a prose surface that has grown faster than
anyone reads it. Each section ends with the concrete change.

---

## 1. The pipe is healthy; the plumbing under it is not

**Throughput.** Steady state over the last eight full weeks is **~98 completions
per week**; September has 228 records in 17 days. The backlog is roughly
stable at ~210 drafts (September: 298 filed vs 228 completed — a slow rise, not
a drain). 73 % of September's completions target science libraries and
workspaces; 24 % target organs. Draft age median is 15 days, p90 66 days. The
oldest ~20 drafts date from April–July and 31 drafts carry `Difficulty:
too-large` — those are the ones that never get picked; they need splitting or
shelving, not waiting.

**Traffic.** PyAutoMind took **2,972 commits in 30 days** (~100/day), 96 % of
which touch only ledger files. `active.md` (a 188-line file holding nine rows)
is rewritten in 43 % of all commits; `dashboard.md` and `dashboard.html`
(150 KB and 250 KB, both generated) are regenerated and committed ~1,500 times
each in eight weeks. That volume is the direct cause of the next finding.

### Finding 1.1 — the ledger auto-merge is silently dropping shipped work

`mind_ledger_merge.yml` ran 100 times between 09-11 and 09-17: **76 success, 24
failure**. Two failure modes, both read from the run logs:

- *Merge conflict on shared files* — `active.md`, `autonomy_log.md`,
  `dashboard.html`: "conflicts with main — resolve it by hand". Every branch
  edits the same three files, so any two sessions in flight collide.
- *A repo-wide drift check red for an unrelated row* — run 34677840370 refused
  a three-record branch because `active.md: model-figures-graphical` (a
  different task) was missing a PR key.

**The workflow notifies nobody on failure.** The result on `origin`:
85 `claude/*` branches on PyAutoMind (69 already merged but never deleted, 17
unmerged) and 40 on PyAutoCortex (38 merged-not-deleted, 4 unmerged). Among the
17 unmerged Mind branches, **six carry `complete:` records for shipped tasks that
exist nowhere on `main`** (`wcs-json-slow-suite-pixelized-fit`,
`reconstruction-noise-map-zeroed-pixels`, `gradient-eager-jit-divergence-py313`,
plus three from today: `demo-subplot-fit-interferometer-combined`,
`interferometer-dirty-images-call-sites`, `jit-visualization-outputs`). The
dashboard on `main` still lists today's three as "in flight / awaiting merge".
The organism's own definition of "shipped" is the `complete/` record; three
tasks from August–September have quietly stopped existing.

On the Cortex side the same gate holds three PRs open since 09-11 (#31, #32,
#37) because a new project's birth touches `projects.yaml`, which the classifier
rightly calls code — so **every new science project waits on a human merge**,
and job ids 342650 and 343043 recorded on those branches are not on `main`.

**Change.** Make the ledger conflict-free by construction, then the gate can
stay strict:

1. **Stop committing generated pages on branches.** `dashboard.md`,
   `dashboard.html` and `complete/index.md` already self-heal on `main`
   (`dashboard_refresh.yml`); regenerating them per branch adds ~400 KB of
   guaranteed-conflicting diff to every push for nothing. Branches write source
   files only; `main` renders.
2. **One file per task, no shared tables.** Move each `active.md` row into the
   front matter of its `active/<slug>.md`, and each `autonomy_log.md` row into
   the task's completion record. `active.md` becomes generated (like the
   dashboard). Two sessions then never touch the same file unless they work
   the same task — which is the one conflict worth a human.
3. **Scope the drift check to the diff.** `lifecycle.py check --paths <changed>`
   on the merge job; the repo-wide check stays on `main` and on
   `lifecycle_drift.yml`.
4. **Fail loudly.** On a failed auto-merge, open (or update) one tracking issue
   listing the branch and the record slugs it carries. Today the only trace is
   a red run nobody is subscribed to.
5. **Sweep merged branches.** 107 merged-but-undeleted `claude/*` heads across
   two repos means the delete step in the merge job is not firing on the
   PR-merge path; `branch_sweep.yml` is `workflow_dispatch`-only. Put it on a
   schedule.
6. **Cortex: let `new` land.** A `projects.yaml` row *addition* whose `status`
   is `active` and whose sibling ledger is in the same diff is a ledger event,
   not code. Edits and deletions to existing rows stay code.

Items 1, 3, 4 and 5 are each an afternoon. Item 2 is the real fix and is a
Mind-only refactor with a `lifecycle.py` migration; everything downstream reads
through `lifecycle.py` already.

### Finding 1.2 — the Heart gate is acknowledged, not obeyed

Across the autonomy log and September's 228 records, the Heart verdict at ship
was **YELLOW 199 times, RED 139, GREEN 10**. The recurring reasons are the same
two strings ("workspace validation not passing", "release validation failed
(stage integrate)"). Every ship contains a line of the form "heart RED-acked,
five organism-scope reasons, nothing in this branch is in the release chain".
A gate that is green 3 % of the time and overridden 97 % of the time is not a
gate; it is a ritual that costs a paragraph per task and trains every session
to write the override.

**Change.** Two options, pick one:

- *Scope the verdict.* Have `vitals` return the verdict **for the repos in the
  branch's blast radius** (the ship skills already compute this set). A
  PyAutoFit branch should not be RED because `autogalaxy_workspace` smoke is
  failing. Organism-wide RED stays the release gate, where it belongs.
- *Fix the persistent reasons.* If workspace validation has been red for weeks
  and every session agrees it is not theirs, the reasons are either real (then
  they are the highest-priority bug) or stale (then Heart should expire them).
  Either way, a RED that nobody acts on for a month should page, not decorate.

Also: 37 of September's records say the Heart was unreachable from the web
container. About a third of Mind commits carry the remote-session trailer. For
that third, the gate does not run at all. The Heart publishes `badge.json` to
Pages already; `vitals` should read that over HTTPS when the CLI is absent, the
way the Brain board does.

### Finding 1.3 — the review leg is mostly not run

Ship records name the review outcome: CLEAN 126, human 22, pending 19, **none
9, n/a 7, FINDINGS 4**. The recent (September) rows overwhelmingly read "review
NONE — no independent review leg ran"; the CLEANs are July–August. The
autonomous-ship gate is documented as four legs; in practice the fourth leg
has been dropped and the record says so each time. Either make the review
faculty a mandatory step the `ship_*` skills run (it is a 287-line script that
takes seconds), or remove it from the gate and stop writing "none" 200 times.

---

## 2. The Brain: five doors carry the load; fifteen are documented

**Where the traffic goes.** Strict commit-message hits for verb invocations
across Brain + Mind: `feature` 282, `bug` 158, `prm` 78, `intake` 56, `cortex`
53, `health` 50, `refactor` 42, `hygiene` 41, `batch` 37 … `eyes` 5, **`route`
4**. Independently, 64 % of the 1,547 completion records route through three
conductors (bug/feature/refactor), while 30 % (`maintenance`, `docs`,
`research`, `test`) go through work-types that have **no conductor at all**.
`/route`, described in `COMMANDS.md` as "the primary interface", is the least
used verb in the organism. `start_library` + `start_workspace` appear 297
times to `start_dev`'s 24 — sessions skip the front door and go straight to
stage two.

**Where the code is.** 65 % of the Brain's Python sits in four agents
(`intake` 4.1k lines, `batch` 3.6k, `hygiene` 2.8k, `cortex` 1.2k). Five
conductors (`eyes`, `community`, `refactor`, `workspace`, `build`) have ≤ 4
lifetime commits; `eyes` and `build` are untouched since July; `build` and
`vitals` contain no Python at all — `vitals` has the third-largest AGENTS.md
(233 lines) over a 53-line shell script.

**The batch conductor.** 3,606 lines of Python, 908 + 773 lines of tests, a
581-line AGENTS.md, a `batches/` tree in the Mind with four AGENTS.md files —
and **one batch has ever run** (2026-08-31 pm; last touched 09-03).
`review-minutes-actual` was never filled, which `lifecycle.py check` has warned
about on every run since. The Cortex already reached the same verdict on its
own copy of this apparatus (schema decision 58: "0 slots were opened by the
conductor, 0 rulings came from a packet … cost with no reader") and deleted it.

**Change.**

- **Demote, don't delete, the idle conductors.** `eyes`, `community`,
  `workspace`, `build` become faculties or skill bodies (prose the session
  follows), which is what they are in practice. Keep the router registry
  honest: the README says 13 conductors, the router has 15,
  `docs/concepts/agents.md` lists 11.
- **Give the 30 % a home.** `maintenance`, `docs`, `research`, `test` are
  real work-types with real volume. Either a single "work-type" conductor that
  the four map onto, or state plainly in ROUTING.md that these route to the
  Feature Agent with a work-type flag — which is what happens today.
- **Decide about `batch`.** Either run a batch a week for a month and keep
  what survives, or archive it the way the Cortex archived its review-slot
  apparatus. At 4.4k lines it is the largest thing in the Brain that does not
  run.
- **Make `start_dev` the door people actually use.** If sessions go to
  `start_library` directly, fold the classification step into it (or make
  `start_dev` a 40-line dispatcher and move the plan step where it is used).

### Finding 2.1 — a red drift check nobody runs

`bin/install.sh --check-project-discovery` (the check that keeps the
committed `.claude/` and `.codex/` symlinks in step with `skills/`) is wired
into no test and no workflow. Run today it reports **9 missing links** —
`batch`, `ci_speedup` and the brand-new `start_bundle` are invisible to every
web/mobile session — and **4 dangling links** to `register_and_iterate` and
`run_queue`, skills that no longer exist. `bin/check_skill_line_counts.sh` (the
200-line skill budget) is likewise unwired. One line in `tests.yml` fixes both.

Also: `tests/test_branch_sweep.py::test_a_failed_delete_reports_why` fails in
this container (871 pass). Mind's suite has one root-only permissions artefact
(`test_the_hook_survives_an_unwritable_tools_dir`); Cortex 59/59, Memory
181/181.

---

## 3. Memory: the machinery outgrew the knowledge

Memory is the one organ where the measurement is unambiguous.

- **Zero new wiki pages in 60 days.** Last one: 2026-07-17. In the same window
  22 files were added, all pipeline (five workflows, six scripts, five test
  files, hooks). Three of five sub-wiki logs have a single entry, from the
  2026-05-22 build.
- **Read six times.** Of 1,547 completion records, **6** cite a wiki page and
  **1** names `pyauto-brain memory`. The faculty works (verified: exit 0, eight
  ranked hits) — it is simply not consulted. `WORKFLOW.md` says the Feature
  Agent consults Memory before planning; the records say it does not.
- **The intake funnel leaks 95 %.** ~152 papers surfaced by the two arXiv
  workflows → 8 promoted → **7 filed** into wiki + bib. 114 `arxiv-interests`
  entries sit unread (eleven day-batches); the `## Interests` section of the
  reading queue, their promotion target, holds no papers. 1,463 lines of
  `board.py` plus 1,078 lines of workflow drive a 4.6 % funnel.
- **Quality debt CI cannot see.** 389 of 651 source entries (60 %) are
  `Canonical BibTeX key: TODO`; 2,727 TODOs are the *content* of 58 pages;
  708 of 2,123 wikilinks (33 %) point at pages never written; 823 of 1,074 bib
  entries (77 %) support no claim; 0 of 147 pages are `reviewed`. `make
  validate` passes on all of it — placeholders were designed to validate.
- **Small drift.** `bibkey_aliases.yaml` is documented in AGENTS.md, index.md
  and wiki/CLAUDE.md; it was retired in #34 and does not exist.

**Change.** The question is what Memory is *for* now, and the honest answer
from the data is: an inbox, not a library. Three moves, in order of return:

1. **Make consultation automatic where it is cheap.** `intake` already sizes a
   prompt; have it run the memory faculty on the prompt title and paste the
   top three citations into the draft's header. That turns "consult before
   planning" from a doctrine nobody follows into a line every prompt carries.
   The same hook belongs in `research/` work-types.
2. **Turn the digest off, or make it lapse.** `arxiv-interests.md` never
   expires, so it only grows. Give it the inbox's seven-day lapse. If the
   Slack `#papers` post is the product (the workflow says it is), the Mind can
   keep posting and stop writing into Memory at all; a day's ten papers that
   nobody promotes are not knowledge.
3. **Stop treating the seed as a wiki.** Move the eight all-TODO source pages
   (1,747 lines) and the 389 unresolved entries under `wiki/<domain>/seed/` (or
   a single `unfiled.md` per domain), excluded from the index, and add a
   wikilink resolver to `make validate` so the 708 dangling links become a
   number that has to go down. A wiki whose index only lists pages a human
   has read is smaller and worth consulting.

---

## 4. Cortex: used daily, redesigned weekly

The Cortex is the best-used organ by traffic share: 79 % of its 209 commits
carry ledger content, 186 logged events, 21 live runs, ledgers written today.
Its cost is elsewhere.

- **Three model rewrites in eleven days** (gates retired 09-03, phases 09-07,
  tasks/rulings/batches 09-12), each justified by measurement, each leaving
  its predecessor frozen in `archive/` (90 files, 5,170 lines). The 465-line
  decision log is half the size of the 943-line script it explains. The
  current shape (one ledger per project: Now / Runs / Log) is the one the
  human kept coming back to, so this should now stop — but the organism table
  has not caught up (below).
- **The one door does not open from where it is driven.** `checkin --apply`
  needs `/mnt/c`, `/home/jammy`, `/mnt/ral` and `gh`. In a cloud session
  seven of seven pulls fail and the push is refused; ~27 % of the conductor
  (the pull, the push, the issue verb) is inert. Two of four verbs work; the
  headline one is a dry run. 27 % of Cortex commits are the `ledger_merge`
  bot compensating, and the newest commit on the repo is another patch to
  that seam.
- **Small drift.** `status: planned` is in the schema and on no row; log kind
  `lesson` is in the grammar and used 0 times; five of fifteen rows have no
  ledger despite "one ledger per project".

**Change.** Accept the split the data shows: the laptop *pulls*, the web
*writes*. Make `checkin` two verbs — `pull` (laptop only, fails fast with the
list of missing roots) and `checkin` (renders + pushes from anywhere, reading
`jobs` output the human pastes or the pull leg cached). Then the door works on
every surface and the conductor stops carrying 316 lines of code that cannot
run where it is invoked.

---

## 5. Prose: the organism describes itself faster than it is read

Every session loads the four AGENTS.md files: **7,700 words, ~13k tokens**,
before the first tool call. Then a `/start_dev` reads `start_dev.md` (181) +
`reference.md` (201) + `WORKFLOW.md` (351) + `GITHUB_ACCESS.md` (158), and
`/prm` reads 762 lines. On the Brain, 5,951 lines of Markdown are skills and
4,090 are agent docs, against 36.7k lines of Python.

Duplication is the failure mode, despite a no-duplication doctrine stated in
two places:

- **"No `gh` in remote sessions"** — the same four-line banner in 16 skill
  files, plus 46 lines in Brain AGENTS.md, all 158 lines of
  `GITHUB_ACCESS.md`, 81 lines in `board/AGENTS.md`, and sections of
  `OPERATIONS.md` and `WORKFLOW.md`: **~330 lines on one fact**, and the
  "Remote sessions" block rides in every one of 34 repos' AGENTS.md.
- **The organism table** — three copies with three different row sets
  (ORGANISM.md: 8 organs; Brain AGENTS.md: 8, different wording;
  `docs/concepts/organism.md`: 7, Nerves missing). `docs/index.md` says "eight
  repositories"; `docs/satellites.md` says "the five organism repos".
- **ORGANISM.md, "the one canonical page", is stale on the Cortex.** It still
  describes "rulings of record for every science run … a verdict recorded
  only outside the Cortex does not exist". Cortex decision 60 (09-12) removed
  rulings, verdicts and witnesses; Cortex AGENTS.md says "no state machine,
  no witness, no verdict". The canonical page now contradicts the organ.
- **The call chain** — seven copies, ending in "Build" in five and "Hands" in
  two; ORGANISM.md carries a paragraph solely to reconcile the two spellings.
- **Retirement notices as permanent prose.** `z_features/`, `z_vault/`,
  `autoprompt/` (retired 07-13) are still explained in five files;
  REFERENCE.md carries 12 "retired" notices; "`complete.md` retired 07-16" is
  restated in five places; `/wake_up` is "superseded" and still installed.
- **Vocabulary drift** the tooling does not catch: `Priority: normal` (108
  drafts) vs `Priority: medium` (44); `Type: human` (2) vs `human review`.

**Change.**

1. **Generate the AGENTS.md remote-sessions block as a two-line pointer**
   ("web sessions: run `session_bootstrap.sh`; GitHub via MCP — see
   `PyAutoBrain/skills/GITHUB_ACCESS.md`"), and delete the 16 skill banners.
   `test_gh_surface.py` should assert the pointer, not the essay.
2. **Move retirement notices to a CHANGELOG** (one per organ) and delete them
   from the operating prose. A retired folder needs one line, once, dated.
3. **Fix ORGANISM.md's Cortex row and the organ counts today** — this is the
   page every other page defers to.
4. **Put procedure into scripts.** `prm.md` + `reference.md` are 762 lines
   telling an LLM to do, in order, things `lifecycle.py` could do in one
   verb (`lifecycle.py close <slug> --pr …` : record, retire, index,
   dashboard, commit). The Cortex already does this (`cortex.py done`). Every
   line moved from prose to a deterministic verb is a line no session
   re-reads and no session gets subtly wrong.
5. **Cut the completion record to what is read.** September's 228 records
   total 30,439 lines (median 124, p90 207). The Memory faculty is the only
   reader, and it greps titles. Keep the "What shipped / What the filed scope
   missed / Root cause" sections; drop the narrative. Same for
   `autonomy_log.md` rows, some of which exceed 1,000 characters in a single
   table cell.

---

## 6. What to do first

Ordered by value over effort, with the organ that owns each:

| # | Change | Organ | Effort | Why first |
|---|--------|-------|--------|-----------|
| 1 | Recover the six lost `complete/` records from their branches; land Cortex PRs #31/#32/#37 | Mind, Cortex | hour | shipped work is currently missing |
| 2 | Ledger merge: stop committing generated pages on branches; diff-scoped check; failure opens an issue; scheduled sweep | Mind | day | removes ~all of the 24 % failure rate |
| 3 | Wire `--check-project-discovery` and the skill line budget into `tests.yml`; fix the 13 links | Brain | hour | three skills are invisible to web sessions today |
| 4 | Fix ORGANISM.md Cortex row + organ counts; pointer-ise the remote-sessions block | Brain, Mind | half day | the canonical page contradicts an organ |
| 5 | Vitals: blast-radius-scoped verdict; read Pages `badge.json` when the CLI is absent | Brain, Heart | day | turns the gate back into a gate |
| 6 | Per-task ledger files; `active.md` and `autonomy_log.md` become generated | Mind | 2–3 days | ends shared-file conflicts for good |
| 7 | Intake pastes top-3 Memory citations into every draft; interests file lapses | Brain, Memory | day | Memory read on every prompt instead of six times ever |
| 8 | Decide `batch`: run weekly for a month or archive | Brain | decision | 4.4k lines that ran once |
| 9 | `lifecycle.py close` verb; shrink `prm` to a wrapper | Mind, Brain | 2 days | 762 lines of procedure → one command |
| 10 | Seed-vs-wiki split in Memory; wikilink resolver in `make validate` | Memory | day | makes the wiki worth consulting |
| 11 | Cortex `pull` / `checkin` split | Brain, Cortex | day | the one door opens from the web |
| 12 | Demote idle conductors; home for the 30 % work-types | Brain | day | roster matches usage |

Items 1–4 are mechanical and safe to do in one sitting. Item 6 is the
structural one; everything in section 1 gets easier after it.

---

## Method

Three survey agents inventoried Mind, Brain, and Memory + Cortex (file and
line counts, `git log` by week and by path, commit-message hits per verb,
header censuses over `draft/` and `complete/`, test runs, drift-check runs).
The ledger-merge findings come from the last 100 `mind_ledger_merge.yml` runs
and two failed-job logs via the GitHub MCP tools, the branch findings from
`git ls-remote` plus `merge-base --is-ancestor` against `origin/main`, and the
Heart/review tallies from a regex over `autonomy_log.md` and September's
records. Spot-checks re-ran the headline numbers directly. Nothing outside
`docs/organism/` was edited.
