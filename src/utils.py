import shutil
from datetime import datetime

from mistralai.client import MistralClient
import os

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv("MISTRAL_API_KEY")
client = MistralClient(api_key=api_key)

client2 = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv('OPENAI_API_KEY')
)

def get_completion_from_messages(messages,
                                 model="mistral-large-latest",
                                 temperature=0,
                                 response_format=None,
                                 ):
    response = client.chat(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format=response_format
    )
    return response .choices[0].message.content


def get_completion_from_messages2(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 response_format=None):
    response = client2.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content


def format_news_article_from_jsonl(jsonl_string):
    """
    Format the content of a news article from a JSONL string.

    Args:
    jsonl_string (str): A JSONL string containing the news article details.

    Returns:
    str: A string with the formatted content of the news article.
    """
    try:
        article = jsonl_string

        title = article.get("title", "")
        content = article.get("content", "")
        author = article.get("author", "")
        location = article.get("location", "")
        date = article.get("date", "")

        formatted_content = (
            f"{title}\n\n"
            f"{author}\n\n"
            f"{date}\n\n"
            f"{content}\n\n"
            f"{location}\n"
        )
    except TypeError as te:
        print(te)
        return jsonl_string

    return formatted_content

def save_results(results, jsonl_output_file_path):
    # Check if the file exists
    if os.path.exists(jsonl_output_file_path):
        # Get current time suffix
        time_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Formulate backup file path
        # Find the position of the last dot before the extension
        base_name, extension = os.path.splitext(jsonl_output_file_path)
        # Formulate backup file path
        backup_file_path = f"{base_name}_{time_suffix}{extension}"
        # Backup the existing file
        shutil.copy(jsonl_output_file_path, backup_file_path)
        print(f"Existing file backed up as: {backup_file_path}")

    # Create a new file and save results
    with open(jsonl_output_file_path, "w") as f:
        for result in results:
            if result is not None:
                f.write(result + '\n')