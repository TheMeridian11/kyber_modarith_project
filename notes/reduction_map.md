# Reduction map

I use this map to record the findings of source inspection. It applies to upstream revision 3edd5af5991927164edd4aacebfcbee00b8064e7. This is a starting point for experiment-specific bounds, not a completed safety proof.

## Functions and boundaries

| Location | Existing behaviour | Research implication |
|---|---|---|
| reduce.c: montgomery_reduce | Accepts bounded int32_t; returns a residue scaled by 2^-16 | Moving/removing calls requires representation and range arguments |
| reduce.c: barrett_reduce | Accepts int16_t; returns a centred residue | An oversized int32_t argument narrows before reduction |
| ntt.c: ntt | Seven stages with unreduced butterfly additions/subtractions | Forward NTT already uses delayed reduction |
| poly.c: poly_ntt | Calls ntt then poly_reduce | Consumers determine whether that reduction is needed |
| ntt.c: invntt | Barrett on each butterfly sum; Montgomery twiddle products and final scaling | Candidate for a fixed public-stage schedule |
| ntt.c: basemul | Five Montgomery reductions per coefficient pair | Candidate for fused sums of products |
| polyvec.c: polyvec_basemul_acc_montgomery | Accumulates K polynomial products, then reduces once | Wider raw-product accumulation is a distinct candidate |
| poly.c: poly_add and poly_sub | No modular reduction | Do not count additions as reduction calls |
| poly.c/polyvec.c: serialization and compression | Expect bounded representatives | Preserve these consumer contracts |
| kem.c: decapsulation | Includes decryption and re-encryption | Include both in per-operation counts |

poly_reduce applies Barrett to each coefficient; polyvec_reduce applies it to each polynomial. The old note listed poly_csubq, but that function does not exist in this snapshot.

## Required per-experiment additions

Record caller-specific input/output ranges, Montgomery scale, intermediate bounds, narrowing and affected consumers, including invalid-input paths. A candidate relying on centred inputs must not silently be used with callers or microbenchmarks supplying larger values. Diagnostic range checks remain separate from timing builds.

See the [experiment register](experiment_register.md) and [baseline plan](experiments/EXP-000-baseline.md). RUN-0004 confirmed the predicted baseline counts for all parameter sets. The [EXP-001 plan](experiments/EXP-001-fused-basemul.md) records fused basemul bounds; [EXP-002](experiments/EXP-002-wide-dot.md) records accepted vector fusion and its incremental timing result. [EXP-003](experiments/EXP-003-staged-invntt.md) applies the len=16 inverse-NTT schedule, with centred inputs retained and a maximum sum/difference of 26624. Its [accepted validation](runs/EXP-003-RUN-0001.md) confirms the counts implied by 128 Barrett calls per inverse transform, unchanged Montgomery counts and matching tested KEM bytes. The inverse body grows while local stack use falls; scoped assembly/security findings are recorded. Its [accepted timing](runs/EXP-003-RUN-0002.md) shows 4.30–4.98% median encap/decap reductions and small keygen tradeoffs.

[EXP-005](experiments/EXP-005-error-ntt.md) now applies the call-site-specific deferral: transform only the keygen error vector e with direct ntt calls and keep the existing final public-key reduction. Conservative raw-error/addition bounds are 23299/26627 for Kyber512 and 23298/26626 for Kyber768/1024. [Accepted validation](runs/EXP-005-RUN-0001.md) confirms K*256 fewer keygen Barrett calls, unchanged Montgomery/encap/decap counts and matching tested bytes. All other forward reductions and EXP-003's inverse-input contract stay intact. Reviewed keygen canaries remain, with larger code and local stack changes of +16/+16/0 bytes. The unchanged NTT/reducers match accepted assembly. Fresh incremental timings remain pending.
