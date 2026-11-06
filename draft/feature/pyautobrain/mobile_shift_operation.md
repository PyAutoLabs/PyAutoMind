# Run a shift from mobile: the weekend cloud lane (2026-11-07/08)

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: draft
Filed: 2026-11-06
Epic: autonomous-orchestrators
Consequence: judge
Witness: from a phone only (no laptop keyboard), the human lands a shift brief, the watcher on the laptop opens it at `dispatched:`, workers run, the digest posts on its issue, the human reads it and runs `/prm` on one PR — each step recorded as it happened, including what failed
Review-minutes: 20
Unattended: never
Lane: any

Original request (human, 2026-11-06): "I am away this weekend so would like to try running this stuff on mobile, could we make a prompt to begin trying to set that up in a new mobile chat?"

## Plan (agreed 2026-11-06): a manual cloud lane, no laptop

The automatic watcher is laptop-only, so this weekend the human is the orchestrator: start each worker as a **Claude Code web session** (claude.ai/code, or Code in the mobile app) on the task's repo, paste its prompt below, and let it run to a PR. Moving the watcher itself to the cloud is filed separately (`draft/feature/pyautobrain/shift_watcher_in_the_cloud.md`, judge).

### On the phone

1. In the Claude app: **Code** → new session → choose the repo named for the task → paste the prompt → send. Start all three; they run in parallel in the cloud.
2. Check back whenever. If a session asks you something, answer it in the app (nothing stalls on a laptop permission prompt any more).
3. When a session says its PR is open: open the PR in the GitHub app and read the proof comment and the diff.
   - **Merge from the GitHub app once CI is green**, unless the PR has the `decision-taken` label or something looks wrong. If it does, leave it for Monday.
4. Note roughly how many minutes the reviewing took, in total.

### Monday, on the laptop

Tell the laptop session: the minutes, which PRs you merged or left, and anything odd. It writes the Mind close-outs (records, the shadow-window rows) and adds one `cloud` row to `batches/pilot/pilot.md`.

### The three worker prompts

These were checked against `main` on 2026-11-06. Each is self-contained: cloud sessions don't load the laptop's skills, and they can't read PyAutoMind.

**1. Repo: `PyAutoLabs/PyAutoBrain`** — ⚠ **DO NOT RUN (stale, verified 2026-11-06):** the `*_visualization` instances still ship `gallery/gallery_run.sh`, so the next action is correct; retired as `complete/2026/11/eyes-survey-next-action-stale.md`. Run tasks 2 and 3 only.
```
You are a cloud worker in a PyAutoLabs pilot shift. Read AGENTS.md in this repo first and follow it.

Task: `pyauto-brain eyes survey` still tells people to run the retired `gallery/gallery_run.sh`. That harness was deleted on 2026-09-30 (PyAutoEyes phase 5). Lens figures are now rendered by the `*_visualization` repos and collected by the PyAutoEyes dashboard. In agents/conductors/eyes/_eyes.py, fix the docstring (around line 29) and the `next_action` string (around line 144) to name the current route; check agents/conductors/eyes/AGENTS.md for the exact wording. Add a test asserting no survey next action mentions gallery_run.sh.

Done when: the full test suite passes (`python -m pytest tests -q`) and a PR is open against main with a summary of what changed, the test output lines that matter, and what you didn't check. Branch `feature/eyes-survey-next-action`. If you make any decision the task didn't settle, add the label `decision-taken` to the PR. Do not merge. Stop at PR-open.
```

**2. Repo: `PyAutoLabs/PyAutoHands`**
```
You are a cloud worker in a PyAutoLabs pilot shift. Read AGENTS.md in this repo first and follow it.

Task: autohands/bump_colab_urls.sh (run by the release workflow) rewrites the `blob/<version-tag>/` part of Colab links only for autofit/autogalaxy/autolens/autocti _workspace, HowToGalaxy, HowToLens and HowToFit; see its PATTERN at around line 30. The assistant repos now carry Colab notebooks linked from their READMEs (autolens_assistant: docs/colab/cosmos_web_ring_colab.ipynb), so their links go stale at each release. Extend the pattern and the repo or file list to cover the `*_assistant` repos (autofit_assistant, autogalaxy_assistant, autolens_assistant, autocti_assistant), including each assistant's README. Add or extend a test (or a documented dry run on a fixture file) showing an assistant Colab link is rewritten and a non-matching link is left alone.

Done when: the repo's tests pass and a PR is open against main with a before/after example of a rewritten link and what you didn't check. Branch `feature/bump-colab-urls-assistants`. If you make any decision the task didn't settle, add the label `decision-taken`. Do not merge. Stop at PR-open.
```

