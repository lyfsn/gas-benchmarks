


#!/bin/bash

./run.sh \
  -t "testburnt/" \
  -w "./testburntwarm/warm.txt" \
  -c "reth" \
  -r 1 \
  -o "results" 

./run.sh \
  -t "testburnt/" \
  -w "./testburntwarm/warm.txt" \
  -c "nethermind" \
  -r 1 \
  -o "results" 

./run.sh \
  -t "testburnt/" \
  -w "./testburntwarm/warm.txt" \
  -c "erigon" \
  -r 1 \
  -o "results" 

python3 report_tables.py --resultsPath results --clients reth --testsPath testburnt --runs 1
python3 report_tables.py --resultsPath results --clients nethermind --testsPath testburnt --runs 1
python3 report_tables.py --resultsPath results --clients erigon --testsPath testburnt --runs 1


./nethermind/tools/Nethermind.Tools.Kute/bin/Release/net8.0/Nethermind.Tools.Kute -i testburnt/Burnt/Burnt_113M.txt -s /tmp/jwtsecret -r results/erigon_113.txt

