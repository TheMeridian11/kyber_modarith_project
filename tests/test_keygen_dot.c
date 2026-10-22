/* Reuse public KEM fixtures; keep the production arithmetic user-applied. */
int prior_basemul_validation_main(void);
#define main prior_basemul_validation_main
#include "test_fused_basemul.c"
#undef main
#include "polyvec.h"

#ifndef EXPECT_KEYGEN
#define EXPECT_KEYGEN 0
#endif

static int check_keygen_dot(const polyvec *a, const polyvec *b)
{
  poly prior, candidate, error, sum_prior, sum_candidate;
  int32_t expected[KYBER_N], wanted, sum;
  int64_t acc0, acc1;
  int16_t zeta;
  uint8_t bytes_prior[KYBER_POLYBYTES], bytes_candidate[KYBER_POLYBYTES];
  const int32_t error_bound = KYBER_ETA1 + 7*(KYBER_Q - 1);
  uint32_t state = 1;
  unsigned int pair, j, pattern;

  polyvec_basemul_acc_montgomery(&prior, a, b);
  poly_tomont(&prior);
#if EXPECT_KEYGEN
  polyvec_basemul_acc_keygen(&candidate, a, b);
#else
  /* Existing baseline path for pre-application support checks. */
  polyvec_basemul_acc_montgomery(&candidate, a, b);
  poly_tomont(&candidate);
#endif
  for(pair = 0; pair < KYBER_N/2; pair++) {
    zeta = zetas[64 + pair/2];
    if(pair & 1)
      zeta = (int16_t)-zeta;
    acc0 = 0;
    acc1 = 0;
    for(j = 0; j < KYBER_K; j++) {
      const int16_t *ap = &a->vec[j].coeffs[2*pair];
      const int16_t *bp = &b->vec[j].coeffs[2*pair];
      /* Ordinary modular oracle: remove the twiddle's Montgomery factor. */
      acc0 += (int64_t)ap[0] * bp[0]
            + (int64_t)ap[1] * bp[1] * canonical((int64_t)zeta * 169);
      acc1 += (int64_t)ap[0] * bp[1] + (int64_t)ap[1] * bp[0];
    }
    expected[2*pair] = canonical(acc0);
    expected[2*pair + 1] = canonical(acc1);
  }
  for(j = 0; j < KYBER_N; j++) {
    if(canonical(prior.coeffs[j]) != expected[j]
        || canonical(candidate.coeffs[j]) != expected[j]
        || prior.coeffs[j] < -(KYBER_Q - 1) || prior.coeffs[j] > KYBER_Q - 1
        || candidate.coeffs[j] < -(KYBER_Q - 1) || candidate.coeffs[j] > KYBER_Q - 1) {
      fprintf(stderr, "Keygen-dot residue/range failure at coefficient %u.\n", j);
      return 0;
    }
  }
  for(pattern = 0; pattern < 4; pattern++) {
    for(j = 0; j < KYBER_N; j++) {
      if(pattern == 0)
        error.coeffs[j] = (int16_t)-error_bound;
      else if(pattern == 1)
        error.coeffs[j] = (int16_t)error_bound;
      else if(pattern == 2)
        error.coeffs[j] = (int16_t)((j & 1) ? error_bound : -error_bound);
      else
        error.coeffs[j] = (int16_t)((int32_t)(next_value(&state) % (2*error_bound + 1)) - error_bound);
      sum = (int32_t)candidate.coeffs[j] + error.coeffs[j];
      if(sum < -32768 || sum > 32767) {
        fprintf(stderr, "Keygen-dot error addition would narrow out of range.\n");
        return 0;
      }
    }
    poly_add(&sum_candidate, &candidate, &error);
    poly_add(&sum_prior, &prior, &error);
    poly_reduce(&sum_candidate);
    poly_reduce(&sum_prior);
    for(j = 0; j < KYBER_N; j++) {
      wanted = canonical((int64_t)expected[j] + error.coeffs[j]);
      if(wanted > (KYBER_Q - 1)/2)
        wanted -= KYBER_Q;
      if(sum_candidate.coeffs[j] != wanted || sum_prior.coeffs[j] != wanted) {
        fprintf(stderr, "Keygen-dot differs after retained public-key reduction.\n");
        return 0;
      }
    }
    poly_tobytes(bytes_candidate, &sum_candidate);
    poly_tobytes(bytes_prior, &sum_prior);
    if(memcmp(bytes_candidate, bytes_prior, sizeof(bytes_candidate)) != 0) {
      fprintf(stderr, "Keygen-dot changes polynomial bytes.\n");
      return 0;
    }
  }
  return 1;
}

