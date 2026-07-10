# PyAutoMind

📖 **Full documentation → <https://pyautoscientist.readthedocs.io>** — the whole PyAutoScientist organism, including how to fork and run your own.

The Mind of the PyAuto organism: every piece of work in the ecosystem starts
here, as a markdown file describing what you want in plain English. An AI
agent (or a human) picks the file up and turns it into a tracked GitHub
issue, a feature branch, and a merged pull request. No template, no special
syntax — if you can describe the change in a GitHub issue, you can drive the
workflow.

What lives here:

| File / folder | What it is |
|---------------|------------|
| `ideas.md` | raw incubating ideas, no structure required |
| `<work-type>/<target>/*.md` | scoped prompts (`feature/`, `bug/`, `docs/`, …) |
| `active.md`, `planned.md`, `complete.md` | the task registry: in flight, queued, done |
| `issued/` | prompts that have become tracked issues |
| `repos.yaml` | the body map — the single source of repo identity |
| `scripts/` | registry sync + drift checks (`repos_sync.py`) |

A prompt flows: idea → prompt file → `/start_dev` → GitHub issue +
`active.md` entry → worktree development → PR → `complete.md`. The registry
is shared state, so any machine or session can pick up an in-flight task.

The schemas and conventions — prompt taxonomy, prompt file format, the
`active.md` / `complete.md` schemas, epic trackers, bootstrap on a new
machine — are in [REFERENCE.md](REFERENCE.md). How agents should operate
this repo is in [AGENTS.md](AGENTS.md).

The organism this repo is the Mind of (Mind, Brain, Heart, Hands, Memory) is
described once in
[PyAutoBrain/ORGANISM.md](https://github.com/PyAutoLabs/PyAutoBrain/blob/main/ORGANISM.md)
and documented in full at <https://pyautoscientist.readthedocs.io>.
