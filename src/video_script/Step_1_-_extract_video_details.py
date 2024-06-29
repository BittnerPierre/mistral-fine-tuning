import json

from utils_videos import fetch_course_details

out_dir = "./data"

# Example usage
input_path = f"{out_dir}/deeplearning.json"
input_path2 = f"{out_dir}/deeplearning2.json"
output_path = f"{out_dir}/videos_details.jsonl"

base_url = "https://www.deeplearning.ai"

example_json = """{
    "results": [
        {
            "hits": [
                {
                    "title": "LangChain: Chat with Your Data",
                    "slug": "langchain-chat-with-your-data",
                    "date": "2023-07-05T00:11:36",
                    "date_timestamp": 1688515896000,
                    "landing_page": "/short-courses/langchain-chat-with-your-data",
                    "trailer_thumbnail": "https://wordpress.deeplearning.ai/wp-content/uploads/2023/07/LangChain_-Chat-with-Your-Data-1.png",
                    "trailer_yt_id": "fo7bD-NgA4Y",
                    "trailer_video_url": "",
                    "course_type": "Short Courses",
                    "skill_level": [
                        "Beginner"
                    ],
                    "partnership": [
                        "LangChain"
                    ],
                    "course": "",
                    "description": "Create a chatbot with LangChain to interface with your private data and documents. Learn from LangChain creator, Harrison Chase.",
                    "partnershipInfos": [
                        {
                            "title": "LangChain",
                            "logo": {
                                "sourceUrl": "https://wordpress.deeplearning.ai/wp-content/uploads/2024/06/langchain.png"
                            }
                        }
                    ],
                    "instructors": "Harrison Chase",
                    "difficulyLevle": "Beginner",
                    "courseDuration": "1 Hour",
                    "prerequisites": "Basic Python",
                    "enrollLink": "http://learn.deeplearning.ai/langchain-chat-with-your-data/",
                    "certificate": "",
                    "isPrivate": null,
                    "objectID": "cG9zdDozMTMxNg==",
                    "_highlightResult": {
                        "title": {
                            "value": "LangChain: Chat with Your Data",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "slug": {
                            "value": "langchain-chat-with-your-data",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "description": {
                            "value": "Create a chatbot with LangChain to interface with your private data and documents. Learn from LangChain creator, Harrison Chase.",
                            "matchLevel": "none",
                            "matchedWords": []
                        }
                    }
                },
                {
                    "title": "Generative AI with LLMs",
                    "slug": "generative-ai-with-llms",
                    "date": "2023-06-18T22:48:06",
                    "date_timestamp": 1687128486000,
                    "landing_page": "/courses/generative-ai-with-llms",
                    "trailer_thumbnail": "https://wordpress.deeplearning.ai/courses/generative-ai-with-llms/generative-ai-with-llms-1/",
                    "trailer_yt_id": null,
                    "trailer_video_url": null,
                    "course_type": "Courses",
                    "skill_level": [
                        "Intermediate"
                    ],
                    "partnership": [],
                    "course": "",
                    "description": "Understand the generative AI lifecycle. Describe transformer architecture powering LLMs. Apply training/tuning/inference methods. Hear from researchers on generative AI challenges/opportunities.",
                    "partnershipInfos": [
                        {
                            "title": "AWS",
                            "logo": {
                                "sourceUrl": "https://wordpress.deeplearning.ai/wp-content/uploads/2024/02/aws.jpeg"
                            }
                        }
                    ],
                    "instructors": "Antje Barth, Chris Fregly, Shelbee Eigenbrode Instructor, Mike Chambers",
                    "difficulyLevle": "",
                    "courseDuration": "",
                    "prerequisites": "Basic Python",
                    "enrollLink": "https://www.coursera.org/learn/generative-ai-with-llms?utm_campaign=WebsiteCoursesGAIA&utm_medium=institutions&utm_source=deeplearning-ai",
                    "certificate": "",
                    "isPrivate": null,
                    "objectID": "cG9zdDozMTE3Mg==",
                    "_highlightResult": {
                        "title": {
                            "value": "Generative AI with LLMs",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "slug": {
                            "value": "generative-ai-with-llms",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "description": {
                            "value": "Understand the generative AI lifecycle. Describe transformer architecture powering LLMs. Apply training/tuning/inference methods. Hear from researchers on generative AI challenges/opportunities.",
                            "matchLevel": "none",
                            "matchedWords": []
                        }
                    }
                },
            ]
        }
    ]
}"""

# Sample data extracted from your JSON description
def fetch_courses(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_path}: {e}")
        return None


def extract_course_details(courses, file_path, mode):
    extracted_data = []

    for result in courses["results"]:
        for course in result["hits"]:
            title = course["title"]
            description = course.get("description", "No description available.")
            prerequisites = course.get("prerequisites", "No prerequisites listed.")
            instructors = course.get("instructors", "No instructor listed.")
            landing_page = course.get("landing_page", "")
            skill_level = ", ".join(course.get("skill_level", ["No skill level listed."]))
            partnership = ", ".join(course.get("partnership", ["No partnership listed."]))

            course_details = {
                "Title": title,
                "Description": description,
                "Prerequisites": prerequisites,
                "Instructor": instructors,
                "Skill Level": skill_level,
                "Partnership": partnership,
                "Features": None
            }

            if landing_page:
                url = f"{base_url}{landing_page}"
                course_details["Landing Page"] = url
                features = fetch_course_details(url)
                if features:
                    course_details["Features"] = features

            extracted_data.append(course_details)

    with open(file_path, mode) as outfile:
        for entry in extracted_data:
            json_line = json.dumps(entry)
            outfile.write(json_line + '\n')



if __name__ == "__main__":
    courses = fetch_courses(input_path)
    extract_course_details(courses, output_path, "w")
    courses2 = fetch_courses(input_path2)
    extract_course_details(courses2, output_path, "a")