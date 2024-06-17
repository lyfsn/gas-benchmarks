


#!/bin/bash

nohup \
  ./run.sh \
  -t "tests/" \
  -w "warmup/warmup-1000bl-16wi-24tx.txt" \
  -c "nethermind,geth,reth,erigon,besu" \
  -r 8 \
  -o "results" \
  > output.log 2>&1 &



./run.sh \
  -t "testburnt/" \
  -w "./testburnt/Burnt/Burnt_90M.txt" \
  -c "nethermind" \
  -r 1 \
  -o "results"


./run.sh \
  -t "testburnt/" \
  -w "./testburnt/Burnt/Burnt_90M.txt" \
  -c "nethermind,erigon,geth,reth,besu" \
  -r 1 \
  -o "results"


nohup \
  ./run.sh \
  -t "testburnt/" \
  -w "./testburnt/Burnt/Burnt_90M.txt" \
  -c "nethermind,erigon,geth,reth,besu" \
  -r 8 \
  -o "results" \
  > output.log 2>&1 &
