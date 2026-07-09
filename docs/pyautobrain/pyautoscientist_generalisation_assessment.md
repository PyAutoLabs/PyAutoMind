# PyAutoScientist generalisation — feasibility assessment

Companion scoping note for `pyautoscientist_generalisation.md` (the intake
prompt). Research only — no changes made. Assessed 2026-07-09 against the live
checkouts.

**Verdict: feasible, moderate effort, and it does not require splitting off
from the repos in daily use.** The architecture has already done the hard part:
domain facts live in declarative tables and policy files, not in algorithms,
and the framework/instance boundary happens to align with existing repo
boundaries. The recommended model is *docs-first reference implementation*,
with the live lensing stack kept as the worked example rather than purged.

**Revised after the adversarial pass in §7:** there is exactly **one live
organism — the current one**. The generic offering is (a) docs and (b) a
demand-gated *generated* skeleton, never a second running system and never
the live organs made multi-tenant. All behaviour-touching work is deferred
until a concrete adopter exists; the phases in §6 are ordered by risk to the
live setup, not by logical appeal.

## 1. Where the domain coupling actually lives (audit)

Raw counts of lensing/astronomy references: Heart ~230, Build ~105, Brain
~100, Mind ~5, Memory ~everything (by design). But the *kind* of reference is
what matters, and it is remarkably uniform — module-level constant tables and
config rows, almost never logic:

- **PyAutoMind** — already nearly domain-clean. `repos.yaml` (the body map) is
  the single source of repo identity; `scripts/` are generic; the work-type
  taxonomy is generic. The *content* (prompts, `active.md`, `complete.md`) is
  inherently instance data.
- **PyAutoBrain** — reasoning, conductor/faculty architecture, `AUTONOMY.md`
  (0 domain hits) and `ORGANISM.md` are fully generic. Coupling is confined to
  constant tables: `agents/faculties/sizing/_sizing.py` (LIBRARY/WORKSPACE
  repo sets, REPO_ALIASES, MEMORY_WIKIS science vocabulary), intake's
  TARGET_SIGNALS, feature's repo→wiki map, refactor's repo→test-dir map,
  release's LIBRARIES tuple and `nightly.sh` TAG_REPO — plus lensing examples
  woven through the skills prose.
- **PyAutoHeart** — heaviest count but cleanest seam: `config/repos.yaml` is
  already an explicit *policy* file (what to poll/gate) checked for drift
  against the body map. Remaining hardcodes: `version_skew.py`'s
  workspace→(library, package) map, `readiness.py`'s DEFAULT_LIBRARIES tuple,
  and `url_check_live.py`'s bespoke URL-fixup rules (instance "immune
  memory" — pure config for an adopter).
- **PyAutoBuild** — a declarative `run_workspace <repo> <package> <flags>
  <library>` table in `pre_build.sh` plus small maps in `autobuild/*.py`
  (`run_all.py`, `slow_skip_check.py`, navigator scripts).
- **PyAutoMemory** — content is 100% domain *by design*; the generic asset is
  the shape (sub-wikis, bibliographies, `index.md`, reading queue). The
  coupling point to the rest of the organism is Brain's MEMORY_WIKIS keyword
  map.

Portability is already decent: `bin/install.sh` and `agents/_common.sh`
resolve the workspace root relative to the checkout (one `~/Code/PyAutoLabs`
fallback); `repos_sync.py --check` already enforces identity/policy agreement.
Generalisation is largely *finishing a migration the design already started*:
move the remaining constant tables into per-organ policy files keyed off the
body map's categories.

## 2. The satellite pattern is already abstracted

`repos.yaml` categories — organ / library / workspace / workspace_test /
workspace_developer / howto / assistant / pipeline / project / admin — *are*
the generalised PyAutoProject pattern. An adopter does not need literal
`PyAutoProject` / `autoproject_workspace` stub repos; they need the **category
contract** documented: what each satellite kind is for, and what the organism
expects of it (Heart's version_skew expects workspace→(library, package);
pre_build expects a `run_workspace` row; Brain sizing expects the repo in the
right set). Document the contract first; an optional cookiecutter that stamps
out a library+workspace+howto skeleton can come later if demand appears.

## 3. Open-sourcing without splitting: framework vs instance

The split that matters is framework vs instance, and it already falls on repo
boundaries:

- **Framework organs (Brain, Heart, Build)** — code + skills, already public.
  In principle reusable; **but see §7** — they carry committed instance
  policy/state today, so "others use these same repos directly" is not honest
  without relocation surgery. The corrected model: others *copy from* these
  repos (via docs and a generated skeleton); only Jammy's instance runs them
  live.
- **Instance organs (Mind, Memory)** — these are Jammy's committed state and
  science; an adopter must not fork the backlog. Ship *skeletons*: either a
  `template/` directory inside each repo, or two tiny generated
  `*-template` repos stamped from the structure. Either way the daily-use
  repos are untouched — this is publishing a mould, not splitting the clay.

