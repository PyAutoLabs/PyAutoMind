# Campaign decision history on Pulse and Insight

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight, PyAutoPulse
Difficulty: medium
Consequence: glance
Autonomy: safe
Filed: 2026-10-08

## High-level plan

- Add a Decision History disclosure immediately below Profiling Results / Inference Results, with matching navigation and row typography.
- Show a flat newest-first list of named decisions; clicking opens a GitHub Markdown record in a new tab. Do not group by repository, likelihood or dataset.
- Keep each decision in one canonical Markdown page in the campaign-leading organ, with lightweight links from either or both dashboards. Cite authoritative project/Cortex records; do not duplicate scientific ledgers.
- Extend both CHECKIN.md procedures with an explicit natural-language capture trigger ("record this decision"). Capture campaign context, evidence, alternatives, human decision, implications and revisit conditions. A dedicated installed skill is optional later; the existing check-in entry point can handle this now.
- Preserve prior decisions through dated superseding records rather than silently rewriting conclusions. Do not infer a decision from performance results or seed NNLS from an illustrative title.
- Validate links, record/index consistency, escaping, newest-first display, empty state, cross-organ links, browser accessibility and existing dashboard tests.

Tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary.
Witness: both dashboards show one flat Decision History disclosure beneath Results; a cross-domain decision opens one canonical readable GitHub page; no fabricated approved decisions.

## Detailed implementation plan

Each organ: decisions.yaml registry (id, title, date, URL); decisions/README.md documenting record contract and a non-indexed template; <package>/decisions.py loading, validating and rendering a minimal flat list; <package>/board.py HTML and Markdown integration and navigation target; CHECKIN.md capture trigger and procedure; REFERENCE.md ownership/schema; targeted tests plus browser checks; regenerated dashboard artifacts. Reuse Brain's section_layout/heading disclosure and shared theme rather than introducing hidden tabs or CSS forks. Validate GitHub HTTPS URLs and escape labels, reject duplicate ids, retain historical entries. One record may be listed on both boards; records may cite many repositories and datasets with no categorization in navigation.

Record content: title/date; campaign goal and scope; evidence summary with pinned source links and relevant hardware/start conditions; options and tradeoffs; explicit human decision and source; consequences for defaults/SLaM/API or follow-up work; limitations and conditions for revisiting; supersedes/superseded-by links where relevant. Recording the decision does not itself authorize implementation, scientific acceptance or compute. If a user flags that a decision is pending but has not made the choice, prepare a draft and obtain the missing decision rather than publishing it as accepted.

Branch survey: Insight canonical main clean; Pulse canonical feature/pulse-linear-solver-p4a-merged-p5-issued clean. Use isolated feature/decision-history worktrees from latest origin/main, preserving the Pulse checkout. No claims for either organ in Mind active.md at survey. No library dependency. Proposed primary issue: PyAutoInsight. User's earlier autonomous authorization covered completed inference/dashboard phases; this new durable record/capture feature is presented for explicit plan confirmation per start_dev and workspace AGENTS new-scope rule.

## Original request

What both PyAutoPulse and PyAutoInsight need is a "Decision History" tab, which goes under "Profiling Results" / "Inference Results". These campaigns often reach a point where I'm rpesented with a load of evdience, and I make a key design decision about a likelihood function or inference pipeline like what is used in SLaM. When I flag a key decision is being made (maybe this needs a skill?) A high level summary of the whole campaign, the evidence, the decision and its implications should be procued and written to this Decision History tab. For now, when I click the Decision History drop down it should list each decision (e.g. "NNLS Solver Setup"), and then take one to a markdown page or something on GitHub so the decision can be read. Decisions can span multiple repos and dataset types so dont categorize drop down that way.

Routing note: FeatureDecision direct/medium; override keyword-derived library route because both targets are organ dashboard/documentation repos with no published-library API changes. start_workspace → ship_workspace applies. Conflict helper passed for both repos.
