# `sub_slim_indexes_for_pix_index` appends -1 row padding to the last pixel's list

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft

Found 2026-10-15 by the code survey for PyAutoArray#629 (unverified — confirm first).
`Mapper.sub_slim_indexes_for_pix_index` (`autoarray/inversion/mappers/abstract.py:222-229`)
iterates every column of `pix_indexes_for_sub_slim_index` instead of the first
`pix_sizes_for_sub_slim_index[i]` entries. Padded slots hold `-1`, and Python's negative
indexing would append those sub-pixels to the LAST source pixel's list. Affects any mesh with
padded rows: DelaunayNN (rows padded to 32), and Delaunay rows with an outside-mesh size-1
fallback. Check callers (what consumes this mapping — plotting/visualisation, mapper
diagnostics?), write a failing test, fix by honouring `pix_sizes`.
