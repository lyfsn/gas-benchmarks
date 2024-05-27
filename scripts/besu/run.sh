# Prepare nethermind image that we will use on the script
cd scripts/besu

cp besu.json /tmp/besu.json
cp jwtsecret /tmp/jwtsecret

docker compose up -d

sleep 15

docker compose logs
