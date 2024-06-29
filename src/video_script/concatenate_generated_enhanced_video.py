import glob
import json
import os

from utils import save_results

out_dir = "./data"
dump_directory = "./data/dumps-4"


def clean_json_string(json_str):
    """
    Clean the JSON string to ensure it can be properly parsed.
    This function will remove extra quotes and escape sequences.
    """
    # Strip outer single or double quotes
    if (json_str.startswith('\'') and json_str.endswith('\'')) or (json_str.startswith('"') and json_str.endswith('"')):
        json_str = json_str[1:-1]

    # Replace escaped quotes
    json_str = json_str.replace('\\"', '"').replace("\\'", "'")
    json_str = json_str.replace('\\\\', '\\')

    return json_str



if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    #jsonl_input_file_path = f"{out_dir}/generated_news_critique.jsonl"
    #result_new_video_to_critic_c893d15d.jsonl
    jsonl_output_file_path = f"{out_dir}/generated_enhanced_video.jsonl"

    # Pattern to match all versions of generated_news_critique.jsonl with time suffixes
    file_pattern = os.path.join(dump_directory, "result_new_video_*.jsonl")

    # Retrieve all files matching the pattern
    jsonl_files = glob.glob(file_pattern)

    # Initialize a list to collect all lines
    all_lines = []

    # Process each JSONL file
    for jsonl_file in jsonl_files:
        print(f"Processing file: {jsonl_file}")
        # Add your file processing logic here
        with open(jsonl_file, 'r') as f:
            lines = f.readlines()
            all_lines.extend(lines)

    # Join all collected lines into a single string
    # results = [line.strip() for line in all_lines if line.strip()]
    results = []
    for line in all_lines:
        stripped_line = line.strip()
        if stripped_line:
            try:
                # Convert the line from a string back to a JSON object
                cleaned_str = clean_json_string(stripped_line)
                json_obj = json.loads(cleaned_str)
                results.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    # Convert the results to JSON strings to write them to the file
    json_strings = [json.dumps(result) for result in results]

    save_results(json_strings, jsonl_output_file_path)