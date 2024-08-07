import json
import sys

def process_file(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        try:
            # Parse each line as JSON
            data = json.loads(line)
            if data.get("method") == "engine_forkchoiceUpdatedV3":
                # Remove the second set of parameters if it exists
                if len(data.get("params", [])) > 1:
                    data["params"][1] = None
            # Convert the modified Python object back to JSON string
            modified_lines.append(json.dumps(data))
        except json.JSONDecodeError:
            print(f"Invalid JSON in line: {line}")
            continue

    # Write the modified data back to the original file
    with open(file_path, 'w') as file:
        file.write("\n".join(modified_lines))

    print(f"File '{file_path}' has been updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_file(file_path)