Added a **HowToFit mode** to the autofit_assistant and propagated its
copy-and-paste activation prompt to the three READMEs a learner reaches the
course from.

**autofit_assistant** — `modes/howtofit.md` following the `start_here` / `byol`
conventions, a `## HowToFit mode` README section with the activation prompt,
and the mode registered in the routing. The mode points the learner at the
HowToFit GitHub repository, explains the Jupyter notebooks (recommended, to run
the lecture code) and the Markdown lectures (read on GitHub), and then answers
questions using the learner's current lecture, cell, code or error as context.
Merged as autofit_assistant#43 (`feature/howtofit-mode`, 2026-09-14); issue #42
closed; released in autofit_assistant 2026.9.15.1.

**Approved scope amendment (2026-09-14)** — the same activation prompt and
notebook/Markdown guidance added, README-only, to:

- HowToFit#55 — `README.md` "Study with the assistant" under Getting Started.
- autofit_workspace#157 — the HowToFit section of `README.md`.
- PyAutoFit#1625 — the HowToFit section of `README.md`.

All three: one commit each on `feature/howtofit-mode`, merged by the human on
2026-09-14 19:59 UTC. No lecture, notebook or library source changed.

The activation prompt, verbatim in all four places:

```text
Enter HowToFit mode.

I want to work through the HowToFit lectures. Show me where to find them
and how to use Jupyter Notebook or Markdown, then help me with questions
as I go.
```

**Ledger drift, found at close-out (2026-09-17).** The `active.md` row still
read "propagation in progress; shipping held by Heart YELLOW; source remains
local and uncommitted" three days after every PR had merged — the human merged
all three propagation PRs directly and no `/prm` ran, so the row, the
`active/` prompt and the dashboard all kept offering shipped work as
in-flight. A `/start_dev` resume on the prompt from a web session found the
merges (no `feature/howtofit-mode` branch left on any remote; the prompt text
present on `main` of all three repos) and ran the close-out. Lesson: a
human-merged PR still needs `/prm` for the Mind leg, or the row lies until
someone resumes it.

The Heart YELLOW ship hold the row recorded (workspace validation 3 failures,
manifest drift, three matrix_free SLQ profiling drifts) was acknowledged by the
merge itself; no `heart-ack:` block was ever written to the row.

The task worktree `/home/jammy/Code/PyAutoLabs/.worktrees/howtofit-mode` lives
on the laptop and could not be removed from this session — `worktree_remove
howtofit-mode` is still owed locally. The `feature/howtofit-mode` branches were
deleted on all four remotes at merge.

All three merged heads are contained in release tag `2026.9.15.1` of their
repo (verified by ancestry at close-out), so nothing is pending release.

## Original prompt

# autofit_assistant: HowToFit learning mode

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
- HowToFit
- autofit_workspace
- PyAutoFit
Themes:
- assistants
Difficulty: small
Autonomy: safe
Priority: medium
Filed: 2026-09-14
Issued: 2026-09-14
Issue: https://github.com/PyAutoLabs/autofit_assistant/issues/42

## Original request

In autofit_assistant, we recently added start_here and byol models where users hit the README.md, and then paste in a standard prompt to do that. Can you add a "HowToFit" mode to the agent, which points the user to the HowToFit GitHub, explinas they can do the lectures using Jupyter Notebook (recommended if they want to run code) or markdown, and once they are in this how the assistant will answer any questions they have.

## Scope

- Add a HowToFit entry and standard copy-and-paste activation prompt to @autofit_assistant/README.md alongside its existing modes.
- Add a mode document following the existing start_here and byol conventions and register its routing where needed.
- Direct learners to the HowToFit GitHub repository; explain Jupyter Notebook (recommended for running lecture code) and Markdown reading options.
- Explain that the assistant answers lecture questions in this mode, using the learner's current lecture, question, code or error as context.
- Check consistency of mode activation, internal links and the course link; no lecture or library changes are required.

## Approved scope amendment — 2026-09-14

Original request verbatim:

Ok great, yes put that on HowToFit but also autofit_workspace in its section and the main PyAutoFit REAMDE.md in its section

- Propagate the same approved HowToFit mode activation prompt to @HowToFit/README.md, the HowToFit section of @autofit_workspace/README.md, and the HowToFit section of @PyAutoFit/README.md.
- Keep this within the same howtofit-mode task and branch; README-only additions, no lecture or library source changes. Existing Heart YELLOW shipping hold still applies.
