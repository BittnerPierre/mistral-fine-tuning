
import requests
from bs4 import BeautifulSoup


def fetch_course_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract course highlights
        features_section = soup.find("section", id="features")
        features = features_section.text.strip() if features_section else "No features section found"
        features = "\n".join(line for line in features.split("\n") if line.strip())  # Remove empty lines

        return f"{features}"
    else:
        return None

# example = "{\"video\":{\"title\": \"<title>\",\"transcript\": \"<transcript>\",\"author\": \"<author>\",\"publication_date\": \"<publication_date>\"}}"

def format_video_from_jsonl(jsonl_string):
    """
    Format the content of a news article from a JSONL string.

    Args:
    jsonl_string (str): A JSONL string containing the news article details.

    Returns:
    str: A string with the formatted content of the news article.
    """
    try:
        video = jsonl_string

        title = video.get("title", "")
        transcript = video.get("transcript", "")
        author = video.get("author", "")
        date = video.get("publication_date", "")

        formatted_content = (
            f"{title}\n"
            f"by {author} - {date}\n"
            f"\n#### BEGIN TRANSCRIPT ####\n"
            f"{transcript}\n"
            f"#### END TRANSCRIPT ####"
        )
    except TypeError as te:
        print(f"format_video_from_jsonl error: te")
        return jsonl_string

    return formatted_content


def format_critique_from_jsonl(json_data):
    data = json_data # json.loads(json_data)
    positive_points = data['critique']['positive_points']
    areas_for_improvement = data['critique']['areas_for_improvement']

    formatted_critique = "Positive Points:\n\n"
    for point in positive_points:
        formatted_critique += f"- {point}\n"

    formatted_critique += "\nAreas for Improvement:\n\n"
    for point in areas_for_improvement:
        formatted_critique += f"- {point}\n"

    return formatted_critique.strip()


if __name__ == "__main__":
    # URL for the course page
    course_url = "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/"
    course_url = "https://www.deeplearning.ai/short-courses/prompt-engineering-with-llama-2"
    # Fetch and print course details
    course_details = fetch_course_details(course_url)
    print(course_details)