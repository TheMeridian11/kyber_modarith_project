# EXP-006 — Defer the keygen dot-product Barrett reduction

## Identity and stopping point

- Activity: ACT-0014.
- Lifecycle: closed in ACT-0016; correctness/counts/scoped assembly and initial timing review complete.
- Outcome: mixed; general keygen-benefit hypothesis not supported. Decision: do not adopt as general candidate; preserve secondary/parameter-specific comparison; select EXP-005 for closing evaluation.
- Variant: keygen-dot, cumulative on EXP-005.
- Predecessor: EXP-005 validation source 5a499bd1940ce0ff8fd5d973f6f46b62b50c0648; timing source 4bd813ed71a90c7722275dc802336852214a5388; timing results eb4c34586c7531bc87dcd165e952d3278cea0b5e.
- Original reference: upstream 3edd5af5991927164edd4aacebfcbee00b8064e7.
- Accepted first run: [EXP-006/RUN-0001](../runs/EXP-006-RUN-0001.md), correctness/counts/scoped assembly. Source/support commit 4c9d539eba8903c2404591b8024e7afef15bbf47; results commit 571f597a0b35fd0c9df264402d4b74d07a725204.
- Accepted timing: [EXP-006/RUN-0002](../runs/EXP-006-RUN-0002.md). Next: [EXP-007 secret-flow assessment](EXP-007-secret-flow.md).
- Origin: local inspection of indcpa.c, polyvec.c, poly.c and reduce.c, extending the consumer-specific reasoning in EXP-005. I make no novelty claim or attribution of this exact proposal to an unreviewed paper.

I make this the final planned optimisation trial before freezing the candidate set. A correct but slower result completes the experiment and can be rejected for performance. It does not require another optimisation. The [practical completion checklist](../practical_completion.md) then requires the focused security assessment, final comparisons and reproducibility outputs.

## Question and isolated change

In EXP-005, key generation calls polyvec_basemul_acc_montgomery, which ends with poly_reduce, and then immediately calls poly_tomont on that result. The wide dot already returns representable Montgomery residues before its final Barrett centring. I ask whether keygen can skip that centring, retain poly_tomont and defer centring until the existing final public-key reduction after adding the error vector.

I proposed, and have now manually applied, a separate keygen-only function containing the existing wide-dot arithmetic and ending in poly_tomont instead of poly_reduce. The keygen call replaces the old dot-plus-tomont pair. The general dot function stays unchanged because encryption/decryption callers feed the centred result into the EXP-003 inverse transform. The new API includes the scale conversion and is not interchangeable with that general API.

Duplicating the small kernel intentionally isolates this caller-specific contract. It can increase code size, change inlining, call placement, register use or instruction-cache behaviour. I will measure and report these tradeoffs; fewer reductions do not guarantee faster code. No allocation, parameter, noise distribution, cryptographic security level or protection flag changes.

| Parameter | Keygen Barrett EXP-005 -> predicted EXP-006 | Calls removed | Encap / decap Barrett, unchanged | Montgomery keygen / encap / decap, unchanged |
|---|---:|---:|---:|---:|
| Kyber512 | 1536 -> 1024 | 512 | 2432 / 3584 | 4864 / 6400 / 9728 |
| Kyber768 | 2304 -> 1536 | 768 | 3328 / 4736 | 7296 / 8832 / 13056 |
| Kyber1024 | 3072 -> 2048 | 1024 | 4224 / 5888 | 9728 / 11264 / 16384 |

These were source-derived predictions before execution. RUN-0001 now confirms all ninety instrumented observations against them. Saving K*256 calls removes one third of EXP-005 keygen Barrett calls, not one third of keygen time. Encap and decap remain control operations with no predicted direct arithmetic benefit.

## Range, representation and consumer argument

In this call, the public matrix coefficients lie in [0,3328] and skpv retains its post-NTT reduction to [-1664,1664]. K is 2, 3 or 4. The int32 accumulators satisfy |sum00|,|sum11| <= K*3328*1664 and |sum01| <= 2*K*3328*1664. The inner products and their partial sums fit int32_t. Signed twiddles have magnitude at most 1664. Each Montgomery result has magnitude at most 3328 under the documented input interval [-109084672,109084671].

| Parameter | Bound on sum00 / sum11 | Bound on sum01 | Bound on M(sum11)*zeta+sum00 | Bound on product in poly_tomont | Post-tomont bound | EXP-005 raw error bound | Final addition bound |
|---|---:|---:|---:|---:|---:|---:|---:|
| Kyber512 | 11075584 | 22151168 | 16613376 | 4502784 | 3328 | 23299 | 26627 |
| Kyber768 | 16613376 | 33226752 | 22151168 | 4502784 | 3328 | 23298 | 26626 |
| Kyber1024 | 22151168 | 44302336 | 27688960 | 4502784 | 3328 | 23298 | 26626 |

