/* Reuse public KEM fixtures; the unchanged basemul test is not repeated. */
int prior_basemul_validation_main(void);
#define main prior_basemul_validation_main
#include "test_fused_basemul.c"
#undef main

static void reference_inverse(int32_t r[KYBER_N])
{
  unsigned int len, start, j, k = 127;
  int32_t left, right, root;

  /* Test-only ordinary modular arithmetic, independent of both reducers. */
  for(len = 2; len <= 128; len <<= 1)
    for(start = 0; start < KYBER_N; start = j + len) {
      root = canonical((int64_t)zetas[k--] * 169);
      for(j = start; j < start + len; j++) {
        left = r[j];
        right = r[j + len];
        r[j] = canonical((int64_t)left + right);
        r[j + len] = canonical((int64_t)(right - left) * root);
      }
    }
  for(j = 0; j < KYBER_N; j++)
    r[j] = canonical((int64_t)r[j] * 1441 * 169);
}

static int check_inverse_vector(const int16_t input[KYBER_N])
{
  int16_t actual[KYBER_N];
  int32_t expected[KYBER_N];
  unsigned int j;

  memcpy(actual, input, sizeof(actual));
  for(j = 0; j < KYBER_N; j++)
    expected[j] = canonical(input[j]);
  reference_inverse(expected);
  invntt(actual);
  for(j = 0; j < KYBER_N; j++)
    if(canonical(actual[j]) != expected[j]
        || actual[j] < -(KYBER_Q - 1) || actual[j] > KYBER_Q - 1) {
      fprintf(stderr, "Inverse-NTT residue or output-bound failure at coefficient %u.\n", j);
      return 0;
    }
  return 1;
}

static int check_inverse_arithmetic(void)
{
  static const unsigned int positions[] = {0, 1, 2, 3, 126, 127, 128, 129, 254, 255};
  int16_t input[KYBER_N];
  unsigned int j, sign, bit, selected, sample, cases = 0;
  uint32_t state = 1;

  memset(input, 0, sizeof(input));
  if(!check_inverse_vector(input))
    return 0;
  cases++;

  /* Dense extremes exercise long chains of unreduced sums. */
  for(sign = 0; sign < 2; sign++) {
    for(j = 0; j < KYBER_N; j++)
      input[j] = sign ? 1664 : -1664;
    if(!check_inverse_vector(input))
      return 0;
    cases++;
  }
  /* Both signs across each index bit exercise sum/difference paths. */
  for(bit = 0; bit < 8; bit++)
    for(sign = 0; sign < 2; sign++) {
      for(j = 0; j < KYBER_N; j++)
        input[j] = (((j >> bit) & 1) ^ sign) ? 1664 : -1664;
      if(!check_inverse_vector(input))
        return 0;
      cases++;
    }
  for(selected = 0; selected < sizeof(positions)/sizeof(positions[0]); selected++)
    for(sign = 0; sign < 2; sign++) {
      memset(input, 0, sizeof(input));
      input[positions[selected]] = sign ? 1664 : -1664;
      if(!check_inverse_vector(input))
        return 0;
      cases++;
    }
  for(sample = 0; sample < 8; sample++) {
    for(j = 0; j < KYBER_N; j++)
      input[j] = (int16_t)((int32_t)(next_value(&state) % 3329) - 1664);
    if(!check_inverse_vector(input))
      return 0;
    cases++;
  }
  fprintf(stderr, "invntt_vectors=%u\ninvntt_coefficient_checks=%u\ninvntt_oracle=pass\n",
          cases, cases * KYBER_N);
  return 1;
}

int main(void)
{
  if(!check_inverse_arithmetic() || !check_kem())
    return 1;
  if(fflush(stdout) != 0 || ferror(stdout)) {
    fprintf(stderr, "Transcript flush failure.\n");
    return 2;
  }
  fprintf(stderr, "transcript=public-deterministic-test-vectors\n");
  return 0;
}
