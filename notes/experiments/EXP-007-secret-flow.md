# EXP-007 — Dynamic secret-flow assessment

## Question and scope

I freeze arithmetic trials after ACT-0016 and ask whether marked secret operands reach branches or addresses in the executed changed paths. I select EXP-005 as the primary candidate; EXP-006 is a secondary comparison because its timing benefit is parameter-dependent. I compare both with the original reference. This experiment assesses implementation behaviour; it is not another optimisation.

I use Valgrind 3.22.0 Memcheck client requests, with GCC 13.3.0 and the existing normal -O3 flags plus -g for diagnostic locations. The runner records exact tool/header/runtime, compiler, source, support and executable hashes. It requires the accepted EXP-005/006 validation manifests and reviews. The original matches pinned upstream. EXP-005 is restored byte-for-byte from 4bd813ed71a90c7722275dc802336852214a5388 into the ignored build directory; current production arithmetic stays at accepted EXP-006. I do not introduce parameter-dependent production dispatch.

Memcheck's undefined-value propagation is used as a secret marker, following the ctgrind approach. The client macros deliberately mark initialised operands undefined; defined twins distinguish that marking from actual uninitialised memory. The relevant interfaces are inspected in the pinned installed headers. [Official manual, sections 4.2.2 and 4.7](https://valgrind.org/docs/manual/mc-manual.html), [ctgrind author repository](https://github.com/agl/ctgrind).

## Fixed protocol before formal execution

I use all three parameters, three variants and eight path/operand-role cases. Each path executes eight fixtures in both a fully defined mode and a marked-secret mode. Centred-secret patterns are zero, positive bound, negative bound, alternating sign, an index-bit pattern and three deterministic interior patterns, with xorshift32 seed 1 per process. For first-operand encoded-secret cases the nonnegative patterns are zero, upper bound, half-bound, alternating zero/bound, an index-bit zero/bound pattern and three deterministic interiors; the second operand is a fixed defined interior vector. These are coverage fixtures, not a statistical sample or a complete set of reachable KEM inputs. Public operands and indices stay defined. This stage collects no timing evidence.

| Path | Marked secret | Public/fixed material | Coverage and bounds |
|---|---|---|---|
| basemul | Second operand | First operand, twiddles and pair index | 8 polynomials, each 128 pairs; first operand [0,4095], second [-1664,1664]; every used twiddle/sign |
| basemul-first | First operand | Second operand, twiddles and pair index | 8 polynomials, each 128 pairs; first [0,4095], second [-1664,1664] |
| dot | Second vector | First vector and K | 8 calls; first [0,4095], second [-1664,1664], including general noncanonical-input envelope |
| dot-first | First vector | Second vector and K | 8 calls; encoded-secret envelope [0,4095], second [-1664,1664] |
| inverse | Input/output polynomial | Stages, twiddles and positions | 8 calls with centred input [-1664,1664] |
| error-path | Noise polynomial | NTT schedule and fixed post-product 3328 | 8 polynomial paths; noise [-ETA1,ETA1]; original poly_ntt versus raw ntt, then final addition/reduction |
| keygen-dot | Secret vector and synthetic error | Matrix [0,3328], K and positions | 8 calls; vector [-1664,1664]; original/EXP-005 dot+tomont versus EXP-006 dedicated function; synthetic error bounded by ETA1+7*3328; final addition/reduction |
| indcpa-dec | Entire generated IND-CPA secret-key byte array | Ciphertext, K and lengths | 8 generated fixtures: two valid, two single-bit-corrupted, two all-255 and two deterministic random ciphertexts; valid outputs checked |

I test both operand roles because indcpa_enc passes secret sp second, whereas indcpa_dec passes decoded secret skpv first. The [0,4095] first-secret envelope also stresses noncanonical encoded values; it is wider than a valid generated key. I mark only the selected secret role in each process.

The keygen-dot synthetic errors stress the established bound; they are not claimed to be sampled noise outputs. Full key generation is not marked: its matrix generation uses public data and must not be misclassified. IND-CPA decryption is a representative integration check; full KEM implicit-rejection/reencryption secret-flow coverage is not claimed. Existing invalid-input functional tests remain separate evidence.

I initialise fixtures before marking. I make outputs defined only after the entire target call/path returns, at the explicit test boundary, then consume them in an observable checksum. No production function performs test declassification. The checksum is a harness liveness check, not a cross-variant correctness oracle; raw representatives can differ. Existing residue/transcript gates provide correctness evidence.

For every build I run a fixed-trace negative control, a deliberately secret-dependent branch and a deliberately secret-indexed address. Both positive controls must produce the expected Memcheck diagnostic in the named control function, with exit code 99; the negative control must remain quiet. Defined twins of all controls must remain quiet. Volatile stores/loads and noinline functions preserve observability; I retain their generated assembly. Every invocation requires RUNNING_ON_VALGRIND, even in defined mode, preventing a no-op native execution from appearing to pass.

The full budget is 9 builds and 198 Memcheck processes: 144 target processes (72 defined, 72 marked) and 54 controls (18 deliberately marked positives, 9 marked negatives and 27 defined controls). Each target process covers 8 fixtures; the basemul fixture expands to 128 pairs. I use a 120-second timeout per process, origin tracking, XML diagnostics, no default suppressions, no error limit and no leak-check analysis. I preserve all stdout/stderr/XML and requested function assembly. There is no early success stopping or retry under the same run ID.

## Interpretation

I require complete XML and a matching harness completion marker. Expected positive-control exits remain recorded as nonzero raw exits and are explicitly classified as detected controls; they are not silently rewritten. An insensitive or unexpected control blocks candidate conclusions. A defined-mode diagnostic suggests a real initialisation/memory issue or harness problem. A marked-only conditional/address diagnostic needs source and assembly diagnosis. I preserve the full matrix when target diagnostics occur, and report diagnostics-require-review rather than a security pass. A completed run means execution completed, not that every finding is resolved.

A quiet, sensitive run supports only no dependency observed on these executed paths with these marked operands. Memcheck does not measure operand-dependent instruction latency, power/EM, faults, unexecuted paths or every microarchitectural channel. It does not prove whole-program constant time. The required statistical timing-leakage assessment remains a separate stage with a pinned tool, sensitivity pilot and predeclared finite budgets. The inherited EXP-002 local-canary tradeoff also remains a separate hardening finding.

## Execution after committing support

I review and commit the harness, runner and research records before a formal run. On this Ubuntu installation the package version inspected for the development setup is 1:3.22.0-0ubuntu3. The development check uses an extracted package in a temporary directory, without a system installation. For a durable formal setup I install the packaged tool:

```sh
sudo apt-get install valgrind=1:3.22.0-0ubuntu3
valgrind --version
python3 -B scripts/run_secret_flow.py --experiment EXP-007 --run RUN-0001
echo $?
```

The runner uses /usr by default; --valgrind-prefix may identify an equivalent extracted installation, with its exact bytes recorded. I do not substitute another Valgrind/compiler version without reviewing and updating this protocol. If the package manager cannot obtain this version, I preserve that setup failure and resolve tool identity before formal collection. The collector requires committed support and a clean Git-visible tree outside results/. I commit results after execution and request review of manifest.json, controls, diagnostics and assembly. A failed/interrupted attempt remains under its allocated ID; a retry receives a new ID.

## Development status

ACT-0016 prepares this protocol and checks the real harness/runner in a temporary development directory. This is explicitly separate from a formal EXP-007/RUN-0001 result. The activity evidence records the exact support snapshot, controls, source restoration, diagnostic parser checks and actual outcomes. Formal collection is pending the support commit.
