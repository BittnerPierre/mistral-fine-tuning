import pandas as pd


def check_unique_titles(jsonl_file):
    # Read the JSON lines file into a DataFrame
    df = pd.read_json(jsonl_file, lines=True)

    # Extract the titles from the original video data and new video data
    original_titles = df['video'].apply(lambda x: x['title'])
    new_titles = df['new_video'].apply(lambda x: x['title'])

    # Combine the titles into one list
    all_titles = list(original_titles) + list(new_titles)

    # Check for uniqueness by comparing length of set with length of list
    if len(all_titles) == len(set(all_titles)):
        print("All video titles are unique.")
    else:
        print("There are duplicate video titles.")
        # Optionally, print out the duplicate titles
        duplicates = pd.Series(all_titles).value_counts()
        duplicates = duplicates[duplicates > 1]
        print("Number of duplicate titles:", len(duplicates))
        print("Duplicate titles are:", duplicates.index.tolist())

    # Print line count
    print("Total line count in the file:", len(df))


# Usage
check_unique_titles('./data/generated_enhanced_video.jsonl')
