import shutil

import secrets

from tqdm.contrib.concurrent import process_map
import json
import random
import time

import os
from datetime import datetime

from dotenv import load_dotenv, find_dotenv

from prompts import prefix
from utils import get_completion_from_messages, format_news_article_from_jsonl, save_results, \
    get_completion_from_messages2

_ = load_dotenv(find_dotenv())

out_dir = "./data"
dump_directory = "./data/dumps-3"

def process_line(args):
    line = args
    try:
        record = json.loads(line)
    except json.decoder.JSONDecodeError as e:
        print(f"{e} - {line}")
        return

    news_article = record.get("news")

    news = format_news_article_from_jsonl(news_article)

    # wait 3sec
    time.sleep(1)
    try:
        messages = [
                {"role": "user", "content": prefix + news}
            ]
        critique = get_completion_from_messages2(
            messages=messages,
            temperature=0.2)

    except Exception as e:
        print(f"{e} while processing "+news_article)
        return

    result = json.dumps(
            {"news": news_article, "critique": critique}
        )
    # Generate a random 8-digit hexadecimal string
    random_hash = secrets.token_hex(4)

    with open(f"{dump_directory}/result_new_critique_news_{random_hash}.jsonl", "w") as f:
        f.write(result)

    return result


if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    jsonl_input_file_path = f"{out_dir}/generated_news_to_critique.jsonl"
    jsonl_output_file_path = f"{out_dir}/generated_news_critique.jsonl"


    with open(jsonl_input_file_path, "r") as f:
        lines = f.readlines()
        lines = [line for line in lines if line.strip()]
        results = process_map(process_line, lines, max_workers=10, chunksize=1)

        save_results(results, jsonl_output_file_path)
