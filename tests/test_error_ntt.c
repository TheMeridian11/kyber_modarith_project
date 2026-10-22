/* Reuse the public KEM fixtures without repeating the basemul oracle. */
int prior_basemul_validation_main(void);
#define main prior_basemul_validation_main
#include "test_fused_basemul.c"
#undef main
#include "poly.h"

static void reference_forward(int32_t r[KYBER_N])
{
  unsigned int len, start, j, k = 1;
  int32_t left, product, root;

  /* Test-only ordinary modular arithmetic; neither reducer is called. */
  for(len = 128; len >= 2; len >>= 1)
    for(start = 0; start < KYBER_N; start = j + len) {
      root = canonical((int64_t)zetas[k++] * 169);
      for(j = start; j < start + len; j++) {
        left = r[j];
        product = canonical((int64_t)r[j + len] * root);
        r[j] = canonical((int64_t)left + product);
        r[j + len] = canonical((int64_t)left - product);
      }
    }
}

static int check_error_vector(const int16_t input[KYBER_N])
{
  poly raw, centred, offset, sum_raw, sum_centred;
  int32_t expected[KYBER_N], wanted, sum;
  uint8_t bytes_raw[KYBER_POLYBYTES], bytes_centred[KYBER_POLYBYTES];
  const int32_t bound = KYBER_ETA1 + 7*(KYBER_Q - 1);
  uint32_t state = 1;
  unsigned int j, pattern;

  memcpy(raw.coeffs, input, sizeof(raw.coeffs));
  memcpy(centred.coeffs, input, sizeof(centred.coeffs));
  for(j = 0; j < KYBER_N; j++)
    expected[j] = canonical(input[j]);
  reference_forward(expected);
  ntt(raw.coeffs);
  poly_ntt(&centred);
  for(j = 0; j < KYBER_N; j++) {
    wanted = expected[j];
    if(wanted > (KYBER_Q - 1)/2)
      wanted -= KYBER_Q;
    if(canonical(raw.coeffs[j]) != expected[j]
        || raw.coeffs[j] < -bound || raw.coeffs[j] > bound
        || centred.coeffs[j] != wanted) {
      fprintf(stderr, "Error-NTT residue/range failure at coefficient %u.\n", j);
      return 0;
    }
  }

  /* Enclose the unchanged post-poly_tomont public-key coefficient range. */
  for(pattern = 0; pattern < 4; pattern++) {
    for(j = 0; j < KYBER_N; j++) {
      if(pattern == 0)
        offset.coeffs[j] = -(KYBER_Q - 1);
      else if(pattern == 1)
        offset.coeffs[j] = KYBER_Q - 1;
      else if(pattern == 2)
        offset.coeffs[j] = (j & 1) ? KYBER_Q - 1 : -(KYBER_Q - 1);
      else
        offset.coeffs[j] = (int16_t)((int32_t)(next_value(&state) % (2*KYBER_Q - 1)) - (KYBER_Q - 1));
      sum = (int32_t)raw.coeffs[j] + offset.coeffs[j];
      if(sum < -32768 || sum > 32767) {
        fprintf(stderr, "Error-NTT addition would narrow out of range.\n");
        return 0;
      }
    }
    poly_add(&sum_raw, &offset, &raw);
    poly_add(&sum_centred, &offset, &centred);
    poly_reduce(&sum_raw);
    poly_reduce(&sum_centred);
    for(j = 0; j < KYBER_N; j++) {
      wanted = canonical((int64_t)expected[j] + offset.coeffs[j]);
      if(wanted > (KYBER_Q - 1)/2)
        wanted -= KYBER_Q;
      if(sum_raw.coeffs[j] != wanted || sum_centred.coeffs[j] != wanted) {
        fprintf(stderr, "Deferred error reduction differs after final reduction.\n");
        return 0;
      }
    }
    poly_tobytes(bytes_raw, &sum_raw);
    poly_tobytes(bytes_centred, &sum_centred);
    if(memcmp(bytes_raw, bytes_centred, sizeof(bytes_raw)) != 0) {
      fprintf(stderr, "Deferred error reduction changes polynomial bytes.\n");
      return 0;
    }
  }
  return 1;
}

static int check_error_arithmetic(void)
{
  static const unsigned int positions[] = {0, 1, 2, 3, 126, 127, 128, 129, 254, 255};
  int16_t input[KYBER_N];
  unsigned int j, sign, bit, selected, sample, cases = 0;
  uint32_t state = 1;

  memset(input, 0, sizeof(input));
  if(!check_error_vector(input))
    return 0;
  cases++;
  for(sign = 0; sign < 2; sign++) {
    for(j = 0; j < KYBER_N; j++)
      input[j] = sign ? KYBER_ETA1 : -KYBER_ETA1;
    if(!check_error_vector(input))
      return 0;
    cases++;
  }
  for(bit = 0; bit < 8; bit++)
    for(sign = 0; sign < 2; sign++) {
      for(j = 0; j < KYBER_N; j++)
        input[j] = (((j >> bit) & 1) ^ sign) ? KYBER_ETA1 : -KYBER_ETA1;
      if(!check_error_vector(input))
        return 0;
      cases++;
    }
  for(selected = 0; selected < sizeof(positions)/sizeof(positions[0]); selected++)
    for(sign = 0; sign < 2; sign++) {
      memset(input, 0, sizeof(input));
      input[positions[selected]] = sign ? KYBER_ETA1 : -KYBER_ETA1;
      if(!check_error_vector(input))
        return 0;
      cases++;
    }
  for(sample = 0; sample < 8; sample++) {
    for(j = 0; j < KYBER_N; j++)
      input[j] = (int16_t)((int32_t)(next_value(&state) % (2*KYBER_ETA1 + 1)) - KYBER_ETA1);
    if(!check_error_vector(input))
      return 0;
    cases++;
  }
  fprintf(stderr, "error_ntt_vectors=%u\nerror_ntt_coefficient_checks=%u\n"
          "error_ntt_addition_checks=%u\nerror_ntt_serialization_checks=%u\n"
          "error_ntt_oracle=pass\n",
          cases, cases * KYBER_N, cases * 4 * KYBER_N, cases * 4);
  return 1;
}

int main(void)
{
  if(!check_error_arithmetic() || !check_kem())
    return 1;
  if(fflush(stdout) != 0 || ferror(stdout)) {
    fprintf(stderr, "Transcript flush failure.\n");
    return 2;
  }
  fprintf(stderr, "transcript=public-deterministic-test-vectors\n");
  return 0;
}
