# Recorded baseline functional validation

I use scripts/run_validation.py to establish an archived functional baseline before collecting timing measurements. It builds and tests the existing reference C code without changing its arithmetic.

## Scope

The runner accepts only the baseline implementation and requires its C files, headers and Makefile to match the pinned upstream reference. It uses the existing test/test_kyber.c for Kyber512, Kyber768 and Kyber1024. Each completed test executes 1000 iterations of valid exchange, randomly replaced secret key and nonzero single-byte ciphertext corruption.

The program returns a nonzero exit code on a detected comparison failure. It uses operating-system randomness; input bytes are not archived. Independent known-answer/vector testing, sanitizers, arithmetic proofs, timing-leakage checks and performance measurements remain separate work.

## Invocation

After reviewing and committing the support files, I run these commands from the repository root in Ubuntu/WSL:

```bash
python3 -B scripts/run_validation.py --experiment EXP-000 --run RUN-0002
echo $?
python3 -m json.tool results/EXP-000/RUN-0002/manifest.json
```

The default timeout is 120 seconds for each build or test. I may supply --host-os, --power-mode and --background-load with facts I have verified. Unspecified values remain unknown. A timeout limit is execution control, not a measured performance result.

The collector requires committed files outside results/ and refuses an existing run directory. I do not manually run the collector with RUN-0002 first: the validation runner reserves that ID itself.

## Output and build policy

- metadata.json: unchanged pre-execution environment/source snapshot.
- manifest.json: actual invocation, source hashes, compiler identity, explicit flags, process environment, expected test counts, step statuses and final checks.
- raw/: build/test stdout and stderr, each recorded with its SHA-256.
- build/: freshly compiled executables and compiler temporary files; ignored by Git and kept locally.

The build flags match the pinned upstream functional-test flags. The command explicitly selects KYBER_K=2, 3 or 4. Fresh output paths avoid reusing stale binaries. I use a defined PATH, LC_ALL and TMPDIR environment for child processes; arbitrary inherited include/library overrides are not forwarded.

The original source trees and Makefiles remain unchanged. The manifest retains executable hashes and build commands even though generated binaries are ignored. The initial metadata file continues to say metadata-only and not-run; actual execution belongs in manifest.json.

## Acceptance and failure handling

I accept the run only if:

1. The runner exits with code 0 and manifest status is completed.
2. All six build/test steps have status completed and exit code 0.
3. All three checks.upstream_functional values are pass.
4. provenance_recheck is pass.
5. benchmark_executed remains false, with arithmetic_safety and timing_behaviour still not-run.

Any failure stops subsequent builds/tests and retains completed and partial evidence. A negative subprocess exit code represents termination by a signal. Ordinary interruption is recorded; an abrupt system shutdown or uncatchable termination may leave status running, which is incomplete and must not be accepted.

I preserve failed/incomplete directories and use a new run ID after correcting the cause. I do not reuse RUN-0002 if an attempt has already reserved it.

## Development checks

I can check the infrastructure without compiling or running Kyber:

```bash
python3 -B -m unittest discover -s tests -p test_run_validation.py -v
```

These tests use dummy processes and mocked workflows. ACT-0003 records 15 passing checks and tested file hashes. The first real runner execution remains pending the source commit and launch.
