# Create argument parser
import argparse
import datetime
import json
import os
import subprocess

from utils import print_computer_specs

executables = {
    'kute': './nethermind/tools/Nethermind.Tools.Kute/bin/Release/net8.0/Nethermind.Tools.Kute'
}


def run_command(test_case_file, jwt_secret, response, ec_url, kute_extra_arguments):
    # Add logic here to run the appropriate command for each client
    command = f'{executables["kute"]} -i {test_case_file} -s {jwt_secret} -r {response} -a {ec_url} ' \
              f'{kute_extra_arguments} '
    results = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(results.stdout)
    print(results.stderr)
    return results.stdout


def save_to(output_folder, file_name, content):
    output_path = os.path.join(output_folder, file_name)
    with open(output_path, "w") as file:
        file.write(content)


def main():
    parser = argparse.ArgumentParser(description='Benchmark script')
    parser.add_argument('--testsPath', type=str, help='Path to test case folder')
    parser.add_argument('--client', type=str, help='Name of the client we are testing')
    parser.add_argument('--runs', type=int, help='Number of times we are going to run the kute against the node')
    parser.add_argument('--jwtPath', type=str,
                        help='Path to the JWT secret used to communicate with the client you want to test')
    parser.add_argument('--responseFile', type=str, help='Name for the response file')
    parser.add_argument('--output', type=str, help='Output folder for metrics charts generation. If the folder does '
                                                   'not exist will be created.',
                        default='results')
    # Executables path
    parser.add_argument('--dotnetPath', type=str, help='Path to dotnet executable, needed if testing nethermind and '
                                                       'you need to use something different to dotnet.',
                        default='dotnet')
    parser.add_argument('--kutePath', type=str, help='Path to kute executable.',
                        default=executables["kute"])
    parser.add_argument('--kuteArguments', type=str, help='Extra arguments for Kute.',
                        default='')
    parser.add_argument('--ecURL', type=str, help='Execution client where we will be running kute url.',
                        default='http://localhost:8551')
    parser.add_argument('--warmupPath', type=str, help='Set path to warm up file.', default='')

    # Parse command-line arguments
    args = parser.parse_args()

    # Get client name and test case folder from command-line arguments
    tests_paths = args.testsPath
    jwt_path = args.jwtPath
    execution_url = args.ecURL
    output_folder = args.output
    executables['dotnet'] = args.dotnetPath
    executables['kute'] = args.kutePath
    kute_arguments = args.kuteArguments
    response_file = args.responseFile
    warmup_file = args.warmupPath
    client = args.client
    runs = args.runs

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if response_file is None:
        response_file = f'{client}_response_{runs}.txt'

    response_path = os.path.join(output_folder, response_file)

    warmup_response = ''
    if warmup_file != '':
        warmup_response_path = os.path.join(output_folder, 'warmup_' + client + '_' + response_file)
        warmup_response = run_command(warmup_file, jwt_path, warmup_response_path, execution_url, kute_arguments)
        save_to(output_folder, f'warmup_{client}_response.txt', warmup_response)

    # Print Computer specs
    computer_specs = print_computer_specs()
    save_to(output_folder, 'computer_specs.txt', computer_specs)

    for run in range(runs):
        print(f"Running {client} for the {run + 1} time")
        response = run_command(tests_paths, jwt_path, response_path, execution_url, kute_arguments)
        timestamp = datetime.datetime.now().timestamp()
        save_to(output_folder, f'{client}_response_{run}_{int(timestamp)}.txt', response)


if __name__ == '__main__':
    main()
