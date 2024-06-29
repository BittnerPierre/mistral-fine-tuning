import pandas as pd
import json

# Sample JSON line (you can replace this with the file reading part)
jsonl_file_path = './data/generated_enhanced_video_scored.jsonl'

# Load the JSONL data
data = []
with open(jsonl_file_path, 'r') as f:
    for line in f:
        data.append(json.loads(line))

# Create a DataFrame
df = pd.DataFrame(data)

# Create DataFrames for initial and revised scores
initial_scores_df = pd.json_normalize(df['score'])
revised_scores_df = pd.json_normalize(df['new_score'])

# Create a DataFrame for improvements
improvements_df = pd.json_normalize(df['improvement'])

# Calculate the average improvement for each category
average_overall_improvement = improvements_df['overall'].mean()
average_tone_improvement = improvements_df['tone'].mean()
average_structure_and_content_improvement = improvements_df['structure_and_content'].mean()

# Calculate the initial and revised average scores for 'overall'
initial_average_overall = initial_scores_df['overall'].mean()
revised_average_overall = revised_scores_df['overall'].mean()

initial_average_overall = round(initial_average_overall, 5)
revised_average_overall = round(revised_average_overall, 5)
average_overall_improvement = round(average_overall_improvement, 5)
average_tone_improvement = round(average_tone_improvement, 5)
average_structure_and_content_improvement = round(average_structure_and_content_improvement, 5)


# Print initial and revised average overall scores
print("------")
print("Initial Average Overall Score:", initial_average_overall)
print("Enhanced Average Overall Score:", revised_average_overall)
print("------")
print("Average Overall Improvement:", average_overall_improvement)
print("Average Tone Improvement:", average_tone_improvement)
print("Average Structure and Content Improvement:", average_structure_and_content_improvement)


# Filter out rows with negative overall improvement
negative_improvements_df = df[improvements_df['overall'] >= 0]

# Recalculate statistics for positive improvements only
if not negative_improvements_df.empty:
    # Recreate DataFrames for initial and revised scores with positive improvements only
    initial_scores_negative_df = pd.json_normalize(negative_improvements_df['score'])
    revised_scores_negative_df = pd.json_normalize(negative_improvements_df['new_score'])
    improvements_negative_df = pd.json_normalize(negative_improvements_df['improvement'])

    # Calculate the average improvements for positive improvements only
    avg_overall_improvement_neg = improvements_negative_df['overall'].mean()
    avg_tone_improvement_neg = improvements_negative_df['tone'].mean()
    avg_structure_and_content_improvement_neg = improvements_negative_df['structure_and_content'].mean()

    # Calculate the initial and revised average scores for 'overall' for positive improvements only
    initial_avg_overall_neg = initial_scores_negative_df['overall'].mean()
    revised_avg_overall_neg = revised_scores_negative_df['overall'].mean()

    initial_avg_overall_neg = round(initial_avg_overall_neg, 5)
    revised_avg_overall_neg = round(revised_avg_overall_neg, 5)
    avg_overall_improvement_neg = round(avg_overall_improvement_neg, 5)
    avg_tone_improvement_neg = round(avg_tone_improvement_neg, 5)
    avg_structure_and_content_improvement_neg = round(avg_structure_and_content_improvement_neg, 5)

    # Print statistics for positive improvements only
    print("------")
    print("Statistics excluding negative overall improvements:")
    print("Initial Average Overall Score:", initial_avg_overall_neg)
    print("Enhanced Average Overall Score:", revised_avg_overall_neg)
    print("------")
    print("Average Overall Improvement:", avg_overall_improvement_neg)
    print("Average Tone Improvement:", avg_tone_improvement_neg)
    print("Average Structure and Content Improvement:", avg_structure_and_content_improvement_neg)
else:
    print("------")
    print("No positive overall improvements to display statistics for.")

# Filter out rows with negative overall improvement
negative_improvements_df = df[improvements_df['overall'] < 0]

# Recalculate statistics for positive improvements only
if not negative_improvements_df.empty:
    # Recreate DataFrames for initial and revised scores with positive improvements only
    initial_scores_negative_df = pd.json_normalize(negative_improvements_df['score'])
    revised_scores_negative_df = pd.json_normalize(negative_improvements_df['new_score'])
    improvements_negative_df = pd.json_normalize(negative_improvements_df['improvement'])

    # Calculate the average improvements for positive improvements only
    avg_overall_improvement_neg = improvements_negative_df['overall'].mean()
    avg_tone_improvement_neg = improvements_negative_df['tone'].mean()
    avg_structure_and_content_improvement_neg = improvements_negative_df['structure_and_content'].mean()

    # Calculate the initial and revised average scores for 'overall' for positive improvements only
    initial_avg_overall_neg = initial_scores_negative_df['overall'].mean()
    revised_avg_overall_neg = revised_scores_negative_df['overall'].mean()

    initial_avg_overall_neg = round(initial_avg_overall_neg, 5)
    revised_avg_overall_neg = round(revised_avg_overall_neg, 5)
    avg_overall_improvement_neg = round(avg_overall_improvement_neg, 5)
    avg_tone_improvement_neg = round(avg_tone_improvement_neg, 5)
    avg_structure_and_content_improvement_neg = round(avg_structure_and_content_improvement_neg, 5)

    # Print statistics for positive improvements only
    print("------")
    print("Statistics excluding postive overall improvements:")
    print("Initial Average Overall Score:", initial_avg_overall_neg)
    print("Enhanced Average Overall Score:", revised_avg_overall_neg)
    print("------")
    print("Average Overall Improvement:", avg_overall_improvement_neg)
    print("Average Tone Improvement:", avg_tone_improvement_neg)
    print("Average Structure and Content Improvement:", avg_structure_and_content_improvement_neg)
else:
    print("------")
    print("No negative overall improvements to display statistics for.")