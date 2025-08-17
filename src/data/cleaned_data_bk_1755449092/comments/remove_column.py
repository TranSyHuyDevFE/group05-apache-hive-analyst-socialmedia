import pandas as pd

# Read CSV file with error handling
try:
    df = pd.read_csv('./comments_17_08_2025.csv',
                     on_bad_lines='skip',  # Skip problematic lines
                     quoting=1,            # Handle quoted fields properly
                     encoding='utf-8')     # Ensure proper encoding
except Exception as e:
    print(f"Error reading CSV: {e}")
    # Try with different options
    df = pd.read_csv('./comments_17_08_2025.csv',
                     on_bad_lines='skip',
                     sep=',',
                     quotechar='"',
                     encoding='utf-8',
                     engine='python')

# Keep only specified columns
columns_to_keep = ['username', 'content', 'likes', 'video_url', 'sentiment']
df_filtered = df[columns_to_keep]

# Optional: Save filtered data to new CSV file
df_filtered.to_csv('filtered_output.csv', index=False)

# Display the filtered dataframe
print(df_filtered.head())
print(f"Shape of filtered data: {df_filtered.shape}")
print(f"Available columns: {df.columns.tolist()}")
