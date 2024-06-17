
mkdir results

./nethermind/tools/Nethermind.Tools.Kute/bin/Release/net8.0/Nethermind.Tools.Kute \
  -i testburntwarm/warm.txt \
  -s scripts/nethermind/jwtsecret \
  -r results/res.txt \
  -a http://127.0.0.1:8551

