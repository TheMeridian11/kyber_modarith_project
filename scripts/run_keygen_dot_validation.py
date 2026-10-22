#!/usr/bin/env python3
"""Validate EXP-006 keygen dot-product reduction deferral on top of EXP-005."""

import argparse
import json
import shutil
import signal
import subprocess
import sys
from pathlib import Path

import collect_run_metadata as metadata
import run_counts as counts
import run_validation as validation

ROOT = metadata.ROOT
CANDIDATE = ROOT / "implementation/kyber-optimised-ref"
HARNESS = ROOT / "tests/test_keygen_dot.c"
VARIANTS = {"baseline": validation.BASELINE, "keygen-dot": CANDIDATE}
CASES = 100
TRANSCRIPT_BYTES_PER_CASE = {512: 4160, 768: 5952, 1024: 8064}
EXPECTED = {
    512: ((4864, 1024), (6400, 2432), (9728, 3584)),
    768: ((7296, 1536), (8832, 3328), (13056, 4736)),
    1024: ((9728, 2048), (11264, 4224), (16384, 5888)),
}
MODES = {
    "normal": validation.FLAGS,
    "ubsan": (
        *(flag for flag in validation.FLAGS if flag not in ("-O3", "-fomit-frame-pointer")),
        "-O1", "-g", "-fno-omit-frame-pointer",
        "-fsanitize=undefined", "-fno-sanitize-recover=all",
    ),
}
SUPPORT = (
    "scripts/run_keygen_dot_validation.py", "tests/test_keygen_dot.c",
    "scripts/run_validation.py", "scripts/collect_run_metadata.py",
    "scripts/run_counts.py", "benchmarks/count_reductions.c",
    "tests/test_fused_basemul.c",
)


REFERENCE = ROOT / "results/EXP-005/RUN-0001/manifest.json"
REFERENCE_SHA256 = "6bf9833c02e9744e92360cecd37d6668cb4c4dc01ad4803ee72315fce8f0bd5d"
PROPOSED_SOURCE_SHA256 = {'polyvec.c': '880c7733174e89356a4bc9e5fd75353694693bf4ab328396d08c59e3fbed4f16', 'polyvec.h': 'c95db983c8b6f2284df16897c268733fa580b476e9e385c069c637193220dac1', 'indcpa.c': '664a62a2efe3771cc9bbd70e70a7823db1df0cc42cf82dfcefeb386705132be2'}


def reference_sources():
    if metadata.sha256(REFERENCE) != REFERENCE_SHA256:
        raise RuntimeError("The accepted EXP-005 validation manifest changed.")
    return json.loads(REFERENCE.read_text())["source_file_sha256"]


def source_snapshot(require_change=True):
    previous = reference_sources()
    baseline = validation.source_snapshot()
    if baseline != previous["baseline"]:
        raise RuntimeError("Baseline differs from the accepted source.")
    files = {
        p.relative_to(CANDIDATE).as_posix(): p for p in CANDIDATE.rglob("*")
        if p.is_file() and (p.suffix in (".c", ".h") or p.name == "Makefile")
    }
    if files.keys() != baseline.keys() or any(p.is_symlink() for p in files.values()):
        raise RuntimeError("Candidate source file set differs or contains symlinks.")
    current = {name: metadata.sha256(p) for name, p in sorted(files.items())}
    previous_candidate = previous["raw-error-ntt"]
    expected = {**previous_candidate, **PROPOSED_SOURCE_SHA256}
    if current == previous_candidate:
        if require_change:
            raise RuntimeError("Apply the exact EXP-006 function/header/keygen-call edits before this recorded run.")
    elif current != expected:
        raise RuntimeError("Apply only the reviewed EXP-006 edits in polyvec.c, polyvec.h and indcpa.c; preserve all other source bytes.")
    return {"baseline": baseline, "keygen-dot": current}


def build_test_command(compiler, directory, parameter, k, mode, executable,
                       cases=CASES, expect_fused=None, expect_keygen=None):
    if expect_fused is None:
        expect_fused = directory == CANDIDATE
    if expect_keygen is None:
        expect_keygen = directory == CANDIDATE
    return [
        compiler, *MODES[mode], f"-DKYBER_K={k}",
        f"-DVALIDATION_CASES={cases}", f"-DEXPECT_FUSED={int(expect_fused)}",
        f"-DEXPECT_KEYGEN={int(expect_keygen)}",
        "-I", str(directory), *validation.SOURCES[:-1], str(HARNESS),
        "-o", str(executable),
    ]


def compare_transcripts(paths, parameter, cases=CASES):
    expected_size = cases * TRANSCRIPT_BYTES_PER_CASE[parameter]
    reference = None
    for path in paths:
        data = path.read_bytes()
        if len(data) != expected_size:
            raise RuntimeError(f"Incomplete transcript: {path}; {len(data)} bytes")
        if reference is None:
            reference = data
        elif data != reference:
            offset = next(i for i, (a, b) in enumerate(zip(reference, data)) if a != b)
            raise RuntimeError(f"Byte-level compatibility failure: {path}, offset {offset}")
    return expected_size


