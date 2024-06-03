rm -rvf reports
rm -rvf results

rm nohup.out


docker stop gas-execution-client
docker stop gas-execution-client-sync

docker rm gas-execution-client
docker rm gas-execution-client-sync


