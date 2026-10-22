# EXP-008 — Bounded statistical timing-leakage screening

## Question and frozen scope

I ask whether selected secret classes produce detectable timing differences in the original reference, EXP-003 and EXP-005 under the recorded GCC/WSL setup. EXP-005 includes EXP-003. I retain EXP-003 as an explicit comparator and possible fallback, while EXP-006 remains the adverse/secondary arithmetic trial. This is implementation-security evidence, not a performance comparison or a full-KEM constant-time proof.

I use a custom dudect-style harness and fixed-look Welch analysis, not unmodified dudect. I inspected and pinned [dudect source](https://github.com/oreparaz/dudect/blob/dc269651fb2567e46755cfb2a13d3875592968b5/src/dudect.h) at dc269651fb2567e46755cfb2a13d3875592968b5, retaining the original header and repository license under tests/reference/dudect/. The header contains a public-domain notice and the repository supplies an MIT license; both are preserved. I use its two-class Welch approach and conservative absolute-t screening threshold 10. The precise differences below are intentional and prevent calling this a standard dudect result. The reference header is not linked into Kyber or the timing executable.

## Class contracts

Each path has two separate profiles: zero versus uniform within the stated envelope; alternating lower/upper boundaries versus uniform strictly inside that envelope. These are synthetic stress distributions, not claims about Kyber's natural secret/noise distribution or the reachability of every internal state. Each class is exactly half of every 1000-sample block, shuffled with xorshift32. Class-order and value streams use separate states. All fixtures for a block are prepared before its measurements, and copied to the same working buffer outside the measured interval. A fixed public operand/ciphertext is shared by both classes. Output consumption occurs after timing.

| Path | Varying secret material | Fixed material / contract |
|---|---|---|
| basemul | Second operand [-1664,1664] | First [0,4095]; all 128 pairs and public twiddles |
| basemul-first | First operand [0,4095] | Second [-1664,1664]; encoded-secret stress envelope |
| dot | Second vector [-1664,1664] | First [0,4095], public K and positions |
| dot-first | First vector [0,4095] | Second [-1664,1664] |
| inverse | Polynomial [-1664,1664] | Public stage schedule and twiddles |
| error-path | Error noise [-ETA1,ETA1] | Original/EXP-003 poly_ntt versus EXP-005 raw ntt, then fixed 3328 addition and final reduction |
| keygen-dot | Transformed secret vector [-1664,1664] and noise [-ETA1,ETA1] | Matrix [0,3328], general dot plus tomont, corresponding error NTT and final addition/reduction |
| indcpa-dec | Encoded secret coefficients [0,4095] | One fixed generated ciphertext; synthetic keys need not match it or be valid generated keys |

The IND-CPA probe covers decoded-key processing without changing its public ciphertext between classes. It does not mark public key generation secret or claim full KEM implicit-rejection coverage. EXP-007 separately includes valid generated decryption fixtures. All random fixtures stay within reviewed arithmetic envelopes. The keygen probe retains scale conversion; no production arithmetic is patched.

## Timer, budget and controls

[Machine-readable protocol](../../tests/timing_leakage_protocol.json) fixes GCC 13.3.0, existing normal -O3 flags, logical CPU 0, three variants, three parameters, eight paths, two profiles and two process repetitions with seeds 305419896 and 2271560481. Variant order reverses for repetition two. These are fresh processes within one session, not independent host sessions. The runner restores the complete historical EXP-003/005 source byte-for-byte from recorded commits into ignored build directories. Production checkout remains unchanged. It archives production and harness assembly and all source/tool/support/executable hashes.

Each process performs 1000 unrecorded warm-ups, 2000 retained calibration observations and 50000 analysis observations. Every observation times one complete path, using MFENCE/LFENCE/RDTSCP/LFENCE boundaries and compiler memory barriers. RDTSCP availability and single-CPU affinity are checked. Units are **TSC ticks**, not variable-frequency core cycles or nanoseconds. AUX values at both boundaries are retained; an unchanged guest AUX cannot establish physical-core placement or exclude host preemption. The fences and wrapper overhead are part of each observation. This is a warm-buffer probe; it does not cover all cache states. The instruction ordering follows the [Intel instruction reference](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html); applicability is restricted to the inspected x86-64 setup.

Each build/repetition also runs two controls. A positive control performs 64 volatile recurrence steps for one secret class and one step for the other. A negative control performs fixed unsigned arithmetic on its secret input. I require detection in the final uncropped positive-control mean test, and no threshold crossing in any negative-control view/look. This demonstrates sensitivity to that deliberately large effect; it does not establish sensitivity to every possible small leak. Inadequate/failed controls make the candidate assessment inconclusive, including quiet candidates.

The total formal budget is 9 builds, 180 assembly extractions and **324 measurement processes**: 288 target cells and 36 controls. That is 16200000 analysis observations and 648000 calibration observations, plus warm-ups. No sampling continues until a desired outcome appears. A timeout or execution failure preserves the attempt; a retry receives a new run ID.

## Analysis fixed before formal collection

I retain every duration, both AUX values and the class in a versioned little-endian binary stream (magic KTL00801 followed by repeated <QIIB records). Exact lossless gzip archives replace the temporary uncompressed stream, with both hashes recorded and decompression equality verified. The first 2000 records provide retained timer warm-up/calibration diagnostics, never candidate test observations or the cropping cutoff. Invalid nonpositive intervals or unequal AUX values are excluded by this predeclared rule and their indices retained; more than 1% invalid observations makes the process inconclusive. No other raw outliers are discarded.

I inspect exactly two cumulative looks, 25000 and 50000 analysis observations, and three views at each look:

1. Uncropped first-order Welch test of mean TSC ticks.
2. Welch mean test retaining durations at or below a pooled, class-blind 99th-percentile cutoff recomputed by the fixed rule at each planned look. The uncropped test remains visible. This within-look cutoff is data-dependent but does not use class labels; no calibrated p-value is claimed.
3. Welch test of squared deviations from the current pooled mean, a complementary second-moment screen. Its units differ from the first-order views.

I require at least 10000 retained observations per class in every view/look. Zero standard error with unequal means is flagged explicitly, not replaced by a passing statistic. All 1944 view/look statistics are retained (1728 target and 216 control). A crossing of |t| > 10 at any planned target look/view triggers investigation, even if later values fall below 10. I do not pick favourable profiles or hide a transient crossing. The threshold is a conservative diagnostic convention, **not a calibrated family-wise error probability or a confidence interval**. Repeated/correlated observations, multiple tests, skew and host scheduling limit formal significance claims. I do not use the upstream 100 percentile tests, its continuously updated per-class centring, its timer, or open-ended sequential stopping. These coverage differences are recorded rather than claiming equivalence.

A reproducible signal must be investigated using its raw classes, controls, assembly and baseline/predecessor comparison. A signal in only the candidate is especially important, but is not itself proof of exploitable key recovery. A clean finite screen supports only no difference detected for these classes, budget, timer and environment. It cannot prove constant time or assess power/EM/fault resistance. EXP-002's inherited local-canary tradeoff remains a separate finding.

## Development and formal execution

ACT-0017 records separate development sensitivity and support checks with exact source snapshots. Development measurements are not formal EXP-008 results. A reduced-budget trial showed an uncropped positive control obscured by a timing outlier; all 18 positive controls crossed the uncropped threshold at 50000 observations. The initial calibration-only cropping cutoff also lost too many class-1 samples in one control when timing shifted after calibration. I preserved that attempt and changed the cutoff to the predeclared class-blind within-look percentile before formal collection. This avoids a stale calibration cutoff; it does not suppress uncropped observations or guarantee statistical calibration. I commit the reviewed protocol, runner, harness and accepted EXP-007 evidence before formal collection; the collector checks a clean Git-visible tree outside results/. No additional package installation is required: the runner uses Python's standard library, the existing compiler and objdump.

```sh
python3 -B scripts/run_timing_leakage.py --experiment EXP-008 --run RUN-0001 --cpu 0
echo $?
```

I keep host activity low as for earlier measurements. Completion/exit zero means the fixed collection completed; the manifest assessment and control results still require review. I preserve and commit the entire run directory except ignored rebuildable binaries. The finite screening stage is followed by diagnosis/repetition of any findings and the final direct/repeat-session performance comparison of original, EXP-003 and EXP-005.