def execute(run_dir, snapshot, sources, args):
    compiler = snapshot["environment"]["available_compiler"]
    support = {name: metadata.sha256(ROOT / name) for name in SUPPORT}
    build = run_dir / "build"
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(build)}
    objdump = shutil.which("objdump", path=environment["PATH"])
    manifest = {
        "schema_version": 1, "record_type": "candidate-validation",
        "experiment_id": args.experiment, "run_id": args.run,
        "variant": "keygen-dot", "status": "running",
        "source_commit": snapshot["provenance"]["source_commit"],
        "upstream_commit": metadata.PIN, "metadata_file": "metadata.json",
        "metadata_sha256": metadata.sha256(run_dir / "metadata.json"),
        "predecessor_validation_manifest": REFERENCE.relative_to(ROOT).as_posix(),
        "predecessor_validation_sha256": REFERENCE_SHA256,
        "source_file_sha256": sources, "support_file_sha256": support,
        "compiler": compiler, "build_modes": {k: list(v) for k, v in MODES.items()},
        "process_environment": environment, "invocation_arguments": sys.argv[1:],
        "protocol": {
            "kem_fixtures_per_parameter_and_build": CASES,
            "fixture_mode": "derand-shake256-v1; seed 1; phase 1",
            "keygen_dot_vectors_per_build_by_parameter": {str(p): 29 + 8*k for p, k in validation.PARAMETERS},
            "coefficient_checks_per_vector": 256,
            "addition_patterns_per_vector": 4,
            "addition_coefficient_checks_per_build_by_parameter": {str(p): (29 + 8*k)*4*256 for p, k in validation.PARAMETERS},
            "serialization_checks_per_build_by_parameter": {str(p): (29 + 8*k)*4 for p, k in validation.PARAMETERS},
            "oracle": "test-only int64 ordinary modular dot product; post-tomont bounds, error addition/final reduction and polynomial bytes",
            "input_contract": "keygen matrix coefficients in [0,3328], centred skpv in [-1664,1664]; output after poly_tomont bounded by 3328; retained final public-key reduction",
            "proposed_change": "add dedicated keygen dot function ending in poly_tomont instead of poly_reduce; replace only keygen dot-plus-tomont calls; preserve general dot and all inverse inputs",
            "standalone_inverse_transform_retested": False,
            "general_dot_product_used_as_comparator": True,
            "standalone_basemul_retested": False,
            "transcript_order": [
                "public_key", "secret_key", "valid_ciphertext", "encapsulated_secret",
                "decapsulated_secret", "corrupt_ciphertext_secret", "random_ciphertext_secret",
                "malformed_secret_key_secret", "noncanonical_public_key_ciphertext",
                "noncanonical_public_key_encapsulated_secret",
            ],
            "comparison": "exact transcript bytes across both variants and build modes",
            "count_fixtures_per_parameter": 10,
        },
        "checks": {
            "parameters": {str(p): "not-run" for p, _ in validation.PARAMETERS},
            "assembly_review": "pending", "statistical_leakage": "not-run",
            "constant_time_proof": "not-established",
        },
        "steps": [], "executables": {}, "comparisons": [], "reduction_counts": [],
        "provenance_recheck": "not-run", "benchmark_executed": False,
    }
    validation.save_manifest(run_dir, manifest)

    def step(label, command, directory, binary_output=False):
        if not validation.run_step(
            run_dir, manifest, label, command, directory, environment, args.timeout,
        ):
            raise RuntimeError(f"Step failed or incomplete: {label}; inspect retained logs.")
        item = manifest["steps"][-1]
        if binary_output:
            target = run_dir / "raw" / f"{label}.bin"
            if target.exists():
                raise RuntimeError(f"Refusing to replace {target}")
            (run_dir / item["stdout"]).rename(target)
            item["stdout"] = target.relative_to(run_dir).as_posix()
            validation.save_manifest(run_dir, manifest)
        return run_dir / item["stdout"]

    def build_executable(label, command, directory, executable):
        step("build-" + label, command, directory)
        manifest["executables"][label] = {
            "path": executable.relative_to(run_dir).as_posix(),
            "sha256": metadata.sha256(executable),
        }

    try:
        build.mkdir()
        (run_dir / "raw").mkdir()
        commit = manifest["source_commit"]
        for name in SUPPORT:
            metadata.git("cat-file", "-e", f"{commit}:{name}")
        validation.check_source_state(commit, sources["baseline"])
        if source_snapshot() != sources or metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Source or compiler changed after collection.")
        if objdump is None:
            raise RuntimeError("objdump is required to retain generated-code evidence.")
        manifest["objdump"] = {"path": objdump, "sha256": metadata.sha256(Path(objdump))}
        for parameter, k in validation.PARAMETERS:
            print(f"Validating Kyber{parameter}: baseline and candidate...", flush=True)
            manifest["checks"]["parameters"][str(parameter)] = "running"
            transcripts = []
            for mode in MODES:
                for variant, directory in VARIANTS.items():
                    label = f"{variant}-{parameter}-{mode}"
                    executable = build / label
                    command = build_test_command(
                        compiler["path"], directory, parameter, k, mode, executable,
                    )
                    build_executable(label, command, directory, executable)
                    transcript = step("test-" + label, [str(executable)], directory, True)
                    transcripts.append(transcript)
                    stderr = (run_dir / manifest["steps"][-1]["stderr"]).read_text()
                    vectors = 29 + 8*k
                    expected = (f"keygen_dot_vectors={vectors}\nkeygen_dot_coefficient_checks={vectors*256}\n"
                                f"keygen_dot_addition_checks={vectors*4*256}\nkeygen_dot_serialization_checks={vectors*4}\n"
                                f"keygen_dot_oracle=pass\nkem_fixtures={CASES}\nkem_checks=pass\n"
                                "transcript=public-deterministic-test-vectors\n")
                    if stderr != expected:
                        raise RuntimeError(f"Unexpected test or sanitizer diagnostics: {label}")
                    if mode == "normal":
                        for function in ("indcpa_keypair_derand", "polyvec_basemul_acc_montgomery",
                                         "poly_tomont", "montgomery_reduce", "barrett_reduce",
                                         *(("polyvec_basemul_acc_keygen",) if variant == "keygen-dot" else ())):
                            step("assembly-" + label + "-" + function,
                                 [objdump, "-d", "--insn-width=16", f"--disassemble=pqcrystals_kyber{parameter}_ref_{function}",
                                  str(executable)], directory)
            size = compare_transcripts(transcripts, parameter)
            manifest["comparisons"].append({
                "parameter_set": f"Kyber{parameter}", "status": "pass",
                "bytes_per_transcript": size,
                "transcripts": [p.relative_to(run_dir).as_posix() for p in transcripts],
            })

            label = f"upstream-candidate-{parameter}"
            executable = build / label
            command = [compiler["path"], *validation.FLAGS, f"-DKYBER_K={k}",
                       *validation.SOURCES, "-o", str(executable)]
            build_executable(label, command, CANDIDATE, executable)
            step("test-" + label, [str(executable)], CANDIDATE)

            label = f"counts-candidate-{parameter}"
            executable = build / label
            command = counts.build_command(
                compiler["path"], parameter, k, executable, source_dir=CANDIDATE,
            )
            build_executable(label, command, CANDIDATE, executable)
            csv_path = step("test-" + label, [str(executable), "10", "1"], CANDIDATE)
            manifest["reduction_counts"].extend(
                counts.summarise_csv(csv_path, parameter, 10, expected_counts=EXPECTED)
            )
            manifest["checks"]["parameters"][str(parameter)] = "pass"
            validation.save_manifest(run_dir, manifest)

        manifest["provenance_recheck"] = "running"
        validation.check_source_state(commit, sources["baseline"])
        if source_snapshot() != sources:
            raise RuntimeError("Candidate source changed during validation.")
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed during validation.")
        for name, digest in support.items():
            if metadata.sha256(ROOT / name) != digest:
                raise RuntimeError(f"Support file changed: {name}")
        for item in manifest["executables"].values():
            if metadata.sha256(run_dir / item["path"]) != item["sha256"]:
                raise RuntimeError("Executable changed during validation.")
        manifest["provenance_recheck"] = "pass"
        manifest["status"] = "completed"
    except KeyboardInterrupt:
        manifest["status"] = "interrupted"
        manifest["error"] = "Interrupted; preserve partial evidence."
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        manifest["status"] = "failed"
        manifest["error"] = str(error)
    finally:
        for parameter, status in manifest["checks"]["parameters"].items():
            if status == "running":
                manifest["checks"]["parameters"][parameter] = (
                    "fail" if manifest["status"] == "failed" else "inconclusive"
                )
        if manifest["provenance_recheck"] == "running":
            manifest["provenance_recheck"] = "inconclusive"
        validation.save_manifest(run_dir, manifest)
    print(f"Validation status: {manifest['status']}")
    print(f"Record: {run_dir.relative_to(ROOT).as_posix()}/manifest.json")
    print("No timings collected. Assembly review remains pending.")
    return 0 if manifest["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP-006")
    parser.add_argument("--run", required=True)
    parser.add_argument("--compiler", default="gcc")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if sys.platform != "linux" or args.timeout <= 0 or args.experiment != "EXP-006":
        parser.error("Use Linux/WSL, EXP-006 and a positive timeout.")
    sources = source_snapshot()
    command = [
        sys.executable, "-B", str(ROOT / "scripts/collect_run_metadata.py"),
        "--experiment", args.experiment, "--run", args.run,
        "--variant", "keygen-dot", "--compiler", args.compiler,
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    run_dir = ROOT / "results" / args.experiment / args.run
    snapshot = json.loads((run_dir / "metadata.json").read_text())
    return execute(run_dir, snapshot, sources, args)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, validation.interrupt_requested)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted; preserve any created run directory.", file=sys.stderr)
        sys.exit(130)
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}; preserve any created run directory.", file=sys.stderr)
        sys.exit(1)
