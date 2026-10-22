# EXP-003 — Fixed inverse-NTT Barrett-reduction schedule

## Identity and scope

- Originating activity: ACT-0010.
- Lifecycle: closed initial evaluation; validation/counts/assembly and incremental timing accepted. Outcome: supported for the targeted encap/decap benefit. Decision: keep as a research reference with observed keygen tradeoffs.
- Variant: staged-invntt, containing the accepted EXP-002 arithmetic plus the applied inverse-NTT change.
- Predecessor: EXP-002 wide-dot, validated at 61279b2b2373c7594e40f06712bc9f93b734b8ed and timed at a32a81d12225e00a8b3e0baeb32734f44cf78ab3; timing results 5a09a01496fae8dd4b908934c2e5524f5d3ecc9f.
- Original reference: pinned upstream 3edd5af5991927164edd4aacebfcbee00b8064e7.
- Validation source: 9ec22141e6acc98812438544be0bec5b35d00b5c; results commit: 705f21f7f07dcd4162052aacda3adbcc54c4051a.
- Accepted record: [EXP-003/RUN-0001](../runs/EXP-003-RUN-0001.md), validation/counts/assembly only.
- Accepted timing: [EXP-003/RUN-0002](../runs/EXP-003-RUN-0002.md), source cf8ae0dd700bb41628c158016a7c15926a0b790f, results 23b4736206a8f79d13fb4898d474eb327e1dab3c.
- Next treatment: [EXP-005 error-vector reduction deferral](EXP-005-error-ntt.md), not yet applied.
- Idea origin: local source/range analysis of LIT-003. No novelty claim or attribution of this exact schedule to the unreviewed full text of LIT-001.

I retain EXP-002 and change only invntt in implementation/kyber-optimised-ref/ntt.c. The accepted basemul and vector-dot-product functions remain in place. This is an incremental experiment conditional on EXP-002, not a standalone estimate of the inverse-NTT treatment on the original reference. This scope avoids a redundant branch of combination experiments. EXP-004 remains optional if a later interaction or combination question warrants it; it is not an automatic extra step.

## Hypothesis specified before measurement

The EXP-002 inverse NTT has seven butterfly stages with lengths 2, 4, 8, 16, 32, 64 and 128. Each stage applies Barrett reduction to 128 butterfly sums: 896 calls per inverse transform. I proposed retaining those sum reductions only at length 16, for 128 calls. All 896 Montgomery twiddle reductions and 256 final scaling reductions remain unchanged.

The hypothesis is that removing 768 Barrett calls per inverse transform reduces encapsulation/decapsulation duration while preserving the existing KEM outputs. Key generation does not call this inverse transform, so it has no predicted arithmetic/count benefit and provides a useful comparison where no direct gain is expected. Code-layout/compiler effects may still change its measured duration.

| Parameter | Keygen Barrett EXP-002 -> proposed | Encap Barrett EXP-002 -> proposed | Decap Barrett EXP-002 -> proposed |
|---|---:|---:|---:|
| Kyber512 | 2048 -> 2048 | 4736 -> 2432 | 6656 -> 3584 |
| Kyber768 | 3072 -> 3072 | 6400 -> 3328 | 8576 -> 4736 |
| Kyber1024 | 4096 -> 4096 | 8064 -> 4224 | 10496 -> 5888 |

There are zero, K+1 and K+2 inverse transforms in keygen, encapsulation and full decapsulation respectively; decapsulation includes re-encryption. Montgomery counts should remain 4864/6400/9728, 7296/8832/13056 and 9728/11264/16384 for keygen/encap/decap across the three parameter sets. These were source-derived predictions. ACT-0011 subsequently confirmed all full-operation counts in RUN-0001; the prior prediction is retained here. Removing 85.7% of inverse-transform Barrett calls does not imply an 85.7% speedup.

## Caller contract, modular argument and bounds

Every inverse-transform input in the current KEM is produced by polyvec_basemul_acc_montgomery, whose final poly_reduce is retained. This gives centred coefficients in [-1664,1664]. Encryption produces b and v this way; decryption produces mp this way. The earlier EXP-002 bounds include malformed/noncanonical key coefficients and the transformed ciphertext inputs. I preserve those reductions, callers and byte-handling code. This new contract does not cover arbitrary int16_t arrays supplied by unrelated callers or microbenchmarks.

Reducing an intermediate sum modulo 3329 earlier or later preserves its residue. Each later addition, subtraction and Montgomery multiplication therefore has the same residue, provided stored values stay representable and reducer contracts hold. I retain twiddle order, all Montgomery operations and final factor 1441, preserving the transform's Montgomery scale. Internal signed representatives can differ by multiples of q; the kernel oracle compares residues and output bounds, while full KEM transcripts must remain byte-identical after the existing downstream reductions.

