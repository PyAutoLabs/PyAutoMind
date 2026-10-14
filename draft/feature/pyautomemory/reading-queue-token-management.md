# Simplify reading-queue token management

Target: @PyAutoMemory
Status: deferred by the human; layout-only portion shipped in PyAutoMemory#131.
Related completion: complete/2026/10/compact-memory-board.md

Original remaining request:
> Having to put a github issue up to put something on the to read list is too much time, I want to put like 5
> papers with 1 day left there today but it should be a single click and done, is that possible?

The human directed: "do it, we will sort token stuff in a bit". Token work was explicitly deferred. Existing one-tap mode creates issues through the API using a browser-stored fine-grained token; inspect setup and permission/error handling before proposing changes. Decide separately whether bulk selection is needed. No token-management or batch-selection implementation has shipped.