All five organs are already public on GitHub, but **four of five have no
LICENSE** (only PyAutoBuild does) — legally all-rights-reserved. Adding
licenses (and deciding one for Memory's *content* vs its *structure*) is a
prerequisite for any adoption story.

## 4. Docs: one ReadTheDocs, "PyAutoScientist"

- **Home**: per the ORGANISM.md growth rule (no new organs by default), start
  the docs source as `PyAutoBrain/docs/` — Brain already owns the canonical
  organism prose (`ORGANISM.md`) — published to RTD under the
  `pyautoscientist` project name. Split into a dedicated docs repo only if it
  outgrows that.
- **Content**: (1) concepts — the organism, organs, call chain,
  conductors/faculties, growth rule; (2) adoption guide — "bring your own
  body": write your `repos.yaml`, per-organ policy, Mind/Memory skeletons;
  (3) per-organ reference; (4) the category contract from §2; (5) the worked
  example — the live lensing instance. **Do not purge lensing from the
  docs**: a generic framework documented against a real, running,
  battle-tested instance is far more credible than a sanitised one. Label it
  as the example.
- **READMEs**: shrink every organ README to ~20–40 human-written lines — what
  it is, one table or diagram, link to the RTD. This directly fixes the
  "long AI-written README" problem, and ORGANISM.md stays the single canonical
  organs page.
- **pyautolabs.github.io** gains one card linking the PyAutoScientist docs;
  per-project library docs stay on their existing RTD (matches the hub's
  stated design).

## 5. Honest caveats

- **The real adoption cost is not the lensing coupling** — it's the stack
  assumptions: Claude Code (`~/.claude` skills/commands/hooks), `gh` CLI,
  single-maintainer trunk-based flow, worktree layout, GitHub Actions + PyPI
  releases. Position the offering as an *opinionated reference implementation
  of an agentic dev organism*, not a turnkey framework, and state the
  prerequisites up front.
- **Maintenance drag**: generic docs and templates must track a fast-moving
  personal system. Mitigate by extending the existing `repos_sync.py` drift
  pattern to docs, and by keeping the worked example = the live system (no
  second thing to maintain).
- **Audience**: solo/small-team maintainers of multi-repo scientific Python
  stacks using agentic tooling — niche but real, and the docs double as the
  best available marketing for the PyAuto stack itself.

## 6. Suggested phasing (for start_dev to split) — risk-ordered per §7

Zero-risk to the live setup (do first; touch no agent-read files, no code):

- **A — licenses + README rewrites**: pick licenses, shrink the five
  READMEs. READMEs are human-facing only — agents load `AGENTS.md`/skills,
  not READMEs — so this cannot regress behaviour. `AGENTS.md` files and
  skill bodies are explicitly **out of scope**.
- **B — PyAutoScientist RTD**: `PyAutoBrain/docs/`, concepts + adoption guide
  + category contract + worked example. All **new** prose; it documents the
  skills, it never rewrites them.
- **C — hub card + CONTRIBUTING** with an explicit stability disclaimer:
  the organs are a living reference implementation, main moves fast, no
  compatibility promises — copy, don't track.

Demand-gated (only when a concrete adopter exists):

- **D — config extraction** (touches tested code paths in Heart/Build/Brain
  for zero personal benefit until someone needs it): Heart
  version_skew/readiness/URL rules → `config/`; Build tables → policy YAML;
  Brain constant tables → derived from `repos.yaml` where identity, policy
  file where vocabulary. One PR per organ, behind its test suite.
- **E — generated skeleton**: a `pyautoscientist-template` stamped from the
  live repos by a script (the `repos_sync.py` pattern: single source,
  generated view, drift-checked). Regeneration, not manual duplication.

Never:

- Making the live organs multi-tenant (serving Jammy and strangers from one
  deployment/config surface).
- Stability guarantees on organ `main` branches.
- Genericisation passes over `skills/*.md` — those files are the production
  prompts symlinked into `~/.claude`.

## 7. Adversarial pass: protecting the live setup (added 2026-07-09)

A second, deliberately hostile look at the §3 claim that others could "use
these very repos". Three findings kill the naive version of that idea:

1. **The framework organs carry committed instance matter.** Heart's
   `config/repos.yaml` is Jammy's polling/gating policy; Build has
   `test_results/` (committed autolens run outputs) and `to_do_list/`;
   Brain's skills prose references Jammy-specific workflow in 15+ files
   (`admin_jammy`, worktree layout, GitHub handles). Anyone cloning the
   organs today clones the instance. Making these repos genuinely
   multi-tenant means relocating policy and state out of them — invasive
   surgery on tested, working code, with zero benefit to the live setup.

2. **The organs are hot.** Last 90 days: Brain 75 commits, Heart 71, Build
   138, Mind 838. This is living personal infrastructure, not a stable
   library. Offering the live repos as "the framework" creates an implied
   stability contract: either Jammy slows down (direct damage to the setup's
   main virtue — the freedom to churn tooling daily), or external users
   tracking `main` break constantly (dead-project optics, support burden).

3. **The skills are production prompts.** `skills/*.md` bodies are symlinked
   into `~/.claude/commands/` — they *are* the agents' behaviour, and the
   prose is battle-tested. A "genericisation pass" over them is editing
   production prompts to please hypothetical readers; the regression risk
   lands entirely on the working setup.

**Answer to "will I have two PyAutoBrains and double the repos?" — No,
provided the model is corrected as follows.** There is exactly one live
PyAutoBrain (and Heart, Build, Mind, Memory): the current ones, unchanged.
The generic offering is not a running system; it is:

- **Docs** (the PyAutoScientist RTD) describing the architecture with the
  live organism as the labelled worked example — new prose, zero behaviour
  surface; and
- **later, only if demand appears**, a *generated* skeleton repo stamped
  from the live repos by a script — the `repos_sync.py` single-source →
  generated-view pattern already in use. Updating the generic version is
  re-running the generator, not maintaining a parallel organism. If someone
  forks the skeleton and diverges, that divergence is theirs; improvements
  come back as ordinary PRs to take or leave.

The double-maintenance trap only springs if the generic thing is
hand-maintained or the live organs become dual-purpose. Both are listed as
"Never" in §6. The honest costs that do remain: writing and keeping the RTD
truthful (docs drift is real; mitigate with drift checks and by keeping the
worked example = the live system), and the social cost of visitors filing
issues against a fast-moving personal system (mitigate with the
CONTRIBUTING disclaimer).

## 8. The real ambition: adopters run their OWN organisms (added 2026-07-09)

Clarified intent: PyAutoScientist is not "docs people crib from" — it is the
**basis for someone else's AI dev workflow**, driving projects completely
independent of PyAutoFit/PyAutoLens. That kills the §7 stamped-skeleton model
for the organs: a stamped copy has no upgrade path, so every adopter becomes
an orphaned fork. The model that serves this ambition without creating a
second PyAutoBrain is the **config-diff fork**:

- **One upstream: the live organs.** Adopters fork Brain/Heart/Build and edit
  *only the declared config surfaces* — Heart's `config/repos.yaml`,
  pre_build's `run_workspace` table, Brain's constant tables — plus their own
  Mind (from a skeleton) holding their own `repos.yaml` body map with their
  own libraries/workspaces/categories. Because their diff is confined to
  config, `git pull` from upstream stays clean: they get every improvement
  Jammy ships, Jammy maintains exactly what he maintains today.
- **The mechanism already exists.** Nothing reads the body map at runtime;
  the organism works by *hand-maintained mirrors + drift checks*
  (`repos_sync.py --check` already knows every config surface:
  `check_heart`, `check_pre_build`, `check_labels`, `check_origins`) and by
  *generated prose blocks* (`repos_sync:begin/end` markers in AGENTS.md and
  WORKFLOW.md). An adopter edits their body map, runs `repos_sync --write`,
  and their fork's routing tables and doc blocks regenerate from *their*
  repos — the generation pattern is the parameterisation mechanism, already
  battle-tested in-repo.
- **Domain independence is confirmed** by the §1 audit: organ logic is
  domain-free; everything lensing-specific sits in the config surfaces the
  adopter replaces. Memory's generic asset is its shape; the MEMORY_WIKIS
  keyword map is adopter config like everything else.

What upstream must do to enable this (all self-beneficial or cheap):

1. **Evacuate run-state from the organs**: gitignore Build's
   `test_results/` and `to_do_list/` (repo hygiene Jammy benefits from
   anyway; committed run outputs would collide with any fork's own runs).
2. **The tenant firewall**: extend `repos_sync.py --check` with a check that
   no instance fact (repo name, owner, path) appears in organ code outside
   the declared config surfaces. This keeps future changes from silently
   breaking the clean-pull property — and doubles as drift hygiene for the
   live system.
3. **Docs** (§4 unchanged) plus an adoption guide written against the fork
   model: fork, replace config surfaces, `repos_sync --write`, go.
4. **Demand-gated, later**: teach `repos_sync --write` to *stamp* the organ
   config surfaces from the body map + per-repo policy fields (it already
   stamps doc blocks). That turns "edit five mirrors" into "edit one file,
   regenerate" — for adopters and for Jammy alike. This is the only real
   engineering in the whole plan, and it removes his own hand-mirroring
   burden, so it pays for itself even with zero adopters.

**Still one PyAutoBrain.** Upstream is the live repo; N downstream forks are
owned by their adopters; divergence is confined by design to config. The §6
"Never" list gains a sharper phrasing: never one *shared deployment* serving
multiple humans — but N private deployments of the same code is exactly how
this should work. Residual honest costs: upstream-maintainer social load
(issues/PRs from strangers — pace set by the CONTRIBUTING disclaimer), and
the hard prerequisites (Claude Code, `gh`, worktree layout) which the docs
must state up front rather than apologise for.
