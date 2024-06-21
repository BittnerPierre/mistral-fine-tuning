# Let's first read the uploaded JSON file to understand its structure
import json
import os

import jsonlines

# Define the file path
file_path = './data/scratch_15.jsonl'


def convert_json_to_jsonl(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        data = json.load(input_file)

    with jsonlines.open(output_file_path, mode='w') as writer:
        # If the top level is a list, write each item separately
        if isinstance(data, list):
            for item in data:
                writer.write(item)
        # If the top level is a dictionary, write the dictionary itself
        elif isinstance(data, dict):
            writer.write(data)
        else:
            raise ValueError("Unsupported JSON format")

def to_jsonl(file_path, output_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Reformat the content into valid JSON lines
    json_lines = []
    current_json = ""
    open_brace_count = 0

    for line in lines:
        line = line.strip()
        if line == '{':
            current_json += '{'
            open_brace_count += 1
        elif line == '}':
            current_json += '}'
            open_brace_count -= 1

            if open_brace_count == 0:
                json_lines.append(current_json)
                current_json = ""

        elif line == '},':
            current_json += '}'
            json_lines.append(current_json)
            current_json = ""
            open_brace_count = 0
        else:
            current_json += line

    if current_json:
        print(f"'{current_json}'")
        json_lines.append(current_json)

    # Join all JSON lines with a newline character to create the final JSONL content
    jsonl_content = '\n'.join(json_lines)+ '\n'

    # Write the JSONL content to a new file
    with open(output_file_path, 'w') as output_file:
        output_file.write(jsonl_content + '\n')


    # with open(file_path, 'r') as file:
    #     lines = file.readlines()
    #
    # # Reformat the content into valid JSON lines
    # json_lines = []
    # current_json = ""
    #
    # for line in lines:
    #     line = line.strip()
    #     if line == '{':
    #         current_json = '{'
    #     elif line == '}':
    #         current_json += '}'
    #     elif line == '},':
    #         current_json += '}'
    #         json_lines.append(current_json)
    #         current_json = ""
    #         print("New Json")
    #     else:
    #         current_json += line
    #
    # if current_json:
    #     json_lines.append(current_json)
    #
    # # Join all JSON lines with a newline character to create the final JSONL content
    #
    # jsonl_content = '\n'.join(json_lines)
    # print(jsonl_content)
    #
    # # Write the JSONL content to a new file
    # with open(output_file_path, 'w') as output_file:
    #     output_file.write(jsonl_content)

    #
    # # The file seems to be not in a valid JSON format, let's read it as text and process it accordingly
    # with open(file_path, 'r') as file:
    #     lines = file.readlines()
    #
    # # Reformat the content into valid JSON lines
    # json_lines = []
    # current_json = ""
    #
    # for line in lines:
    #     line = line.strip()
    #     #if line == '{' or line == '}':
    #     #    continue
    #     if line == '{':
    #         current_json = '{'
    #     #elif line == '}':
    #     #    continue
    #     elif line == '},':
    #         current_json += '}'
    #         json_lines.append(current_json)
    #         current_json = "{"
    #     else:
    #         current_json += line
    #
    # # Join all JSON lines with a newline character to create the final JSONL content
    # jsonl_content = '\n'.join(json_lines)
    #
    # # Write the JSONL content to a new file
    # with open(output_file_path, 'w') as output_file:
    #     output_file.write(jsonl_content)

if __name__ == "__main__":
    dump_directory = "./tests"

    # Original file for audit
    file_path = os.path.join(dump_directory, "result_new_news_to_critique_58e68d1d.json")

    # New output file for JSONL content
    output_file_path = os.path.join(dump_directory, "result_new_news_to_critique_58e68d1d.jsonl")

    # Assuming the to_jsonl function outputs a JSONL file
    convert_json_to_jsonl(file_path, output_file_path)

    # Read the content of the JSONL file into the result variable
    with open(output_file_path, "r") as f:
        result = f.read()

    print(result)