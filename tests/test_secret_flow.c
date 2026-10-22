/* EXP-007: bounded Memcheck secret-flow harness; no production edits. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <valgrind/memcheck.h>
#include "params.h"
#include "poly.h"
#include "polyvec.h"
#include "ntt.h"
#include "indcpa.h"

#ifndef FLOW_VARIANT
#error FLOW_VARIANT must be 0 (original), 5 (EXP-005), or 6 (EXP-006)
#endif
#if FLOW_VARIANT != 0 && FLOW_VARIANT != 5 && FLOW_VARIANT != 6
#error Invalid FLOW_VARIANT
#endif

#define FLOW_CASES 8
#define SECRET(x) ((void)VALGRIND_MAKE_MEM_UNDEFINED(&(x), sizeof(x)))
#define PUBLIC(x) ((void)VALGRIND_MAKE_MEM_DEFINED(&(x), sizeof(x)))
static volatile uint32_t sink;
static uint32_t state = 1;
static uint32_t next_word(void)
{
  state ^= state << 13;
  state ^= state >> 17;
  state ^= state << 5;
  return state;
}

/* All class selection and fixture generation happens before marking. */
static int16_t value(unsigned int pattern, unsigned int i, int bound)
{
  switch(pattern) {
    case 0: return 0;
    case 1: return (int16_t)bound;
    case 2: return (int16_t)-bound;
    case 3: return (int16_t)((i & 1) ? bound : -bound);
    case 4: return (int16_t)((i & 8) ? bound : -bound);
    default: return (int16_t)((int)(next_word() % (uint32_t)(2*bound+1)) - bound);
  }
}
static void observe(poly *r)
{
  unsigned int i;
  PUBLIC(*r); /* Explicit test boundary: never inside a production function. */
  for(i = 0; i < KYBER_N; i++) sink += (uint16_t)r->coeffs[i];
}

/* Observable volatile stores force a real conditional branch at -O3. */
__attribute__((noinline)) static void positive_branch(volatile uint32_t *secret)
{
  if(*secret & 1) { sink = 17; sink += 29; }
  else { sink = 43; sink += 59; }
}
__attribute__((noinline)) static void positive_address(volatile uint32_t *secret)
{
  volatile uint32_t table[2] = {17, 29};
  sink = table[*secret & 1];
}
__attribute__((noinline)) static void negative_control(volatile uint32_t *secret)
{
  sink = (*secret * 17u) ^ 29u;
}
static int controls(const char *name, int taint)
{
  volatile uint32_t secret = 1;
  if(taint) SECRET(secret);
  if(!strcmp(name, "positive-branch")) positive_branch(&secret);
  else if(!strcmp(name, "positive-address")) positive_address(&secret);
  else if(!strcmp(name, "negative-control")) negative_control(&secret);
  else return 0;
  PUBLIC(secret);
  PUBLIC(sink);
  return 1;
}

