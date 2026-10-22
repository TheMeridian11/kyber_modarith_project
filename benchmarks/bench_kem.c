#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "kem.h"
#include "fips202.h"

typedef struct {
  uint64_t elapsed_ns[3];
  int roundtrip_ok;
} sample;

static uint64_t now_ns(void)
{
  struct timespec value;
  if(clock_gettime(CLOCK_MONOTONIC_RAW, &value) != 0) {
    perror("clock_gettime");
    exit(2);
  }
  return (uint64_t)value.tv_sec * UINT64_C(1000000000)
       + (uint64_t)value.tv_nsec;
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

static int measure(sample *result, uint64_t seed, uint64_t index, int measured)
{
  uint8_t input[32] = {'k','y','b','e','r','-','b','e','n','c','h','-','v','1',0,0};
  uint8_t coins[3*KYBER_SYMBYTES];
  uint8_t pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES];
  uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
  uint8_t ss_enc[CRYPTO_BYTES], ss_dec[CRYPTO_BYTES];
  uint64_t start, end;
  int key_rc, enc_rc, dec_rc;

  input[14] = (uint8_t)KYBER_K;
  input[15] = (uint8_t)measured;
  put_u64_le(input + 16, seed);
  put_u64_le(input + 24, index);
  /* Public reproducible benchmark fixtures, generated outside timing windows. */
  shake256(coins, sizeof(coins), input, sizeof(input));

  start = now_ns();
  key_rc = crypto_kem_keypair_derand(pk, sk, coins);
  end = now_ns();
  result->elapsed_ns[0] = end - start;

  start = now_ns();
  enc_rc = crypto_kem_enc_derand(ct, ss_enc, pk, coins + 2*KYBER_SYMBYTES);
  end = now_ns();
  result->elapsed_ns[1] = end - start;

  start = now_ns();
  dec_rc = crypto_kem_dec(ss_dec, ct, sk);
  end = now_ns();
  result->elapsed_ns[2] = end - start;

  result->roundtrip_ok = key_rc == 0 && enc_rc == 0 && dec_rc == 0
                     && memcmp(ss_enc, ss_dec, CRYPTO_BYTES) == 0;
  return result->roundtrip_ok;
}

int main(int argc, char **argv)
{
  uint64_t iterations, warmup, seed, i, count = 0;
  uint64_t probe_min = UINT64_MAX;
  unsigned int operation;
  int ok = 1;
  sample discarded, *samples;
  struct timespec resolution;
  const char *names[3] = {"keygen", "encap", "decap"};

  if(argc != 4) {
    fprintf(stderr, "Usage: bench_kem ITERATIONS WARMUP SEED\n");
    return 2;
  }
  iterations = parse_number(argv[1]);
  warmup = parse_number(argv[2]);
  seed = parse_number(argv[3]);
  if(iterations < 1 || iterations > 1000000 || warmup > 1000000) {
    fprintf(stderr, "Iterations must be 1..1000000; warmup 0..1000000.\n");
    return 2;
  }
  samples = calloc((size_t)iterations, sizeof(*samples));
  if(!samples) {
    perror("calloc");
    return 2;
  }
  if(clock_getres(CLOCK_MONOTONIC_RAW, &resolution) != 0) {
    perror("clock_getres");
    free(samples);
    return 2;
  }
  for(i = 0; i < 1000; i++) {
    uint64_t start = now_ns();
    uint64_t delta = now_ns() - start;
    if(delta < probe_min)
      probe_min = delta;
  }
  fprintf(stderr, "timer=CLOCK_MONOTONIC_RAW\nunit=ns\n");
  fprintf(stderr, "clock_resolution_ns=%" PRIu64 "\n",
          (uint64_t)resolution.tv_sec * UINT64_C(1000000000)
          + (uint64_t)resolution.tv_nsec);
  fprintf(stderr, "empty_timer_pair_min_ns=%" PRIu64 "\n", probe_min);
  fprintf(stderr, "iterations=%" PRIu64 "\nwarmup=%" PRIu64 "\nseed=%" PRIu64 "\n",
          iterations, warmup, seed);
  fprintf(stderr, "input_mode=derand-shake256-v1\n");

  for(i = 0; i < warmup; i++) {
    if(!measure(&discarded, seed, i, 0)) {
      fprintf(stderr, "Warmup round-trip failure at iteration %" PRIu64 "\n", i);
      free(samples);
      return 1;
    }
  }
  /* Buffer measurements: no CSV formatting or file I/O between samples. */
  for(i = 0; i < iterations; i++) {
    ok = measure(&samples[i], seed, i, 1);
    count++;
    if(!ok)
      break;
  }
  printf("parameter_set,operation,iteration,elapsed_ns,roundtrip_ok\n");
  for(i = 0; i < count; i++)
    for(operation = 0; operation < 3; operation++)
      printf("%s,%s,%" PRIu64 ",%" PRIu64 ",%d\n",
             CRYPTO_ALGNAME, names[operation], i,
             samples[i].elapsed_ns[operation], samples[i].roundtrip_ok);
  if(fflush(stdout) != 0 || ferror(stdout)) {
    perror("CSV output");
    free(samples);
    return 2;
  }
  free(samples);
  if(!ok) {
    fprintf(stderr, "Measured round-trip failure; partial CSV retained.\n");
    return 1;
  }
  return 0;
}
