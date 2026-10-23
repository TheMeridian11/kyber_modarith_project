# Raw timing pilot

I use benchmarks/bench_kem.c and scripts/run_timing.py to measure the unchanged reference implementation. The first committed pilot, EXP-000/RUN-0003, is accepted; see the [run review](runs/EXP-000-RUN-0003.md).

## Protocol

| Item | Choice |
|---|---|
| Implementations | Baseline reference only |
| Parameters | Kyber512, Kyber768, Kyber1024 |
| Operations | Key generation, encapsulation, decapsulation |
| Timer and unit | CLOCK_MONOTONIC_RAW duration in nanoseconds |
| Input mode | Existing keypair_derand and enc_derand APIs; normal decapsulation |
| Fixtures | SHAKE256-derived public input bytes, seed 1 |
| Warm-up | 100 complete exchanges per process, excluded from CSV |
| Measurements | 1000 complete exchanges per process, three operation rows each |
| Repetitions | Five fresh processes per parameter set |
| CPU | One allowed logical CPU, explicitly selected or lowest allowed by default |
| Build flags | Same explicit GCC flags as the accepted functional builds |
| Output | 15 raw CSV files; 45000 measurements; 45 summary rows |
| Exclusions | None; no timer-overhead subtraction |
| Timing/safety instrumentation | None |

The fixture input is exactly 32 bytes: ASCII kyber-bench-v1 in bytes 0..13, KYBER_K in byte 14, phase in byte 15, the unsigned seed in bytes 16..23 and iteration index in bytes 24..31. Integers use little-endian encoding. Phase 0 identifies warm-up and phase 1 identifies measured samples. SHAKE256 produces 96 bytes: 64 for key-generation coins and 32 for encapsulation coins. Each repetition uses the same measured fixture sequence.

These fixtures are public benchmark inputs. Their purpose is reproducibility; they are not randomness for deployed cryptographic use.

## Measurement meaning

Each iteration measures key generation, then encapsulation, then valid-ciphertext decapsulation. Fixture generation and shared-secret comparison are outside the timed intervals. The harness buffers results in memory and prints CSV after the measured loop.

The deterministic API mode measures the KEM computation without operating-system randomness calls. The subsequent candidate comparisons use the same mode. These numbers are not full RNG-inclusive API latency or CPU-cycle counts.

The timer includes interruption and scheduling effects. The stderr log records reported clock resolution and the minimum of 1000 empty timer-pair probes as a diagnostic. I do not subtract that minimum from operation durations, and reported resolution is not a guarantee of accuracy.

Logical CPU affinity limits guest scheduling movement. It does not establish physical-core placement under WSL or control host frequency, thermal behaviour or background load. Unknown manual conditions remain explicit in metadata. This pilot informed the initial five-pair comparison budget; the final comparison later used three sessions of twelve matched blocks.

## Execution and acceptance

The accepted RUN-0003 was launched from the repository root with the command below. It is historical evidence; I use a new run ID for any further execution:

```bash
python3 -B scripts/run_timing.py --experiment EXP-000 --run RUN-0003 --cpu 0
echo $?
```

The runner reserves the ID through the existing collector, freshly builds all three binaries and runs the repetitions. I do not invoke the collector separately for this ID. Optional --power-mode, --background-load and --host-os values must describe observed conditions. I preserve an incomplete run and use a new ID after failure.

A completed pilot requires exit code 0, manifest status completed, provenance_recheck pass, all build/measurement steps successful, and both measured_roundtrips and csv_integrity pass. Arithmetic-safety and timing-behaviour checks remain not-run.

Each CSV has parameter_set, operation, iteration, elapsed_ns and roundtrip_ok. The final field reports the complete exchange check, not independent proof of each operation. The runner rejects missing, reordered, failed or invalid rows.

The manifest records source and support-file hashes, build commands/flags, binary hashes, execution order, selected CPU, protocol and data hashes. Completed CSV files are under raw/. If a process fails, its partial CSV may remain in the corresponding stdout.log; I retain it. metadata.json remains the pre-execution snapshot.

derived/summary.csv is generated from the retained raw measurements and contains per-process/operation median, minimum and maximum. It does not pool all repetitions into an apparent sample of independent experiments, discard outliers or claim a speedup.

## Development evidence

ACT-0004 records short real compile/execution checks of all three binaries, with two warm-up exchanges and twelve measured exchanges each. All 108 operation rows had positive durations and successful round trips. Invalid argument and CSV-integrity checks also passed.

[Retained development output](evidence/ACT-0004/harness-smoke.json) contains the raw smoke-check CSVs and build/test output. These are uncommitted-development checks and are excluded from the thesis performance dataset.

## Accepted pilot and collection budget

ACT-0005 verified all 45000 raw observations and recomputed all 45 summary rows. I retain five fresh processes of 1000 exchanges as the initial comparison budget. There are 1000 fixture indices per parameter set reused across repetitions, so repeated rows must not be treated as independent experimental runs. The [review](runs/EXP-000-RUN-0003.md) records durations, descriptive variation and limitations.

The original summary uses CRLF and remains unchanged because its hash identifies the saved evidence. The writer now specifies LF for future summaries; the CSV-format correction changes neither timing code nor parsed numeric values.