The three Montgomery calls per coefficient pair therefore remain within contract. Their outputs already fit int16_t before the omitted Barrett operation. poly_tomont multiplies each by 1353, the unchanged R^2 modulo q constant; 3328*1353=4502784 is within both int32_t and the Montgomery input interval. Its output remains bounded by 3328, the same envelope used in EXP-005's error-addition argument. Adding the unreduced error yields at most 26627/26626, still representable in int16_t. The existing final polyvec_reduce is retained and restores the unique centred residue before serialization.

Montgomery reduction contributes R^-1 with R=2^16. The wide-dot result has the original R^-1 scale, including the Montgomery-scaled twiddle. Barrett only changes the representative. Keeping exactly one poly_tomont changes the result to the same ordinary dot-product scale as the old keygen path. The error NTT scale is unchanged. Thus the sum modulo q and final public-key bytes should agree; skpv and secret-key serialization are unchanged.

This proof is conditional on the documented callers and target arithmetic assumptions. The actual matrix has the tighter 3328 bound; I do not broaden this keygen API into a general replacement. The general dot's centred output, encryption/decryption paths, malformed-input handling and EXP-003's inverse-input bound remain intact. Input/output objects at the keygen call are distinct. New callers or changed bounds require a new argument.

## Applied manual changes — preserved edit record

I manually applied and committed the following three edits, preserving all other bytes and using LF line endings. These snippets preserve the applied change; they are not another edit to perform. RUN-0001 now verifies the exact source hashes, including whitespace. The assistant prepared support/records and reviewed the evidence without editing arithmetic.

### 1. Add the dedicated function to polyvec.c

In implementation/kyber-optimised-ref/polyvec.c, keep the complete existing polyvec_basemul_acc_montgomery function. Immediately after its closing brace, insert the following block with one blank line between functions and one blank line before the following existing documentation comment. Do not replace or edit the general function.

~~~c
/* Keygen-only dot product: defer centring until the final public-key reduction.
 * Keep the general dot-product function unchanged for inverse-NTT callers.
 */
void polyvec_basemul_acc_keygen(poly *r, const polyvec *a,
                                    const polyvec *b)
{
  unsigned int pair, j;
  int16_t zeta, t;
  int32_t sum00, sum11, sum01;

  for(pair = 0; pair < KYBER_N/2; pair++) {
    sum00 = 0;
    sum11 = 0;
    sum01 = 0;

    for(j = 0; j < KYBER_K; j++) {
      const int16_t *ap = &a->vec[j].coeffs[2*pair];
      const int16_t *bp = &b->vec[j].coeffs[2*pair];

      sum00 += (int32_t)ap[0] * bp[0];
      sum11 += (int32_t)ap[1] * bp[1];
      sum01 += (int32_t)ap[0] * bp[1] + (int32_t)ap[1] * bp[0];
    }

    zeta = zetas[64 + pair/2];
    if(pair & 1)
      zeta = (int16_t)-zeta;

    t = montgomery_reduce(sum11);
    r->coeffs[2*pair] = montgomery_reduce((int32_t)t * zeta + sum00);
    r->coeffs[2*pair + 1] = montgomery_reduce(sum01);
  }

  poly_tomont(r);
}
~~~

### 2. Declare it in polyvec.h

In implementation/kyber-optimised-ref/polyvec.h, immediately after the existing polyvec_basemul_acc_montgomery prototype, add one blank line followed by:

~~~c
/* Keygen only: same dot-product input bounds; output is scaled by poly_tomont. */
#define polyvec_basemul_acc_keygen KYBER_NAMESPACE(polyvec_basemul_acc_keygen)
void polyvec_basemul_acc_keygen(poly *r, const polyvec *a, const polyvec *b);
~~~

Keep one blank line before the next existing declaration/macro block.

### 3. Replace only the keygen call pair in indcpa.c

Inside indcpa_keypair_derand's matrix-vector loop in implementation/kyber-optimised-ref/indcpa.c, replace exactly:

~~~c
    polyvec_basemul_acc_montgomery(&pkpv.vec[i], &a[i], &skpv);
    poly_tomont(&pkpv.vec[i]);
~~~

with:

~~~c
    polyvec_basemul_acc_keygen(&pkpv.vec[i], &a[i], &skpv);
~~~

The new function already performs poly_tomont, so the old separate call must be removed. Keep the EXP-005 direct error NTT loop, skpv reduction, final public-key reduction and every other call unchanged. Do not add commented-out copies of the old lines.

