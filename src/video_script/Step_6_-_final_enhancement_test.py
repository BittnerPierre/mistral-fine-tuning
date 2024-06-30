import secrets
from json import JSONDecodeError

from tqdm.contrib.concurrent import process_map
import json
import time

import os

from dotenv import load_dotenv, find_dotenv

from video_prompt import critic_prompt, evaluation_framework, delimiter, role, critic_task, video_structure, \
    writing_tips
from utils import get_completion_from_messages, save_results
from video_script.utils_videos import format_video_from_jsonl

_ = load_dotenv(find_dotenv())

out_dir = "./data"
dump_directory = f"{out_dir}/dumps-6"

jsonl_input_file_path = f"{out_dir}/generated_enhanced_video.jsonl"
jsonl_output_file_path = f"{out_dir}/enhanced_videos_ft_open-mistral-7b.jsonl"

debug = False

fake_critic_str = '''
{
  "score": {
    "overall": 7,
    "tone": 8,
    "structure_and_content": 6
  },
  "critique": {
    "positive_points": [
      "Engaging introduction.",
      "Clear language."
    ],
    "areas_for_improvement": [
      "Add more humor.",
      "Improve pacing."
    ]
  }
}
'''


rewrite_prompt = f"""{role},
{critic_task}.
The script will be delimited with four hashtags,\
i.e. {delimiter}.
 
{video_structure}

{writing_tips}
"""


def process_line(args):
    line = args
    try:
        record = json.loads(line)
    except json.decoder.JSONDecodeError as e:
        print(f"{e} - {line}")
        return

    # we take original video
    video = record.get("video")

    reformatted_video = format_video_from_jsonl(video)

    # wait 3sec
    time.sleep(2)
    result = None
    try:
        messages = [
            {"role": "user", "content": rewrite_prompt +
             "\nVideo script: " + delimiter + reformatted_video + delimiter + "\n\n"
             }
        ]

        new_script = get_completion_from_messages(
            model="ft:mistral-small-latest:c056c2e4:20240628:f732bd21",
            # model="mistral-small-latest",
            # model="mistral-large-latest",
            messages=messages,
            temperature=0.2)

        new_video = {
            "video": {
                "title": video.get("title", ""),
                "transcript": new_script,
                "author": video.get("author", ""),
                "publication_date": video.get("publication_date", "")
            }
        }

        result = json.dumps(new_video)

    except Exception as e:
        print(f"{e} while processing {video}")
        return

    # Generate a random 8-digit hexadecimal string
    random_hash = secrets.token_hex(4)

    with open(f"{dump_directory}/result_new_enhanced_video_{random_hash}.jsonl", "w") as f1:
        f1.write(result)

    return result


if __name__ == "__main__":
    os.makedirs(dump_directory, exist_ok=True)

    with open(jsonl_input_file_path, "r") as f:
        lines = f.readlines()
        lines = [line for line in lines if line.strip()]
        results = process_map(process_line, lines, max_workers=10, chunksize=1)

        save_results(results, jsonl_output_file_path)
