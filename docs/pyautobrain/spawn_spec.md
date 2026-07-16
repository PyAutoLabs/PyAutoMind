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
| 2 | `REFERENCE.md`, `AGENTS.md`, `CLAUDE.md`, `LICENSE`, `CONTRIBUTING.md`, `ROUTING.md`, `.gitignore` | KEEP verbatim |
| 3 | `README.md` | KEEP verbatim (already generic post-Phase-1) |
| 4 | `repos.yaml` | SUBSTITUTE → the **template body map**: the five organ rows kept with `github:` owner replaced by `YOURORG`; all live satellite rows replaced by the PyAutoProject family rows (`PyAutoProject` category `library`, `autoproject_workspace` category `workspace`, `autoproject_workspace_test` category `workspace_test`) + a commented-out `autoproject_assistant` row ("uncomment when the clone agent seeds it") |
| 5 | `active.md`, `planned.md`, `complete.md`, `parked.md`, `condemned.md`, `ideas.md`, `queue.md`, `autonomy_log.md` | EMPTY → header line + schema pointer comment only (e.g. `# Active Tasks` + `<!-- schema: REFERENCE.md -->`); autonomy_log keeps its schema header rows |
| 6 | `draft/**` (the work-type dirs `feature/ bug/ refactor/ docs/ test/ release/ maintenance/ research/ experiment/ triage/` now live under `draft/`) | SKELETON → keep a single `draft/.gitkeep`; drop all draft prompts and their work-type/target subdirs (a fresh Mind starts with an empty `draft/`; intake recreates the work-type subdirs on demand) |
| 6b | `complete/AGENTS.md` | KEEP verbatim (the finished-work archive **schema** is template content; matched before rule 7's `complete/*` DROP) |
| 7 | `active/ complete/ z_features/ z_vault/ autoprompt/` + instance reference docs (`docs/**` now holds only reference material like `spawn_spec.md`) + instance root docs (`dashboard.md`, `overview.md`) + legacy pre-migration prompt dirs (`autolens/`) | DROP (lifecycle records + instance content) |
| 8 | `skills/**`, `policy/**` | KEEP verbatim (`OWNERSHIP.md`, `create_issue/` are generic; `policy/` is org-agnostic safety text) |
| 9 | `.github/**` | KEEP verbatim EXCEPT workflows that reference live secrets/repos beyond the org placeholder — those SUBSTITUTE `PyAutoLabs` → `YOURORG` and keep |
| 10 | `.claude/**`, `.codex/**` | DROP — agent-discovery symlinks are install artifacts recreated by the PyAutoBrain installer, not source content |

### PyAutoMemory → PyAutoMemory-template

| # | Pattern | Action |
|---|---------|--------|
| 1 | `bibliography/*.py`, `bibliography/README.md`, `scripts/`, `tests/`, `Makefile`, `LICENSE`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore` | KEEP verbatim (tooling + schema + policy — scripts/tests are the citation-validation tooling the Makefile drives) |
| 2 | `bibliography/*.bib` and any bibliography data files | EMPTY → file kept with header comment ("populated by your literature") |
| 3 | `wiki/CLAUDE.md` (the shared schema) | KEEP verbatim — since the wiki/ restructure (PyAutoMemory#24) the schema is a single domain-neutral file at `wiki/CLAUDE.md`, kept canary-clean at the source (its examples carry no instance tokens), so spawn no longer maintains a duplicate schema asset |
| 4 | `wiki/*` (all live sub-wikis, all pages) | DROP; generate instead ONE `wiki/example/` containing a slim scope-only `CLAUDE.md` (the schema is inherited from rule 3, not copied), an `index.md` skeleton listing zero sources, and one `sources/EXAMPLE_stub.md` demonstrating the stub format (hand-written once, stored inside spawn as a heredoc/template asset — not copied from live content) |
| 5 | `index.md` | SUBSTITUTE → skeleton: intro line + a table with the single `wiki/example/` row + "add sub-wikis following the same schema" |
| 6 | `reading-queue.md` | EMPTY → header + section-format comment |
| 7 | `README.md` | GENERATE → a template README asset held inside spawn (text surgery on the live README is brittle across edits; the asset keeps `--check` round-trips stable) |
| 8 | `.github/**` | KEEP with owner substitution; `logo.png` (instance branding) | DROP. The old legacy-family DROP rules (root `*.bib`, PDFs, `CTI/` etc.) are retired — those files are gone from the live repo and PyAutoMemory's structure lint (`make validate-structure`, in CI) prevents their return at the source |

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
- `autoproject_workspace/config/build/copy_files.yaml` — empty list + usage
  comment.
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
