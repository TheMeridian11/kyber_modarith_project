# Benchmark conditions

## Evidence and scope

This record describes fourteen accepted performance runs: the original-reference pilot (EXP-000/RUN-0003), the five incremental comparisons (EXP-001/002/003/005/006, each RUN-0002), the three final sessions (EXP-009/RUN-0001–0003), and the five random-seed follow-up sessions (EXP-010/RUN-0001–0005). Their retained metadata and manifests agree on the environment, compiler identity and common build flags below. The [original conditions review](evidence/ACT-0024/documentation-and-conditions-review.json) covers the first nine runs; the [follow-up review](evidence/ACT-0026/exp010-five-session-review.json) covers the additional five.

**Recorded** means captured during collection. **Retrospective** means recalled afterwards. **Current observation** describes the host inspected during this documentation review. These categories are kept separate: the original metadata's unknown manual fields have not been overwritten. metadata.json is a pre-execution snapshot; completed builds and measurements are established by manifest.json and the raw records.

## Recorded performance environment

| Condition | Recorded value |
|---|---|
| CPU and architecture | 12th Gen Intel Core i9-12900KS; x86_64 |
| Guest-visible topology and affinity | 24 logical CPUs visible; selected guest logical CPU 0; observed affinity [0] |
| Guest-visible memory | 16646680576 bytes, approximately 15.50 GiB; this is not installed physical RAM |
| Guest OS and kernel | Ubuntu 24.04.2 LTS; 5.15.167.4-microsoft-standard-WSL2; WSL detected |
| Compiler | GCC 13.3.0 at /usr/bin/x86_64-linux-gnu-gcc-13; exact executable hash in each manifest |
| Collector interpreter | Python 3.12.3 at /usr/bin/python3.12 |
| Build settings | -O3 -fomit-frame-pointer -z noexecstack, with the warning flags listed below; -DKYBER_K=2, 3 or 4 for the parameter set |
| Primary timing builds | Ordinary reference-C builds, without reduction counters or sanitizer instrumentation; no explicit -march=native or AVX2 flag |
| Process environment | LC_ALL=C; PATH=/usr/bin:/bin; TMPDIR set to the run's build directory |
| Power/frequency visibility | No scaling-governor information available in the guest; historical power mode not recorded |
| Physical CPU placement | Unknown: guest CPU 0 does not establish a fixed physical core or P-core/E-core placement on the Windows host |

## Final comparison: source and build identity

The final three-way comparison used the original reference, the cumulative inverse-transform candidate (EXP-003), and that candidate plus the key-generation error-vector treatment (EXP-005), for Kyber512, Kyber768 and Kyber1024. These are separate source snapshots built afresh for each session.

| Identity | Reference |
|---|---|
| Original upstream Kyber | [3edd5af59919](source_revisions.md) |
| Cumulative inverse-transform candidate | [cf8ae0dd700b](source_revisions.md) |
| Selected error-vector candidate | [4bd813ed71a9](source_revisions.md); 35-file selection in [final_candidate.json](../analysis/final_candidate.json) |
| Session 1 support/source checkpoint | [8a5e36e5d041](source_revisions.md) |
| Sessions 2 and 3 support/source checkpoint | [99733b9f5401](source_revisions.md); evaluated source bytes, protocol and support identities match session 1 |
| Executables | Each run's build/bench-{baseline,exp003,exp005}-{512,768,1024}; nine per session, 27 recorded build identities in total |

The [session 1](../results/EXP-009/RUN-0001/manifest.json), [session 2](../results/EXP-009/RUN-0002/manifest.json) and [session 3](../results/EXP-009/RUN-0003/manifest.json) manifests retain every executable path/SHA-256, source-file hash, compiler/tool identity and exact build argv/cwd. All 27 final builds completed without compiler warnings. Long revision IDs are collected in the [revision index](source_revisions.md); file and executable hashes remain in the evidence.

The common compiler flags are:

```text
-Wall -Wextra -Wpedantic -Wmissing-prototypes -Wredundant-decls -Wshadow -Wpointer-arith -O3 -fomit-frame-pointer -z noexecstack
```

For example, session 1's original Kyber512 build used the following argv from cwd /home/meridian/Honours_2026_PQC/kyber_modarith_project/implementation/kyber-baseline-ref (line breaks are for readability):

