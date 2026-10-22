#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "kem.h"
#include "ntt.h"
#include "fips202.h"

#ifndef VALIDATION_CASES
#define VALIDATION_CASES 100
#endif
#ifndef EXPECT_FUSED
#define EXPECT_FUSED 0
#endif

/* Test-only ordinary modular arithmetic; never linked into timing builds. */
static int32_t canonical(int64_t value)
{
  int32_t residue = (int32_t)(value % KYBER_Q);
  return residue < 0 ? residue + KYBER_Q : residue;
}

static int check_pair(const int16_t a[2], const int16_t b[2], int16_t zeta)
{
  int16_t r[2];
  int32_t expected0, expected1;
  const int32_t r_inverse = 169; /* 65536 * 169 == 1 modulo 3329. */
  int32_t root = canonical((int64_t)zeta * r_inverse);
  int32_t limit = EXPECT_FUSED ? KYBER_Q - 1 : 2*(KYBER_Q - 1);

  expected0 = canonical(
      ((int64_t)a[0]*b[0] + (int64_t)a[1]*b[1]*root) * r_inverse);
  expected1 = canonical(
      ((int64_t)a[0]*b[1] + (int64_t)a[1]*b[0]) * r_inverse);
  basemul(r, a, b, zeta);
  if(canonical(r[0]) != expected0 || canonical(r[1]) != expected1
      || r[0] < -limit || r[0] > limit || r[1] < -limit || r[1] > limit) {
    fprintf(stderr, "Base multiplication residue or output-bound failure.\n");
    return 0;
  }
  return 1;
}

static uint32_t next_value(uint32_t *state)
{
  *state = *state * UINT32_C(1664525) + UINT32_C(1013904223);
  return *state;
}

static int check_arithmetic(void)
{
  unsigned int z, signs, i;
  uint32_t state = 1;
  int16_t a[2], b[2], zeta;
  unsigned int cases = 0;

  /* All sign corners of the conservative caller envelope, for every twiddle. */
  for(z = 0; z < 128; z++) {
    zeta = zetas[64 + z/2];
    if(z & 1)
      zeta = (int16_t)-zeta;
    for(signs = 0; signs < 16; signs++) {
      a[0] = (signs & 1) ? 4095 : -4095;
      a[1] = (signs & 2) ? 4095 : -4095;
      b[0] = (signs & 4) ? 1664 : -1664;
      b[1] = (signs & 8) ? 1664 : -1664;
      if(!check_pair(a, b, zeta))
        return 0;
      cases++;
    }
    a[0] = a[1] = b[0] = b[1] = 0;
    if(!check_pair(a, b, zeta))
      return 0;
    cases++;
  }
  /* Deterministic interior samples, supplementary to the range argument. */
  for(i = 0; i < 1024; i++) {
    a[0] = (int16_t)((int32_t)(next_value(&state) % 8191) - 4095);
    a[1] = (int16_t)((int32_t)(next_value(&state) % 8191) - 4095);
    b[0] = (int16_t)((int32_t)(next_value(&state) % 3329) - 1664);
    b[1] = (int16_t)((int32_t)(next_value(&state) % 3329) - 1664);
    zeta = zetas[64 + (i % 64)];
    if(i & 64)
      zeta = (int16_t)-zeta;
    if(!check_pair(a, b, zeta))
      return 0;
    cases++;
  }
  fprintf(stderr, "basemul_cases=%u\nbasemul_oracle=pass\n", cases);
  return 1;
}

static void put_u64_le(uint8_t out[8], uint64_t value)
{
  unsigned int j;
  for(j = 0; j < 8; j++)
    out[j] = (uint8_t)(value >> (8*j));
}

static int emit(const uint8_t *data, size_t size)
{
  if(fwrite(data, 1, size, stdout) != size) {
    fprintf(stderr, "Transcript write failure.\n");
    return 0;
  }
  return 1;
}

