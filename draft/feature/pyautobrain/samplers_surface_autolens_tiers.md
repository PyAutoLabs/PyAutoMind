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
