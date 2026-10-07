# Shared dashboard freshness footer

Type: feature
Target: @PyAutoBrain
Difficulty: large

## Original request

Should all dashboards have a last updated text? Feels like they should and thtat this should be homogenized
and common amongst all. I would put it to the right of the "> Read the prompt" thing on each copyable button under the copy button,
with its text the same across all and it being in green if its within a certain time threshold (under 1 hour?) yellow for another and red for another, with it clickable or an update button next to it, but it should be smaller font that the other stuff in the button

## Approved design

User approved with “go”. Shared footer beside Read the prompt, under controls: Last updated <relative age> and Update. Green under 1 hour; yellow 1–24 hours; red at least 24 hours; grey unavailable. Smaller font, mobile wrapping, exact timestamp accessible on click, browser age advances without resetting source time. Timestamp represents successful displayed-information refresh, separate from scientific evidence age and health. Owner supplies real refresh destination; no fake reload-as-update behavior.

## Scope and validation

Extend Brain shared orchestration_panel/CSS/JS and standard; adopt across the thirteen organ boards (Brain, Mind, Cortex, Ears, Heart, Hands, Memory, Pulse, Insight, Nerves, Gut, Eyes, Scientist). Survey owner timestamps, refresh mechanisms and claims. Preserve domain meanings and actions. Validate boundary and missing timestamps, multiple panels, accessibility, prompt copying and responsive rendering. No merge authorization.
