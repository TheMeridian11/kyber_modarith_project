# Master experiment register

I use this register as the master index; detailed records and raw outputs provide the evidence. No formal runs have been recorded.

| ID | Question or treatment | Lifecycle | Evidence and result | Decision |
|---|---|---|---|---|
| [EXP-000](experiments/EXP-000-baseline.md) | Establish a reproducible reference baseline and validation procedure | planned | Setup verified in ACT-0002; collector implementation and smoke check pending; no formal runs | pending |
| EXP-001 | Fuse products before Montgomery reduction within base multiplication | proposed | Prediction: 5 to 3 Montgomery calls per coefficient pair; no implementation or measurements | pending |
| EXP-002 | Use local wider accumulators across a vector dot product | proposed | Prediction under reviewed bounds: 640K to 384 Montgomery calls per dot product; no implementation or measurements | pending |
| EXP-003 | Reduce Barrett frequency on a fixed inverse-NTT stage schedule | proposed | Candidate: 896 to 128 Barrett calls per inverse transform with centred input retained; no implementation or measurements | pending |
| EXP-004 | Combine selected independently validated treatments | proposed | Conditional on earlier findings and a new combined range/compatibility review | pending |

K is 2, 3 or 4. Predictions originated in the preliminary source review and are not collected data. EXP-002 extends EXP-001; their savings must not be added as independent savings. EXP-003's centred-input assumption must be revalidated if an upstream reduction changes.

A targeted error-vector reduction-removal pilot remains optional and has no allocated ID. Create a record before implementing it if selected.

After execution, I add links to run IDs, source commits, baseline comparisons, functional/arithmetic/timing checks, measured effects and uncertainty, memory observations, limitations and retention decisions. Never reuse a rejected experiment's ID for an unrelated proposal.
