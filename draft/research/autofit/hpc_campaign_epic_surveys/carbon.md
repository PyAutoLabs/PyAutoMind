# Energy and CO2e for PyAuto HPC campaigns: methods, inputs, worked estimate

*Research note, 2026-09-27. No repository files edited. Items marked **[UNVERIFIED]** still need a primary source or a site confirmation.*

## 1. Tools: which measure and which estimate

**Green Algorithms (GA), Lannelongue, Grealey & Inouye 2021, *Adv. Sci.*: estimation.** The formula below is copied from the paper text (arXiv 2007.07610, eqs. 1 & 4):

`E [kWh] = t × (n_c × P_c × u_c + n_m × P_m) × PUE × 0.001`, and `C [gCO2e] = E × CI`

- `t` is runtime in hours. `n_c` is the number of cores. `P_c` is TDP per core. `u_c` is the core usage factor, between 0 and 1; when it is unknown the paper assumes 1. `n_m` is **memory available (allocated)** in GB, not memory used. `P_m` is 0.3725 W/GB.
- The paper says memory power "is mainly affected by the total memory allocated, not by the actual size of the database used." So over-reserving memory costs energy in this model.
- Defaults: PUE is 1.67 (the 2019 global average; the calculator uses 1 for laptops) and CI is 475 gCO2e/kWh (world average). Equivalence factors: a tree-month is 917 g, a car 175 gCO2e/km (EU), and a Paris–London flight 50 kg.
- The model has no motherboard, network or storage term, and it cites evidence that the motherboard is negligible.
- Limitations the paper states: no life-cycle assessment (LCA) or embodied emissions; TDP can underestimate power, since hyperthreading can reach 2× TDP; storage is ignored; it uses annual-average CI although CI varies within a day; PUE is reported inconsistently between sites; and literature parameters are assumed.
- Sources: https://arxiv.org/abs/2007.07610 and https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202100707

**GA4HPC (GreenAlgorithms4HPC): estimation from `sacct`.** Source: https://github.com/GreenAlgorithms/GreenAlgorithms4HPC
- It runs without special privileges. It pulls the user's `sacct` logs and applies the GA formula.
- The site fills in `cluster_info.yaml`: per partition the type, model and `TDP` (W per core for CPU; the whole card for GPU, plus `TDP_CPU` for host cores), then `PUE`, `CI`, `granularity_memory_request` and postcode. The fixed constants live in `fixed_parameters.yaml` (`power_memory_perGB: 0.3725`, `tree_month: 917`).
- It computes the usage factor from TotalCPU/CPUTime. It reports failed-job footprint and a "memory needed only" counterfactual, which captures the cost of over-allocation.
- Documented caveats: when CPU time is missing it assumes 100% usage; it assumes GPUs run at 100%; and it says memory-overallocation waste is "largely underestimated".
- A companion HPC dashboard also exists: https://github.com/Cambridge-Sustainable-Computing-Lab/Green-Algorithms-HPCdashboard

