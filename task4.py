import pandas as pd
from datasets import load_dataset
import gzip
import shutil
import os
import re

def clean_special_characters(text):
    """
    Remove special characters from diff text to avoid string encoding errors
    """
    if pd.isna(text) or text is None:
        return ""

    # Convert to string if not already
    text = str(text)

    # Remove or replace problematic characters
    # Keep only ASCII printable characters and common whitespace
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)

    return text

# Load the 'pr_commit_details' subset from the dataset
print("Loading dataset from HuggingFace...")
dataset = load_dataset("hao-li/AIDev", "pr_commit_details")

# Access the train split
commit_data = dataset['train']
print(f"Loaded {len(commit_data)} commit details")

# Convert to pandas DataFrame
df = pd.DataFrame(commit_data)

# Print available columns to verify field names
print(f"\nAvailable columns: {df.columns.tolist()}")

# Create the output DataFrame with renamed columns
print("\nProcessing data and cleaning special characters from PRDIFF...")
output_df = pd.DataFrame({
    'PRID': df['pr_id'],
    'PRSHA': df['sha'],
    'PRCOMMITMESSAGE': df['message'],
    'PRFILE': df['filename'],
    'PRSTATUS': df['status'],
    'PRADDS': df['additions'],
    'PRDELSS': df['deletions'],
    'PRCHANGECOUNT': df['changes'],
    'PRDIFF': df['patch'].apply(clean_special_characters)  # Clean special characters
})

# Save to CSV
output_file = 'task4_output.csv'
print(f"\nSaving to CSV...")
output_df.to_csv(output_file, index=False, encoding='utf-8')

print(f"\n✓ Task 4 Complete!")
print(f"Total commit details processed: {len(output_df)}")
print(f"CSV file saved as: {output_file}")

# Create compressed version for GitHub
compressed_file = 'task4_output.csv.gz'
print(f"\nCreating compressed version for GitHub...")
with open(output_file, 'rb') as f_in:
    with gzip.open(compressed_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

original_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
compressed_size = os.path.getsize(compressed_file) / (1024 * 1024)  # MB
compression_ratio = (1 - compressed_size / original_size) * 100

print(f"✓ Original CSV size: {original_size:.2f} MB")
print(f"✓ Compressed size: {compressed_size:.2f} MB ({compression_ratio:.1f}% reduction)")
print(f"\n📦 Upload '{compressed_file}' to GitHub (it's much smaller!)")

print(f"\nFirst 5 rows:")
print(output_df.head())

# Show statistics
print(f"\n📊 Dataset Statistics:")
print(f"- Total Commits: {len(output_df)}")
print(f"- Unique PRs: {output_df['PRID'].nunique()}")
print(f"- Unique Files: {output_df['PRFILE'].nunique()}")
print(f"- Total Additions: {output_df['PRADDS'].sum()}")
print(f"- Total Deletions: {output_df['PRDELSS'].sum()}")