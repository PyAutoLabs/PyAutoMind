# PyAutoScientist Phase 3 — the template family, the fresh slate, and the Nerves

Research note, 2026-07-10. Companion to `pyautoscientist_generalisation_assessment.md`
(and the issued prompt's Phase 3 section). Prompted by the post-Phase-2
discussion: the maintainer's vision is **more rigid** than the shipped docs'
category contract — a literal `PyAutoProject` / `autoproject_workspace` /
`autoproject_workspace_test` / `autoproject_assistant` family a new scientist
adopts wholesale, with PyAutoConf promoted to the organism's "nervous system".
Constraints unchanged: no duplicated code, no impact on the live setup, and
the live organs stay the single fast-moving upstream adopters tag along with.

## 1. The load-bearing finding: satellite conventions already live outside satellites

The fear behind "rigid template = second thing to maintain" is mostly
unfounded, because the code has already externalised almost every convention
a satellite must follow:

| Convention | Where it actually lives | Satellite carries only |
|------------|------------------------|------------------------|
| scripts → notebooks conversion (docstring-cell format, scratch/ exclusion) | `PyAutoBuild/autobuild/generate.py` + `build_util` | plain `.py` files under `scripts/` |
| Which files ship into notebooks | `config/build/copy_files.yaml` — **workspace-local override already supported** (generate.py prefers it over autobuild's keyed dict) | one small YAML |
| Version pinning + runtime staleness warning | `autoconf/workspace.py` reads `config/general.yaml → version.workspace_version`; Heart's `version_skew.py` reads the same file | one YAML key |
| Navigator/catalogue check | **reusable workflow** `PyAutoBuild/.github/workflows/navigator_check.yml@main` | a 6-line thin caller |
| Docs build check | **reusable workflow** `PyAutoHeart/.github/workflows/docs-build.yml@main` (Phase 2 added the docs-only mode) | a thin caller |
| Release pipeline membership | `pre_build.sh` `run_workspace` row + Heart `config/repos.yaml` row | nothing |
| Config layering (packaged defaults ← workspace override) | the `autoconf` package at runtime | a `config/` directory in the documented shape |

**The one gap:** `smoke_tests.yml` is a fat per-workspace copy (hard-coded
checkout chain of PyAutoConf → … → the library) in every workspace and HowTo —
~10 near-identical files in the live setup. Generalising it into a reusable
workflow parameterised by the dependency chain is a Phase 3 work item that
pays the live setup directly (one definition instead of ten) *and* is the
missing piece that makes an adopter's workspace CI a thin caller too.

**Conclusion:** rigidity should come from **contracts enforced by the
organism** (generate.py, autoconf at runtime, Heart's checks, reusable
workflows `@main`) — not from file-copies inside the template. Then the
template family can be almost embarrassingly thin, and "tag along live" is
automatic: adopters get convention updates through `pip install --upgrade
autoconf` and through reusable workflows resolving `@main`, without ever
pulling template repos again.

## 2. The template family — what each repo actually is

Verdict: **build it.** The assessment §2 said adopters only need the contract
*documented*; the maintainer is right that a working embodiment is worth far
more — provided each repo contains only what must be *theirs*:

- **PyAutoProject** (library template) — the PyAutoGalaxy-to-PyAutoFit
  pattern distilled: a package with `__version__`, an `af.Analysis` subclass,
  a model module, packaged `config/` defaults in the autoconf shape,
  `pyproject.toml` depending on `autoconf` (+ `autofit` for the modelling
  API), `tests/`, thin CI caller. Exemplar science: the canonical **1D
  Gaussian fit** — tiny, domain-neutral, exercises model → analysis → search
  → results end to end.
- **autoproject_workspace** — `scripts/start_here.py` in the docstring-cell
  convention (written to *teach the convention itself*: end-to-end script
  that builds to a notebook), `config/general.yaml` with the version pin,
  `config/build/copy_files.yaml`, thin-caller workflows, `notebooks/`
  generated not committed by hand.
- **autoproject_workspace_test** — one smoke script + `smoke_tests.txt`
  seed, wired for the (generalised) smoke workflow; documents "this is where
  cross-package and integration checks live".
- **autoproject_assistant** — **not hand-built.** This is the Clone/Mitosis
  agent's `lightweight-seed` mode (design already approved, Brain#59,
  `agents/conductors/clone/DESIGN.md` — no CLI yet). The adoption story:
  "when your project matures, run the clone agent in lightweight-seed mode
  against `autolens_assistant` as reference." Gated on implementing the
  clone agent; do not hand-fake it in the template family.

Hand-seeded once; the mechanical layers (workflow callers, config
skeletons) **stamped from the live conventions by the spawn script** (§3) so
they cannot drift. Published as GitHub **template repositories** under
PyAutoLabs ("Use this template" — copy-and-diverge is *correct* for
satellites, unlike organs: their content becomes the adopter's science
immediately, and everything that must track upstream has been moved out).

## 3. The fresh slate: spawn, not reset

The "agent/skill which turns my live setup into a fresh slate" and the
"standalone fresh PyAutoMemory" are the same artifact reached two ways, and
the assessment already blessed the mechanism (§6-E, §8-4): **generated
skeletons, stamped from the live repos by a script — regeneration, not
manual duplication.** Name it **`spawn`** (organism reproduction; the
germline counterpart to the clone agent's assistant-level mitosis).

What spawn produces (all *-template* repos, CI-regenerable):

- **PyAutoMind-template** — folder skeleton (work-type dirs with `.gitkeep`),
  empty `active.md`/`planned.md`/`complete.md`/`ideas.md`, `scripts/`
  verbatim (they are generic — repos_sync, prompt_sync), `REFERENCE.md`
  verbatim, and a `repos.yaml` **pre-filled with the PyAutoProject family**
  so `repos_sync --write` works on first run.
- **PyAutoMemory-template** — the shape only: `index.md` skeleton, one
  example sub-wiki with the schema `CLAUDE.md`, `bibliography/` tooling +
  Makefile verbatim, empty reading queue. (Resolves the "my papers and wiki
  surely need a fresh repo" problem exactly: the structure is MIT and
  generic; the content never leaves the live repo.)

The **partition rules** (structure-vs-content, per file class) are the
judgment-heavy core of spawn — the same seam the clone agent's DESIGN.md
formalises for assistants ("the template seam ... owned by the reference").
Rule sketch, to be settled at implementation: keep = scripts, schema/CLAUDE
files, REFERENCE/AGENTS/LICENSE, Makefiles, folder shape; empty = registries,
queues; drop = prompts, wiki pages, bibliographies (content), issued/;
substitute = repos.yaml → template body map. Spawn is a Brain-planned,
Build-executed generation (mirroring the clone agent's organ split), but the
pragmatic first cut is a script in PyAutoMind/scripts + a skill that runs it
and diff-reports — promote to a conductor only if it earns it.

Spawn also owns stamping the template family's mechanical layers (§2), so
one generator maintains every fresh-slate artifact against the live source
of truth. Drift check: a CI job re-runs spawn and fails on diff — the
repos_sync pattern, again.

## 4. PyAutoConf → PyAutoNerves: promote the role now, defer the rename

PyAutoConf genuinely is the nervous system — the runtime layer connecting
workspace conventions to libraries (layered config with workspace override,
version handshake, test_mode, jax_wrapper, notebook/Colab setup). The
adopter-facing framing "your project gets `autoproject/config/` +
`autoproject_workspace/config/` and the Nerves make them work" is correct
and should be documented as such.

But the literal rename decomposes into three moves with very different costs:

1. **Promote the role** — body map `role:` text, an RTD "Nerves" page beside
   the organ pages, template family wired through it. Zero risk. **Do now.**
2. **Rename the repo** (PyAutoConf → PyAutoNerves, keep package `autoconf`)
   — GitHub redirects help, but the name is hard-coded in every fat
   `smoke_tests.yml` checkout, docs-build.yml's dep chains, Heart config,
   pre_build, repos.yaml + all generated blocks, and the firewall allowlist.
   Doable behind `repos_sync --check`, pointless until the fat workflows are
   generalised (§1) — **defer until after the smoke-workflow work, if still
   wanted.**
3. **Rename the package** (`autoconf` → e.g. `autonerves`) — new PyPI name,
   every import in five libraries, floor pins, conda. **Not worth it**; the
   organism metaphor lives happily at the repo/docs level while `pip install
   autoconf` stays stable for every existing user.

Category stays `library` in the body map (Heart gates it and Build releases
it as one); the docs present it as "the sixth organ, delivered as a package."

## 5. What this does to the live setup (risk ledger)

Pure-additive (zero live risk): template family repos, spawn script +
templates, Nerves docs/role text, RTD adoption-guide updates.
Touches live CI (needs parity care): smoke-workflow generalisation — land the
reusable workflow, convert one workspace, diff the checks, then sweep.
Touches tested organ code (the original Phase 3 §1 extraction — unchanged
scope, still config-surface moves behind test suites): Heart
version_skew/readiness tables, Build maps, Brain constant tables; each
shrinks the tenant-firewall allowlist.
Gated on other work: autoproject_assistant (clone agent implementation);
`repos_sync --write` stamping organ config surfaces (the "only real
engineering", §8-4 — pays for itself but is not urgent for adoption day one).

## 6. Phasing against the Fable deadline (access ends Sunday 2026-07-12)

Judgment-tier work that should happen **before Sunday** (3a):

1. Settle this note (this document) + file the Phase 3 prompt series in Mind
   — **one prompt issued at a time** per the no-bulk-queue rule, but the
   series *written* now while the design is hot.
2. The spawn **partition rules** (the judgment core) written as a spec the
   implementation follows mechanically.
3. The template family's **exemplar prose** — `start_here.py` and the
   PyAutoProject README/model code are teaching material (tutorial-prose
   rule: judgment tier).
4. Decisions locked: Nerves = promote-not-rename (above), assistant =
   clone-gated, templates = generated-not-hand-maintained.

Execution-tier work that can run **after Sunday** on Opus (3b): spawn script
implementation against the spec, template repo creation + stamping CI,
smoke-workflow generalisation + sweep, the §1 config extractions, clone
agent lightweight-seed implementation (it has an approved design to execute
against).

## 7. The adoption story, restated end-to-end

"Fork Brain/Heart/Build. `Use this template` on PyAutoMind-template (your
body map already lists the PyAutoProject family), PyAutoMemory-template,
and the PyAutoProject family. Rename `autoproject` to your science. `pip
install autoconf autofit`. `repos_sync --write`. Write your first prompt.
Your organs pull upstream forever; your Nerves and libraries update by pip;
your CI updates itself through reusable workflows; everything else is
yours." — Rigid where the organism needs contracts, free where the science
lives, and nothing in it hand-maintained twice.
