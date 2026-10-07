# Right-aligned dashboard Markdown icons

## Original request

Common for "markdown version" text to be a URL next to dashboard items (e.g. on PyAutoMind) can you make this an icon
and to the right of each, so its more outt he way but still clickable.

## Scope

@PyAutoBrain shared board presentation; @PyAutoMind is the reference dashboard.
Replace visible Markdown-version text links with discreet document icons at the right of their section or header row. Preserve destinations, accessible labels, tooltips, keyboard focus and independent disclosure behavior. Implement centrally where possible and validate affected board consumers; regenerate owned dashboard output through its normal renderer.

## Proposed implementation

Inspect shared board/_theme.py section_layout and the owner renderers. Add a reusable source-link presentation, keeping domain destinations owner-defined. Validate desktop/mobile layout, links and disclosure interactions with existing renderer checks and browser inspection. No scientific or task-lifecycle behavior changes.

Tier: undeclared; human merge.
