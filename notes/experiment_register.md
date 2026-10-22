# Master experiment register

I use this register as the master index; detailed records and raw outputs provide the evidence. EXP-000 is closed as the initial baseline preparation: metadata, sampled functional checks, timing pilot and reduction counts are accepted. EXP-001 is running: its manually applied arithmetic change and RUN-0001 validation are accepted for a matched timing comparison.

| ID | Question or treatment | Lifecycle | Evidence and result | Decision |
|---|---|---|---|---|
| [EXP-000](experiments/EXP-000-baseline.md) | Establish a reproducible reference baseline and validation procedure | closed | RUN-0001 metadata, RUN-0002 functional checks, RUN-0003 timing pilot and [RUN-0004 counts](runs/EXP-000-RUN-0004.md) accepted | baseline preparation complete; security claims remain bounded by evidence |
| [EXP-001](experiments/EXP-001-fused-basemul.md) | Fuse products before Montgomery reduction within base multiplication | running | [RUN-0001](runs/EXP-001-RUN-0001.md) accepted: exact sampled API compatibility, kernel/UBSan checks, predicted counts and scoped assembly review; 5 to 3 calls observed | proceed to [RUN-0002 matched timings](paired_timing.md); retention deferred pending performance |
| EXP-002 | Use local wider accumulators across a vector dot product | proposed | Prediction under reviewed bounds: 640K to 384 Montgomery calls per dot product; no implementation or measurements | pending |
| EXP-003 | Reduce Barrett frequency on a fixed inverse-NTT stage schedule | proposed | Candidate: 896 to 128 Barrett calls per inverse transform with centred input retained; no implementation or measurements | pending |
| EXP-004 | Combine selected independently validated treatments | proposed | Conditional on earlier findings and a new combined range/compatibility review | pending |

K is 2, 3 or 4. Predictions originated in the preliminary source review and are not collected data. EXP-002 extends EXP-001; their savings must not be added as independent savings. EXP-003's centred-input assumption must be revalidated if an upstream reduction changes.

A targeted error-vector reduction-removal pilot remains optional and has no allocated ID. Create a record before implementing it if selected.

After execution, I add links to run IDs, source commits, baseline comparisons, functional/arithmetic/timing checks, measured effects and uncertainty, memory observations, limitations and retention decisions. Never reuse a rejected experiment's ID for an unrelated proposal.
