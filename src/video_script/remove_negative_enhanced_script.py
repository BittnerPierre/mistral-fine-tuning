import pandas as pd
import json

with open('./data/generated_enhanced_video_scored.jsonl', 'r') as file:
    for i in range(5):  # read first 5 lines
        print(file.readline().strip())

# Read the JSONL file line by line
df = pd.read_json('./data/generated_enhanced_video_scored.jsonl', lines=True)

print(df.head())

# Normalize the nested JSON data so that 'improvement.overall' becomes a top-level column
improvement_df = pd.json_normalize(df['improvement'])

# Normalize the 'video' column
video_df = pd.json_normalize(df['video'])

# Combine the normalized improvements and video structures back with the original DataFrame
df = pd.concat([df, improvement_df, video_df], axis=1)

# Print out the columns to inspect them
print("Columns in DataFrame:", df.columns)

# Check if 'overall' and 'title' columns now exist in the DataFrame
if 'overall' in df.columns and 'title' in df.columns:
    # Extract titles where the overall improvement is negative
    negative_improvement_titles = df[df['overall'] < 0]['title'].tolist()

    # Print the count of negative improvements
    print(f"Count of negative improvements: {len(negative_improvement_titles)}")

    # Print the titles with negative overall improvement, one per line
    for title in negative_improvement_titles:
        print(title)

        # Generate statistics on how many times each title appears
    title_counts = df['title'].value_counts()

    print("\nTitle appearance statistics:")
    print(title_counts)
else:
    print("Required columns not found in DataFrame.")