Using |zeta| <= 1664 and the existing Montgomery output bound 3328, the following induction is conservative for every coefficient. A butterfly sum/difference is at most twice the incoming bound. At length 16 the sum becomes centred, while the twiddle output is at most 3328; the shared output bound is therefore 3328.

| Stage length | Incoming absolute bound | Sum/difference absolute bound | Barrett on sums? | Outgoing absolute bound |
|---|---:|---:|---|---:|
| 2 | 1664 | 3328 | no | 3328 |
| 4 | 3328 | 6656 | no | 6656 |
| 8 | 6656 | 13312 | no | 13312 |
| 16 | 13312 | 26624 | yes | 3328 |
| 32 | 3328 | 6656 | no | 6656 |
| 64 | 6656 | 13312 | no | 13312 |
| 128 | 13312 | 26624 | no | 26624 |

The maximum sum/difference is 26624, below 32767, so every assignment to int16_t and every Barrett argument is representable. The largest twiddle product is 26624*1664 = 44302336. Final scaling uses at most 26624*1441 = 38365184. Both fit int32_t and the existing Montgomery input interval [-109084672,109084671]. Final outputs are bounded by 3328. The arithmetic proof uses the source's documented reducer contracts and fixed caller envelope; it does not establish a globally optimal reduction schedule.

After the inverse transform, encryption adds noise of magnitude at most 2, giving |b| <= 3330, and also a message coefficient at most 1665 for v, giving |v| <= 4995. Decryption subtracts the inverse result from a decompressed coefficient in [0,3328], giving an absolute bound of 6656. These fit int16_t before the existing poly_reduce calls. Those downstream reductions remain in place.

## Applied replacement, retained for reproducibility

I manually replaced the complete invntt function in implementation/kyber-optimised-ref/ntt.c with the following. ACT-0011 verified an exact match and preserved surrounding source. This is the applied code record; no further arithmetic edit is needed for timing.

~~~c
void invntt(int16_t r[256]) {
  unsigned int start, len, j, k;
  int16_t t, zeta;
  const int16_t f = 1441; // mont^2/128

  /* Requires centred inputs: every coefficient is in [-1664, 1664]. */
  k = 127;
  for(len = 2; len <= 128; len <<= 1) {
    for(start = 0; start < 256; start = j + len) {
      zeta = zetas[k--];
      for(j = start; j < start + len; j++) {
        t = r[j];
        if(len == 16)
          r[j] = barrett_reduce(t + r[j + len]);
        else
          r[j] = t + r[j + len];
        r[j + len] = r[j + len] - t;
        r[j + len] = fqmul(zeta, r[j + len]);
      }
    }
  }

  for(j = 0; j < 256; j++)
    r[j] = fqmul(r[j], f);
}
~~~

I applied and committed this code before RUN-0001. The original ACT-0010 support check tested the preflight rejection of the then-unapplied change; ACT-0011 verifies the now-applied source and saved validation.

## Implementation security and correctness gates

| Concern | Assessment and required evidence |
|---|---|
| Overflow and narrowing | The centred-input precondition and length-16 reset are essential. Removing the reset, shifting it later, or removing an input reduction can invalidate int16_t bounds. Check the range argument, dense extremes, normal/UBSan builds and actual source. |
| Sanitizer limits | Passing UBSan is supplementary. Integer promotions can make arithmetic valid as int while a later narrowing is still unsuitable for the algorithm; the explicit bounds and modular oracle are necessary. |
| Montgomery representation | Keep every twiddle reduction and factor 1441; compare with an ordinary modular inverse-transform oracle. |
| External compatibility | Repeat the established KEM byte transcripts, including corrupted/random ciphertexts, malformed secret keys and noncanonical public keys, against the original reference. |
| Timing/indexing | The new condition depends only on public stage length; no coefficient-dependent reduction decision is introduced. Inspect actual normal-build invntt and both reducers before timing. |
| Memory and hardening | No new array or allocation is introduced. ACT-0011 observed 347 -> 458 inverse-function bytes and 104 -> 72 local stack bytes including saved registers, excluding return address/callees. Neither inverse version has a local canary. EXP-002's dot-product local-canary tradeoff remains inherited. |
| Portability | The recorded GCC target and existing signed-narrowing/right-shift assumptions remain. No claim for untested compilers, arbitrary input ranges or different parameters is added. |
| Broader security | Ordinary speed measurements do not establish constant-time security. Statistical leakage, whole-program proof, power/EM leakage and fault resistance remain unestablished or unassessed. |

The sanitizer limitation follows GCC's explanation of signed-overflow instrumentation and integer promotions; see [GCC 13.3 instrumentation options](https://gcc.gnu.org/onlinedocs/gcc-13.3.0/gcc/Instrumentation-Options.html), LIT-005. A failed correctness/range/security gate prevents acceptance for timing even if a candidate appears faster.

## Validation budget and execution

