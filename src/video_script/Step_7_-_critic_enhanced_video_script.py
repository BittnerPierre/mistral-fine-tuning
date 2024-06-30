import secrets
from json import JSONDecodeError

from tqdm.contrib.concurrent import process_map
import json
import time

import os

from dotenv import load_dotenv, find_dotenv

from video_prompt import critic_prompt, evaluation_framework, delimiter
from utils import get_completion_from_messages, save_results
from video_script.utils_videos import format_video_from_jsonl

_ = load_dotenv(find_dotenv())

out_dir = "./data"
dump_directory = f"{out_dir}/dumps-7"

jsonl_input_file_path = f"{out_dir}/enhanced_videos_mistral-large-latest.jsonl"
jsonl_output_file_path = f"{out_dir}/enhanced_video_critics_mistral-large-latest.jsonl"

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


def process_line(args):
    line = args
    try:
        record = json.loads(line)
    except json.decoder.JSONDecodeError as e:
        print(f"{e} - {line}")
        return

    video = record.get("video")

    reformatted_video = format_video_from_jsonl(video)

    # wait 3sec
    time.sleep(1)
    result = None
    try:
        messages = [
            {"role": "user", "content": critic_prompt + evaluation_framework +
             "\nVideo script: " + delimiter + reformatted_video + delimiter + "\n\n" +
             "Critical advises:" + delimiter + "<critical advises>" +
             "Make sure to include " + delimiter + " to separate every step."
             }
        ]

        critique = None
        if not debug:
            try:
                critique = get_completion_from_messages(
                    messages=messages,
                    temperature=0.2)

                critique_split = critique.split(delimiter)[-1].strip()
                critique_json = json.loads(critique_split)
            except JSONDecodeError as je:
                print(f"Error while parsing critique: {je}")
                print(f"Critique : {critique}")
                return
        else:
            critique_json = json.loads(fake_critic_str)
            print(messages)

        if critique_json:
            result = json.dumps(
                {"video": video, "analysis": critique_json}
            )
    except Exception as e:
        print(f"{e} while processing {video}")
        return

    # Generate a random 8-digit hexadecimal string
    random_hash = secrets.token_hex(4)

    with open(f"{dump_directory}/result_new_critique_video_{random_hash}.jsonl", "w") as f1:
        f1.write(result)

    return result


if __name__ == "__main__":
    os.makedirs(dump_directory, exist_ok=True)

    with open(jsonl_input_file_path, "r") as f:
        lines = f.readlines()
        lines = [line for line in lines if line.strip()]
        results = process_map(process_line, lines, max_workers=10, chunksize=1)

        save_results(results, jsonl_output_file_path)
