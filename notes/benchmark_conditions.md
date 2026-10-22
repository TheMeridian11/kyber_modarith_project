# Benchmark conditions worksheet

I use this worksheet to identify manual controls and fields needed for a complete benchmark record. Blank fields are not observations. I record unavailable values as unknown and distinguish the Windows host from the Linux/WSL guest.

- Experiment ID:
- Run ID and record type:
- Variant and parameter set:
- Source commit:
- Upstream commit:
- Machine description:
- CPU model and visible topology:
- Guest-visible RAM:
- Physical RAM, if verified:
- Guest operating system and kernel:
- Host operating system and WSL version, if verified:
- Compiler path and version:
- Actual build command and flags:
- Executable path and SHA-256:
- Power mode and frequency controls:
- CPU affinity and physical-core placement, if verified:
- Background workload:
- Timer and measurement units:
- Warm-up and measured iterations:
- Independent repetitions and comparison order:
- Input/RNG mode and fixture identifier:
- Evidence locations and limitations:

The metadata collector will automate selected observations and retain manual fields as unknown unless supplied. Its first smoke check is a metadata-only snapshot: it does not build Kyber, run tests or measure performance. I will record full build and execution evidence when the harness is ready.
