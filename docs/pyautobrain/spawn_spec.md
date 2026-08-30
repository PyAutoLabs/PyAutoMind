# spawn — the fresh-slate generator: specification

Spec for `PyAutoMind/scripts/spawn.py` (3b-1). Written 2026-07-10 so the
implementation is mechanical — an execution-tier session follows this file
and makes **no judgment calls**; anything genuinely ambiguous goes back to a
human, it is not decided at implementation time. Design context:
`pyautoscientist_phase3_research.md` §3.

## What spawn is

A generator that stamps **fresh-slate template repos** from the live Mind
and Memory checkouts, plus the mechanical layers of the PyAutoProject
family. Same doctrine as `repos_sync.py`: single source (the live repos) →
generated view (the templates), re-runnable, drift-checked in CI. Spawn
never mutates a live repo; it only writes into template working dirs.

```
python3 scripts/spawn.py                # dry-run: report the file plan (default)
python3 scripts/spawn.py --write DIR   # materialise the templates under DIR
python3 scripts/spawn.py --check DIR   # regenerate + diff against DIR (CI job; exit 1 on drift)
```

## The partition rules

Every file in the source repo is assigned exactly one action by the FIRST
matching rule (order matters). Anything unmatched is **DROP + WARN** — the
warning list is printed on every run so new file classes get classified
deliberately, never silently shipped into a template.

### PyAutoMind → PyAutoMind-template