I prepared tests/test_staged_invntt.c and scripts/run_invntt_validation.py. The test reuses the established deterministic KEM fixtures but tests the changed inverse transform with an independent ordinary-modular oracle that calls neither reducer. Each build checks 47 full vectors, all 256 output coefficients: zero, both dense extremes, both signs for each of eight index-bit patterns, both signs at ten selected boundary positions and eight deterministic interior vectors. It compares residues and the final 3328 bound. This targets the changed arithmetic without repeating dedicated basemul/dot-product oracle suites.

The formal runner uses the original baseline and new cumulative candidate in normal and UBSan modes for all three parameters, with 100 KEM fixtures per build. It also runs the candidate's existing upstream functional suites, checks ten counting fixtures per parameter and retains invntt/Montgomery/Barrett assembly. The expected 54 steps include 18 disassembly extractions. No timings are collected. Source guards preserve all files except invntt itself, including EXP-002 polyvec.c and the accepted basemul.

After manually applying and committing source/support/notes, I ran the following. It is historical; RUN-0001 exists and must not be reused:

~~~bash
python3 -B scripts/run_invntt_validation.py --experiment EXP-003 --run RUN-0001
echo $?
~~~

I do not invoke the metadata collector separately. I preserve failed attempts and use a fresh run ID for a retry. After successful execution, I retain the run directory for review; the initial manifest will still mark assembly review pending until it is inspected separately.

[Development support evidence](../evidence/ACT-0010/invntt-validation-support-smoke.json) records twelve real builds using only the existing original reference and accepted EXP-002, with two KEM fixtures each. All 47-vector oracles, transcript comparisons and exercised UBSan checks passed. The unapplied-change guard rejected the then-current EXP-002 source, and old EXP-002 counts were rejected against the new predictions. The interval induction/count formulas were checked separately. No Git commands, metadata collector, proposed candidate or formal run were executed during those support checks.

## ACT-0011 validation decision and pending performance

I accepted [RUN-0001](../runs/EXP-003-RUN-0001.md) after checking all 54 steps, 108 raw hashes, eighteen binaries, committed source/support, exact transcripts, oracle outputs, counts and generated code. All twelve builds passed 47 inverse-transform vectors and 100 KEM fixtures each; all six UBSan builds had no diagnostics, and all three candidate upstream suites passed. All 90 count observations match the table above. The oracle shares the transform layout and twiddles while using independent reduction arithmetic; sampled success is not exhaustive specification conformance.

I verified actual inverse/reducer assembly against retained EXP-002 binaries. The only new stage-selection branch depends on public length 16; other conditional branches and addresses use public counters/endpoints. Both reducers are unchanged, with no value-dependent branches, division or indirect calls in the reviewed bodies. The inverse body is 111 bytes larger and its local stack use is 32 bytes smaller. These generated-code changes may affect runtime alongside removed Barrett calls. No inverse-function stack canary was removed by this treatment.

The original centred-input and downstream bounds still hold for the current KEM call paths. No arbitrary-int16 input guarantee, whole-program constant-time proof, statistical leakage result or production security approval follows. The original manifest remains immutable with its execution-stage assembly_review=pending field; the [later review](../evidence/ACT-0011/exp-003-run-0001-review.json) records acceptance separately.

At ACT-0011, performance remained unmeasured. The [timing protocol](../invntt_timing.md) specified fresh EXP-002/EXP-003 builds, eighteen assembly comparisons and five pairs per parameter. Development timings were excluded. The completed formal result is recorded below.

## ACT-0012 timing result and retention

I verified [RUN-0002](../runs/EXP-003-RUN-0002.md) and reproduced all 90000 raw durations into the exact saved 90 summaries, 45 pairs and nine aggregates. All eighteen timing-build inverse/reducer bodies match the earlier assembly review. Encapsulation/decapsulation improve in all 30 pairs: median reductions are 4.69%/4.64% for Kyber512, 4.98%/4.90% for Kyber768 and 4.30%/4.63% for Kyber1024. Both order groups favour EXP-003 for these operations.

Keygen median changes are -0.31%, -0.51% and +0.70%; negative means slower. Kyber512 crosses zero, Kyber768 is slower in all five pairs and Kyber1024 faster in all five. Keygen does not call invntt and its two inspected entry points retain the same normalised instructions and entry locations. I retain these small effects without crediting them to inverse reduction savings or asserting an identified noise/layout cause.

I keep EXP-003 for its consistent targeted benefit, with the keygen tradeoffs and the single-session/compiler/WSL scope recorded. Five pairs, reused fixtures and unequal order groups do not establish universal gains or formal significance. The range/security assessment remains conditional on current callers; no new leakage test or whole-program constant-time proof was performed. Larger inverse code, smaller local stack and compiler/layout changes accompany call savings, so their timing contributions remain confounded.

The next proposed experiment is EXP-005, narrowly deferring the error vector's forward-NTT reduction in key generation. It preserves the reductions that establish this experiment's centred inverse inputs. EXP-004 remains deferred for a separate interaction question; cumulative original-baseline performance still requires a later direct comparison.
