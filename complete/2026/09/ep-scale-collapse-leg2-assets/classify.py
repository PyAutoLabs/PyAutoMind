"""
Classify a results file into the three states that actually occur, rather than
the toy's crude `scatter < 0.4 * truth` split.

  PATHOLOGICAL — near-zero scatter with an error that is tiny RELATIVE to it.
                 This is the #1405 defect and what the shipped leg-1 guard fires
                 on (mean < 0.2 * initial AND std/mean < 0.5).
  BIASED-TIGHT — scatter well below truth with an error bar too small to cover
                 truth (>3 sigma away). Wrong and over-confident, but NOT caught
                 by the guard's mean-fraction gate.
  RECOVER      — truth within ~3 sigma of the reported scatter.
"""
import re
import sys

TRUTH = 10.0
INITIAL = 10.0          # parent scale hyper-prior mean
GUARD_MEAN_FRACTION = 0.2
GUARD_RELATIVE_ERROR = 0.5


def classify(scatter, err):
    guard_fires = (
        scatter < GUARD_MEAN_FRACTION * INITIAL
        and (err / scatter if scatter > 0 else 0.0) < GUARD_RELATIVE_ERROR
    )
    if guard_fires:
        return "PATHOLOGICAL", True
    sigmas = abs(TRUTH - scatter) / err if err > 0 else float("inf")
    if sigmas > 3:
        return "BIASED-TIGHT", False
    return "RECOVER", False


for path in sys.argv[1:]:
    rows = []
    for line in open(path):
        m = re.search(r"seed=(\d+) outcome=(\w+) scatter=([\d.eE+-]+) err=([\d.eE+-]+)", line)
        if m:
            seed, _, scatter, err = int(m.group(1)), m.group(2), float(m.group(3)), float(m.group(4))
            rows.append((seed, scatter, err))
        elif "outcome=CRASH" in line:
            rows.append((int(re.search(r"seed=(\d+)", line).group(1)), None, None))

    tally, guard_count = {}, 0
    print(f"\n=== {path} ({len(rows)} runs) ===")
    for seed, scatter, err in sorted(rows):
        if scatter is None:
            state, fires = "CRASH", False
        else:
            state, fires = classify(scatter, err)
        guard_count += fires
        tally[state] = tally.get(state, 0) + 1
        if scatter is not None:
            sig = abs(TRUTH - scatter) / err if err > 0 else float("inf")
            print(f"  seed {seed:2d}  scatter={scatter:9.4f}  err={err:11.4g}  "
                  f"({sig:8.1f} sigma from truth)  {state}")
        else:
            print(f"  seed {seed:2d}  CRASH")
    print("  ---")
    for state in ("PATHOLOGICAL", "BIASED-TIGHT", "RECOVER", "CRASH"):
        if state in tally:
            print(f"  {state:14s} {tally[state]:2d} / {len(rows)}")
    print(f"  guard fires on {guard_count} / {len(rows)}")
