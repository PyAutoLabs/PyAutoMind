# Publish Scientist board navigation

Type: maintenance
Epic: scientist-adoption-pilot
Consequence: judge

Follow-up to complete/2026/10/scientist-board-navigation.md. Source implementation is merged in seven repos; do not reimplement it. The original request was: “Next, quick polish put the list of all organs at the bottom of Scientist and make sure Scientist is first in all the other boards”. The subsequent `$prm` authorized merge and close-out; cross-board publication/live verification remains.

Inspect successful post-merge deployments first, then use owning workflows as needed. Brain brain_board.yml; Mind/Cortex dashboard_refresh.yml then pages_dashboard.yml; Memory knowledge_board.yml; Eyes/Pulse/Insight pages_dashboard.yml (tracked HTML already regenerated); Ears/Broca/DNA pages.yml; Heart heart-health.yml; Hands release_board.yml; Nerves nerves_board.yml; Gut gut_board.yml; Scientist organism_board.yml. Keep original evidence timestamps; do not run science or package releases. Verify live ul.boards first link Scientist on other14 boards, all14 organ links below Scientist dashboard cards. Record workflow URLs and live checks; close this follow-up after publication verification.

## Resource dropdown publication

Also verify merged Heart#295, Broca#7 and Scientist#66 from `complete/2026/10/organ-resource-dropdowns.md`: publish Heart/Broca destinations before Scientist deep links, then check all four test-workspace and 18 communication-resource anchors on live pages. Source merges do not prove publication.

## Latest Heart publication diagnosis — 2026-10-11

Public Heart HTML lacks test-workspaces/resource-lens-tests. Latest successful heart-health run38134638064 at source1f94d00 predates merged Heart#295. Scheduled/manual-only workflow does not publish on this source merge. Build deploy dry-run aborts with `Could not obtain a readiness verdict ('stale').` despite authoritative readiness having only `release validation incomplete: no rehearsal for current source`. No dispatch or override attempted. Resolve the supported board-publication route before claiming Heart is live; do not run a software release to refresh HTML. Evidence: tmp/broca-resource-categories/build.json.

Also verify the merged polish from `complete/2026/10/broca-resource-categories.md`: Broca#9 category dropdowns and assistant links; Hands#309 shortcut removal; Insight#26 nested PyAutoFit results; DNA#3 concise HTML. Existing automatic publication may cover some boards; inspect successful post-merge deployments before dispatching.
