## samplers-surface-autolens-tiers
- issue: (none — shipped directly from the draft prompt in a single session; no tracking issue was opened)
- completed: 2026-08-10 (both PRs merged 2026-08-10)
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/216 (squash-MERGED as 31b810e; pytest 3.12 + 3.13 green)
- mind-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/174 (squash-MERGED as 485d1161)
- prompt: draft/feature/pyautobrain/samplers_surface_autolens_tiers.md (folded below)
- summary: the samplers faculty's SamplerSurface now scans the findings
  maturation lane's experiment tier (autolens_workspace_developer/searches_minimal
  — 37 probes + 8 `*_findings.md` docs as `name — first heading`) and mature tier
  (autolens_profiling — 34 sampler/dataset_class/model_type cells), closing the
  "Surface gap, filed" note the faculty carried in its own AGENTS.md. Both
  surfaces are present-if-checked-out and read-only, matching the three that
  already existed; resolution is `PYAUTO_LENS_DEVELOPER` / `PYAUTO_PROFILING`.
- KEY FINDING (the reason this is not a five-line glob): **a mature-tier cell's
  identity must be read from its leaf's `run_search(...)` declaration, not from
  its path.** The two genuinely disagree on the live tree — all six
  `scripts/cluster/searches/*/mge.py` leaves declare `dataset_class="group"`
  while every sibling in the same tree declares `"cluster"`. Path parsing would
  mislabel six cells and collide them with real ones. Implemented with stdlib
  `ast` (the module is stdlib-only by contract), with a path-shape fallback so a
  leaf with no parsable declaration degrades instead of vanishing. Pinned by a
  test whose fixture leaf's declared class disagrees with its directory, so a
  future refactor cannot quietly regress to path parsing.
- NOT a bug (checked before reporting one): `group` is a legitimate dataset class
  even though `_runner._DEFAULT_INSTRUMENTS` has no `"group"` key — all six such
  leaves pass an explicit `default_instrument="hst"`, so the missing key never
  fires.
- TRAP, cost ~nothing because it was found while planning rather than at PR time:
  the change is **two repos, not one**. The prompt's `Repos:` header said
  PyAutoBrain only, but naming either autolens repo in `_samplers.py` /
  `samplers.sh` trips the tenant firewall — `PyAutoMind/scripts/repos_sync.py`'s
  `FIREWALL_ALLOWLIST` pins both files to their then-current three tokens, and a
  NEW instance fact in an ALREADY-allowlisted file is drift. Proven rather than
  assumed: the check was run before the edit and flagged exactly those two files.
  Both allowlist entries GREW (rather than new entries being added), which is the
  form the surrounding comment permits — "a new entry means a new file an
  adopting fork must rewrite".
- firewall corollary worth remembering: `PyAutoBrain/tests/` **is** inside the
  firewall scan and its files are allowlisted individually. The new
  `tests/test_samplers_surface.py` therefore takes its tier labels and surface
  names from module constants (`_samplers.SURFACE_PROFILING`, `TIER_LENS_MATURE`,
  …) instead of spelling repo names, and needs no allowlist entry at all. Same
  trick as `test_eyes_conductor.py`'s invented domain names.
- scope held (both deliberate, both recorded so they are not re-litigated):
  (1) `_MULTI_START_*_BY_CELL` is NOT surfaced — the prompt names it as a way in,
  but it holds per-cell *tuning knobs* (n_starts / n_steps / batch_size), not cell
  identity, and covers only 4 of the 34 cells; (2) no autolens benchmark table —
  `searches_minimal/output/comparison.txt` exists and `benchmarks()` would read it
  verbatim, but `d["benchmarks"]` is single-valued and re-keying it is a schema
  break for no asked-for value. Worth a follow-up prompt.
- no new judgment: `gaps` stays keyed on the autofit promotion tiers, so the lane
  tiers are inventory only — asserted by a test.
- evidence: live digest against the real trees gives 37 probes / 8 findings /
  34 cells with `gaps` unchanged; exit 4 (not a traceback) with no checkouts
  present; 6 new hermetic tests pass; full Brain suite 279 passed. The two
  `tests/test_skill_install.py` failures seen locally were environment-only —
  they did NOT occur in GitHub CI, confirmed against a stashed clean tree.
- STILL OPEN, pre-existing, NOT fixed here: `repos_sync.py --check` reports
  `PyAutoBrain/tests/test_worktree_conflict_guard.py` naming 7 repos with no
  allowlist entry, from PyAutoBrain 13d222c (#215). Left alone deliberately —
  closing it means adding a NEW FILE entry, the consequential form the code warns
  against, and that call belongs with that test's author. The deeper point: this
  check is wired into NO CI workflow in any repo (it needs all sibling
  checkouts), which is how the drift survived a merge.
- ranker finding, filed separately: the Brain Feature Agent's `select` mode
  ranked `draft/feature/autonomy/10_scheduled_runs.md` first — a prompt carrying
  `Status: blocked`, `Priority: low` and an explicit `Blocked-by:`. It reads none
  of those header keys and derives difficulty from prose length rather than the
  declared `Difficulty:`. See draft/bug/pyautobrain/feature_ranker_ignores_header_keys.md.

## Original prompt

# SamplerSurface: scan the autolens-side findings-lane tiers

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft

The samplers faculty's SamplerSurface
(`agents/faculties/samplers/_samplers.py`) scans only the autofit-side tiers
(autofit_workspace_developer/searches_minimal, the archive,
autofit_workspace_test integration scripts, PyAutoFit promoted searches).
The **findings maturation lane** documented in the faculty AGENTS.md
("Judgment: the maturation lane", added 2026-07-28 from the wsdev#117
campaign) is invisible to it:

- experiment tier: `autolens_workspace_developer/searches_minimal/` —
  surface the `*_findings.md` docs (name + first heading) and the runnable
  probes.
- mature tier: `autolens_profiling/scripts/<dataset>/searches/<sampler>/` —
  surface the (sampler × dataset × model_type) cell matrix (the searches
  framework's `_MULTI_START_*_BY_CELL` keys and `run_search` call args make
  this greppable).

PyAutoMind is in scope because naming either repo in `_samplers.py` /
`samplers.sh` trips the tenant firewall: `scripts/repos_sync.py`'s
`FIREWALL_ALLOWLIST` pins both files to their current three tokens, and a *new*
instance fact in an allowlisted file is drift. The two entries must grow with
the change.

Add both as surfaces (present-if-checkout-exists, like the existing ones),
so a conductor consulting the faculty sees where a search × likelihood
combination sits in the lane — experimented / matured / user-documented —
instead of only the autofit-side sampler tiers. Keep it read-only; no new
judgment logic. Update the faculty AGENTS.md "Surface gap, filed" note to
point at this prompt.
