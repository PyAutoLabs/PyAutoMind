# Do the Nautilus costs measured on toy fits transfer to representative fits?

Type: research
Target: autofit_profiling
Consequence: judge

## Original request

> I approve of all this, would it be a fair statement to say at the moment we are doing a lot of profiling and getting run times but not getting many great leads for speed up?

> ok continue

## Approved investigation

Check existing PyAutoFit and lensing results for neural-training and bound-geometry costs. Recover the timing denominator, hardware, repeats and measurement method. Where a record contains only a likelihood estimate or total time, state which costs can be identified. Identify one CPU speedup lead and record the decision in the parent epic. Use archived data and existing domain-owned tasks.
