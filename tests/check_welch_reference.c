/* Independent numerical oracle: pinned upstream dudect Welch implementation. */
#define DUDECT_IMPLEMENTATION
#include "reference/dudect/dudect.h"
void prepare_inputs(dudect_config_t *c,uint8_t *data,uint8_t *classes) {(void)c;(void)data;(void)classes;}
uint8_t do_one_computation(uint8_t *data) {(void)data;return 0;}
int main(void) {
  ttest_ctx_t ctx;unsigned int c;double x;t_init(&ctx);
  while(scanf("%u %lf",&c,&x)==2) {if(c>1) return 2;t_push(&ctx,x,(uint8_t)c);}
  if(ctx.n[0]<2||ctx.n[1]<2) return 2;
  printf("%.17g\n",t_compute(&ctx));return 0;
}
