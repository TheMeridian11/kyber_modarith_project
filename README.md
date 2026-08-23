# Kyber Modular Arithmetic Optimisation

This repository supports my honours project on modular arithmetic optimisation in CRYSTALS-Kyber / ML-KEM.

The project benchmarks baseline and optimised Kyber implementations across:

- Kyber512
- Kyber768
- Kyber1024

The main operations evaluated are:

- key generation
- encapsulation
- decapsulation

The project focuses on whether reducing modular reduction overhead can improve runtime while preserving correctness and avoiding obvious implementation-security issues.

## Repository structure

- `external/kyber-official/`: untouched official Kyber repository
- `impl/kyber-baseline-ref/`: baseline reference implementation
- `impl/kyber-optimised-ref/`: modified implementation
- `scripts/`: benchmark automation scripts
- `results/`: benchmark outputs
- `analysis/`: result processing scripts
- `notes/`: benchmark conditions, optimisation notes, and implementation logs


- Note: The official Kyber README says the reference implementation is clean but not platform-optimised, so its benchmark numbers should be used as a baseline for comparison rather than as production-level performance numbers 