import pandas as pd
import json

# Sample JSON line (you can replace this with the file reading part)
fine_tuned_jsonl_file_path = './data/enhanced_video_critics_fine-tuned.jsonl'

# Sample JSON line (you can replace this with the file reading part)
initial_jsonl_file_path = './data/generated_enhanced_video_scored.jsonl'






def compute_score(df):

    # Create DataFrames for initial and revised scores
    scores_df = pd.json_normalize(df['analysis'].apply(lambda x: x['score']))

    # Calculate the initial and revised average scores for 'overall'
    average_overall = scores_df['overall'].mean()
    average_tone = scores_df['tone'].mean()
    structure_and_content = scores_df['structure_and_content'].mean()

    average_overall = round(average_overall, 5)
    average_tone_overall = round(average_tone, 5)
    average_structure_and_content_overall = round(structure_and_content, 5)

    return average_overall, average_tone_overall, average_structure_and_content_overall


if __name__ == "__main__":

    # Load the JSONL data
    initial_data = []
    with open(initial_jsonl_file_path, 'r') as f:
        for line in f:
            initial_data.append(json.loads(line))

    # Create a DataFrame
    df = pd.DataFrame(initial_data)

    # Create DataFrames for initial and revised scores
    initial_scores_df = pd.json_normalize(df['score'])

    # Calculate the initial and revised average scores for 'overall'
    initial_average_overall = initial_scores_df['overall'].mean()
    initial_average_tone = initial_scores_df['tone'].mean()
    initial_average_structure_and_content = initial_scores_df['structure_and_content'].mean()

    initial_average_overall = round(initial_average_overall, 5)
    initial_average_tone = round(initial_average_tone, 5)
    initial_average_structure_and_content = round(initial_average_structure_and_content, 5)

    # Print initial and revised average overall scores
    print("------ Initial statistics")
    print(f"Initial / Average: {initial_average_overall}, Tone: {initial_average_tone}, Structure and content: {initial_average_structure_and_content}")

    # Load the JSONL data
    data_fine_tuned = []
    with open(fine_tuned_jsonl_file_path, 'r') as f:
        for line in f:
            data_fine_tuned.append(json.loads(line))

    # Create a DataFrame
    df = pd.DataFrame(data_fine_tuned)

    fine_tuned_average, fine_tuned_tone, fine_tuned_structure_and_content = compute_score(df)

    print("------ Fine Tuned statistics")
    print(f"Fine Tuned / Average: {fine_tuned_average}, Tone: {fine_tuned_tone}, Structure and content: {fine_tuned_structure_and_content}")

