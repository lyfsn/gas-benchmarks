


#!/bin/bash

nohup \
  ./run.sh \
  -t "tests3/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 4 \
  -o results3_1 \
  > output.log 2>&1 &




./run.sh \
  -t "tests3/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 1 \
  -o results3_1 

python3 report_html.py \
  --clients "nethermind,geth,reth,erigon,besu" \
  --testsPath "tests3" \
  --resultsPath "results3_1"




./run.sh \
  -t "tests3/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind" \
  -r 1 \
  -o results3_1 

python3 report_html.py \
  --clients "nethermind" \
  --testsPath "tests3" \
  --resultsPath "results3_1" \
  --runs 1