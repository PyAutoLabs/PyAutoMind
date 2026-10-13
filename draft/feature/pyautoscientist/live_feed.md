# Scientist Live Feed
Difficulty: medium
Consequence: judge
Status: blocked
Blocked-by: design discussion and explicit implementation-plan approval

Target: @PyAutoScientist only for first implementation; MyScientist adoption later.

## Original request
next on both PYAuto and My I want to put a new section on the Scientist Dashboard between Projects and Dashboards called Live Feed. This would be a single live feed of all activity, which therefroe updates frequenrly when any work is done. It should say what board it is associate with and as the name suggestions really act as a live feed to know what work is being done. only implement on PYAutoScietist for now and first do some planning and back and forth with me on how we should set it up noting we need to avoid walls of text and information overload

## Discussion draft, not implementation approval
Place Live Feed between Projects and Dashboards. Propose five concise newest-first rows with board label/link, short factual activity text and event time; expand details on demand. Group repeated progress updates for the same task. Include starts, meaningful progress, blockers and completions; exclude routine refreshes and unchanged checks. Propose one-minute foreground refresh with last-checked time, freshness/coverage disclosure and stable reading position.

Existing Scientist REPORTING.md distinguishes owner event timestamps from feed generation times and current status from history. overview.js currently polls state feeds every 60 seconds; these are not universal event streams. Determine which owner records offer durable IDs, timestamps and deep links before promising all-activity coverage. Scientist can aggregate existing published evidence first; any missing producer event contracts require separately agreed scope, not hidden cross-organ changes. Do not manufacture history from snapshot refresh timestamps. Preserve private-source boundaries on public Pages.

Open choices: default activity granularity, five versus more visible rows, grouping and history depth, refresh latency and behavior on new entries, and honest first-version coverage. No source changes, deployment, collectors or recurring workflows authorized in this planning conversation. Route agreed design through start-dev branch survey and setup before implementation.
