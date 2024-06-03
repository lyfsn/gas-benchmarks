docker stop gas-execution-client
docker stop gas-execution-client-sync

docker rm gas-execution-client
docker rm gas-execution-client-sync

nohup ./run.sh -t "tests/" -w "warmup/warmup-1000bl-16wi-24tx.txt" -c "nethermind,geth,reth,erigon,besu" -r 8
nohup &