| File | Required proposed SHA-256 |
|---|---|
| polyvec.c | 880c7733174e89356a4bc9e5fd75353694693bf4ab328396d08c59e3fbed4f16 |
| polyvec.h | c95db983c8b6f2284df16897c268733fa580b476e9e385c069c637193220dac1 |
| indcpa.c | 664a62a2efe3771cc9bbd70e70a7823db1df0cc42cf82dfcefeb386705132be2 |

The other 32 tracked source files must retain accepted EXP-005 identities. An unapplied or different candidate is rejected before allocating the formal run.

## Correctness and implementation-security gates

| Concern | Argument and required executed evidence |
|---|---|
| Integer arithmetic | The bounds above cover each product, partial sum, narrowing, scale conversion and error addition. Normal and UBSan tests exercise dense, sparse, boundary and interior cases; sanitizer success alone does not prove safe narrowing. |
| Compatibility | An ordinary int64 modular oracle checks the dot result, final error addition, unique centred coefficients and polynomial bytes. Original-reference/candidate normal/UBSan KEM transcripts must match, including invalid/noncanonical inputs. |
| Caller isolation | Preserve the general dot function and all inverse-input centring. Check the actual source diff and normal assembly for the single intended keygen call replacement. |
| Secret-dependent behaviour | Loop bounds, pair parity and twiddle indices are public. Inspect actual generated branches, addresses and reduction instructions. The required later secret-flow and timing-leakage checks complement this review. |
| Memory and hardening | Inspect code size, local stack, register saves, spills, canaries, endbr64 and page probes in affected functions. No protection flag is disabled. The inherited EXP-002 local-dot-canary tradeoff remains; do not assume the new function's hardening before inspection. |
| Duplication and maintenance | Confirm the copied arithmetic matches the accepted general dot up to the final operation. Keep the distinct scale/output contract explicit so later callers do not use the wrong API. |
| Limits | No unexecuted security check is a pass. This does not establish a whole-program constant-time proof, exhaustive memory safety, portable signed-conversion behaviour, power/EM/fault resistance, final ML-KEM conformance or production approval. |

I reject or revise a candidate that violates compatibility, range or reviewed secret-dependent control/address requirements before timing. A later reproducible new leakage finding can also disqualify a performance winner. See the [security assessment protocol](../implementation_security.md).

## Support checks versus candidate validation

I prepared scripts/run_keygen_dot_validation.py and tests/test_keygen_dot.c. The test uses an ordinary int64 modular dot oracle, not the production reducers, but shares the twiddle table and coefficient layout. It covers 45/53/61 vectors for Kyber512/768/1024: zero, dense endpoints, index-bit patterns, sparse endpoints and deterministic interior values. Each build performs 11520/13568/15616 coefficient checks, 46080/54272/62464 error-addition/final-reduction checks and 180/212/244 polynomial serialization comparisons. Error patterns include both conservative endpoints, alternating signs and interior values.

The formal runner built baseline/candidate in normal and UBSan modes and compared four complete 100-fixture KEM transcripts per parameter. It also runs the existing upstream candidate suites and ten-fixture reduction counts. It collects normal assembly for keygen, the general dot, poly_tomont and both reducers, plus the candidate-only keygen dot. The completed total is 69 steps, 138 raw streams, eighteen executables and 33 assembly extracts. The original collection manifest retains assembly review pending; ACT-0015 records the completed review separately. No formal timings were collected. Unchanged standalone basemul/inverse tests are not rerun as separate oracles.

[Development evidence](../evidence/ACT-0014/keygen-dot-validation-support-smoke.json) records twelve successful real normal/UBSan builds of the existing original reference and EXP-005, with EXPECT_KEYGEN=0 and two KEM fixtures per build. The new arithmetic/addition/serialization oracle passes on these existing paths and all four transcripts per parameter match. Unapplied/altered-source guards reject before collection; current EXP-005 counts reject the EXP-006 prediction. Formula and bounds checks pass. Temporary outputs were removed after recording identities. No Git commands, metadata collection, formal run, arithmetic edits, EXP-006 candidate execution or performance measurement occurred in these support checks.

That ACT-0014 smoke check verified only the support machinery. Subsequent manual application and RUN-0001 now establish the actual candidate validation/counts/scoped assembly findings below. At ACT-0015, speed and performance retention remained pending; ACT-0016 resolves them below.

## Historical execution sequence — already completed

After applying the three snippets and reviewing source/support/records, I executed the following sequence. RUN-0001 exists and must not be reused:

~~~bash
git diff --check
git add -- implementation/kyber-optimised-ref/polyvec.c \
  implementation/kyber-optimised-ref/polyvec.h \
  implementation/kyber-optimised-ref/indcpa.c \
  scripts/run_keygen_dot_validation.py tests/test_keygen_dot.c \
  README.md notes/
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Record EXP-005 timings and add EXP-006 keygen dot reduction"
git status --short
python3 -B scripts/run_keygen_dot_validation.py \
  --experiment EXP-006 \
  --run RUN-0001
