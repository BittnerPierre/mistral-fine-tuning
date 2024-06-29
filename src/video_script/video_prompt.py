video_structure = f"""The video must follow this structure :\n 
- [Video hook and introduction]\n
- [Body content]\n
- [Conclusion and call to action]\n"""

writing_tips = """The video must follow those writing tips:
 1) Use Short Sentences.
 2) Use the Present Tense.
 3) Use first person
 3) Write in a Conversational Style.
 4) Use More Active Voice Than Passive Voice.
 5) Be Clear and simple: translates jargon into simpler words.
 6) Sprinkle in Some Humor.
 7) Avoid repetition.
 8) Avoid conventional messages and overdoing it with words like “cutting edge”, “revolutionize
 9) Be Confident: removes words that undermine authority.
 10) Be Concise: makes writing more digestible with fewer than 25 words in a sentence,
 fewer than 4 sentences per paragraph, and no double descriptions."""

role = "As a 'Youtube Video Script Writer' for 'GenAI and LLM powered application' influencer"

critic_task = ("your task is to refine video script to ensure they are engaging"
               " and meet the expected style and structure")

evaluation_framework = """# Evaluation Framework
Point attribution should be lowered. In case of 0.5 point, give 0.

## Evaluation of the Tone - 12 points

The video must follow these writing styles:
1. Conciseness: use Short Sentences (less than 25 words per sentence): 1 point
2. Use the Present Tense: 1 point
3. Use first person: 1 point
4. Write in a conversational style: 1 point
5. Use more active voice than passive voice: 1 point
6. Keep it simple - no jargon employed: 1 point
7. Sprinkle in some Humor: 1 point
8. Avoid repetition: 1 point
9. Avoid conventional messages: 1 point
10. Avoid overdoing it or over-sensational with words like “cutting edge”, “revolutionize”: 1 point
11. Confident: no words that undermine authority: 1 point
12. Energetic and Enthusiastic Tone: 1 point

## Evaluation of the Structure and Content: 12 points

### Section 1: Video hook and intro: 6 points
- Does the script provide enough context for the video to make sense? 1 point
- Does the Stakes and payoff are introduce to know why we should watch until the end? 1 point
- A curiosity gap is created: What viewers want to know and not all information is given away. 1 point
- Leverage input bias: the effort (time, energy, money) that went into the video is showed. 1 point
- The video body starts no later than the 20-second mark 1 point
- Includes an engaging story or comparison to make the topic relatable 1 point
### Section 2: Body, main content, and research: 4 points
- Consistent contrast is incorporated to keep things from getting stale 1 point
- Good pacing: cycles of high energy and low energy are alternated 1 point
    - Each cycle should be 2 - 4 minutes long, with shorter cycles in the beginning and longer cycles at the end 1 point
    - The last 20% of long video can be used for slower content, while the beginning of the video is allocated for lighter, faster content 1 point
- Critical analysis and personal insights are included 1 point
- Practical, real-world applications of the technologies are discussed 1 point
- Balanced optimism and realism 1 point
### Section 3: CTA (call to action) and conclusion: 2 points
- Conclusion leaves a lasting impression by revealing the payoff 1 point
- Ends on a high note, either dramatic, wholesome, or funny 1 point

## Global score (10): half tone, half structure, and content
"""

delimiter = "####"

example_critic_format = '''
{
  "score": {
    "overall": 5.5,
    "tone": 8,
    "structure_and_content": 3
  },
  "critique": {
    "positive_points": [
      "Clear introduction of the topic and advantages of Streamlit.",
      "Use of active voice and simple language.",
      "Present and encouraging call to action."
    ],
    "areas_for_improvement": [
      "Add more humor to make the content more enjoyable.",
      "Introduce more curiosity and stakes at the beginning to capture the audience.",
      "Improve contrast and pacing to maintain interest.",
      "Make the conclusion more memorable and engaging."
    ]
  }
}
'''

simple_critic_prompt = f"""{role},
{critic_task}.

Read the transcript carefully and point out all stylistic issues according
to the following writing style guide. 

{writing_tips}

{video_structure}

Do not rewrite the transcript.

"""


critic_prompt = f"""{role},
{critic_task}.

An evaluation framework to check writing style and script structure will be given to you below.

Follow these steps to review the video script.
The transcript and each steps will be delimited with four hashtags,\
i.e. {delimiter}. 

You will revise the script by following these steps in order:
- Step 1:{delimiter} Assimilate the evaluation framework. Don't write anything.
- Step 2:{delimiter} Analyse critically the script and point out all the stylistic, structure and content issues.
- Step 3:{delimiter} Grade the script using the evaluation framework. Write down score for style,
 structure and global score.
- Step 4:{delimiter} Write down the strong points of the script that must be kept.
- Step 5:{delimiter} Write down the most critical changes.
- Step 5:{delimiter} Make a report with score: global, style, structure and critique: strong points, critical changes.
Report must be in a json line format.

Use the following format:
Step 1:{delimiter} <step 1 reasoning>
Step 2:{delimiter} <step 2 reasoning>
Step 3:{delimiter} <step 3 reasoning>
Step 4:{delimiter} <step 4 reasoning>
Critique: {delimiter} {example_critic_format}

Do not rewrite the transcript. \n\n"""

count = 10

synthesize_task = (f"your task is to write {count} scripts"
                   " of engaging videos of 5 to 10 minutes (1000 to 2000 words) each.")
