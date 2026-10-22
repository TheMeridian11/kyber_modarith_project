#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "kem.h"
#include "fips202.h"
#include "reduce.h"

/* Expand Kyber's namespace macros before forming the linker wrapper names. */
#define JOIN_INNER(a, b) a##b
#define JOIN(a, b) JOIN_INNER(a, b)
#define WRAP(name) JOIN(__wrap_, name)
#define REAL(name) JOIN(__real_, name)

int16_t REAL(montgomery_reduce)(int32_t a);
int16_t REAL(barrett_reduce)(int16_t a);
int16_t WRAP(montgomery_reduce)(int32_t a);
int16_t WRAP(barrett_reduce)(int16_t a);

static uint64_t montgomery_calls;
static uint64_t barrett_calls;

int16_t WRAP(montgomery_reduce)(int32_t a)
{
  montgomery_calls++;
  return REAL(montgomery_reduce)(a);
}

int16_t WRAP(barrett_reduce)(int16_t a)
{
  barrett_calls++;
  return REAL(barrett_reduce)(a);
}

static void reset_counts(void)
{
  montgomery_calls = 0;
  barrett_calls = 0;
}

static uint64_t parse_number(const char *text)
{
  char *end;
  unsigned long long value;
  if(!text[0] || strspn(text, "0123456789") != strlen(text)) {
    fprintf(stderr, "Expected an unsigned decimal integer.\n");
    exit(2);
  }
  errno = 0;
  value = strtoull(text, &end, 10);
  if(errno || *end) {
    fprintf(stderr, "Invalid integer.\n");
    exit(2);
  }
  return (uint64_t)value;
}

static void put_u64_le(uint8_t out[8], uint64_t value)
{
  unsigned int j;
  for(j = 0; j < 8; j++)
    out[j] = (uint8_t)(value >> (8*j));
}

int main(int argc, char **argv)
{
  uint64_t iterations, seed, i;
  uint64_t counts[3][2];
  unsigned int operation;
  uint8_t input[32] = {'k','y','b','e','r','-','b','e','n','c','h','-','v','1',0,0};
  uint8_t coins[3*KYBER_SYMBYTES];
  uint8_t pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES];
  uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
  uint8_t ss_enc[CRYPTO_BYTES], ss_dec[CRYPTO_BYTES];
  const char *names[3] = {"keygen", "encap", "decap"};
  int key_rc, enc_rc, dec_rc, ok = 1;

  if(argc != 3) {
    fprintf(stderr, "Usage: count_reductions ITERATIONS SEED\n");
    return 2;
  }
  iterations = parse_number(argv[1]);
  seed = parse_number(argv[2]);
  if(iterations < 1 || iterations > 1000) {
    fprintf(stderr, "Iterations must be 1..1000.\n");
    return 2;
  }

  /* Check linker wiring before collecting any KEM observations. */
  reset_counts();
  if(montgomery_reduce(0) != 0 || barrett_reduce(0) != 0
      || montgomery_calls != 1 || barrett_calls != 1) {
    fprintf(stderr, "Reduction-wrapper self-check failed.\n");
    return 1;
  }
  fprintf(stderr, "wrapper_self_check=pass\ninput_mode=derand-shake256-v1\n");
  fprintf(stderr, "iterations=%" PRIu64 "\nseed=%" PRIu64 "\n", iterations, seed);
  fprintf(stderr, "performance_measurements=false\n");

  input[14] = (uint8_t)KYBER_K;
  input[15] = 1; /* Match the timing harness's measured-fixture phase. */
  put_u64_le(input + 16, seed);
  printf("parameter_set,operation,iteration,montgomery_calls,barrett_calls,roundtrip_ok\n");
  for(i = 0; i < iterations; i++) {
    put_u64_le(input + 24, i);
    shake256(coins, sizeof(coins), input, sizeof(input));

    reset_counts();
    key_rc = crypto_kem_keypair_derand(pk, sk, coins);
    counts[0][0] = montgomery_calls;
    counts[0][1] = barrett_calls;

    reset_counts();
    enc_rc = crypto_kem_enc_derand(ct, ss_enc, pk, coins + 2*KYBER_SYMBYTES);
    counts[1][0] = montgomery_calls;
    counts[1][1] = barrett_calls;

    reset_counts();
    dec_rc = crypto_kem_dec(ss_dec, ct, sk);
    counts[2][0] = montgomery_calls;
    counts[2][1] = barrett_calls;

    ok = key_rc == 0 && enc_rc == 0 && dec_rc == 0
      && memcmp(ss_enc, ss_dec, CRYPTO_BYTES) == 0;
    for(operation = 0; operation < 3; operation++)
      printf("%s,%s,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%d\n",
             CRYPTO_ALGNAME, names[operation], i,
             counts[operation][0], counts[operation][1], ok);
    if(!ok)
      break;
  }
  if(fflush(stdout) != 0 || ferror(stdout)) {
    perror("CSV output");
    return 2;
  }
  if(!ok)
    fprintf(stderr, "Round-trip failure; partial CSV retained.\n");
  return ok ? 0 : 1;
}
