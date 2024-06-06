#!/bin/bash

# Default inputs
TEST_PATH="tests/"
WARMUP_FILE="warmup/warmup-1000bl-16wi-24tx.txt"
CLIENTS="nethermind,geth,reth"
RUNS=8
IMAGES="default"
OUTPUT_DIR="results"

# Parse command line arguments
while getopts "t:w:c:r:i:o:" opt; do
  case $opt in
    t) TEST_PATH="$OPTARG" ;;
    w) WARMUP_FILE="$OPTARG" ;;
    c) CLIENTS="$OPTARG" ;;
    r) RUNS="$OPTARG" ;;
    i) IMAGES="$OPTARG" ;;
    o) OUTPUT_DIR="$OPTARG" ;;
    *) echo "Usage: $0 [-t test_path] [-w warmup_file] [-c clients] [-r runs] [-i images] [-o output_dir]" >&2
       exit 1 ;;
  esac
done

IFS=',' read -ra CLIENT_ARRAY <<< "$CLIENTS"
IFS=',' read -ra IMAGE_ARRAY <<< "$IMAGES"

# Set up environment
mkdir -p "$OUTPUT_DIR"

# Install dependencies
pip install -r requirements.txt

# Function to check if the port is open
check_port_open() {
  local client=$1
  while ! nc -z 127.0.0.1 8551; do   
    sleep 1
  done
  echo $(date +%s%3N)  # Return the timestamp in milliseconds
}

# Run benchmarks
for run in $(seq 1 $RUNS); do
  for i in "${!CLIENT_ARRAY[@]}"; do
    client="${CLIENT_ARRAY[$i]}"
    image="${IMAGE_ARRAY[$i]}"

    cd "scripts/$client"
    docker compose down
    sudo rm -rf execution-data
    cd ../..

    # Record the start time
    start_time=$(date +%s%3N)

    if [ -z "$image" ]; then
      echo "Image input is empty, using default image."
      python3 setup_node.py --client $client
    else
      echo "Using provided image: $image for $client"
      python3 setup_node.py --client $client --image $image
    fi

    # Record the time when the port is open
    port_open_time=$(check_port_open $client)

    # Calculate the interval
    interval=$((port_open_time - start_time))
    
    # Write the interval to a file in OUTPUT_DIR
    output_file="${OUTPUT_DIR}/${client}_${i}.txt"
    echo "$client: $interval ms" > "$output_file"

    cd "scripts/$client"
    docker compose down
    sudo rm -rf execution-data
    cd ../..
  done
done

