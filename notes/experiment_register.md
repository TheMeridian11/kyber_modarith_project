# Master experiment register

I use this register as the master index; detailed records and raw outputs provide the evidence. The metadata checkpoint, sampled functional run and first raw timing pilot are accepted. The recorded reduction-count run is pending.

| ID | Question or treatment | Lifecycle | Evidence and result | Decision |
|---|---|---|---|---|
| [EXP-000](experiments/EXP-000-baseline.md) | Establish a reproducible reference baseline and validation procedure | running | [RUN-0001 metadata](runs/EXP-000-RUN-0001.md), [RUN-0002 functional validation](runs/EXP-000-RUN-0002.md) and [RUN-0003 timing pilot](runs/EXP-000-RUN-0003.md) accepted; counters checked in ACT-0005 | sampled functional and timing baseline accepted; RUN-0004 counts pending |
| EXP-001 | Fuse products before Montgomery reduction within base multiplication | proposed | Prediction: 5 to 3 Montgomery calls per coefficient pair; no implementation or measurements | pending |
| EXP-002 | Use local wider accumulators across a vector dot product | proposed | Prediction under reviewed bounds: 640K to 384 Montgomery calls per dot product; no implementation or measurements | pending |
| EXP-003 | Reduce Barrett frequency on a fixed inverse-NTT stage schedule | proposed | Candidate: 896 to 128 Barrett calls per inverse transform with centred input retained; no implementation or measurements | pending |
| EXP-004 | Combine selected independently validated treatments | proposed | Conditional on earlier findings and a new combined range/compatibility review | pending |

K is 2, 3 or 4. Predictions originated in the preliminary source review and are not collected data. EXP-002 extends EXP-001; their savings must not be added as independent savings. EXP-003's centred-input assumption must be revalidated if an upstream reduction changes.

A targeted error-vector reduction-removal pilot remains optional and has no allocated ID. Create a record before implementing it if selected.

After execution, I add links to run IDs, source commits, baseline comparisons, functional/arithmetic/timing checks, measured effects and uncertainty, memory observations, limitations and retention decisions. Never reuse a rejected experiment's ID for an unrelated proposal.
