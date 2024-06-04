


#!/bin/bash

./run.sh \
  -t "tests1/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 1 \
  -o "results1"


./run.sh \
  -t "tests1/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 1 \
  -o "results2"

./run.sh \
  -t "tests1/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 1 \
  -o "results3"




python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "test1" \
  --resultsPath "results1"

python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "test1" \
  --resultsPath "results2"

python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "test1" \
  --resultsPath "results3"