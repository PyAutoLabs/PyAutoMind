# JAX 0.12.1 breaks step-0 structured triangle containment (bit-identity vs gather fails)

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- jax
- triangles
- point-source
- release-blocker
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: on jax 0.12.1, `pytest test_autoarray/structures/triangles/test_coordinate_jax.py -k step0_route_is_bit_identical` passes (or jax 0.12.1 is excluded from the pin with a recorded reason), and the PyAutoHands release.yml TestPyPI test step passes for PyAutoArray.
Lane: any

Found 2026-11-19 by the release session (/release, stopped at vitals). The PyAutoHands `release.yml` TestPyPI test step
(run 44501247836, 2026-11-19T09:58Z) failed on PyAutoArray: 5 of 2473 tests failed, all
`test_autoarray/structures/triangles/test_coordinate_jax.py::test__step0_route_is_bit_identical_to_gather[...-structured]`
(cases solver, solver_deflected, alternating, alternating_padded, even_rows). The structured route's containment differs
from the gather route at 83–836 points per case, e.g. "structured on solver: 83 of 15443 points differ from gather,
first at [-6.75 9.8726896]".

Cause (strongly indicated): the JAX version, not a code change. Yesterday's run 44279589911 passed on the same PyAutoArray
main (5815019d) with jax/jaxlib 0.12.0.1; today's installed jax/jaxlib 0.12.1 (PyPI 2026-11-18T13:57Z). The test and the
triangles code are unchanged since 2026-09-27 (#579 step-0 routes; 462ad094 MAX_CONTAINING_SIZE 15->20). Library CI on
main last ran before 0.12.1 existed, so it still shows green.

Impact: the pin `jax>=0.12,<0.13` admits 0.12.1, so fresh installs of the released 2026.11.13.1 are also affected
(point-source containment on the structured step-0 route may be wrong). It blocks the pending library release (18
pending-release PRs across Fit/Galaxy/Array/Lens): a rehearsal would fail the same way.

Fix options: (1) exclude jax 0.12.1 in the pin (`!=0.12.1` or `<0.12.1`) — fast and protects current users; needs the
DNA/Nerves version-policy view (memory: jax-version-policy, pin jax>=0.12,<0.13 shipped 2026.11.12.1); (2) reproduce
locally on 0.12.1, find which op changed (likely a sort/searchsorted/float rounding or scatter semantics change in the
structured route) and fix it so the route is bit-identical on both versions. Prefer (2) if small; else (1) now and (2)
as a follow-up.
