/* Reuse the existing public KEM fixtures and transcript format. */
int prior_basemul_validation_main(void);
#define main prior_basemul_validation_main
#include "test_fused_basemul.c"
#undef main
#include "polyvec.h"

static int check_dot_vector(const polyvec *a, const polyvec *b)
{
  poly result;
  unsigned int pair, j;
  int16_t zeta;
  int32_t root, expected0, expected1;
  int64_t sum0, sum1;

  polyvec_basemul_acc_montgomery(&result, a, b);
  for(pair = 0; pair < KYBER_N/2; pair++) {
    zeta = zetas[64 + pair/2];
    if(pair & 1)
      zeta = (int16_t)-zeta;
    root = canonical((int64_t)zeta * 169);
    sum0 = sum1 = 0;
    for(j = 0; j < KYBER_K; j++) {
      const int16_t *ap = &a->vec[j].coeffs[2*pair];
      const int16_t *bp = &b->vec[j].coeffs[2*pair];
      /* Ordinary int64_t modular oracle; no Montgomery reducer calls. */
      sum0 += (int64_t)ap[0]*bp[0] + (int64_t)ap[1]*bp[1]*root;
      sum1 += (int64_t)ap[0]*bp[1] + (int64_t)ap[1]*bp[0];
    }
    expected0 = canonical(sum0 * 169);
    expected1 = canonical(sum1 * 169);
    if(expected0 > (KYBER_Q - 1)/2)
      expected0 -= KYBER_Q;
    if(expected1 > (KYBER_Q - 1)/2)
      expected1 -= KYBER_Q;
    if(result.coeffs[2*pair] != expected0 || result.coeffs[2*pair + 1] != expected1) {
      fprintf(stderr, "Vector dot-product residue or centred-output failure at pair %u.\n", pair);
      return 0;
    }
  }
  return 1;
}

static int check_dot_arithmetic(void)
{
  polyvec a, b;
  unsigned int signs, mode, pair, j, selected, sample, cases = 0;
  uint32_t state = 1;

  memset(&a, 0, sizeof(a));
  memset(&b, 0, sizeof(b));
  if(!check_dot_vector(&a, &b))
    return 0;
  cases++;

  /* Same-sign accumulation and cancellation across vector components. */
  for(mode = 0; mode < 2; mode++)
    for(signs = 0; signs < 16; signs++) {
      for(j = 0; j < KYBER_K; j++)
        for(pair = 0; pair < KYBER_N/2; pair++) {
          int sign = (mode && (j & 1)) ? -1 : 1;
          a.vec[j].coeffs[2*pair] = (int16_t)(sign * ((signs & 1) ? 4095 : -4095));
          a.vec[j].coeffs[2*pair + 1] = (int16_t)(sign * ((signs & 2) ? 4095 : -4095));
          b.vec[j].coeffs[2*pair] = (signs & 4) ? 1664 : -1664;
          b.vec[j].coeffs[2*pair + 1] = (signs & 8) ? 1664 : -1664;
        }
      if(!check_dot_vector(&a, &b))
        return 0;
      cases++;
    }

  /* Each component must contribute, including the last component. */
  for(selected = 0; selected < KYBER_K; selected++) {
    memset(&a, 0, sizeof(a));
    memset(&b, 0, sizeof(b));
    for(pair = 0; pair < KYBER_N/2; pair++) {
      a.vec[selected].coeffs[2*pair] = 4095;
      a.vec[selected].coeffs[2*pair + 1] = -4095;
      b.vec[selected].coeffs[2*pair] = b.vec[selected].coeffs[2*pair + 1] = 1664;
    }
    if(!check_dot_vector(&a, &b))
      return 0;
    cases++;
  }

  for(sample = 0; sample < 8; sample++) {
    for(j = 0; j < KYBER_K; j++)
      for(pair = 0; pair < KYBER_N; pair++) {
        a.vec[j].coeffs[pair] = (int16_t)((int32_t)(next_value(&state) % 8191) - 4095);
        b.vec[j].coeffs[pair] = (int16_t)((int32_t)(next_value(&state) % 3329) - 1664);
      }
    if(!check_dot_vector(&a, &b))
      return 0;
    cases++;
  }
  fprintf(stderr, "dot_product_vectors=%u\ndot_product_coefficient_pairs=%u\ndot_product_oracle=pass\n",
          cases, cases * (KYBER_N/2));
  return 1;
}

int main(void)
{
  /* The unchanged standalone basemul test is not repeated in this driver. */
  if(!check_dot_arithmetic() || !check_kem())
    return 1;
  if(fflush(stdout) != 0 || ferror(stdout)) {
    fprintf(stderr, "Transcript flush failure.\n");
    return 2;
  }
  fprintf(stderr, "transcript=public-deterministic-test-vectors\n");
  return 0;
}
