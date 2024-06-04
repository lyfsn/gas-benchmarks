


#!/bin/bash

nohup \
  ./run.sh \
  -t "tests/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 4 \
  -o results_4 \
  > output.log 2>&1 &


