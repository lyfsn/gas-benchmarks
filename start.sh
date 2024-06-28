


#!/bin/bash

nohup \
  ./run.sh \
  -t "testburnt/" \
  -w "./testburntwarm/warm.txt" \
  -c "nethermind,erigon,geth,reth,besu" \
  -r 8 \
  -o "results" \
  > output.log 2>&1 &
