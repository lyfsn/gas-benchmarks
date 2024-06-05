


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
  -r 4 \
  -o results3_1 