Track and fix correctness issues in the HowToLens tutorials as they are found during student use, and use the equivalent HowToGalaxy material as a cross-check so shared explanations do not drift.

Primary target: @HowToLens
Cross-check: @HowToGalaxy
Source-of-truth checks where relevant: @PyAutoGalaxy and @PyAutoArray.

This should be treated as a living documentation task. Add newly reported tutorial errors to the findings below as they crop up, verify them against the implementation and any relevant literature/convention, then fix the canonical source scripts and regenerate/sync notebooks and generated markdown according to each repository's instructions. Where HowToLens and HowToGalaxy contain equivalent material, check both and keep them consistent rather than fixing only one copy.

Current findings
================

1. Grid rotation / position-angle wording
-----------------------------------------

In chapter 1 tutorial 1, the tutorial says the grid is rotated counter-clockwise by the profile angle, but the code does:

```python
theta = np.arctan2(y, x) - np.radians(angle_degrees)
```

The source implementation deliberately rotates coordinates clockwise into the profile reference frame. The *profile position angle* is defined counter-clockwise from the positive x-axis; transforming the grid into that profile frame is the inverse coordinate transformation and is therefore clockwise.

Check and correct the wording in both:

- @HowToLens/scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py
- @HowToGalaxy/scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py

The code convention should remain consistent with @PyAutoGalaxy/autogalaxy/profiles/geometry_profiles.py and @PyAutoArray/autoarray/geometry/geometry_util.py.

2. Elliptical radius applies q to the wrong coordinate
------------------------------------------------------

The tutorial correctly states the elliptical coordinate convention as

```
eta^2 = x_r^2 + y_r^2 / q^2
```

but the Python currently computes:

```python
eta = np.sqrt(
    (grid_rotated[:, 0]) ** 2
    + (grid_rotated[:, 1]) ** 2 / axis_ratio**2
)
```

PyAuto uses (y, x) ordering, so `[:, 0]` is y and `[:, 1]` is x. The correct implementation is therefore:

```python
eta = np.sqrt(
    (grid_rotated[:, 0]) ** 2 / axis_ratio**2
    + (grid_rotated[:, 1]) ** 2
)
```

This matches @PyAutoGalaxy/autogalaxy/profiles/geometry_profiles.py, where `elliptical_radii_grid_from` evaluates `sqrt(x^2 + (y/q)^2)`, and it matches the Keeton (2001) convention in Eq. 5 (astro-ph/0102341), where the ellipse is aligned with the x-axis.

Check and correct this in both HowToLens and HowToGalaxy.

3. Related source docstrings
----------------------------

While validating the tutorial fixes, also check the relevant PyAutoGalaxy geometry docstrings for consistency with the actual implementation. In particular:

- `elliptical_radii_grid_from` documentation appears to omit the square on q even though the code uses `(y/q)^2`.
- Check that all descriptions of axis ratio use the actual convention q = minor / major (b/a), not the inverse.

Do not change working source-code mathematics merely to match stale prose. The implementation and established convention are the source of truth.

Ongoing process
===============

When another HowToLens tutorial issue is reported:

1. Append it to this task with the exact tutorial/file/section.
2. Check the equivalent HowToGalaxy section where one exists.
3. Check PyAutoGalaxy/PyAutoArray implementation for the real convention.
4. Check a literature convention when scientifically relevant.
5. Fix canonical source scripts first, then regenerate/sync notebooks and generated markdown.
6. Add a small regression/check where practical if the error is mathematical rather than purely prose.

Keep this task open until the current student-led pass through HowToLens is complete, then perform one final parity sweep against HowToGalaxy before closing.