**3. Repo: `PyAutoLabs/autolens_assistant`**
```
You are a cloud worker in a PyAutoLabs pilot shift. Read AGENTS.md in this repo first and follow it.

Task: finish this repo's leg of the shared AI-options page (PyAutoLabs/PyAutoScientist AI_OPTIONS.md; mirror what autogalaxy_assistant#36 did). The README is already done. Remaining:
- add an AI_OPTIONS.md stub beside AI_POLICY.md that points to https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md
- delete docs/setup/opencode_cli.md, docs/evaluation/agent_evaluation.md, docs/archive/ and .gemini/settings.json, first folding anything still unique into the setup page that remains
- fix every reference to the deleted files (grep the repo, including AGENTS.md, llms.txt, modes/, docs/setup/troubleshooting.md and skills/); paper/paper.md keeps its llms.txt mention
- check for dangling links (the repo's wiki-currency check)

Done when: no dangling links, CI green, and a PR open against main listing what was deleted, what was folded where, and what you didn't check. Branch `feature/ai-options-autolens-leg`. If you make any decision the task didn't settle, add the label `decision-taken`. Do not merge. Stop at PR-open.
```

## Background

## Where the pilot stands (PyAutoBrain#574, phase 4c)

- 4 of 6+ pilot shifts done: 2 shadow, 1 live that failed at spawn (systemd killed the workers; fixed in PyAutoBrain#593), 1 live re-run. The re-run's 3 named tasks gave 2 stale-prompt verdicts and 1 PR, autogalaxy_workspace_test#134, merged. Rows are in `batches/pilot/pilot.md`.
- Shift fixes since then, all merged: readable digest (#580), a shift opens at `dispatched:` (#590), `KillMode=process` + ended workers reaped (#593), no EnterWorktree + `decision-taken` label rule + late-arrival sweep (#595).
- How a shift runs today (`PyAutoBrain/agents/conductors/batch/AGENTS.md`, `PyAutoMind/batches/AGENTS.md`):
  - The human writes a brief into `PyAutoMind/batches/<slot>.md`, and that is the dispatch.
  - A **systemd user timer on the laptop** (WSL) runs `orchestrator_watch.py` every 2 min.
  - Real workers are `claude --bg` sessions on the laptop. The digest posts once on the brief's `issue:`.
  - Merges beyond the one unattended `glance` close-out are the human's `/prm`.

## What blocks running it from a phone (check each; do not assume)

1. **The laptop must stay up.** WSL's VM shuts down when idle, and `loginctl show-user jammy -p Linger` was `Linger=no` on 2026-11-06, so the user timer may not run with no terminal open. Needs: the laptop awake and plugged in, the WSL VM kept alive (`.wslconfig` `vmIdleTimeout`, or a keep-alive), and possibly `loginctl enable-linger` (the human's act).
2. **Landing a brief from the phone.** A brief committed to `PyAutoMind/main` from GitHub reaches the laptop only if the canonical Mind checkout is pulled. The watcher reads the local file. Options: the watcher reads the brief from `origin/main` (git fetch: is that inside its network surface? AUTONOMY.md "The watcher's network surface — 2026-11-03" allows only `gh pr checks`, `claude agents` and one comment, so this needs a ruling), or a separate pull timer.
3. **Pointing the timer at the brief.** `PYAUTO_SHIFT_BRIEF` in `~/.config/pyauto/orchestrator.env` names one brief, so every new shift means editing a laptop file. Proposal to evaluate: the watcher picks the open brief itself (the newest record in `batches/` whose window covers now).
4. **Reading and acting from the phone.** The digest is a GitHub issue comment (fine on mobile). `/prm` needs a Claude session with GitHub access: Claude Code on the web or app (cloud session, no `gh`; see `PyAutoBrain/skills/GITHUB_ACCESS.md`), or Remote Control of a laptop session. Worth testing which is real today.
5. **Attaching to a stuck worker** (`claude attach`) is laptop-only. With the #595 fixes it should be rarer; a parked worker posts its question on its issue.

## (Earlier plan: laptop-run shifts from a phone. Superseded by the cloud lane above; kept for the cloud-watcher draft.)

### What a mobile session should do

1. Read this prompt, PyAutoBrain#574 and `PyAutoMind/batches/pilot/pilot.md`. Find out what this surface can do: GitHub read/write? Remote Control? Mind commits?
2. Report which of blockers 1–5 can be worked around from mobile **this weekend** and which need laptop changes the human must make before leaving. Give the exact commands for each laptop step.
3. Propose the smallest path to one mobile-run live shift. Likely: keep-alive + linger on the laptop, the brief and env set before leaving, and only reading digests and `/prm` from the phone.
4. File any code change as its own draft prompt; do not build in this session. A watcher change to the network surface or brief discovery is `judge` and needs the human's ruling.

Next live shift candidates must be checked against current `main` before briefing: 2 of 3 named prompts in the last shift were stale.

<!-- filed by hand 2026-11-06 at the human's request; headers mirror intake's -->