```text
/usr/bin/x86_64-linux-gnu-gcc-13 -Wall -Wextra -Wpedantic -Wmissing-prototypes -Wredundant-decls -Wshadow -Wpointer-arith -O3 -fomit-frame-pointer -z noexecstack \
  -DKYBER_K=2 -I /home/meridian/Honours_2026_PQC/kyber_modarith_project/implementation/kyber-baseline-ref \
  kem.c indcpa.c polyvec.c poly.c ntt.c cbd.c reduce.c verify.c fips202.c symmetric-shake.c randombytes.c \
  /home/meridian/Honours_2026_PQC/kyber_modarith_project/benchmarks/bench_kem.c \
  -o /home/meridian/Honours_2026_PQC/kyber_modarith_project/results/EXP-009/RUN-0001/build/bench-baseline-512
```

## Final comparison: measurement and analysis

| Condition | EXP-009 setting |
|---|---|
| Sessions | Three separately launched invocations, RUN-0001, RUN-0002 and RUN-0003 |
| Matched blocks | 12 blocks per parameter set per session; all three variants measured in adjacent processes within each block |
| Order | Each of the six variant orders occurs twice per parameter/session; the parameter order rotates between blocks |
| Warm-up and samples | 100 warm-up exchanges followed by 1000 measured exchanges per process; each measured exchange supplies keygen, encapsulation and valid-ciphertext decapsulation durations |
| Coverage | 108 measurement processes and 324000 duration rows per session; 324 processes and 972000 duration rows overall |
| Timer and units | CLOCK_MONOTONIC_RAW, nanoseconds; reported resolution 1 ns |
| Timer diagnostic | Minimum empty timer-pair costs ranged 11–12 ns in session 1, 10–12 ns in session 2 and 11–13 ns in session 3; no subtraction from observations |
| Inputs | Public deterministic SHAKE256 fixtures, derand-shake256-v1 in benchmarks/bench_kem.c; OS randomness cost excluded |
| Fixture matching | Session seed bases 1, 2027 and 4051; block seed = session base + block - 1; identical fixtures across variants within each parameter/block |
| Measurement boundaries | Fixture preparation, warm-up, correctness verification and CSV writing outside the timed operation; all recorded round-trip checks passed |
| Exclusions/stopping | All durations retained; no outlier trimming or effect-dependent extension; the prespecified three sessions completed |
| Primary estimate | Process median → paired within-block percentage reduction → median of 12 effects per session → median of the three session estimates |
| Uncertainty presentation | Individual block effects and descriptive minimum/maximum session estimates; neither session ranges nor ranges across parameter sets are confidence intervals |

The [fixed protocol](../tests/final_comparison_protocol.json) gives the complete permutation rule. The deterministic fixture encodes the parameter, warm-up/measurement phase, seed and iteration; SHAKE256 supplies 64 keygen bytes and 32 encapsulation bytes. Every performance run used 100 warm-up and 1000 measured exchanges per process. Final sessions change seeds and balance order more fully than the earlier studies. Timer resolution and the empty-pair diagnostic do not establish measurement accuracy or eliminate host scheduling noise. Inner duration rows are not independent experimental replicates, and three invocations on one WSL host do not establish statistical independence or portability.

## Earlier performance protocols

| Collection | Process design per parameter set | Order/input distinction |
|---|---|---|
| EXP-000/RUN-0003 pilot | Five original-reference processes; 15 processes and 45000 duration rows across all parameters | Seed 1 reused; no candidate comparison |
| EXP-001/002/003/005/006, each RUN-0002 | Five matched predecessor/candidate pairs; 30 processes and 90000 rows per study across all parameters | Predecessor first in blocks 1/3/5, candidate first in 2/4; fixed parameter order 512/768/1024; seed 1 reused |
| EXP-009/RUN-0001–0003 | Three sessions of 12 three-variant blocks; 324 processes and 972000 rows in total | Balanced variant orders, rotating parameter order and session/block seeds |
| EXP-010/RUN-0001–0005 | Five accepted sessions of 12 three-variant blocks; 540 processes and 1620000 rows | 60 saved random uint64 seeds, matched within each block; balanced orders shuffled before timing; rotating parameter order |

