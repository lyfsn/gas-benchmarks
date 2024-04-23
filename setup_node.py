# Create argument parser
import argparse
import datetime
import json
import os
import subprocess

from utils import print_computer_specs


def run_command(client, run_path):
    # Add logic here to run the appropriate command for each client
    command = f'{run_path}/run.sh'
    print(f"{client} running at url 'http://localhost:8551'(auth), with command: '{command}'")
    subprocess.run(command, shell=True, text=True)


def set_image(client, el_images, run_path):
    if client == "nethermind":
        specifics = "CHAINSPEC_PATH=/tmp/chainspec.json"
    else:
        specifics = "GENESIS_PATH=/tmp/genesis.json"
    env = f"EC_IMAGE_VERSION={el_images[client]}\n" \
          "EC_DATA_DIR=./execution-data\n" \
          "EC_JWT_SECRET_PATH=/tmp/jwtsecret\n" \
          f"{specifics}"

    env_file_path = os.path.join(run_path, ".env")
    if os.path.exists(env_file_path):
        os.remove(env_file_path)
    with open(env_file_path, "w") as file:
        file.write(env)


def main():
    parser = argparse.ArgumentParser(description='Benchmark script')
    parser.add_argument('--client', type=str, help='Client that we want to spin up.', default="nethermind")
    parser.add_argument('--image', type=str, help='Docker image of the client we are going to use.')

    # Parse command-line arguments
    args = parser.parse_args()

    # Get client name and test case folder from command-line arguments
    client = args.client
    image = args.image

    el_images = {
        "nethermind": "nethermind/nethermind:1.25.4",
        "geth": "ethereum/client-go:v1.13.14",
        "reth": " ghcr.io/paradigmxyz/reth:v0.2.0-beta.6"
    }

    if client not in el_images:
        print("Client not supported")
        return

    if image is not None:
        el_images[client] = image

    run_path = os.path.join(os.getcwd(), "scripts")
    run_path = os.path.join(run_path, client)

    set_image(client, el_images, run_path)

    # It will run Kute, might take some time
    run_command(client, run_path)


if __name__ == '__main__':
    main()
