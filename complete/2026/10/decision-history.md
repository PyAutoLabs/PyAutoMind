# decision-history

Completed: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/21
PR: https://github.com/PyAutoLabs/PyAutoInsight/pull/22
PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/39

Added Decision History directly below Results on both dashboards, as one flat newest-first list opening canonical GitHub Markdown records in a new tab. Cross-repository/dataset decisions are not categorized; both boards may link one canonical page. Indexes intentionally start empty: NNLS was an illustrative title, not an approved scientific decision.

CHECKIN.md recognizes explicit decision flags and “record this decision”. The record template captures campaign context, pinned evidence, alternatives, the human's actual choice, implications and revisit conditions. A pending choice remains a draft; superseding choices preserve previous records. Scientific source ledgers stay authoritative. Capture grants no scientific acceptance, compute or implementation authority.

Validated index schema/IDs/date/URLs and locally owned title/date/record existence, escaped HTML/Markdown, chronological ordering, malformed/stale CLI checks, regeneration roundtrip, decision-only refresh paths. Root full183 Insight/206 Pulse tests and both real Chromium suites passed. Independent CLEAN review verified cross-organ/new-tab/native disclosure/mobile behavior and human boundaries; its three findings were fixed. Both actual captured boards passed empty-state/navigation/desktop-mobile witness. Ruff/format/offline/diff checks pass. Heart STALE only: `release validation incomplete: no rehearsal for current source`.

Approved glance plan with merge-on-green and witness. No library dependency or scientific data changes. Deployment and merge receipts recorded below.

Exact-head PR checks: Insight0363a96 lint37760585984/job113255741706 and refresh37760586053/job113255742336; Pulse8159703 lint37760587153/job113255745668 and refresh37760587150/job113255750134. All jobs passed with CLEAN/MERGEABLE status and no skipped test steps. Merged Insight3ee88d610456a18882f0adba939b71c2eb4d0d81; Pulse7d94cf5a2eb70e6fd1cad55cd2565013b2dd2b0d. Every claimed branch is an ancestor of origin/main.

Revert from the respective repos: `git revert -m 1 3ee88d610456a18882f0adba939b71c2eb4d0d81` (Insight); `git revert -m 1 7d94cf5a2eb70e6fd1cad55cd2565013b2dd2b0d` (Pulse).

Final publication: Insight lint37760842886/refresh37760842888 and Pages37760873845 passed at c1abbf48d1ce3414529ff87f6a55362fba70dfed; Pulse lint37760862345/refresh37760862479 and Pages37760897071 passed at fe56107abfaa37329ac9e5741a23ffcba846a161. Initial Pages runs were superseded by these successful refreshed deployments. Live Chromium verified both native disclosures, navigation links, empty state and 1440/390px layouts. Issue closed; active claim released; Mind dashboard regenerated and checked; glance shadow row10/20 appended. Preview/live screenshots retained under Mind tmp/decision-history. Existing Pulse canonical feature checkout preserved.

## Original prompt

# Campaign decision history on Pulse and Insight

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight, PyAutoPulse
Difficulty: medium
Consequence: glance
Autonomy: safe
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/21

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

Approval: user “ok great go” approves the plan and green merge/deployment.