echo $?
~~~

The formal run requires committed source/support and a clean tree outside results/. I preserve any failed or partial record and use a new run ID for a retry. I inspect the completion status and raw diagnostics before committing results:

~~~bash
git add -- results/EXP-006/RUN-0001/
git diff --cached --check
git diff --cached --stat
git commit -m "Record EXP-006 keygen dot validation"
git status --short
~~~

ACT-0015 now accepts the actual bounds/bytes/counts/scoped assembly evidence and prepares the [fresh matched comparison against EXP-005](../keygen_dot_timing.md). I commit that new support and protocol before RUN-0002. No further arithmetic edit or repeat of RUN-0001 is needed.

## Accepted correctness and security/assembly findings (ACT-0015)

I verified all 69 steps, 138 raw streams, eighteen binaries, seven support files and committed source identities. Twelve normal/UBSan builds pass the targeted dot/addition/serialization checks and four-way 100-fixture KEM transcript comparisons per parameter, including the tested invalid/noncanonical cases. Three upstream suites and ninety count observations pass. Keygen Barrett is now 1024/1536/2048; all Montgomery and encap/decap counts remain unchanged. The [run review](../runs/EXP-006-RUN-0001.md) records exact hashes, scope and limitations.

The applied transformation preserves the conditional range and scale argument above. The wide dot's raw outputs fit int16_t, retained poly_tomont stays within its input/output bounds, and the final public-key addition/reduction gives matching tested coefficients/bytes. General dot and inverse-input centring remain untouched. Passing UBSan does not replace the narrowing argument or prove arbitrary-input safety.

The new dedicated dot matches the general dot's normal instructions after function-symbol renaming except its final tail jump from poly_reduce to poly_tomont, after restoring its stack frame. Branches and addresses follow public pair parity/positions and a fixed 128-pair loop. The general dot, poly_tomont and both reducers retain EXP-005 normalised bodies. The changed keygen call path preserves skpv reduction, raw-error NTT, final addition/reduction and serialization.

Keygen bodies change 442->423, 512->521 and 988->980 bytes; new dot bodies add 285/355/413 bytes. The scoped sum therefore grows 266/364/405 bytes, without claiming that this is total executable growth. Keygen local stack including saved registers changes 5272->5272, 9384->9368 and 15032->15032, excluding return address/callees. Each new dot uses 72 local bytes including saves and no canary, matching the preserved general dot's pattern. Keygen canaries, endbr64 and page probes remain; no protection flag is disabled. Kyber768's matrix calls become unrolled and Kyber1024 retains public-matrix rejection sampling, so timing reflects compiler/call-layout effects as well as removed reductions.

No new secret-coefficient-dependent branch/address choice is observed in the scoped changed path. This does not establish whole-program constant time, statistical leakage resistance, power/EM/fault resistance, exhaustive memory safety, signed portability or final ML-KEM conformance. The inherited EXP-002 dot-canary tradeoff remains recorded. Focused dynamic security checks are still required; VTune is excluded from the plan by the user's ACT-0015 preference.

Six development timing builds match all 33 reviewed bodies and twelve short processes pass both-order comparison checks. These are support checks, not evidence of speed. At ACT-0015 I proceeded to RUN-0002 as the final planned optimisation trial. The completed decision follows.

## Accepted timing and closing decision (ACT-0016)

I accept [RUN-0002](../runs/EXP-006-RUN-0002.md) from source 02cdbb13b49e649953dc05653bcb94002491b236, archived in 42d68a7da90f5d19d0539a0e8825a24852121e41. All 90000 raw durations and derived summaries reproduce exactly, and all 33 reviewed bodies match. Keygen paired medians are -2.55%/+0.22%/+1.67% for Kyber512/768/1024; encap is -2.39%/-0.82%/-0.43%, decap -1.89%/-0.72%/-0.02%. Only ten of 45 pairs are positive. Kyber512 regressions and Kyber1024 keygen improvement persist in both order groups; the small/mixed effects require caution.

The intended reduction-count saving is confirmed, but it is insufficient to predict overall speed. I do not attribute the regressions to a proven layout/cache mechanism or dismiss them as known noise. Existing arithmetic/security evidence remains valid within scope; throughput observations are not a leakage test. I close this final arithmetic trial, select EXP-005 as primary and keep EXP-006 as a secondary research comparison without changing production arithmetic. [EXP-007](EXP-007-secret-flow.md), statistical leakage and final direct/repeat-session comparisons remain. [Thesis figures](../thesis_figures.md) retain the adverse result alongside the successes.
