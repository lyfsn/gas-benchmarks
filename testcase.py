import os
import json
import sys

def filter_rpc_files(directory):
    # Get list of all files in the directory
    files = [f for f in os.listdir(directory) if f.startswith("rpc.") and f.endswith(".txt")]
    
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        filtered_lines = []

        with open(file_path, 'r') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    if "method" in data and data["method"] in ["engine_newPayloadV3", "engine_forkchoiceUpdatedV3"]:
                        filtered_lines.append(line)
                except json.JSONDecodeError:
                    continue

        # Write filtered lines back to the file
        with open(file_path, 'w') as file:
            for line in filtered_lines:
                file.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    filter_rpc_files(directory)
    print("Filtering complete.")