**CodeCarbon: measurement where it can, otherwise estimation.** Source: https://docs.codecarbon.io/latest/explanation/methodology/
- CPU: it reads RAPL via `/sys/class/powercap/intel-rapl` (AMD supported since Linux 5.8). Since CVE-2020-8694 (the PLATYPUS side channel), distributions make `energy_uj` **root-only**, so an unprivileged Slurm job usually cannot read it (https://github.com/mlco2/codecarbon/issues/244).
- Fallback: it looks the CPU up in a TDP table and assumes **50% of TDP**.
- RAM (v3): about 5 W per DIMM, from DIMM count rather than GB.
- GPU: NVML (`nvidia-ml-py`), measured per device. NVML is normally readable without root, so **GPU measurement works in-job**.
- `tracking_mode="process"` apportions CPU by the process's CPU time. There is an offline mode with `country_iso_code`.
- Key caveat: RAPL is **package-level** (a whole socket). On a shared 256-core node that holds other users' jobs, the reading is not attributable to one 8-core task.

**Other tools:**
- **perun** (Helmholtz AI) is a measurement tool: RAPL, NVML and psutil, with MPI support. https://perun.readthedocs.io/
- **eco2AI** measures CPU and GPU and applies a regional CI. https://github.com/sb-ai-lab/Eco2AI
- **Cloud Carbon Footprint** estimates from min/max W per vCPU (AWS 0.74–3.5 W) and 0.392 W/GB, plus embodied emissions. It is cloud-oriented but has an on-prem mode. https://www.cloudcarbonfootprint.org/docs/methodology/
- **Boavizta API** estimates embodied (manufacturing) GWP of servers from a bottom-up LCA. https://doc.api.boavizta.org/
- **Slurm energy accounting** is measurement when the site enables it. The `AcctGatherEnergyType` options are `rapl` (root-level daemon reads the socket counters; needs `modprobe msr`), `ipmi` (node BMC, whole node including fans and PSU) and `pm_counters` (HPE Cray). Output goes to `sacct -o ConsumedEnergy` in joules (https://slurm.schedmd.com/acct_gather.conf.html).
  - Caveat: node-level counters only attribute correctly to **node-exclusive** jobs. For shared nodes, Slurm reports node energy during the job, which is not the job's share. **[UNVERIFIED]** whether RAL SCD enables any energy plugin; check with `sacct -j <id> -o ConsumedEnergyRaw`.

**Verified precedent: ARCHER2** (https://docs.archer2.ac.uk/user-guide/energy/):
- Users get `sacct --format=ConsumedEnergy` in joules (×2.78e-7 gives kWh). The counters are HPE `pm_counters` on node-exclusive jobs.
- The measured node energy is multiplied ×1.15 for other hardware (switches, Lustre, CDUs) and ×1.10 for plant overhead. That is an effective PUE of about 1.27 on the node-measured figure.
- The emissions calculation uses the **real-time South Scotland regional CI** from carbonintensity.org.uk.
- It falls back to 0.41 kW/node when counters fail, and adds an embodied factor of 0.014 kgCO2e per CU.

**What works inside an unprivileged job on a shared node:**
- `nvidia-smi` / NVML on an allocated GPU: yes, and it is measured.
- RAPL: normally no, and even when readable it is not attributable on a shared node.
- `sacct`/`seff` post hoc: yes (TotalCPU, elapsed, ReqMem, MaxRSS). This is exactly GA4HPC's input.
- `ConsumedEnergy`: only if the site configured it, and only meaningful for exclusive nodes.

## 2. Per-core power for the RAL `ral` partition and A100

The node model has not been confirmed. Nodes with about 236–252 schedulable CPUs and about 1 TB RAM fit several candidate parts **[UNVERIFIED; get `lscpu` from a node]**:

| Candidate (dual socket) | Cores/node | TDP/socket | W per physical core |
|---|---|---|---|
| EPYC 9754 Bergamo | 256 | 360 W (cTDP 320–400) | 2.8 |
| EPYC 9755 Turin | 256 | 500 W **[UNVERIFIED]** | 3.9 |
| EPYC 7763 Milan, SMT on (256 threads) | 128 physical | 280 W | 4.4 per core (2.2 per thread) |
| EPYC 9654 Genoa | 192 | 360 W | 3.75 |

Sources: https://www.amd.com/en/products/processors/server/epyc/4th-generation-9004-and-8004-series/amd-epyc-9754.html and https://www.phoronix.com/review/amd-epyc-9754-bergamo

If Slurm "CPUs" are hardware threads, then 8 CPUs are 4 physical cores and the per-CPU TDP halves. **I use 3.5 W per Slurm CPU centrally, with a range of 2.8–4.4 W.** A generic GA default of about 10–12 W/core (older Xeons) would **overstate the CPU term 3–4×**.

A100 TDP: SXM4 is 400 W; PCIe is 250 W (40 GB) or 300 W (80 GB). Source: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-nvidia-us-2188504-web.pdf. Real JAX likelihood workloads rarely hold TDP, so measure with `nvidia-smi --query-gpu=power.draw`.

**Usage-factor honesty.** The GA core term `n × P × u × t` reduces to TDP × CPU-seconds. It makes three strong assumptions:
1. An idle allocated core draws nothing. In fact the RAL measurement study found idle servers draw **54% (Intel) to 66% (AMD) of their maximum power** (Ding et al. 2026, arXiv 2608.06622, Finding 1).
2. Over-reserved memory blocks node packing. This is how 64 GB vis_lp reservations capped us at 14 tasks per node.
3. Idle cores and memory on a partially packed node are "someone's" energy.

An attributional (allocation-based) view charges `u = 1` for reserved cores. The truth for a partly loaded shared node lies between the two views, so I use `u = measured` as the low/central case and `u = 1` as the high bound.

## 3. PUE at RAL / STFC

- **R89 (RAL, which hosts the Tier-1 HTC farm): PUE 1.28–1.45 over 2020–2022, mean 1.31**, with seasonal variation, about 1.2 MW IT load and more than 92% utilisation. Ding, Hong, Dewhurst, Greenwood, Walder, Schien & Zilberman, arXiv 2608.06622 (Aug 2026), Fig. 1 and eq. 11. https://arxiv.org/abs/2608.06622
- A new RAL research computer centre (19.8 MW IT, hybrid dry coolers and rear-door coolers at ≥20 °C, no refrigeration) has an **expected peak PUE of about 1.14** (design figure, Tetra Tech). https://www.tetratech.com/projects/ukri-rutherford-appleton-laboratory-research-computer-center-harwell-campus-oxfordshire-england/
- **[UNVERIFIED]** which building hosts the `ral`/euclid-saas nodes and the GPU partition. I found no published PUE for JASMIN/SCD specifically. Ask RAL SCD.
- ARCHER2 has an effective overhead factor of 1.265. GA's global default is 1.67 and should not be used for RAL.
- Recommended: **central 1.31, range 1.20–1.45.**

## 4. UK grid carbon intensity and carbon-aware scheduling

**NESO Carbon Intensity API** (https://api.carbonintensity.org.uk; docs https://carbon-intensity.github.io/api-definitions/) is CC BY 4.0 and needs no key.
- National endpoints: `/intensity`, `/intensity/{from}/fw24h|fw48h|pt24h`, `/intensity/stats/{from}/{to}[/{block}]`, `/generation`.
- Regional endpoints: `/regional/postcode/{outcode}`, `/regional/regionid/{id}`, `/regional/intensity/{from}/{to}/regionid/{id}` (with fw24h/fw48h), at half-hour resolution.
- Harwell (OX11) resolves to **regionid 12, "South England"**.

**Measured from the API** (I pulled every half-hour for 2025-01-01 to 2026-09-20; the script is in scratchpad `hpc_epic/ci.py`, `an.py`, `reg.py`):

| Quantity | Value |
|---|---|
| National 2025 mean (actual) | **129 g/kWh** (p5 51, p95 231) |
| National 2026 year to date | 122 g/kWh |
| Monthly means 2025 | 99 (Jun) – 168 (Jan) |
| Diurnal 2025 mean (UTC) | ~110 at 11–13 h and 01–03 h; **~160 at 17–19 h** |
| South England regional 2025 mean (forecast series) | **188 g/kWh** (p5 81, p95 308) |
| Median absolute forecast error | 6% |

**For company-style reporting, use DESNZ factors instead.**
- The UK electricity factor was 0.20705 kgCO2e/kWh (2024) and 0.177 (2025). Source: https://www.climateessentials.com/articles/carbon-factors-a-2025-update and https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting
- The 2026 factor fell by about 26% (https://circularecology.com/news/desnz-2026-uk-ghg-conversion-factors), which puts it at about 0.13 **[UNVERIFIED exact value]**.
- DESNZ factors lag about 2 years behind the real-time grid and exclude T&D and WTT, which are separate factors.
- Choosing national vs regional vs DESNZ moves CI by about ±40%. That is as large as any other uncertainty, so state which one you used.

**Is carbon-aware delay worth it?** I simulated an oracle (perfect-foresight) choice of start time on the 2025 national series:

| Job shape | Delay window | Oracle saving |
|---|---|---|
| 9 h job | ≤24 h | 25% |
| 9 h job | ≤48 h | 35% |
| 2 h job | ≤48 h | 43% |
| 2-week campaign | ≤48 h | **3%** |

Real forecasts (6% error) and scheduler queueing would reduce these savings. Three caveats:
1. A multi-day array that saturates its allocation **averages over the diurnal cycle** anyway. Only the small, short, deferrable parts benefit, such as SED reruns, test arrays and single re-fits.
2. On a shared, always-busy cluster, delaying your job lets another user's job run. There is no system-level saving unless nodes power down when idle (attributional vs consequential accounting). See Sukprasert et al., EuroSys 2024, "On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting": https://lass.cs.umass.edu/papers/pdf/eurosys24-shiftinglimitations.pdf
3. Average and marginal intensity differ; marginal UK generation is usually gas, at about 350–400 g **[UNVERIFIED]**.

Slurm mechanisms that need no admin rights:
- `sbatch --begin=<fw48h argmin>`
- `--hold` followed by a user cron-free release by a watcher script. Note that our "sessions end at deliverable" rule forbids agent-armed timers, so the scientist would run this.
- `--nice`
- `ArrayTaskThrottle` to spread an array across time.

Site-level options are a carbon-aware partition or power-down policy, or a job_submit plugin.

Prior art:
- carbon-aware-slurm-workflow uses hold/`scontrol release` below a threshold: https://github.com/YagmurKati/carbon-aware-slurm-workflow
- COAST gives start-time advice for HPC: https://arxiv.org/abs/2609.05443
- Google's carbon-intelligent computing (Radovanović et al. 2021): https://arxiv.org/abs/2106.11750
- GSF Carbon Aware SDK: https://github.com/Green-Software-Foundation/carbon-aware-sdk
- GSF SCI, `SCI = (E·I + M) per R`, standardised as ISO/IEC 21031:2024: https://greensoftware.foundation/standards/sci/

**Verdict:** carbon-aware delay is **low priority for full campaigns (≤3%)** and **useful, 20–40%, for short deferrable jobs**. Right-sizing, fewer reruns and memory reservation are bigger levers (§6).

## 5. Reporting in papers

**Guidance:**
- Lannelongue et al. 2021, "Ten simple rules to make your computing more environmentally sustainable", *PLoS Comput Biol* 17:e1009324: https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1009324. It calls for estimating and reporting, and for accounting for the pragmatic scaling factor (all the reruns, tests and failed runs, not only the final run).
- Scientific CO2nduct (Mariani et al., *Commun. Phys.* 2022) proposes standard CO2 reporting tables with LaTeX templates: https://www.nature.com/articles/s42005-022-00930-2 and https://scientific-conduct.github.io/
- Astronomy context:
  - Stevens et al. 2020, *Nat. Astron.*: supercomputing is the largest share of Australian astronomers' emissions, about 15 of ≳25 ktCO2e/yr. https://www.nature.com/articles/s41550-020-1169-1
  - Portegies Zwart 2020, *Nat. Astron.*: https://www.nature.com/articles/s41550-020-1208-y
  - Astronomers for Planet Earth: https://arxiv.org/abs/2303.05259
  - **[UNVERIFIED]** I found no formal RAS or A&A author guideline mandating compute-footprint statements.
- ML precedent:
  - Strubell et al. 2019: https://arxiv.org/abs/1906.02243
  - Patterson et al. 2021, who stress that measured energy, datacentre PUE and location-specific CI change estimates by up to 100×: https://arxiv.org/abs/2104.10350

**How to present uncertainty.** Report a central value and a low–high range, not only a point. Enumerate the bounds per input: TDP per core, usage basis (measured vs allocated), PUE and CI basis. Multiplicative bounds compound; that is acceptable if each factor's range is stated. Give per-lens values as well as totals, and state which pieces were measured and which were estimated.

**Equivalences and their pitfalls.** Car-km (175 g/km), flights (Paris–London 50 kg) and tree-months (917 g) are GA's defaults. The pitfalls:
- Flight emissions per km vary by 1.5–2× (radiative forcing, class).
- Tree-months imply offsetting, which is not equivalent to avoiding emissions.
- Comparisons can trivialise ("less than one flight"). Better comparators are the same analysis on alternative hardware or settings, or the group's travel.

**Template paragraph:**
> The modelling campaign (N = 4,600 lenses; vis_pix, vis_lp and SED stages) ran on the STFC Scientific Computing cluster at RAL, Harwell (AMD EPYC [model], [W] W TDP per core). Following the Green Algorithms methodology (Lannelongue et al. 2021) with CPU time and requested memory from Slurm accounting, a data-centre PUE of 1.31 (RAL R89 2020–22 average; range 1.20–1.45) and the 2025 mean GB grid intensity of 129 gCO2e/kWh (NESO Carbon Intensity API; 188 g for the South England region), we estimate the campaign used ≈1.7 MWh (range 1.2–4.5 MWh), corresponding to ≈0.22 tCO2e (range 0.12–0.85 t), or ≈0.05 kgCO2e per lens. This includes [x]% for failed or timed-out runs and excludes embodied hardware emissions, storage and development runs [or: development runs added via a pragmatic scaling factor of k].

## 6. Worked estimate (Green Algorithms model)

**Assumptions:** 8 Slurm CPUs per task, `P_m` = 0.3725 W/GB, and three cases:

| Case | TDP per CPU | PUE | CI (g/kWh) | Usage | Memory |
|---|---|---|---|---|---|
| Low | 2.8 W | 1.20 | 100 | measured | peak |
| Central | 3.5 W | 1.31 | 130 | measured | as below |
| High | 4.4 W | 1.45 | 190 | **1** (allocation-based) | 64 GB reservation |

Memory per stage: vis_pix 11 GB (high 64); vis_lp 12 GB (low 4 / high 64; tasks were repacked from 64 to 12 GB); SED 8 GB (4–16) **[SED memory assumed]**. vis_lp runtime is 1.5 h (1–2).

**Central arithmetic for vis_pix:**
- Power per task: 8 × 3.5 × 0.83 + 11 × 0.3725 = 23.2 + 4.1 = **27.3 W**
- Energy: 4,600 × 9.1 h × 27.3 W × 1.31 / 1000 = **1,499 kWh**
- Emissions: × 0.130 = **195 kgCO2e**, or 0.33 kWh (42 g) per lens

**Results:**

| Stage | W/task (central) | kWh low / central / high | kgCO2e low / central / high |
|---|---|---|---|
| vis_pix (4,600 × 9.1 h, u 0.83) | 27.3 | 1,140 / **1,499** / 3,584 | 114 / **195** / 681 |
| vis_lp (5,000 × 1.5 h, u 0.53) | 19.3 | 80 / **190** / 856 | 8 / **25** / 163 |
| SED (5,000 × 11 min, u 0.72) | 23.1 | 19 / **28** / 55 | 2 / **4** / 10 |
| **Total** | | 1,239 / **1,717** / 4,494 | 124 / **223** / 854 |

Central total: 223 kg is about 1,270 km in an EU car, about 4.5 Paris–London flights, or about 243 tree-months. The "high" case is dominated by u = 1 and the 64 GB reservations.

For contrast, running GA fully on defaults (10 W/core, PUE 1.67, 475 g) gives vis_pix = 4,600 × 9.1 × (66.4 + 4.1) × 1.67/1000 = 4,928 kWh and **2.34 t**. That is **about 12× the central estimate**, so the site inputs matter more than the formula.

Two cautions on the inputs:
- Using the **median** 9.1 h underestimates the total if the runtime distribution is right-skewed. Use Σ elapsed from `sacct`.
- Development and test runs are excluded; they are the pragmatic scaling factor.

**(a) 4 cores instead of 8 for vis_lp (53% efficiency at 8 cores).**
- Busy core-hours are 8 × 0.53 × 1.5 = 6.36 per task. At 4 cores with u ≈ 0.9, runtime is 6.36 / 3.6 = 1.77 h.
- *GA model (usage-weighted):* the core term depends only on CPU-seconds, so it is unchanged. The memory term grows with runtime. Result: 190 → 198 kWh, **+4%**. GA cannot reward right-sizing.
- *Allocation model (u = 1):* 5,000 × (8 × 3.5 × 1.5 vs 4 × 3.5 × 1.77) plus memory, × 1.31 gives **319 → 214 kWh (−33%, −14 kg)**. With u4 = 0.8 the saving is −25%.
- The real benefit also includes about 2× more tasks per node, and hence a shorter campaign and fewer nodes powered. That argues for reporting the allocation basis for "nudge" purposes.
- **Memory reservation is a comparable lever.** Cutting vis_lp from 64 to 12 GB saves 5,000 × 1.5 × 52 × 0.3725 × 1.31 / 1000 = **190 kWh (25 kg)**, which is the whole central vis_lp footprint again.

**(b) 18% SED timeouts (900 tasks).**
- Wasted energy is 900 × T_limit × 23.1 W × 1.31. That gives **13.6 kWh at a 30-min limit, 27 kWh at 1 h and 55 kWh at 2 h** (1.8 / 3.5 / 7.1 kg). The wall limit is **[UNVERIFIED]**.
- Against the SED base of 28 kWh, that is **+50% to +200% of SED's own footprint**, but only 1–3% of the campaign.
- It is worth fixing for its own sake: raise the limit to about p99 runtime, or checkpoint. It is still small in absolute terms.

**(c) A100 route for vis_pix (46 min per lens).**
- Energy: 4,600 × 0.767 h × (GPU W + host 8 × 3.5 + 32 GB × 0.3725 ≈ 40 W) × 1.31 / 1000.

| GPU draw | kWh | kgCO2e |
|---|---|---|
| 150 W (plausible real draw) | 877 | 114 |
| 250 W | 1,339 | 174 |
| **300 W (as specified)** | **1,570** | **204** |
| 400 W (SXM TDP) | 2,032 | 264 |

- At TDP, the GPU route is **about break-even** with central CPU (1,499 kWh). It wins by about 40% if the real draw is about 150 W, and by about 3× if a generic 10 W/core CPU TDP or u = 1 on the CPU side is correct.
- **This depends on the one-lens 46-min figure** (Q1 example lens; DR1 tiles may differ) and on GPU wall-clock throughput. Measure power draw with NVML during a real array before recommending it on carbon grounds.

## 7. Recommended methodology for PyAutoFit

**Measure inside the job (cheap, no privileges):**
- Wall time, process CPU time (`time.process_time` / `resource.getrusage`, children included) and peak RSS.
- On GPU: poll NVML `power.draw` and integrate it into joules. Write these to the fit's output JSON (for example `energy.json`).
- Read RAPL opportunistically **only** if `/sys/class/powercap/.../energy_uj` is readable **and** the job holds the whole node. Otherwise record "not attributable".
- Record the node's CPU model (`/proc/cpuinfo`) so the TDP lookup can be audited.

**Estimate post hoc (campaign level):**
- Use `sacct` for every task, including failed, timed-out and requeued ones: `Elapsed, TotalCPU, AllocCPUS, ReqMem, MaxRSS, State, ConsumedEnergyRaw`.
- Apply GA twice: once usage-weighted (the low/central basis) and once allocation-weighted (u = 1, reserved memory; the high basis).
- Prefer `ConsumedEnergy` when the site provides it and nodes are exclusive, with an ARCHER2-style overhead.
- Use GA4HPC's `cluster_info.yaml` schema so sites can reuse it.

**Site config values** (a `carbon` config section in autonerves layered config):
- Per partition: `cpu_model`, `tdp_w_per_cpu` (stating whether "CPU" means a thread), `gpu_model`, `gpu_tdp_w`, `host_tdp_w_per_cpu`.
- Site-wide: `pue` with `pue_low` and `pue_high`, `grid_region` (NESO regionid or postcode), `ci_basis` (national-actual, regional or DESNZ-year), an optional fixed `ci_g_per_kwh`, and an optional `embodied_kg_per_node_hour`.
- Whether energy accounting is enabled.
- RAL values to confirm: CPU model/TDP, hosting building PUE, GPU form factor (PCIe or SXM).

**Uncertainty and presentation:**
- Always output central plus [low, high], and list which inputs set each bound.
- Split the total into successful runs vs failed/timeout/rerun runs, and state the pragmatic scaling factor.
- Report per lens as well as the total.
- State the CI basis and source. Fetch CI for the actual run windows from `/intensity/{from}/{to}`; it is CC BY 4.0, so cite NESO.
- Default nudges in the planning estimator: the core-count and memory-reservation deltas on the **allocation basis**, timeout-waste flags, CPU vs GPU break-even with the measured GPU watts, and an optional `--begin` suggestion from `fw48h` **only for short (< ~6 h), small, deferrable arrays**.
