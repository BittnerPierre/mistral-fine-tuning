import glob
import os

from utils import save_results

out_dir = "./data"
dump_directory = "./data/dumps-4"

if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    #jsonl_input_file_path = f"{out_dir}/generated_news_critique.jsonl"
    #result_new_video_to_critic_c893d15d.jsonl
    jsonl_output_file_path = f"{out_dir}/generated_video_conversation.jsonl"

    # Pattern to match all versions of generated_news_critique.jsonl with time suffixes
    file_pattern = os.path.join(dump_directory, "result_new_video_conversation_*.jsonl")

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
    results = [line.strip() for line in all_lines if line.strip()]

    save_results(results, jsonl_output_file_path)