import os
import json

def collect_json_files(root_dir):
    """ Recursively collect all JSON file paths within subdirectories. """
    json_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def merge_json_files(json_files):
    """ Merge JSON contents into a dictionary indexed by filename (without .json). """
    merged_data = {}
    for json_file in json_files:
        file_name = os.path.splitext(os.path.basename(json_file))[0]  # Get filename without extension
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                merged_data[file_name] = data  # Store data under filename key
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {json_file}")
    return merged_data

def save_merged_json(merged_data, output_file):
    """ Save the merged data into a single JSON file. """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4)

# Specify the root directory where JSON files are stored
root_directory = "instagram"
output_json = "new_merged.json"

# Collect, merge, and save JSON
json_files = collect_json_files(root_directory)
merged_data = merge_json_files(json_files)
save_merged_json(merged_data, output_json)

print(f"Combined JSON saved to {output_json}")