import glob
import secrets

from tqdm.contrib.concurrent import process_map
import json
import random
import time

import os
from mistralai.client import MistralClient

from utils import save_results, get_completion_from_messages
from video_script.utils_videos import format_video_from_jsonl, format_critique_from_jsonl
from video_script.video_prompt import critic_prompt, evaluation_framework, simple_critic_prompt

api_key = os.environ.get("MISTRAL_API_KEY")
client = MistralClient(api_key=api_key)

out_dir = "./data"
dump_directory = f"{out_dir}/dumps-4"

conversation_jsonl_output_file_path = f"{out_dir}/generated_video_conversation.jsonl"
enhanced_jsonl_output_file_path = f"{out_dir}/generated_enhanced_video.jsonl"

debug = False


def process_line(args):
    line, prompts = args
    # if debug:
    #     print(line)
    try:
        record = json.loads(line)
    except json.decoder.JSONDecodeError as e:
        print(f"{e} - {line}")
        return

    video = record.get("video")
    if debug:
        print(f"Video source: {video}")
    analysis = record.get("analysis")
    if debug:
        print(f"Critique source: {analysis}")

    part = random.choice(list(range(20)))
    prompt = prompts[part]

    formatted_video = format_video_from_jsonl(video)
    if debug:
        print(f"Video Formatted: {formatted_video}")
    formatted_critique = format_critique_from_jsonl(analysis)
    if debug:
        print(f"Critique Formatted: {formatted_critique}")

    # wait 3sec
    time.sleep(1)
    messages = [
        {"role": "user", "content": critic_prompt + evaluation_framework +
         "\nVideo Transcript: " + formatted_video + "\n"},
        {"role": "assistant", "content": formatted_critique},
        {"role": "user", "content": prompt}
    ]
    try:
        new_script = get_completion_from_messages(
            messages=messages,
            temperature=0.2)
    except Exception as e:
        print(f"{e} while processing {str(video)}")
        return

    result = json.dumps(
        # {"news": news, "critique": critique, "corrected_news": new_news}
        {
            "messages": [
                {"role": "user", "content": simple_critic_prompt +
                 "\nVideo: " + formatted_video + "\n"},
                {"role": "assistant", "content": formatted_critique},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": new_script}
            ]
        }
    )

    new_video = {
        "video": {
            "title": video.get("title", ""),
            "transcript": video.get("transcript", ""),
            "author": video.get("author", ""),
            "publication_date": video.get("publication_date", "")
        },
        "score": analysis.get("score"),
        "new_video": {
            "title": video.get("title", ""),
            "transcript": new_script,
            "author": video.get("author", ""),
            "publication_date": video.get("publication_date", "")
        },
    }

    new_video_s = json.dumps(new_video)

    # Generate a random 8-digit hexadecimal string
    random_hash = secrets.token_hex(4)

    with open(f"{dump_directory}/result_new_video_conversation_{random_hash}.jsonl", "w") as f1:
        f1.write(result)

    # Save the result to a .jsonl file
    with open(f"{dump_directory}/result_new_video_{random_hash}.jsonl", "w") as f2:
        json.dump(new_video_s, f2)

    return result, new_video_s


def separate_lists(tuple_list):
    _conversations = []
    _videos = []

    for item in tuple_list:
        conversation, video = item
        _conversations.append(conversation)
        _videos.append(video)

    return _conversations, _videos


if __name__ == "__main__":

    os.makedirs(dump_directory, exist_ok=True)

    guides = [
        "Incorporate the feedback into the video transcript and respond with the enhanced version, focusing solely on stylistic improvements without altering the content.",
        "Refine the video transcript using the provided feedback and reply with the revised version, ensuring that only the style is enhanced while the content remains unchanged.",
        "Use the feedback to polish the video transcript and return with the improved version, making sure to enhance only the style and keep the content intact.",
        "Integrate the feedback into the video transcript and respond with the updated version, focusing exclusively on stylistic improvements without modifying the content.",
        "Enhance the video transcript according to the feedback and answer with the revised version, ensuring that only the style is refined while the content stays the same.",
        "Apply the feedback to the video transcript to enhance its style and provide the improved version, without changing the original content.",
        "Use the feedback to revise the video transcript for better style and reply with the updated version, keeping the content consistent.",
        "Incorporate the feedback to improve the style of the video transcript and provide the revised version, ensuring the content remains unaltered.",
        "Refine the video transcript based on the feedback, focusing on stylistic enhancements, and respond with the improved version without altering the content.",
        "Apply the provided feedback to enhance the style of the video transcript and reply with the updated version, keeping the original content unchanged.",
        "Use the feedback to revise the video transcript for a better style and return with the enhanced version, ensuring the content remains the same.",
        "Integrate the feedback to polish the style of the video transcript and provide the improved version, without changing the content.",
        "Refine the video transcript using the feedback and reply with the revised version, focusing solely on stylistic improvements without modifying the content.",
        "Apply the feedback to improve the video transcript's style and respond with the enhanced version, keeping the content intact.",
        "Use the feedback to polish the video transcript for a better style and reply with the updated version, ensuring the content stays consistent.",
        "Incorporate the feedback into the video transcript to enhance its style and provide the improved version without changing the original content.",
        "Refine the video transcript based on the feedback and respond with the enhanced version, focusing only on stylistic improvements without altering the content.",
        "Apply the feedback to revise the video transcript for a better style and reply with the updated version, ensuring the content remains unchanged.",
        "Use the feedback to enhance the style of the video transcript and provide the revised version, keeping the content consistent.",
        "Integrate the feedback to improve the style of the video transcript and respond with the enhanced version, without modifying the content."
    ]

    # Pattern to match all versions of generated_video_critique.jsonl with time suffixes
    # Base name and extension
    base_name = "generated_video_critique"
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

            conversations, new_videos = separate_lists(results)

            save_results(conversations, conversation_jsonl_output_file_path)
            save_results(new_videos, enhanced_jsonl_output_file_path)
