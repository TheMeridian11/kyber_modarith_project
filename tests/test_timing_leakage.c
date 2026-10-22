/* EXP-008: native, bounded timing observations. No production instrumentation. */
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sched.h>
#include <cpuid.h>
#include <x86intrin.h>
#include "params.h"
#include "poly.h"
#include "polyvec.h"
#include "ntt.h"
#include "indcpa.h"
#if LEAK_VARIANT != 0 && LEAK_VARIANT != 3 && LEAK_VARIANT != 5
#error LEAK_VARIANT must be original (0), EXP-003 (3), or EXP-005 (5)
#endif
#define BATCH 1000u
#define CALIBRATION 2000u
#define WARMUP 1000u
#define NOIPA __attribute__((noipa))
typedef struct { polyvec a,b; poly r,e; uint8_t sk[KYBER_INDCPA_SECRETKEYBYTES]; uint32_t word; } fixture;
static fixture work;
static uint8_t ciphertext[KYBER_INDCPA_BYTES], message[KYBER_INDCPA_MSGBYTES];
static volatile uint32_t sink;
static uint32_t next_word(uint32_t *s) { *s ^= *s << 13; *s ^= *s >> 17; *s ^= *s << 5; return *s; }
static NOIPA void basemul_path(void) {
  for(unsigned int i=0;i<KYBER_N/2;i++) {
    int16_t z=zetas[64+i/2]; if(i&1) z=(int16_t)-z;
    basemul(&work.r.coeffs[2*i],&work.a.vec[0].coeffs[2*i],&work.b.vec[0].coeffs[2*i],z);
  }
}
static NOIPA void dot_path(void) { polyvec_basemul_acc_montgomery(&work.r,&work.a,&work.b); }
static NOIPA void inverse_path(void) { invntt(work.r.coeffs); }
static NOIPA void error_path(void) {
#if LEAK_VARIANT == 5
  ntt(work.e.coeffs);
#else
  poly_ntt(&work.e);
#endif
  poly_add(&work.r,&work.r,&work.e); poly_reduce(&work.r);
}
static NOIPA void keygen_path(void) {
  polyvec_basemul_acc_montgomery(&work.r,&work.a,&work.b); poly_tomont(&work.r); error_path();
}
static NOIPA void decrypt_path(void) { indcpa_dec(message,ciphertext,work.sk); }
static NOIPA void positive_control(void) {
  if(work.word&1u) { for(unsigned int i=0;i<64;i++) sink = sink*1664525u+1013904223u; }
  else sink = sink*1664525u+1013904223u;
}
static NOIPA void negative_control(void) { sink = work.word*17u+29u; }
static int16_t choose(uint32_t *s,unsigned int cls,unsigned int profile,unsigned int i,int lo,int hi) {
  int inner=profile ? 1:0;
  int random=(int)(next_word(s)%(uint32_t)(hi-lo+1-2*inner))+lo+inner;
  int fixed=profile ? ((i&1u)?hi:lo) : 0;
  return (int16_t)(cls?random:fixed);
}
static void prepare(fixture *f,unsigned int cls,unsigned int profile,int first,int key,int error,uint32_t *s) {
  for(unsigned int j=0;j<KYBER_K;j++) for(unsigned int i=0;i<KYBER_N;i++) {
    unsigned int n=j*KYBER_N+i;
    f->a.vec[j].coeffs[i]=first?choose(s,cls,profile,n,0,4095):(int16_t)((n*17u+31u)%(key?3329u:4096u));
    f->b.vec[j].coeffs[i]=first?(int16_t)((int)((n*29u+7u)%3329u)-1664):choose(s,cls,profile,n,-1664,1664);
  }
  for(unsigned int i=0;i<KYBER_N;i++) {
    f->r.coeffs[i]=error?3328:choose(s,cls,profile,i,-1664,1664);
    f->e.coeffs[i]=choose(s,cls,profile,i,-KYBER_ETA1,KYBER_ETA1);
  }
  for(unsigned int j=0;j<KYBER_K;j++) for(unsigned int i=0;i<KYBER_N/2;i++) {
    uint16_t a=(uint16_t)f->a.vec[j].coeffs[2*i],b=(uint16_t)f->a.vec[j].coeffs[2*i+1];
    unsigned int n=j*KYBER_POLYBYTES+3*i;
    f->sk[n]=(uint8_t)a; f->sk[n+1]=(uint8_t)((a>>8)|(b<<4)); f->sk[n+2]=(uint8_t)(b>>4);
  }
  f->word=cls; /* Controls deliberately encode class in their secret input. */
}
static inline uint64_t stamp(unsigned int *aux) {
  __asm__ volatile("" ::: "memory");
  _mm_mfence(); _mm_lfence(); uint64_t t=__rdtscp(aux); _mm_lfence();
  __asm__ volatile("" ::: "memory"); return t;
}
static void encode(uint8_t *p,uint64_t t,uint32_t a,uint32_t b,uint8_t c) {
  for(unsigned int i=0;i<8;i++) p[i]=(uint8_t)(t>>(8*i));
  for(unsigned int i=0;i<4;i++) {p[8+i]=(uint8_t)(a>>(8*i));p[12+i]=(uint8_t)(b>>(8*i));}p[16]=c;
}
int main(int argc,char **argv) {
  if(argc!=6) {fprintf(stderr,"usage: PATH PROFILE SAMPLES SEED CPU\n");return 2;}
  char *end; unsigned long profile=strtoul(argv[2],&end,10);if(*end||profile>1) return 2;
  unsigned long n=strtoul(argv[3],&end,10);if(*end||n<2000||n>1000000||n%BATCH) return 2;
  unsigned long seed=strtoul(argv[4],&end,10);if(*end||!seed||seed>UINT32_MAX) return 2;
  unsigned long cpu=strtoul(argv[5],&end,10);if(*end||cpu>=CPU_SETSIZE) return 2;
  unsigned int a,b,c,d;
  if(__get_cpuid_max(0x80000000u,0)<0x80000001u || !__get_cpuid(0x80000001u,&a,&b,&c,&d) || !(d&(1u<<27))) return 3;
  cpu_set_t set;CPU_ZERO(&set);CPU_SET(cpu,&set);
  if(sched_setaffinity(0,sizeof(set),&set)||sched_getaffinity(0,sizeof(set),&set)||CPU_COUNT(&set)!=1||!CPU_ISSET(cpu,&set)) return 3;
  void (*fn)(void)=NULL;int first=0,key=0,error=0;
  if(!strcmp(argv[1],"basemul")||!strcmp(argv[1],"basemul-first")) fn=basemul_path;
  if(!strcmp(argv[1],"dot")||!strcmp(argv[1],"dot-first")) fn=dot_path;
  if(!strcmp(argv[1],"inverse")) fn=inverse_path;
  if(!strcmp(argv[1],"error-path")) {fn=error_path;error=1;}
  if(!strcmp(argv[1],"keygen-dot")) {fn=keygen_path;key=1;}
  if(!strcmp(argv[1],"indcpa-dec")) fn=decrypt_path;
  if(strstr(argv[1],"-first")||fn==decrypt_path) first=1;
  if(!strcmp(argv[1],"positive-control")) fn=positive_control;
  if(!strcmp(argv[1],"negative-control")) fn=negative_control;
  if(!fn) return 2;
  uint8_t pk[KYBER_INDCPA_PUBLICKEYBYTES],sk[KYBER_INDCPA_SECRETKEYBYTES],coins[KYBER_SYMBYTES]={0},plain[KYBER_INDCPA_MSGBYTES]={0};
  indcpa_keypair_derand(pk,sk,coins);indcpa_enc(ciphertext,plain,pk,coins);indcpa_dec(message,ciphertext,sk);
  if(memcmp(plain,message,sizeof(plain))) return 4;
  fixture *fixtures=calloc(BATCH,sizeof(fixture));uint8_t *raw=calloc(n+CALIBRATION,17);uint8_t classes[BATCH];
  if(!fixtures||!raw) return 5;
  uint32_t order=(uint32_t)seed,values=(uint32_t)seed^0x9e3779b9u;if(!values) values=1;
  prepare(&work,1,(unsigned int)profile,first,key,error,&values);
  for(unsigned int i=0;i<WARMUP;i++) {prepare(&work,1,(unsigned int)profile,first,key,error,&values);fn();}
  for(size_t start=0;start<n+CALIBRATION;start+=BATCH) {
    for(unsigned int i=0;i<BATCH;i++) classes[i]=(uint8_t)(i&1u);
    for(unsigned int i=BATCH-1;i>0;i--) {unsigned int j=next_word(&order)%(i+1);uint8_t tmp=classes[i];classes[i]=classes[j];classes[j]=tmp;}
    for(unsigned int i=0;i<BATCH;i++) prepare(&fixtures[i],classes[i],(unsigned int)profile,first,key,error,&values);
    for(unsigned int i=0;i<BATCH;i++) {
      memcpy(&work,&fixtures[i],sizeof(work)); /* Same addresses/size, outside measured interval. */
      unsigned int aux0,aux1;uint64_t t0=stamp(&aux0);fn();uint64_t t1=stamp(&aux1);
      encode(raw+17*(start+i),t1>=t0?t1-t0:0,aux0,aux1,classes[i]);
      uint32_t sum=0;for(unsigned int j=0;j<KYBER_N;j++) sum+=(uint16_t)work.r.coeffs[j];
      for(unsigned int j=0;j<sizeof(message);j++) sum+=message[j];
      sink^=sum;
    }
  }
  if(fwrite("KTL00801",1,8,stdout)!=8||fwrite(raw,17,n+CALIBRATION,stdout)!=n+CALIBRATION||fflush(stdout)) return 6;
  fprintf(stderr,"{\"path\":\"%s\",\"profile\":%lu,\"samples\":%lu,\"calibration\":%u,\"warmup\":%u,\"seed\":%lu,\"cpu\":%lu,\"checksum\":%u}\n",argv[1],profile,n,CALIBRATION,WARMUP,seed,cpu,(unsigned int)sink);
  free(fixtures);free(raw);return 0;
}