The earlier studies quantify conditional incremental changes. The [final comparison](final_comparison.md) supplies direct cumulative effects against the original and the additional EXP-003-to-EXP-005 effect. Their estimates must not be substituted for one another.

## Recorded random-seed follow-up conditions

All five EXP-010 sessions use the same recorded source/support checkpoint, [397cd83520c6](source_revisions.md), with identical evaluated source files, 31 recorded support-file identities, compiler/tool hashes and normal build flags. Nine fresh builds per session give 45 recorded executable identities, all verified against the retained local files. All 540 extracted production-function bodies match the previously accepted code. The selected working source remains the same 35-file EXP-005 snapshot.

Each session contains 12 matched blocks per parameter, 100 warm-up and 1000 measured exchanges per process. The saved 60-seed plan uses distinct random uint64 values rather than EXP-009's sequential seed bases; it preserves identical fixtures within each matched comparison. Variant order is shuffled in advance while retaining each of the six permutations twice per parameter/session. The summary is the median of five session medians. Box plots describe the pooled 60 block effects and are not confidence intervals.

All 540 processes report a 1 ns timer resolution. The ranges of minimum empty timer-pair costs are 11–12, 11–19, 11, 11 and 11–12 ns for sessions 1–5 respectively. No overhead is subtracted and no timings are removed. The recorded guest environment, affinity and compiler match the table above. Manual host OS, power mode, background load and physical placement fields remain unknown in all five metadata files; their session notes also leave breaks and thermal conditions unrecorded. The retrospective account below concerns EXP-009 and is not evidence of EXP-010's workload, power or break conditions.

The [accepted follow-up](random_seed_followup.md) reports results separately from EXP-009. Repeating on this one WSL machine does not establish independent hosts or separate input variation from environmental variation.

## Retrospective account and current host observations

For the three final sessions, I recall using this Windows machine through Ubuntu WSL with a few browser tabs open and no other intentional workload. I do not recall applying custom CPU settings. The hardware has not changed since those runs. This is retrospective information, not a contemporaneous workload or configuration log; browser tabs and unobserved system activity can still contribute timing noise.

The current host reports an i9-12900KS with 16 physical cores and 24 logical processors, 32 GiB installed RAM (34359738368 bytes), and an MSI MS-7D91 system. Together with the unchanged-hardware recollection, these observations support a retrospective host description. The guest-visible 15.50 GiB recorded above is a different quantity.

Current software observations are Windows 11 Pro, 64-bit, version 10.0.26200 (build 26200; wsl --version reports 10.0.26200.9711), and WSL package 2.4.13.0. The active Windows power scheme is currently Balanced. These current software/power values are not evidence of the versions or power plan used during collection; software updates and historical settings were not confirmed. Host observations came from read-only CIM queries, wsl --version and powercfg /GETACTIVESCHEME.

## Details still unavailable

| Detail | Status for the three final sessions |
|---|---|
| Windows power plan during collection | Unknown; Balanced is only the current observation |
| Custom CPU/BIOS settings | None recalled; exact turbo, frequency, voltage and firmware settings were not recorded and defaults are not verified |
| Breaks between sessions | Unknown; no duration or cooling/restart interval recorded |
| Historical Windows build and WSL package version | Unknown; the guest OS/kernel versions above were recorded, but current host versions cannot fill these historical gaps |
| Host background activity | A few browser tabs and no other intentional workload recalled; exact tabs, processes and utilisation not recorded |
| Physical core placement, temperature and effective frequency | Not measured/established; cannot be reconstructed from guest affinity |

If any missing conditions can be confirmed, add a clearly labelled retrospective note and its basis here. Otherwise retain unknown: these gaps belong in the thesis limitations and do not justify inventing controls or altering the archived measurements.

## Separate security measurements

Reduction-count and sanitizer builds were separate from performance timing. EXP-007 used dynamic marked-secret branch/address checks. EXP-008 used a bounded statistical timing screen with fenced RDTSCP **TSC ticks**, not CLOCK_MONOTONIC_RAW nanoseconds or measured core cycles. Its calibration, classes, controls and sample budget are specified in the [timing-screen record](runs/EXP-008-RUN-0001.md). Ordinary KEM performance measurements do not add a leakage result; the [security summary](final_security_summary.md) retains the distinct scope of each method.
