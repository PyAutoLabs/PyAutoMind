# Remove PyAutoPulse Compatibility Names

## Original Request

We renamed PyAutoPulse to PyAutoHeart, but the folder still has PyAutoPulse and there is PyautoHeart/autopulse, is it safe to remove these pulse things and if so do it

## Notes

- Remove the old top-level `PyAutoPulse` symlink if it is only an alias to `PyAutoHeart`.
- Remove tracked `pulse` / `pyautopulse` compatibility wrappers from `PyAutoHeart`.
- Update packaging and tests to use canonical `heart` / `pyautoheart` paths only.
