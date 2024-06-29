import json
import os
import secrets
import time

from tqdm.contrib.concurrent import process_map

from utils import get_completion_from_messages, save_results
from video_script.video_prompt import video_structure, writing_tips, role, synthesize_task

out_dir = "./data"
dump_directory = f"{out_dir}/dumps-2"

object_s = "video"

jsonl_output_file_path = f"{out_dir}/generated_{object_s}_to_critique.jsonl"

input_path = f"{out_dir}/videos_details.jsonl"

example = "{\"video\":{\"title\": \"<title>\",\"transcript\": \"<transcript>\",\"author\": \"<author>\",\"publication_date\": \"<publication_date>\"}}"

example2 = '''{"Title": "Function-Calling and Data Extraction with LLMs", "Description": "Learn to apply function-calling to expand LLM and agent application capabilities.", "Prerequisites": "Familiarity with LLMs and basic Python knowledge are recommended. ", "Skill Level": "Beginner", "Partnership": "Nexusflow", "Features": "Learn to extend LLMs with custom functionality via function-calling, enabling them to form calls to external functions.\nExtract structured data from natural language inputs, making real-world data usable for analysis.\nBuild an end-to-end application that processes customer service transcripts using LLMs.", "Landing Page": "https://www.deeplearning.ai/short-courses/function-calling-and-data-extraction-with-llms"}'''

debug = False


def synthesize_data(dumped_directory, result):
    if result is None:
        print("Error: Cannot process None result")
        return None

    non_blank_result = "\n".join([line for line in result.splitlines() if line.strip() != ""])

    random_hash = secrets.token_hex(4)

    # Original file for audit
    file_path = os.path.join(dumped_directory, f"result_new_{object_s}_to_critic_{random_hash}.jsonl")
    with open(file_path, "w") as f1:
        f1.write(non_blank_result)

    return result


def process_result(result):
    if not result:
        return ""

    _lines = result.splitlines()
    json_list = []

    for line in _lines:
        if line.strip():  # Check if line is not blank
            try:
                json_obj = json.loads(line)
                formatted_json = json.dumps(json_obj)
                json_list.append(formatted_json)
            except json.JSONDecodeError as e1:
                # Handle the case where the line is not valid JSON
                print(f"Error processing line {line}. Details: {e1}")
                return ""

    if not json_list:  # If no valid JSON lines were found
        return ""

    # Join each formatted JSON line with newline character
    return '\n'.join(json_list)


def get_valid_completion_from_messages(model="mistral-large-latest", messages=None):
    if not messages:
        return ""
    try:
        result = get_completion_from_messages(
            model=model,
            messages=messages,
            temperature=0.2,
            # response format does not apply if asked to generate multiple object
            #response_format={"type": "json_object"}
        )

        formatted_json = process_result(result)

        # Return the formatted JSON
        return formatted_json
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error processing result. Details: {e}")
        return ""


def process_line(args):
    data = json.loads(args)

    title = data["Title"]
    description = data["Description"]
    prerequisites = data["Prerequisites"]
    skill_level = data["Skill Level"]
    partnership = data["Partnership"]
    features = data["Features"]
    author = data["Instructor"]

    # wait 3sec
    time.sleep(1)

    result = ""
    try:

        synthesize_prompt = f"""{role},\n
{synthesize_task}.
Each script should have a title, the transcript, the author name and a publication date.\n
The video topic, a short description, prerequisites, skill level of audience, the author name,
 some video features and an eventual technology partner will be provided to you later.\n\n
Structure the result in a json line (jsonl) file with video as key.\n
Return the video in short JSON object.\n\n
Format Example:\n
{example}\n
Don't output blank line.\n
you must escape double quote by using a backslash.\n
\n
{video_structure}
\n
{writing_tips}
\n\n
Contents to write the video:
Video topic: {title}\n
Description: {description}\n
Prerequisites: {prerequisites}\n
Skill Level: {skill_level}\n
Partnership: {partnership}\n
Features: {features}\n
Author: {author}\n
"""

        messages = [
                {"role": "user", "content": synthesize_prompt}
            ]

        if not debug:
            result_1 = get_valid_completion_from_messages(model="mistral-large-latest",
                                                        messages=messages)
            result_2 = get_valid_completion_from_messages(model="gpt-3.5-turbo",
                                                        messages=messages)
            result = result_1 + "\n" + result_2
        else:
            print(messages)

    except Exception as e:
        print(f"{e}")

    if result:
        result = synthesize_data(dump_directory, result)

    return result


def run_n_times(n, lines, max_workers=5, chunksize=1):
    _all_results = []

    for _ in range(n):
        results = process_map(process_line, lines, max_workers=max_workers, chunksize=chunksize)
        _all_results.extend(results)

    return all_results



if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]

    lines = lines[0:35]

    all_results = run_n_times(10, lines)

    save_results(all_results, jsonl_output_file_path)
