#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASELINE_DIR="$ROOT_DIR/implementation/kyber-baseline-ref"
RESULT_DIR="$ROOT_DIR/results/baseline/$(date +%Y-%m-%d_%H-%M-%S)"

mkdir -p "$RESULT_DIR"

echo "Running baseline Kyber benchmarks..."
echo "Results will be saved to: $RESULT_DIR"

cd "$BASELINE_DIR"

make clean
make

for ALG in 512 768 1024; do
    echo "Running correctness test for Kyber$ALG..."
    ./test/test_kyber$ALG > "$RESULT_DIR/kyber${ALG}_correctness.txt"

    echo "Running speed test for Kyber$ALG..."
    ./test/test_speed$ALG > "$RESULT_DIR/kyber${ALG}_speed.txt"
done

echo "Baseline benchmark complete."
