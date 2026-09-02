## organ-board-github-link
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/325 (closed completed 2026-09-02)
- completed: 2026-09-01
- prs (all MERGED 2026-09-01, each proven an ancestor of its repo's `origin/main`):
  - PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/326 (merge `8a060473eb0d3a27250fbd1c8eeaa061ecd85f25`)
  - PyAutoHeart https://github.com/PyAutoLabs/PyAutoHeart/pull/194 (merge `5eb530ccd78d7e74dbf5e32bd7d88e1fda876973`)
  - PyAutoHands https://github.com/PyAutoLabs/PyAutoHands/pull/273 (merge `ff34fdcf923f55f95b589134b162684b074f6102`)
  - PyAutoMemory https://github.com/PyAutoLabs/PyAutoMemory/pull/77 (merge `a1fc782f1326c1ba990809ccf8f6ff3c513150e4`)
  - PyAutoScientist https://github.com/PyAutoLabs/PyAutoScientist/pull/25 (merge `6ec1119a4689d3b4ee044b897f61694872509799`)
- classification: feature (organs) — five repos, five PRs, six boards. Ran as a member of batch
  `2026-08-31-pm` (dispatch 2026-08-31, `--auto` at effective level `safe`, session
  `claude-code-remote` / web-github). No local worktree was ever claimed.

- summary: Every organ board header now carries a `GitHub Page` link beside its existing
  `markdown version` link, pointing at that repo's `README.md` on github.com — the way back from
  the Pages-hosted board to the repository front door. PyAutoBrain carried two boards (the Mind
  tasks dashboard in `agents/conductors/intake/_intake.py`, which renders into PyAutoMind, and the
  Brain morning board in `board/_board.py`); Heart, Hands, Memory and Scientist carried one each.
- identity, not literals: the href is derived from the `repos.yaml` `home` (Mind dashboard) and
  from `derive_org` plus the board's own repo name (Brain board) — the non-test diff contains no
  hardcoded owner, and the whole segment drops out when the repo identity is unknown, exactly as
  the pre-existing `markdown version` link does.
- stated decision: the Brain morning board had **no** `markdown version` link to sit beside, so
  PR#326 added the standard two-link `mdsrc` line rather than a `GitHub Page`-only one, so the
  Brain board reads like its five siblings. The prompt explicitly left this to judgement and asked
  for it to be stated. Reverting to the narrower call is one edit: drop
  `<a href="board.md">markdown version</a> · ` from the added line in `render_html`.
- difficulty override (carried from the prompt, honoured): the sizing faculty returned
  `too-large (score 13)`, almost entirely `max(0, repo_count - 1) * 2` — breadth, not depth. Filed
  and shipped as `small`, one small PR per repo, no phase split. That held.
- witness: each generator's existing board test now asserts the new anchor and its README href
  (`test_board.py`, `test_organism_board.py`, `test_intake_dashboard.py` and siblings). PyAutoBrain
  ran `691 passed`.
- ship gate: all five legs passed 2026-08-31 — tests green; smoke n/a (organ repos, no downstream
  workspace script surface); review CLEAN with every claim basis-cited; Heart **STALE** (an
  organism-scope evidence gap, not a branch-scope one — no YELLOW/RED reasons); independent
  adversary CLEAN, witness HOLDS, having rendered both boards through the real production path.
- heart-ack (carried from the `active.md` entry): manifest drift — local checkout origins, 1
  mismatch vs `PyAutoMind/repos.yaml`. Unrelated to a board-header anchor.

- close-out note: this record was written 2026-09-02, a day after the merge date it carries. The
  batch review merged all five PRs on 2026-09-01 but never ran the close-out, so issue #325 stood
  open and the `active.md` entry still read `pr-open` until 2026-09-02. The batch record
  `batches/2026-08-31-pm.md` member line reads `DELIVERED (5 PRs green: …)` and is left as the
  batch conductor wrote it.

## Original prompt

# GitHub Page link in every organ board header

Type: feature
Target: organs
Repos:
- PyAutoBrain
- PyAutoHands
- PyAutoHeart
- PyAutoMemory
- PyAutoMind
- PyAutoScientist
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: each of the six generated board HTML pages contains an `<a>` whose text is `GitHub Page` and whose href resolves to that repo's README.md on github.com, asserted in that generator's existing board test
Review-minutes: 3
Unattended: ready
Filed: 2026-08-31
Issued: 2026-08-31

Original request, verbatim:

> on each of the 6 organ dashboards, next to "markdown version" or similar but
> high up can you include a clickable text URL link saying "GitHub Page" which
> goes to the README.md

Each of the six organ boards renders a small muted header/anchor line carrying a
`markdown version` link to its own generated `.md` twin. Add a second clickable
text link beside it, reading **GitHub Page**, pointing at that repo's `README.md`
on github.com — the way back from the Pages-hosted board to the repository front
door. It must sit high up in the page, next to the existing link, not in the
cross-board footer (that footer already exists and is a different surface).

The six boards and their generators, each with the line the new link goes beside:

| Board | Generator | Anchor |
|---|---|---|
| Mind tasks | `PyAutoBrain/agents/conductors/intake/_intake.py` | `:2319` — `link("dashboard.md", "markdown version")` |
| Brain morning | `PyAutoBrain/board/_board.py` | `:1632` — writes `index.html` + `board.md`; **no `markdown version` link exists yet** |
| Heart readiness | `PyAutoHeart/heart/dashboard.py` | `:1589` — `{age} · <a href="dashboard.md">markdown version</a>` |
| Hands release | `PyAutoHands/autohands/board.py` | `:510` — `<a href="dashboard.md">markdown version</a>` |
| Memory knowledge | `PyAutoMemory/scripts/board.py` | `:1172` — `<p class="muted mdsrc">…` |
| Organism (Scientist) | `PyAutoScientist/scripts/organism_board.py` | `:252` — `<p class="muted mdsrc">…` |

Notes for whoever picks this up:

- **Five repos, five PRs.** The Mind task dashboard is generated by PyAutoBrain
  code even though the rendered page lives in PyAutoMind, so PyAutoBrain carries
  two of the six boards.
- **The Brain board is the odd one out** — its `index.html` has no
  `markdown version` link to sit beside, so place the GitHub Page link in the
  equivalent header position by judgement (adding the markdown link too is a
  reasonable call, but is a separate decision worth stating in the PR).
- **URLs come from `repos.yaml`** where the generator already has access to it
  (the Mind dashboard derives its links that way) rather than being hardcoded per
  repo.
- Each generator has an HTML snapshot/assertion test
  (`tests/test_board.py`, `test_organism_board.py`, `test_intake_dashboard.py`)
  that will need the new anchor.

**Difficulty override (recorded, not silent).** The sizing faculty returned
`too-large (score 13)` and `Unattended: needs-slicing`. That score is almost
entirely `max(0, repo_count - 1) * 2` — breadth, not depth. The change is one
uniform anchor per generator, with no API or behaviour surface, so this is filed
as `small` and should ship as one task with one small PR per repo rather than a
phase split. Carry this override reasoning into the issue body and `active.md`
at `start_dev` time.