static int check_kem(void)
{
  uint8_t input[32] = {'k','y','b','e','r','-','b','e','n','c','h','-','v','1',0,1};
  uint8_t coins[3*KYBER_SYMBYTES];
  uint8_t pk[CRYPTO_PUBLICKEYBYTES], bad_pk[CRYPTO_PUBLICKEYBYTES];
  uint8_t sk[CRYPTO_SECRETKEYBYTES], bad_sk[CRYPTO_SECRETKEYBYTES];
  uint8_t ct[CRYPTO_CIPHERTEXTBYTES], bad_ct[CRYPTO_CIPHERTEXTBYTES];
  uint8_t ss_enc[CRYPTO_BYTES], ss_dec[CRYPTO_BYTES];
  unsigned int i;

  input[14] = (uint8_t)KYBER_K;
  put_u64_le(input + 16, 1);
  for(i = 0; i < VALIDATION_CASES; i++) {
    put_u64_le(input + 24, i);
    shake256(coins, sizeof(coins), input, sizeof(input));
    if(crypto_kem_keypair_derand(pk, sk, coins) != 0
        || crypto_kem_enc_derand(ct, ss_enc, pk, coins + 2*KYBER_SYMBYTES) != 0
        || crypto_kem_dec(ss_dec, ct, sk) != 0
        || memcmp(ss_enc, ss_dec, CRYPTO_BYTES) != 0) {
      fprintf(stderr, "Valid exchange failed at fixture %u.\n", i);
      return 0;
    }
    if(!emit(pk, sizeof(pk)) || !emit(sk, sizeof(sk)) || !emit(ct, sizeof(ct))
        || !emit(ss_enc, sizeof(ss_enc)) || !emit(ss_dec, sizeof(ss_dec)))
      return 0;

    memcpy(bad_ct, ct, sizeof(ct));
    bad_ct[i % sizeof(ct)] ^= 1;
    if(crypto_kem_dec(ss_dec, bad_ct, sk) != 0
        || memcmp(ss_enc, ss_dec, CRYPTO_BYTES) == 0) {
      fprintf(stderr, "Corrupted-ciphertext check failed at fixture %u.\n", i);
      return 0;
    }
    if(!emit(ss_dec, sizeof(ss_dec)))
      return 0;

    shake256(bad_ct, sizeof(bad_ct), coins, sizeof(coins));
    if(crypto_kem_dec(ss_dec, bad_ct, sk) != 0)
      return 0;
    if(!emit(ss_dec, sizeof(ss_dec)))
      return 0;

    /* Exercise arbitrary secret-key bytes, including the 12-bit maximum. */
    if(i == 0)
      memset(bad_sk, 0xff, sizeof(bad_sk));
    else
      shake256(bad_sk, sizeof(bad_sk), coins, sizeof(coins));
    if(crypto_kem_dec(ss_dec, ct, bad_sk) != 0)
      return 0;
    if(!emit(ss_dec, sizeof(ss_dec)))
      return 0;

    /* Compare this pinned implementation's handling of noncanonical keys. */
    memcpy(bad_pk, pk, sizeof(pk));
    memset(bad_pk, 0xff, KYBER_POLYVECBYTES);
    if(crypto_kem_enc_derand(bad_ct, ss_dec, bad_pk,
                            coins + 2*KYBER_SYMBYTES) != 0)
      return 0;
    if(!emit(bad_ct, sizeof(bad_ct)) || !emit(ss_dec, sizeof(ss_dec)))
      return 0;
  }
  fprintf(stderr, "kem_fixtures=%u\nkem_checks=pass\n", (unsigned int)VALIDATION_CASES);
  return 1;
}

int main(void)
{
  if(!check_arithmetic() || !check_kem())
    return 1;
  if(fflush(stdout) != 0 || ferror(stdout)) {
    fprintf(stderr, "Transcript flush failure.\n");
    return 2;
  }
  fprintf(stderr, "transcript=public-deterministic-test-vectors\n");
  return 0;
}