| # | Pattern | Action |
|---|---------|--------|
| 1 | `scripts/**` | KEEP verbatim (generic tooling: repos_sync, prompt_sync, status, spawn itself) |
| 1b | `tests/**` | KEEP verbatim (generator machinery, same class as rule 1; Memory's table already does this). The privacy test in particular must travel with the generator it guards — a spawned org that inherits `spawn.py` without `test_spawn_privacy.py` can reintroduce the rule-5 leak (issue #118) silently |
| 2 | `REFERENCE.md`, `AGENTS.md`, `CLAUDE.md`, `LICENSE`, `ROUTING.md`, `.gitignore` | KEEP verbatim |
| 3 | `README.md` | KEEP verbatim (already generic post-Phase-1) |
| 3b | `AI_POLICY.md`, `CONTRIBUTING.md` (root — the 2026-08 `.github/` declutter of #248 was undone on 2026-08-20, #253: dashboards are the primary interface now, so root scannability no longer justifies the split placement) | KEEP with owner substitution — both are org-wide pointer docs: generic prose that names the owning org and links the canonical copy inside that org's `PyAutoScientist`. They take the same `PyAutoLabs` → `YOURORG` substitution as rule 9 rather than a verbatim KEEP; verbatim would stamp a literal "Contributing to PyAutoLabs" into a template spawned for another org |
| 4 | `repos.yaml` | SUBSTITUTE → the **template body map**: the five organ rows kept with `github:` owner replaced by `YOURORG`; all live satellite rows replaced by the PyAutoProject family rows (`PyAutoProject` category `library`, `autoproject_workspace` category `workspace`, `autoproject_workspace_test` category `workspace_test`) + a commented-out `autoproject_assistant` row ("uncomment when the clone agent seeds it") |
| 5 | `active.md`, `planned.md`, `parked.md`, `condemned.md`, `ideas.md`, `queue.md` | EMPTY → header line + schema pointer comment only (e.g. `# Active Tasks` + `<!-- schema: REFERENCE.md -->`). **The header is GENERATED, never read from the live file** — `planned.md` and `ideas.md` carry no H1 at all, so "keep line 1" yields a registry entry (issue #118), and a heading-shape test cannot save it either: a task slug written as an H2 is a structurally valid heading. Each file's title lives in `EMPTY_TITLES`; an EMPTY-ruled file with no entry is an UNMATCHED-class human decision, not a guess |
| 5b | `autonomy_log.md` | SPECIAL → the ledger's schema header (H1, the prose explaining the log, the `Outcome ∈ …` legend, the table header row and separator), held as the `AUTONOMY_LOG_TEMPLATE` asset. Not rule 5: it is `SPECIAL`, not in `EMPTY_TITLES`, and carries prose and a table rather than a title plus schema-pointer comment. Like rule 5 it is **GENERATED, never parsed** (issue #123): the old implementation copied lines until one started with `\|---`, so a row inserted above the separator was copied, and a cosmetically reformatted separator (`\| --- \|`) meant the break never fired — 231 live task records into a public repo. The canary scan is no backstop: a leaked row with no dataset or person token scans clean. A test asserts the live ledger still starts with the constant, so generating cannot silently go stale |
| 6 | `draft/**` (the work-type dirs `feature/ bug/ refactor/ docs/ test/ release/ maintenance/ research/ experiment/ triage/` now live under `draft/`) | SKELETON → keep a single `draft/.gitkeep`; drop all draft prompts and their work-type/target subdirs (a fresh Mind starts with an empty `draft/`; intake recreates the work-type subdirs on demand) |
| 6b | `complete/AGENTS.md` | KEEP verbatim (the finished-work archive **schema** is template content; matched before rule 7's `complete/*` DROP) |
| 6b′ | `batches/AGENTS.md` | KEEP verbatim (same split one step on: a batch record is what one dispatched shift *did* — instance state — while the schema saying how to write one is template content. Matched before rule 7's `batches/*` DROP) |
| 6c | `complete/index.md` | GENERATE → stamped by running the **generated tree's own** `scripts/lifecycle.py index --apply` after the tree is written (`lifecycle.py` resolves its root from `__file__`, and rule 1 already KEEPs it). The live `index.md` is still DROPped by rule 7 — this is a fresh empty-archive index, not a copy. Required because the template ships `lifecycle_drift.yml`, whose self-heal (PyAutoMind#116) regenerates this file on every push to the template's own `main`: if spawn did not produce it, each sync would be followed by a bot commit creating a file the next `--check` reports as drift, forever. Do NOT hold the text as a constant here — `lifecycle.py` owns the index format, and a second copy would drift from it |
| 7 | `active/ complete/ batches/ z_features/ z_vault/ autoprompt/` + instance reference docs (`docs/**` now holds only reference material like `spawn_spec.md`) + legacy pre-migration prompt dirs (`autolens/`) | DROP (lifecycle records + instance content; the former `overview.md` instance root doc was deleted outright in #248) |
| 7b | `dashboard.md` | EMPTY (rule 5's mechanism, `EMPTY_TITLES` entry) rather than rule 7's DROP: `README.md` ships verbatim under rule 3 and links this page from its top, so dropping it hands every spawned org a broken front-page link. Like every other rule-5 file the generated body is a title plus the schema-pointer comment — a Mind with no tasks has nothing else to truthfully say, and the page fills itself the first time the new org runs `pyauto-brain intake --apply dashboard`. The live page's content is instance state and never travels |
| 7c | `dashboard.html` | DROP — the Pages twin of `dashboard.md`, written by the same `pyauto-brain intake --apply dashboard` run. Unlike 7b there is no broken-link argument to answer: no shipped file links it, and its publisher (`pages_dashboard.yml`) is dropped by rule 9c, so a fresh org has nothing that reads the page until it regenerates the pair itself |
| 8 | `skills/**`, `policy/**` | KEEP verbatim (`OWNERSHIP.md`, `create_issue/` are generic; `policy/` is org-agnostic safety text) |
| 9 | `.github/**` | **Per file, by the succeed-on-a-fresh-repo test below.** Not a blanket rule: owner substitution alone does NOT make a workflow work, because `YOURORG` is a literal placeholder — the template's own `spawn_drift` run failed `repository 'https://github.com/YOURORG/PyAutoMind/' not found`. See rules 9a–9d |
| 9a | `.github/workflows/lifecycle_drift.yml` | KEEP verbatim — operates only on its own repo (checkout + local scripts) and contains no owner reference at all, so it needs no substitution and succeeds unmodified in a fresh org. Empirically the one green workflow in the template's run history |
| 9b | `.github/workflows/spawn_drift.yml` | DROP — was "keep with the `schedule:` stripped", revised in #125. The self-heal added there makes this workflow depend on `secrets.PAT_PYAUTOLABS` AND on published `*-template` repos, neither of which a freshly-spawned org has, so **every** path in it is unrunnable there and the secret reference alone breaks the no-configured-secret condition. "When in doubt DROP" applies: an org that later publishes templates can adopt this workflow deliberately, having read it. The template still ships `scripts/spawn.py` + `tests/`, so the generator and its guards travel; only the org-coupled automation does not |
| 9c | `.github/workflows/{dashboard_refresh,registry_reconcile,morning_status,morning_health,arxiv_papers,arxiv_interests,firewall_gate,session_hook_propagate,pages_dashboard,branch_sweep}.yml`, `.github/scripts/**` | DROP — instance automation. `dashboard_refresh.yml` checks out `PyAutoLabs/PyAutoBrain` (the dashboard renderer lives with the intake conductor, not in Mind), so it fails on checkout in any org that has no such sibling — and owner substitution only turns that into the literal `YOURORG/PyAutoBrain`. The rest hardcode sibling repo lists, organ-specific workflow names (`PyAutoHeart`/`PyAutoBrain`/`PyAutoHands`), org secrets (`PYAUTO_PAPERS_WEBHOOK_URL`, `CLAUDE_CODE_OAUTH_TOKEN`) and, in `arxiv_fetch.py`, strong-lensing search vocabulary plus dated incident notes. All 13 failing runs in the published template came from these. Two later additions join them (2026-08, first caught by the 2026-08-24 drift run): `firewall_gate.yml` checks out `PyAutoLabs/{PyAutoBrain,PyAutoHeart,PyAutoHands}` by name — `dashboard_refresh.yml`'s failure mode three times over; and `pages_dashboard.yml` needs a GitHub Pages site the default token cannot create on a fresh repo (the Hands lesson already recorded for Memory's `knowledge_board.yml`) and takes `pages: write` + `id-token: write`. A third joins them (2026-08-25): `branch_sweep.yml` checks out `PyAutoLabs/PyAutoBrain` for the sweep logic — `dashboard_refresh.yml`'s failure mode again — and carries a weekly cron, so it would also trip rule 9's no-unattended-trigger condition on arrival. The sweep is worth having in a mature organism and worth re-adding deliberately; it is not worth a fresh org inheriting a scheduled job that fails on checkout every Sunday. A fourth joins them (2026-08-27): `arxiv_interests.yml`, the second daily digest, is `arxiv_papers.yml`'s sibling in every relevant way — the same `CLAUDE_CODE_OAUTH_TOKEN` and `PAT_PYAUTOLABS` org secrets, a cron, and a cross-repo push into `PyAutoLabs/PyAutoMemory` by name — and its ranker `.github/scripts/arxiv_interests.py` carries one reader's personal interest vocabulary, which is instance content by definition. A fifth joins them (2026-08-29): `session_hook_propagate.yml` clones every sibling repo in the manifest with `PAT_PYAUTOLABS` and pushes bot commits into them by name — `firewall_gate.yml`'s org-coupled shape at thirty repos rather than three, and pointless in an org with no siblings to propagate into |
| 9d | any other `.github/**` | **No catch-all rule — UNMATCHED by design.** A fallback here is fail-*open*: a workflow added to Mind later would ride it into the template carrying whatever schedule and secrets it has, which is precisely the defect 9a–9c fix. A new `.github` file must fail the run and get an explicit entry above, like every other new file class |
| 10 | `.claude/**`, `.codex/**` | DROP — agent-discovery symlinks are install artifacts recreated by the PyAutoBrain installer, not source content |

### PyAutoMemory → PyAutoMemory-template

| # | Pattern | Action |
|---|---------|--------|
| 1 | `bibliography/README.md`, `scripts/`, `tests/`, `Makefile`, `LICENSE`, `AGENTS.md`, `CLAUDE.md`, `.gitignore` | KEEP verbatim (tooling + schema + policy — scripts/tests are the citation-validation + knowledge-board tooling the Makefile drives; the former `bibliography/*.py` pattern matched nothing and was retired in #32) |
| 1b | `AI_POLICY.md`, `CONTRIBUTING.md` (root — the #32 `.github/` move undone with the Mind's, #253) | KEEP with owner substitution — same org-wide pointer docs as the Mind table's rule 3b |
| 2 | `bibliography/*.bib` and any bibliography data files | EMPTY → file kept with header comment ("populated by your literature") |
| 3 | `wiki/CLAUDE.md` (the shared schema) | KEEP verbatim — since the wiki/ restructure (PyAutoMemory#24) the schema is a single domain-neutral file at `wiki/CLAUDE.md`, kept canary-clean at the source (its examples carry no instance tokens), so spawn no longer maintains a duplicate schema asset |
| 4 | `wiki/*` (all live sub-wikis, all pages) | DROP; generate instead ONE `wiki/example/` containing a slim scope-only `CLAUDE.md` (the schema is inherited from rule 3, not copied), an `index.md` skeleton listing zero sources, and one `sources/EXAMPLE_stub.md` demonstrating the stub format (hand-written once, stored inside spawn as a heredoc/template asset — not copied from live content) |
| 5 | `index.md` | SUBSTITUTE → skeleton: intro line + a table with the single `wiki/example/` row + "add sub-wikis following the same schema" |
| 6 | `reading-queue.md` | EMPTY → header + section-format comment |
| 7 | `README.md` | GENERATE → a template README asset held inside spawn (text surgery on the live README is brittle across edits; the asset keeps `--check` round-trips stable) |
| 8 | `.github/workflows/validate.yml` | KEEP with owner substitution — self-contained (no schedule, no secrets, no sibling repos), so it clears the fresh-repo invariant. `.github/workflows/knowledge_board.yml` | DROP — it needs a GitHub Pages site the default token cannot create on a fresh repo, plus a schedule; `scripts/board.py` itself ships via rule 1, so an adopter re-adds the publisher deliberately. `.github/workflows/queue_actions.yml` | DROP — it mutates the instance reading queue from `queue-read` issues and needs the repo's labels; `scripts/queue_mark_done.py` ships via rule 1, so an adopter re-adds the processor deliberately. `.github/workflows/queue_filing.yml` | DROP — the claude-action filing workflow needs the instance's Claude OAuth secret, labels and reading queue. As in the Mind table's rule 9d there is **no `.github/**` catch-all**: a new Memory workflow is UNMATCHED and needs an explicit decision. `logo.png` (instance branding) | DROP. The old legacy-family DROP rules (root `*.bib`, PDFs, `CTI/` etc.) are retired — those files are gone from the live repo and PyAutoMemory's structure lint (`make validate-structure`, in CI) prevents their return at the source |

**Fresh-repo invariant (hard rule, rule 9):** no workflow shipped into a
template may **fail unattended** on a freshly-spawned repo. A job that runs on
its own and cannot succeed is not "configuration the new owner will finish" —
it fails on their repo and emails them, forever, for work they never asked for.
That is what produced the published template's 13 failing runs.

Precisely, a shipped workflow must satisfy **both**:

1. **No unattended trigger it cannot satisfy.** No `schedule:`, and nothing
   else that fires without a human, unless it succeeds with no secrets and no
   sibling repos. `lifecycle_drift.yml` keeps its `push:` trigger because it
   genuinely does succeed (rule 9a).
2. **No configured secret.** `secrets.GITHUB_TOKEN` is auto-provided by Actions
   and allowed; anything the org must create is not.

Deliberately **not** required: that every human-invoked path succeeds.
`spawn_drift.yml` ships under rule 9b with its schedule stripped but still
clones `<owner>/*-template`, so a manual `workflow_dispatch` in an org that has
not published templates yet will fail. That is a human asking for it, with the
generated comment explaining why — not an inherited job failing on its own. Do
not "fix" this by asserting no `YOURORG/` reference: that would forbid shipping
the generator machinery at all.

When in doubt DROP. A spawned org that later builds the same organs can copy a
workflow across deliberately; it cannot easily discover why an inherited one
keeps failing.

The implementation must include tests asserting (1) and (2) over every shipped
workflow, and that a NEW `.github` file is UNMATCHED rather than classified by
a catch-all (rule 9d).

**Privacy invariant (hard rule):** no live wiki page, bibliography entry,
reading-queue line, prompt, or registry entry may ever appear in a template
output. The implementation must include a test asserting the generated tree
contains none of a canary list of live-content markers (e.g. known paper
keys, `slacs`, `Nightingale`). The one exception is `scripts/spawn.py` itself,
which *defines* the canary-token list as generator machinery; the scan skips it
so its own definition is not mistaken for leaked instance content.

### Template-family mechanical layers (stamped, not hand-maintained)

Into the already-seeded family repos, spawn stamps (overwriting on re-run,
between `spawn:begin/end` markers where the file is shared with hand
content):

- `autoproject_workspace/config/general.yaml` — the version block shape
  (from the live `autolens_workspace` file, values reset:
  `workspace_version` → the placeholder `0000.0.0.0`).
- `autoproject_workspace/config/build/no_run.yaml` — empty list + usage
  comment. Required: the build's `run.py` raises if a workspace has no
  `no_run.yaml`.
- `.github/workflows/smoke_tests.yml` thin caller (chain =
  `PyAutoProject` only — the template's deps come from PyPI) + starter
  `.github/scripts/smoke_install.sh` + a generic `run_smoke.py` runner +
  `smoke_tests.txt` seeds, into workspace + workspace_test (unblocked by
  3b-2, the reusable smoke workflow; Mind#53).
- `LICENSE` (MIT, from PyAutoBrain's), `CONTRIBUTING.md` (the four-organ
  pointer text with the repo name substituted).

## Substitution table (single source in the implementation)

| Token | Replacement |
|-------|-------------|
| `PyAutoLabs` (owner positions only — GitHub slugs, URLs) | `YOURORG` |
| live satellite repo rows in body-map contexts | the PyAutoProject family |
| version pins (spawned Mind/Memory contexts) | `0000.0.0.0` placeholder |
| the family workspace pin | the family's own release version (`0.1.0` at seed) — it must MATCH the template library's `__version__` |

Never blanket-substitute repo-name strings inside KEEP-verbatim scripts —
`scripts/` reads identity from `repos.yaml` at runtime, which is exactly why
it can be kept verbatim.

## Outputs and publication

- Local: `--write DIR` produces `DIR/PyAutoMind-template/` and
  `DIR/PyAutoMemory-template/` as plain directories with a `SPAWNED_FROM`
  file (source repo + commit).
- Publication (separate, human-triggered step in the wrapping skill):
  push to `PyAutoLabs/PyAutoMind-template` + `PyAutoLabs/PyAutoMemory-template`,
  marked as GitHub **template repositories**. Re-publication is a forced
  content sync (these repos are generated views; history is not
  meaningful) — the ONE sanctioned exception to the never-rewrite-history
  rule, called out explicitly in each template's README ("this repo is
  generated; do not PR it; PR the generator").
- CI: a scheduled job in PyAutoMind runs `--check` against the published
  templates and opens/updates a drift issue on failure.

## Acceptance for the implementation (3b-1)

- Dry-run prints a complete file plan with zero unmatched-WARN entries on
  the current live repos (any WARN at implementation time → extend the
  tables above via a human question, then proceed).
- The canary privacy test passes.
- `--check` round-trips clean immediately after `--write`.
- Running `repos_sync.py --check` **inside a written PyAutoMind-template**
  (against a scratch root holding only organ clones) exits 0 — proving the
  template body map and scripts are self-consistent.
