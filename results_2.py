import argparse
import json
import os
import statistics

import numpy as np

import utils
import matplotlib.pyplot as plt


def get_test_cases(tests_path):
    test_cases = {
        # 'test_case_name': ['gas_used']
    }

    for test_case in os.listdir(tests_path):
        if test_case.endswith('.txt'):
            test_case_parsed = test_case.split('_')
            test_case_name = test_case_parsed[0]
            test_case_gas = test_case_parsed[1].split('M')[0]
            if test_case_name not in test_cases:
                test_cases[test_case_name] = [test_case_gas]
            else:
                test_cases[test_case_name].append(test_case_gas)
    return test_cases


def read_results(text):
    sections = {}
    for sections_text in text.split('--------------------------------------------------------------'):
        timestamp = None
        measurement = None
        tags = {}
        fields = {}
        for full_lines in sections_text.split('#'):
            if not full_lines:
                continue

            if full_lines.startswith(' TIMESTAMP:'):
                timestamp = int(full_lines.split(':')[1])
            elif full_lines.startswith(' MEASUREMENT:'):
                measurement = full_lines.split(' ')[3].strip()
            elif full_lines.startswith(' TAGS:'):
                for line in full_lines.split('\n')[1:]:
                    if not line:
                        continue
                    data = line.strip().split(' = ')
                    tags[data[0]] = data[1]
                pass
            elif full_lines.startswith(' FIELDS:'):
                for line in full_lines.split('\n')[1:]:
                    if not line:
                        continue
                    data = line.strip().split(' = ')
                    fields[data[0]] = data[1]

        if timestamp is not None and measurement is not None:
            sections[measurement] = utils.SectionData(timestamp, measurement, tags, fields)

    return sections


def check_sync_status(json_data):
    data = json.loads(json_data)
    if 'status' in data['result']:
        return data['result']['status'] == 'VALID'
    elif 'payloadStatus' in data['result']:
        return data['result']['payloadStatus']['status'] == 'VALID'
    else:
        return False


def extract_response_and_result(results_path, client, test_case_name, gas_used, run, method, field):
    result_file = f'{results_path}/{client}_results_{run}_{test_case_name}_{gas_used}M.txt'
    response_file = f'{results_path}/{client}_response_{run}_{test_case_name}_{gas_used}M.txt'
    response = True
    result = 0
    # Get the responses from the files
    with open(response_file, 'r') as file:
        text = file.read()
        if len(text) == 0:
            return False, 0
        # Get latest line
        for line in text.split('\n'):
            if len(line) < 1:
                continue
            if not check_sync_status(line):
                return False, 0
    # Get the results from the files
    with open(result_file, 'r') as file:
        sections = read_results(file.read())
        if method not in sections:
            return False, 0
        result = sections[method].fields[field]
    return response, float(result)


# Print graphs and tables with the results
def process_results(client_results, clients, results_paths, test_cases, failed_tests, methods, percentiles=False):
    results_to_print = ''
    for test_case, gas_used in test_cases.items():
        for method in methods:
            add_header = ' (Percentiles)' if percentiles else ''
            results_to_print += f'\n\n{test_case}{add_header}:\n'
            gas_bar = [int(gas) for gas in gas_used]
            gas_bar.sort()
            main_headers = [center_string('client/gas', 20)]
            for gas in gas_bar:
                centered_string = center_string(str(gas) + 'M', 14)
                main_headers.append(centered_string)
            header = '|'.join(main_headers)
            results_to_print += f'{header}\n'
            results_to_print += '-' * (30 + (14 * len(gas_bar))) + '\n'
            # Create a table with the results
            # Table will have the following format:
            # | client/gas  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
            # |{client} max | x | x | x | x | x | x | x | x | x | x  |
            # |         min | x | x | x | x | x | x | x | x | x | x  |
            # |         avg | x | x | x | x | x | x | x | x | x | x  |
            # |         std | x | x | x | x | x | x | x | x | x | x  |
            plt.figure(figsize=(10, 5))

            for client in clients:
                table = [['' for _ in range(len(gas_bar))] for _ in range(7)]
                for i in range(0, len(gas_bar)):
                    gas = str(gas_bar[i])
                    if True in failed_tests[client][test_case][gas][method]:
                        na = center_string('N/A', 14)
                        for ti in range(len(table)):
                            table[ti][i] = na
                    max_val = max(client_results[client][test_case][gas][method])
                    min_val = f'{min(client_results[client][test_case][gas][method]):.2f} ms'
                    avg_val = f'{sum(client_results[client][test_case][gas][method]) / len(client_results[client][test_case][gas][method]):.2f} ms'
                    std_val = f'{standard_deviation(client_results[client][test_case][gas][method]):.2f}'
                    p50_val = f'{np.percentile(client_results[client][test_case][gas][method], 50):.2f}'
                    p95_val = f'{np.percentile(client_results[client][test_case][gas][method], 95):.2f}'
                    p99_val = f'{np.percentile(client_results[client][test_case][gas][method], 99):.2f}'
                    table[0][i] = max_val
                    table[1][i] = f'{center_string(min_val, 14)}'
                    table[2][i] = f'{center_string(avg_val, 14)}'
                    table[3][i] = f'{center_string(std_val, 14)}'
                    table[4][i] = f'{center_string(p50_val, 14)}'
                    table[5][i] = f'{center_string(p95_val, 14)}'
                    table[6][i] = f'{center_string(p99_val, 14)}'

                if percentiles:
                    p50_row = center_string(f'{client} p50', 20)
                    results_to_print += f'{p50_row}|{"|".join(table[4])}\n'
                    p90_row = center_string('p90', 20)
                    results_to_print += f'{p90_row}|{"|".join(table[5])}\n'
                    p99_row = center_string('p99', 20)
                    results_to_print += f'{p99_row}|{"|".join(table[6])}\n'
                    results_to_print += '-' * (30 + (14 * len(gas_bar))) + '\n'
                else:
                    max_row = center_string(f'{client} max', 20)
                    row = []
                    for item in table[0]:
                        str_item = f'{item:.2f} ms'
                        row.append(f'{center_string(str_item, 14)}')
                    results_to_print += f'{max_row}|{"|".join(row)}\n'

                    min_row = center_string('min', 20)
                    results_to_print += f'{min_row}|{"|".join(table[1])}\n'
                    avg_row = center_string('avg', 20)
                    results_to_print += f'{avg_row}|{"|".join(table[2])}\n'
                    std_row = center_string('std', 20)
                    results_to_print += f'{std_row}|{"|".join(table[3])}\n'
                # x = range(1, len(gas_bar) + 1)
                plt.plot(gas_bar, [float(x) for x in table[0]], label=client)
                # plt.xticks(lis)

            plt.legend()
            plt.title(f'Max results')
            if not os.path.exists(f'{results_paths}/charts'):
                os.makedirs(f'{results_paths}/charts')
            plt.savefig(f'{results_paths}/charts/{test_case}_{method}_results.png')
            plt.close()

            results_to_print += '\n\n'

    print(results_to_print)
    with open(f'{results_paths}/tables.txt', 'w') as file:
        file.write(results_to_print)


