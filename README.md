# Kyber Modular Arithmetic Optimisation

In this honours project, I evaluate whether reduction scheduling and wider intermediate arithmetic improve a pinned Kyber reference C implementation while preserving compatibility and satisfying documented arithmetic and implementation-safety checks. I compare key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024.

The source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber), pinned to commit 3edd5af5991927164edd4aacebfcbee00b8064e7. Relevance to ML-KEM does not establish conformance to final FIPS 203. Claims will identify the implementation actually tested. Improvements over reference C do not establish improvements over contemporary optimised implementations.

## Research records

- [Research workflow](notes/research_workflow.md)
- [Cumulative activity log](notes/project_log.md)
- [Master experiment register](notes/experiment_register.md)
- [Baseline experiment plan](notes/experiments/EXP-000-baseline.md)
- [Verified metadata checkpoint](notes/runs/EXP-000-RUN-0001.md)
- [Functional validation runner](notes/validation_runner.md)
- [Accepted functional run](notes/runs/EXP-000-RUN-0002.md)
- [Raw timing protocol](notes/raw_timing.md)
- [Accepted timing pilot](notes/runs/EXP-000-RUN-0003.md)
- [Reduction counting protocol](notes/reduction_counts.md)
- [Accepted reduction counts](notes/runs/EXP-000-RUN-0004.md)
- [EXP-001 plan and security assessment](notes/experiments/EXP-001-fused-basemul.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source; no arithmetic modifications recorded yet.
- scripts/: environment collection and benchmark automation.
- benchmarks/: measurement harnesses that leave cryptographic arithmetic unchanged.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state

I have committed the setup at c584c16d7b8a8e8de5e071a4edd5bc1450f92592 on branch reduction-counters. Repository inspection confirms the upstream submodule mapping, corrected ignore rules and a clean working tree before the ACT-0002 documentation updates. All 36 reference source/build files in each local implementation copy match the pinned upstream reference.

I implemented and checked the metadata collector at source commit 7eea4121e19896cc21773c81530ea5201bb235f3. The metadata-only snapshot EXP-000/RUN-0001 is saved in results commit d2a50d7d6f610f28e4e8f5dcb10c09ed46e93750. File hashes and the separate source/results commits have been verified; the supplied terminal evidence confirms refusal to overwrite the existing run.

I completed EXP-000/RUN-0002 using source commit 75b0e38b5436dfa3f2672822edb178087b542b43 and saved its evidence in results commit e1d3734be7d890e0697678a8ae336e0a8a210f92. All three existing functional tests passed; the archived logs, metadata and binary hashes have been checked.

I completed EXP-000/RUN-0003 using source commit d690cfb580f0dd2d1b0805a6635ed56e553ca5f9 and saved its evidence in results commit 8a76f3f1c0bf9da8157b0901b2defbf8f3f618d2. I verified all 45000 timing rows, reproduced the 45 per-process summary rows and checked the retained hashes. All measured exchanges passed. These are pilot nanosecond durations with operating-system randomness excluded; no optimisation speedup has been measured.

| Step | Status | Purpose |
|---|---|---|
| RUN-0001: metadata | Accepted | Identify source and environment |
| RUN-0002: functional tests | Accepted | Check that unchanged Kyber works |
| RUN-0003: timing pilot | Accepted | Establish unchanged-Kyber duration and variation |
| RUN-0004: reduction counts | Accepted | Establish calls per operation |
| EXP-001: first optimisation | Plan and validation support ready; manual arithmetic edit pending | Test fused base multiplication against the baseline |

I accepted RUN-0004 from source commit 3757df58a02408fb9a701869cc1f3ac6f6159a8d, saved in results commit 2a8388c1701dcf66cb5dfa6906921f63bc574c55. All 90 observations matched the predicted counts. EXP-000 is complete as baseline preparation.

I am beginning EXP-001: fused base multiplication. The plan records modular equivalence, caller ranges including malformed keys, predicted counts and implementation-security gates. I prepared tests/test_fused_basemul.c and scripts/run_candidate_validation.py for exact baseline/candidate byte comparisons, kernel checks, UBSan, existing functional tests, counts and retained disassembly. The arithmetic change is pending manual application; no candidate result or speedup exists yet. The legacy summary script remains unused.

I manually apply arithmetic optimisation changes and review supporting automation before committing the exact source used for a run. I preserve raw outputs, evidence limitations and failed experiments alongside successful results. The activity log distinguishes proposed instructions from confirmed changes and executed checks.
