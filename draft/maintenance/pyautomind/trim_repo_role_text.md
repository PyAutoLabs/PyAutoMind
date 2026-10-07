# Trim the verbose `role` rows in repos.yaml (root routing table is half the per-delegation load)

Type: maintenance
Target: pyautomind
Repos:
- @PyAutoMind
Difficulty: small
Autonomy: supervised
Consequence: judge
Priority: medium
Status: draft
Filed: 2026-10-07

## Request (verbatim, 2026-10-07)

> do these: Two things for later: the repos.yaml role-text trim (halves the root
> table, the largest per-delegation cost, but regenerates 8 organ map blocks, so
> it wants its own task) [...]

## Why

The workspace-root `AGENTS.md` routing table (generated from `repos.yaml`
`role:` text) is ~7.8 KB of a 14.8 KB file that loads into every session AND
every delegated subagent (~18-22k tokens per delegation measured 2026-10-07).
Six organ rows are paragraphs (Pulse 752 chars, Eyes 670, Insight 483,
Ears 441, Cortex 278, Gut 234) and the four `<lib>_visualization` rows repeat
one sentence. The same `role` text is rendered into the `repos_sync:map` block
of 8 organ AGENTS.md files and the public organ tables
(`PyAutoScientist/README.md`, `.github/profile/README.md`).

## Scope (this repo only)

1. In `repos.yaml`, replace the `role:` text of exactly these rows with the
   wording below (architect-approved; keep it verbatim apart from YAML quoting):

   - **PyAutoPulse**: The Pulse — cross-project profiling dashboard over the `<lib>_profiling` repos: campaign intent, instance registry, the versioned `profiling-summary` read contract, ingest receipts and the Pages board. Validates the contract only; never judges, scores or issues verdicts (the Brain's profiling conductor judges).
   - **PyAutoEyes**: The Eyes — cross-project visualization dashboard over the `<lib>_visualization` repos: their registry, the `gallery/viz_manifest.yaml` read contract and the Pages board linking their PNGs. Renders and copies nothing, never judges figures (the Brain's Eyes conductor does) and never edits plot code.
   - **PyAutoInsight**: Inference campaign intent, the cross-project inference instance registry, the versioned `inference-summary` read contract, ingest receipts and the evidence dashboard. Projects execute, Cortex records the science, Mind owns task state; never infers scientific acceptance or submits compute.
   - **PyAutoEars**: The Ears — community listening: read-only public conversation collection, the versioned community snapshot contract, coverage receipts and the dashboard. GitHub stays authoritative; Brain's Community conductor judges and drafts replies; never posts, labels, files issues or exports transcripts.
   - **PyAutoCortex**: The Cortex — what is true in the science: the body map (`projects.yaml`) and one ledger per science project (runs, results, learnings, where to pick up); the science mirror of the Mind.
   - **PyAutoGut**: Lifecycle of condemned self-material (stale branches, stashes, dead code/tests): held as recoverable git refs through a transit window, voided on a sweep. The storage mirror of Memory.
   - **autolens_visualization**: Rendered PyAutoLens figures — every visualizer output on HST-scale imaging and SMA interferometer data, with the producers and harness; re-rendered each release; aggregated by PyAutoEyes.
   - **autogalaxy_visualization**: Rendered PyAutoGalaxy figures — every visualizer output on HST-scale imaging, SMA interferometer data and ellipse fits, with the producers and harness; re-rendered each release; aggregated by PyAutoEyes.
   - **autofit_visualization**: Rendered PyAutoFit figures — every sampler, model-graph, expectation-propagation and Visualizer output on the gaussian_x1 example, with the producers and harness; re-rendered each release; aggregated by PyAutoEyes.
   - **autocti_visualization**: Rendered PyAutoCTI figures — every Dataset1D and ImagingCI visualizer output on simulated charge-injection data, with the producers and harness; re-rendered each release; aggregated by PyAutoEyes.

   Touch no other row and no other key.
2. Regenerate only what lives in THIS repo from the new text (whatever
   `repos_sync.py --write` owns inside PyAutoMind — check with `--check` which
   Mind-local legs drift; e.g. the routing table copy if Mind holds one). Do not
   run `--write` against the workspace (it spills into 31 canonical checkouts);
   use a scratch bundle or `--check` only.
3. Report the resulting drift list from `--check` on the real workspace: the
   organism-map blocks in the 8 organ AGENTS.md files and the two public
   tables are EXPECTED to drift until the regeneration wave (separate PRs per
   repo, handled by the architect after merge). Keep the leg names unchanged.
4. Tests green (there are repos.yaml schema/lint tests).

## Done when

The root table regenerated from this `repos.yaml` is ≤ 6 KB; no row loses a
routing fact (which repo to open for what, who judges, what the organ never
does); Mind suite green.