def standard_deviation(numbers):
    if len(numbers) < 2:
        return None
    return statistics.stdev(numbers)


def center_string(string, size):
    padding_length = max(0, size - len(string))
    padding_left = padding_length // 2
    padding_right = padding_length - padding_left
    centered_string = " " * padding_left + string + " " * padding_right
    return centered_string


def check_client_response_is_valid(results_paths, client, test_case, length):
    for i in range(1, length + 1):
        response_file = f'{results_paths}/{client}_response_{i}_{test_case}'
        if not os.path.exists(response_file):
            return False
        with open(response_file, 'r') as file:
            text = file.read()
            if len(text) == 0:
                return False
            # Get latest line
            for line in text.split('\n'):
                if len(line) < 1:
                    continue
                if not check_sync_status(line):
                    return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Benchmark script')
    parser.add_argument('--resultsPath', type=str, help='Path to gather the results', default='results')
    parser.add_argument('--testsPath', type=str, help='resultsPath', default='tests/')
    parser.add_argument('--clients', type=str, help='Client we want to gather the metrics, if you want to compare, '
                                                    'split them by comma, ex: nethermind,geth,erigon,reth',
                        default='nethermind,geth,reth,erigon')
    parser.add_argument('--runs', type=int, help='Number of runs the program will process', default='10')

    # Parse command-line arguments
    args = parser.parse_args()

    # Get client name and test case folder from command-line arguments
    results_paths = args.resultsPath
    clients = args.clients
    tests_path = args.testsPath
    runs = args.runs

    # Get the computer spec
    with open(os.path.join(results_paths, 'computer_specs.txt'), 'r') as file:
        text = file.read()
        computer_spec = text
    print(computer_spec)

    client_results = {}
    failed_tests = {}
    methods = ['engine_newPayloadV3']
    fields = 'max'

    test_cases = get_test_cases(tests_path)
    for client in clients.split(','):
        client_results[client] = {}
        failed_tests[client] = {}
        for test_case_name, test_case_gas in test_cases.items():
            client_results[client][test_case_name] = {}
            failed_tests[client][test_case_name] = {}
            for gas in test_case_gas:
                client_results[client][test_case_name][gas] = {}
                failed_tests[client][test_case_name][gas] = {}
                for method in methods:
                    client_results[client][test_case_name][gas][method] = []
                    failed_tests[client][test_case_name][gas][method] = []
                    for run in range(1, runs + 1):
                        responses, results = extract_response_and_result(results_paths, client, test_case_name, gas,
                                                                         run, method, fields)
                        client_results[client][test_case_name][gas][method].append(results)
                        failed_tests[client][test_case_name][gas][method].append(not responses)

    process_results(client_results, clients.split(','), results_paths, test_cases, failed_tests, methods, False)

    print('Done!')


if __name__ == '__main__':
    main()
