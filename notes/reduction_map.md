# Reduction Map

## Files inspected

- reduce.c
- poly.c
- polyvec.c
- ntt.c

## Reduction functions found

- montgomery_reduce()
- barrett_reduce()
- poly_reduce()
- polyvec_reduce()
- poly_csubq()

## Initial observations

- NTT uses modular multiplication and reduction heavily.
- Polynomial/vector operations call reduction functions after arithmetic.
- Candidate optimisation areas:
  - polynomial add/subtract
  - polyvec reduction
  - NTT/INTT butterfly operations