static int check_keygen_arithmetic(void)
{
  static const unsigned int positions[] = {0, 1, 254, 255};
  polyvec a, b;
  unsigned int i, j, bit, sign, level, selected, position, sample, cases = 0;
  uint32_t state = 1;

  memset(&a, 0, sizeof(a));
  memset(&b, 0, sizeof(b));
  if(!check_keygen_dot(&a, &b))
    return 0;
  cases++;
  for(level = 0; level < 2; level++)
    for(sign = 0; sign < 2; sign++) {
      for(i = 0; i < KYBER_K; i++)
        for(j = 0; j < KYBER_N; j++) {
          a.vec[i].coeffs[j] = level ? KYBER_Q - 1 : 0;
          b.vec[i].coeffs[j] = sign ? (KYBER_Q - 1)/2 : -(KYBER_Q - 1)/2;
        }
      if(!check_keygen_dot(&a, &b))
        return 0;
      cases++;
    }
  for(bit = 0; bit < 8; bit++)
    for(sign = 0; sign < 2; sign++) {
      for(i = 0; i < KYBER_K; i++)
        for(j = 0; j < KYBER_N; j++) {
          a.vec[i].coeffs[j] = (((j >> bit) ^ i ^ sign) & 1) ? KYBER_Q - 1 : 0;
          b.vec[i].coeffs[j] = (((j >> bit) ^ sign) & 1) ? (KYBER_Q - 1)/2 : -(KYBER_Q - 1)/2;
        }
      if(!check_keygen_dot(&a, &b))
        return 0;
      cases++;
    }
  for(selected = 0; selected < KYBER_K; selected++)
    for(position = 0; position < sizeof(positions)/sizeof(positions[0]); position++)
      for(sign = 0; sign < 2; sign++) {
        memset(&a, 0, sizeof(a));
        memset(&b, 0, sizeof(b));
        a.vec[selected].coeffs[positions[position]] = KYBER_Q - 1;
        b.vec[selected].coeffs[positions[position]] = sign ? (KYBER_Q - 1)/2 : -(KYBER_Q - 1)/2;
        if(!check_keygen_dot(&a, &b))
          return 0;
        cases++;
      }
  for(sample = 0; sample < 8; sample++) {
    for(i = 0; i < KYBER_K; i++)
      for(j = 0; j < KYBER_N; j++) {
        a.vec[i].coeffs[j] = (int16_t)(next_value(&state) % KYBER_Q);
        b.vec[i].coeffs[j] = (int16_t)((int32_t)(next_value(&state) % KYBER_Q) - (KYBER_Q - 1)/2);
      }
    if(!check_keygen_dot(&a, &b))
      return 0;
    cases++;
  }
  fprintf(stderr, "keygen_dot_vectors=%u\nkeygen_dot_coefficient_checks=%u\n"
          "keygen_dot_addition_checks=%u\nkeygen_dot_serialization_checks=%u\n"
          "keygen_dot_oracle=pass\n",
          cases, cases * KYBER_N, cases * 4 * KYBER_N, cases * 4);
  return 1;
}

int main(void)
{
  if(!check_keygen_arithmetic() || !check_kem())
    return 1;
  if(fflush(stdout) != 0 || ferror(stdout)) {
    fprintf(stderr, "Transcript flush failure.\n");
    return 2;
  }
  fprintf(stderr, "transcript=public-deterministic-test-vectors\n");
  return 0;
}
