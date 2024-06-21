import glob
import secrets
import sys

from tqdm.contrib.concurrent import process_map
import json
import random
import time

import os
from mistralai.client import MistralClient

from prompts import prefix
from utils import get_completion_from_messages, format_news_article_from_jsonl, save_results

api_key = os.environ.get("MISTRAL_API_KEY")
client = MistralClient(api_key=api_key)

out_dir = "./data"
dump_directory = "./data/dumps-4"

def process_line(args):
    line, prompts = args
    try:
        record = json.loads(line)
    except json.decoder.JSONDecodeError as e:
        print(f"{e} - {line}")
        return

    news_article = record.get("news")
    critique = record.get("critique")

    part = random.choice(list(range(20)))
    prompt = prompts[part]

    news = format_news_article_from_jsonl(news_article)

    # wait 3sec
    time.sleep(1)
    messages = [
                {"role": "user", "content": prefix + news},
                {"role": "assistant", "content": critique},
                {"role": "user", "content": prompt}
            ]
    try:
        new_news = get_completion_from_messages(
            messages=messages,
            temperature=0.2)
    except Exception as e:
        print(f"{e} while processing "+news_article)
        return


    result = json.dumps(
        #{"news": news, "critique": critique, "corrected_news": new_news}
            {
                "messages": [
                    {"role": "user", "content": prefix + news},
                    {"role": "assistant", "content": critique},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": new_news}
                ]
            }
        )
    # Generate a random 8-digit hexadecimal string
    random_hash = secrets.token_hex(4)

    with open(f"{dump_directory}/result_new_news_{random_hash}.jsonl", "w") as f:
        f.write(result)

    return result


if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    #jsonl_input_file_path = f"{out_dir}/generated_news_critique.jsonl"
    jsonl_output_file_path = f"{out_dir}/generated_news_correction.jsonl"

    guides = [
        "Incorporate the feedback into the news article and respond with the enhanced version, focusing solely on stylistic improvements without altering the content.",
        "Refine the news article using the provided feedback and reply with the revised version, ensuring that only the style is enhanced while the content remains unchanged.",
        "Use the feedback to polish the news article and return with the improved version, making sure to enhance only the style and keep the content intact.",
        "Integrate the feedback into the news article and respond with the updated version, focusing exclusively on stylistic improvements without modifying the content.",
        "Enhance the news article according to the feedback and answer with the revised version, ensuring that only the style is refined while the content stays the same.",
        "Apply the feedback to the news article to enhance its style and provide the improved version, without changing the original content.",
        "Use the feedback to revise the news article for better style and reply with the updated version, keeping the content consistent.",
        "Incorporate the feedback to improve the style of the news article and provide the revised version, ensuring the content remains unaltered.",
        "Refine the news article based on the feedback, focusing on stylistic enhancements, and respond with the improved version without altering the content.",
        "Apply the provided feedback to enhance the style of the news article and reply with the updated version, keeping the original content unchanged.",
        "Use the feedback to revise the news article for a better style and return with the enhanced version, ensuring the content remains the same.",
        "Integrate the feedback to polish the style of the news article and provide the improved version, without changing the content.",
        "Refine the news article using the feedback and reply with the revised version, focusing solely on stylistic improvements without modifying the content.",
        "Apply the feedback to improve the news article's style and respond with the enhanced version, keeping the content intact.",
        "Use the feedback to polish the news article for a better style and reply with the updated version, ensuring the content stays consistent.",
        "Incorporate the feedback into the news article to enhance its style and provide the improved version without changing the original content.",
        "Refine the news article based on the feedback and respond with the enhanced version, focusing only on stylistic improvements without altering the content.",
        "Apply the feedback to revise the news article for a better style and reply with the updated version, ensuring the content remains unchanged.",
        "Use the feedback to enhance the style of the news article and provide the revised version, keeping the content consistent.",
        "Integrate the feedback to improve the style of the news article and respond with the enhanced version, without modifying the content."
    ]

    # Pattern to match all versions of generated_news_critique.jsonl with time suffixes
    # Base name and extension
    base_name = "generated_news_critique"
    extension = ".jsonl"

    # The time suffix pattern, optionally empty
    time_suffix_pattern = r"(\d{8}_\d{6})?"  # Optional pattern, matches %Y%m%d_%H%M%S or empty

    # Full file pattern considering an optional time suffix
    file_pattern = os.path.join(out_dir, f"{base_name}_{time_suffix_pattern}{extension}")

    # Adjusting the pattern for glob, since glob does not support regex directly
    file_pattern_glob = os.path.join(out_dir, file_pattern)
    file_pattern_exact = os.path.join(out_dir, f"{base_name}{extension}")

    # Collect all matching files
    jsonl_files = glob.glob(file_pattern_glob) + glob.glob(file_pattern_exact)

    # Process each JSONL file
    for jsonl_file in jsonl_files:
        print(f"Processing file: {jsonl_file}")
        # Add your file processing logic here
        with open(jsonl_file, 'r') as f:
            lines = f.readlines()
            lines = [line for line in lines if line.strip()]
            lines = [(line, guides) for line in lines]

            results = process_map(process_line, lines, max_workers=5, chunksize=1)

            save_results(results, jsonl_output_file_path)