static int kernels(const char *name, int taint)
{
  polyvec a, b;
  poly r, e;
  unsigned int pattern, i, j, pair;
  int bound, first_secret = !strcmp(name,"basemul-first") || !strcmp(name,"dot-first");
  if(strcmp(name,"basemul") && strcmp(name,"basemul-first") && strcmp(name,"dot")
      && strcmp(name,"dot-first") && strcmp(name,"inverse")
      && strcmp(name,"error-path") && strcmp(name,"keygen-dot")) return 0;
  for(pattern = 0; pattern < FLOW_CASES; pattern++) {
    bound = !strcmp(name,"keygen-dot") ? KYBER_Q-1 : 4095;
    for(j = 0; j < KYBER_K; j++) {
      for(i = 0; i < KYBER_N; i++) {
        a.vec[j].coeffs[i] = (int16_t)((pattern == 1 || pattern == 2)
            ? bound : (int)(next_word() % (uint32_t)(bound+1)));
        if(first_secret) {
          /* Encoded secret-key envelope for the first operand in decryption. */
          switch(pattern) {
            case 0: a.vec[j].coeffs[i] = 0; break;
            case 1: a.vec[j].coeffs[i] = (int16_t)bound; break;
            case 2: a.vec[j].coeffs[i] = (int16_t)(bound/2); break;
            case 3: a.vec[j].coeffs[i] = (int16_t)((i & 1) ? bound : 0); break;
            case 4: a.vec[j].coeffs[i] = (int16_t)((i & 8) ? bound : 0); break;
            default: break; /* Deterministic interior value already prepared. */
          }
          b.vec[j].coeffs[i] = (int16_t)((int)(next_word() % 3329u) - 1664);
        } else b.vec[j].coeffs[i] = value(pattern, i+j, 1664);
      }
    }
    for(i = 0; i < KYBER_N; i++) {
      r.coeffs[i] = value(pattern, i, 1664);
      e.coeffs[i] = value(pattern, i, KYBER_ETA1);
    }
    if(!strcmp(name,"inverse")) {
      if(taint) SECRET(r);
      invntt(r.coeffs);
    } else if(!strcmp(name,"error-path")) {
      /* EXP-005 defers poly_ntt's centring only for the keygen error. */
      if(taint) SECRET(e);
#if FLOW_VARIANT == 0
      poly_ntt(&e);
#else
      ntt(e.coeffs);
#endif
      for(i = 0; i < KYBER_N; i++) r.coeffs[i] = 3328;
      poly_add(&r, &r, &e);
      poly_reduce(&r);
    } else {
      if(taint) {
        if(first_secret) SECRET(a);
        else SECRET(b);
      }
      if(!strcmp(name,"basemul") || !strcmp(name,"basemul-first")) {
        for(pair = 0; pair < KYBER_N/2; pair++) {
          int16_t zeta = zetas[64 + pair/2];
          if(pair & 1) zeta = (int16_t)-zeta;
          basemul(&r.coeffs[2*pair], &a.vec[0].coeffs[2*pair],
                  &b.vec[0].coeffs[2*pair], zeta);
        }
      } else if(!strcmp(name,"dot") || !strcmp(name,"dot-first")) {
        polyvec_basemul_acc_montgomery(&r, &a, &b);
      } else {
#if FLOW_VARIANT == 6
        polyvec_basemul_acc_keygen(&r, &a, &b);
#else
        polyvec_basemul_acc_montgomery(&r, &a, &b);
        poly_tomont(&r);
#endif
        /* Separate synthetic error stresses the proved final-addition bound. */
        for(i = 0; i < KYBER_N; i++)
          e.coeffs[i] = value(pattern, i, KYBER_ETA1 + 7*(KYBER_Q-1));
        if(taint) SECRET(e);
        poly_add(&r, &r, &e);
        poly_reduce(&r);
      }
    }
    observe(&r);
    PUBLIC(a); PUBLIC(b); PUBLIC(e);
  }
  return 1;
}

static int integration(int taint)
{
  uint8_t pk[KYBER_INDCPA_PUBLICKEYBYTES], sk[KYBER_INDCPA_SECRETKEYBYTES];
  uint8_t ct[KYBER_INDCPA_BYTES], m[KYBER_INDCPA_MSGBYTES], out[KYBER_INDCPA_MSGBYTES];
  uint8_t keycoins[KYBER_SYMBYTES], enccoins[KYBER_SYMBYTES];
  unsigned int pattern, i;
  for(pattern = 0; pattern < FLOW_CASES; pattern++) {
    for(i = 0; i < KYBER_SYMBYTES; i++) {
      keycoins[i] = (uint8_t)next_word(); enccoins[i] = (uint8_t)next_word();
      m[i] = (uint8_t)next_word();
    }
    indcpa_keypair_derand(pk, sk, keycoins);
    indcpa_enc(ct, m, pk, enccoins);
    switch(pattern % 4) {
      case 1: ct[pattern] ^= 1; break;
      case 2: memset(ct, 255, sizeof(ct)); break;
      case 3: for(i = 0; i < sizeof(ct); i++) ct[i] = (uint8_t)next_word(); break;
      default: break;
    }
    if(taint) SECRET(sk);
    indcpa_dec(out, ct, sk);
    PUBLIC(out); PUBLIC(sk); /* Declassification only after complete IND-CPA call. */
    if(pattern % 4 == 0 && memcmp(m, out, sizeof(m))) return 0;
    for(i = 0; i < sizeof(out); i++) sink += out[i];
  }
  return 1;
}
int main(int argc, char **argv)
{
  int taint, ok;
  if(argc != 3 || (strcmp(argv[2],"marked") && strcmp(argv[2],"defined"))) {
    fprintf(stderr,"usage: test_secret_flow PATH marked|defined\n"); return 2;
  }
  taint = !strcmp(argv[2],"marked");
  if(!RUNNING_ON_VALGRIND) {
    fprintf(stderr,"Memcheck execution is required, including for defined controls.\n"); return 2;
  }
  if(!strcmp(argv[1],"indcpa-dec")) ok = integration(taint);
  else ok = controls(argv[1],taint) || kernels(argv[1],taint);
  if(!ok) { fprintf(stderr,"Unknown path or integration mismatch.\n"); return 2; }
  PUBLIC(sink);
  printf("path=%s mode=%s cases=%d checksum=%u\n",argv[1],argv[2],
         strstr(argv[1],"control") || strstr(argv[1],"positive") ? 1 : FLOW_CASES,
         (unsigned int)sink);
  return 0;
}
