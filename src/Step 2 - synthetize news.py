import json
import os
import secrets
import time

from tqdm.contrib.concurrent import process_map

from to_jsonl import to_jsonl, convert_json_to_jsonl
from utils import get_completion_from_messages2, get_completion_from_messages, save_results

out_dir = "./data"
dump_directory = "./data/dumps-2"


def synthetize_news(dump_directory, result):
    non_blank_result = "\n".join([line for line in result.splitlines() if line.strip() != ""])

    random_hash = secrets.token_hex(4)

    # Original file for audit
    file_path = os.path.join(dump_directory, f"result_new_news_to_critique_{random_hash}.jsonl")
    with open(file_path, "w") as f1:
        f1.write(non_blank_result)

    # # New output file for JSONL content
    #output_file_path = os.path.join(dump_directory, f"result_new_news_to_critique_{random_hash}.jsonl")

    # Assuming the to_jsonl function outputs a JSONL file
    #convert_json_to_jsonl(file_path, output_file_path)

    # Read the content of the JSONL file into the result variable
    #with open(output_file_path, "r") as f2:
    #    result = f2.read()

    return result


def process_line(args):
    line = args

    topic = line

    # wait 3sec
    time.sleep(1)

    result = ""
    try:

        prompt = (f"You are a 'News Writer'. Your task is to write 25 different news of 500–1000 words on {topic}."
                  "Each news should have a title, content, author, location and date."
                  "Structure the result in a json line (jsonl) file with news as key."
                  "Return the news in short JSON object."
                  "Example: "
                  "{\"news\":{\"title\": \"<Title>\",\"content\": \"<content>\",\"author\": \"<author>\",\"location\": \"<location>\",\"date\": \"<date>\"}}"
                  "Don't put blank line."
                  "you must escape double quote by using a backslash."
                )

        messages = [
                {"role": "user", "content": prompt}
            ]
        result = get_completion_from_messages2(#model="open-mixtral-8x7b",
            messages=messages,
            temperature=0.2,
            #response_format={"type": "json_object"}
        )

    except Exception as e:
        print(f"{e}")

    result = synthetize_news(dump_directory, result)

    return result


if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    #jsonl_input_file_path = f"{out_dir}/generated_news_critique.jsonl"
    jsonl_output_file_path = f"{out_dir}/generated_news_to_critique.jsonl"

    topics = ["Environment and Climate",
              "Economy and Finance"]

    topics2 = ["Politics and Government",
               "Economy and Finance",
               "Business and Industry",
               "Technology and Innovation",
               "Health and Medicine",
               "Environment and Climate",
               "Science and Research",
               "Society and Culture",
               "International",
               "Affairs",
               "Education and Learning",
               "Energy and Resources",
               "Trade and Commerce",
               "Law and Justice",
               "Urban Development and Infrastructure",
               "Labor and Employment",
               "Arts and Entertainment",
               "Travel and Tourism",
               "Sports and Recreation",
               "Agriculture and Food",
               "Transportation and Mobility",
               ]

    lines = topics2

    results = process_map(process_line, lines, max_workers=5, chunksize=1)

    save_results(results, jsonl_output_file_path)



