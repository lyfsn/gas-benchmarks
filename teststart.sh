


#!/bin/bash

./run.sh \
  -t "testburnt/" \
  -w "./testburntwarm/warm.txt" \
  -c "reth" \
  -r 1 \
  -o "results" 


python3 report_tables.py --resultsPath results --clients reth --testsPath testburnt --runs 1
python3 report_tables.py --resultsPath results --clients nethermind --testsPath testburnt --runs 1

