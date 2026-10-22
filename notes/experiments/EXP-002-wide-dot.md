# EXP-002 — Reduction fusion across a vector dot product

## Identity and current stage

- Originating activity: ACT-0008.
- Lifecycle: running; manual implementation and RUN-0001 validation/assembly accepted in ACT-0009; timing pending.
- Variant: wide-dot.
- Predecessor: EXP-001 fused-basemul, retained as a validated research reference after [its timing comparison](../runs/EXP-001-RUN-0002.md).
- Predecessor arithmetic validated at 8345f6a0fb273917ed4499356f0966d1c5dc7fc2; matched timings at d407b5134f14a96a4572b3af1132a8f715e0a28d, results 337e4ba6ff1fc8783c47ea7c34dc2ee52c1e8712.
- Original reference: upstream 3edd5af5991927164edd4aacebfcbee00b8064e7, unchanged in implementation/kyber-baseline-ref.
- Accepted record: [EXP-002/RUN-0001](../runs/EXP-002-RUN-0001.md), source 61279b2b2373c7594e40f06712bc9f93b734b8ed, results b943e50b9fee417ae21bffb4822b2aa6f3309a83.
- Next record: EXP-002/RUN-0002, fresh incremental timings against EXP-001.
- Origin: local analysis of the pinned source, LIT-003. No novelty claim or unreviewed literature attribution.

EXP-001 has already been timed. I now test whether accumulating across the vector before reduction gives further benefit. I have applied the manual change and accepted its saved validation and generated-code review. Performance measurement is next.

## Change and prediction

A vector dot product sums K polynomial products. EXP-001 performs three Montgomery reductions for each coefficient pair in each component, or 384K per dot product. I sum the ordinary products across all K components first, then using three reductions per pair, or 384 per dot product for every parameter set.

This changes only polyvec_basemul_acc_montgomery and adds its required ntt.h/reduce.h includes in the candidate polyvec.c. I retain the accepted EXP-001 ntt.c unchanged. The new KEM vector path computes directly and no longer calls the per-polynomial basemul path. Consequently, these are successive treatments, not independent savings to add together. Standalone basemul retains its accepted EXP-001 implementation.

| Parameter set | K | Dot-product calls: original / EXP-001 / EXP-002 |
|---|---:|---:|
| Kyber512 | 2 | 1280 / 768 / 384 |
| Kyber768 | 3 | 1920 / 1152 / 384 |
| Kyber1024 | 4 | 2560 / 1536 / 384 |

Relative to EXP-001, predicted savings are 384(K-1) per dot product. There are K, K+1 and K+2 dot products in keygen, encapsulation and decapsulation respectively; decapsulation includes re-encryption.

| Parameter set | Keygen EXP-001 -> EXP-002 | Encap EXP-001 -> EXP-002 | Decap EXP-001 -> EXP-002 |
|---|---:|---:|---:|
| Kyber512 | 5632 -> 4864 | 7552 -> 6400 | 11264 -> 9728 |
| Kyber768 | 9600 -> 7296 | 11904 -> 8832 | 16896 -> 13056 |
| Kyber1024 | 14336 -> 9728 | 17024 -> 11264 | 23296 -> 16384 |

These source-derived predictions are now confirmed by all 90 RUN-0001 observations. Barrett counts remain 2048/4736/6656, 3072/6400/8576 and 4096/8064/10496 for keygen/encap/decap. The final poly_reduce is retained. Reduced call counts do not predict a particular runtime percentage.

## Algebra and range argument

For each coefficient pair, let S00 = sum(a0*b0), S11 = sum(a1*b1) and S01 = sum(a0*b1 + a1*b0), summing over the K vector components. Let M(x) be Montgomery reduction and let zeta retain its existing Montgomery representation.

The new outputs before final Barrett reduction are M(M(S11)*zeta + S00) and M(S01). Montgomery reduction is linear modulo q, so these have the same residues as the sum of the EXP-001 outputs. The inner M(S11) is essential to preserve the second power of R^-1 in the twiddle term. The final poly_reduce produces the same centred representatives.

The current KEM callers retain |a| <= 4095, |b| <= 1664 and |zeta| <= 1664. This includes arbitrary 12-bit encoded key coefficients, transformed/reduced ciphertext inputs, and all three parameter sets with K <= 4. I inspected the keygen, encryption and decryption call sites; their input and output objects are separate.

| Quantity | Conservative absolute bound for K <= 4 |
|---|---:|
| One product | 6814080 |
| S00 or S11, including partial sums | 27256320 |
| S01, including partial sums | 54512640 |
| t = M(S11) | 3328 |
| t*zeta + S00 | 32794112 |
| Each Montgomery output | 3328 |
| Each output after poly_reduce | 1664 |

All products and accumulations use int32_t. Every input to montgomery_reduce remains within [-109084672, 109084671], and all new arithmetic fits int32_t. Narrowing occurs only after reduction to a bounded int16_t output. I do not pass an unreduced wide accumulator to barrett_reduce.

