


#!/bin/bash

./run.sh \
  -t "tests2/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 8 \
  -o "results11"


./run.sh \
  -t "tests2/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 8 \
  -o "results12"

./run.sh \
  -t "tests2/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 8 \
  -o "results13"




python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "tests2" \
  --resultsPath "results11"

python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "tests2" \
  --resultsPath "results12"

python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "tests2" \
  --resultsPath "results13"







./run.sh \
  -t "tests/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "geth" \
  -r 1 \
  -o "results_geth_1"