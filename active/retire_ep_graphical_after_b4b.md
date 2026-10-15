# `@autofit_workspace_developer` retire `ep/` and `graphical/` via Gut now that B4b re-homed them in autofit_profiling

Type: maintenance
Target: autofit_workspace_developer
Repos:
- autofit_workspace_developer
Difficulty: low
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Epic: search-extensibility
Phase: B4b-followup
Witness: after the PR, `git grep -n "ep/\|graphical/" -- ':!ep' ':!graphical'` in autofit_workspace_developer returns no hit outside the two deleted trees (today the only hits are inside them), the repo's lint/CI leg stays green, and `PyAutoMind/condemned.md` carries one entry `autofit_workspace_developer/ep-graphical-baselines` with the pre-delete SHA, `merged: yes`, and the autofit_profiling re-home locator — exactly the shape of the `searches-minimal-nautilus-profile` entry.
Review-minutes: 5
Unattended: yes
Filed: 2026-10-15
Issued: 2026-10-15

## Request (from the B4b record follow-up, `complete/2026/10/search-ext-b4b-ep-baseline.md`)

"retire the developer `ep/` and `graphical/` scripts via Gut. This is now unblocked; no Mind draft has been filed for it yet." Human launched the batch 2026-10-15: "ok do the next batch of tasks in auto".

## Facts (do not re-derive)

- `autofit_workspace_developer/ep/` and `graphical/` (1.6 MB each: README, `fit.py`, `simulator.py`, `sanity.py`, `util.py`, `config/`, `dataset/`, `profiles/*.pstats`+hotspot txt) are the 1D-Gaussian EP / graphical scale-up baselines from the May 2026 `graphical-ep-scale-up` task (issue Jammy2211/autofit_workspace_developer#16). B4b (autofit_profiling#5, merged 2026-10-15 e63a89127) ported them as `scripts/gaussian_1d_ep/{ep,graphical}/baseline.py` with committed results (9 setups, 31 records) and a campaign page; the developer copies would diverge and mislead.
- Nothing outside the two trees references them (`git grep` 2026-10-15: only self-references and the READMEs' link to `PyAutoPrompt/graphical_ep/*_scoping.md`, a repo that no longer exists in this workspace).
- Precedent: `PyAutoMind/condemned.md` entry `autofit_workspace_developer/searches-minimal-nautilus-profile` (committed deletion in the PR, `archive-ref: n/a`, bytes recoverable from remote history at the pre-delete SHA). Follow that shape; the Gut lifecycle is in `organs/PyAutoGut/AGENTS.md` "Lifecycle: condemn → transit → void".

## Shape

One PR in autofit_workspace_developer: `git rm -r ep graphical`, drop any README/index line that lists them, and point readers at autofit_profiling `scripts/gaussian_1d_ep/` + `wiki/campaigns/` in the top-level README's developer map if one exists. The Mind side (one `condemned.md` entry, pre-delete SHA = the branch's merge-base with main) is written by the main session at ship, in the same style as the A0c and B4a entries. The `searches_minimal/` nautilus leftovers were already retired (record `complete/2026/10/retire-nautilus-leftovers.md`); do not touch `searches_minimal/`.