This is a contract for these callers and K values, not arbitrary int16_t vector inputs. Changing K, removing a preceding reduction or widening deserialised inputs requires a new argument.

## Applied manual replacement

I applied the following include block and complete function replacement in implementation/kyber-optimised-ref/polyvec.c, preserving the remainder. This is the retained implementation record; it does not need to be applied again:

~~~c
#include <stdint.h>
#include "params.h"
#include "poly.h"
#include "polyvec.h"
#include "ntt.h"
#include "reduce.h"
~~~

Replace the complete existing polyvec_basemul_acc_montgomery function with the following body. Preserve its documentation comment and the following functions. Do not retain a commented copy of the old function in the source.

~~~c
void polyvec_basemul_acc_montgomery(poly *r, const polyvec *a,
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

  poly_reduce(r);
}
~~~

This replacement has been applied and passed the recorded validation. The source guard permits this function and the two includes to change while requiring all other candidate sources, including ntt.c, to match the accepted EXP-001 version.

## Implementation security and correctness

| Concern | Assessment and required evidence |
|---|---|
| Montgomery scale | Preserve the inner M(S11); check an independent ordinary-modular oracle and byte-identical API transcripts. |
| Overflow and narrowing | The larger vector sums require the new bounds above. Run normal and UBSan builds; retain explicit casts and final poly_reduce. |
| Twiddle and coefficient indexing | Pair indices select coefficients 2*pair and 2*pair+1 in 0..255; zeta indices are 64..127. Test all pairs and both signs. |
| Timing behaviour | Loop bounds, vector indices and the parity branch depend only on public indices and K. The reviewed assembly branches on public pair termination/parity and uses public coefficient/twiddle indices; no new secret-dependent branch/address was identified in the inspected scope. |
| Invalid inputs and rejection | Recheck corrupted/random ciphertexts, malformed secret keys and noncanonical public keys against the original reference. Preserve rejection and encoding code. |
| Memory | The source replaces a 512-byte temporary polynomial with scalar accumulators. Reviewed local stack including saved registers falls from 552/568/568 to 72 bytes; dot-function sizes rise from 132/173/155 to 285/355/413 bytes. These exclude callee stack and are not whole-program measurements. No heap allocation is added. |
| Stack hardening | The old function has a canary check; the new scalar implementation does not under the same flags. No protection flag was disabled. I record reduced local corruption-detection coverage, without treating the tests as a proof of memory safety or security. |
| Portability | Existing GCC signed-narrowing/shift assumptions remain. No cross-compiler guarantee is inferred. |
| Broader leakage | Statistical timing leakage, whole-program constant-time proof, power/EM leakage and fault resistance are not established by these checks. |

A faster result cannot override a failed arithmetic, compatibility or security gate. Sampled tests and source bounds complement each other; neither becomes a blanket security certificate.

## Validation and next measurement

I added tests/test_fused_dot.c and scripts/run_dot_validation.py. The driver reuses the existing public KEM fixtures and transcript format, and replaces the standalone kernel test with a vector-dot-product oracle. Per parameter/build it checks 41+K full vectors: zero, sixteen aligned sign corners, sixteen alternating-component sign corners, K isolated-component cases and eight deterministic interior vectors. Each vector checks all 128 coefficient pairs against an independent test-only int64_t oracle and the exact centred result.

I executed the following after the source/support commit. This is historical; RUN-0001 is already allocated and must not be reused:

~~~bash
python3 -B scripts/run_dot_validation.py --experiment EXP-002 --run RUN-0001
echo $?
~~~

The runner builds the original baseline and the new candidate in normal and UBSan modes, compares 100 KEM fixtures byte for byte across the four transcripts per parameter set, runs the candidate's existing upstream functional suite, checks ten count fixtures and retains dot-product/reducer assembly. The original source and accepted EXP-001 ntt.c are protected by hashes. The saved execution and later assembly review are accepted. All twelve transcripts match within parameter sets, vector oracles and exercised UBSan checks pass, and counts match predictions. This command did not measure speed.

[Development support evidence](../evidence/ACT-0008/dot-validation-support-smoke.json) records twelve builds using only the existing baseline and accepted EXP-001 arithmetic, with two KEM fixtures each. All vector-oracle checks and four-way transcript comparisons passed without compiler/sanitizer diagnostics. The preflight rejects an unapplied change before allocating a run, and the count parser rejects EXP-001 counts presented as EXP-002 predictions. These checks exercise support code, not the proposed optimisation.

With validation and assembly accepted, the [next timing comparison](../incremental_timing.md) uses fresh EXP-001 versus EXP-002 processes to measure the incremental effect. The accepted EXP-001 source remains recoverable from the recorded commits; its old timing rows will not substitute for a fresh paired control. Any claim versus the original baseline must use a suitable direct comparison, not the sum of separately measured percentages.

Current status: manual implementation complete; candidate validation/counts/assembly accepted within the recorded scope; performance not-run; final retention decision pending. The changed loop, function size and local canary coverage accompany the arithmetic savings, so any runtime effect cannot be attributed solely to reduction-call counts.
