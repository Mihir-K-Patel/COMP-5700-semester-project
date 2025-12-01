import pandas as pd
from datasets import load_dataset

# Load the subset from the dataset
dataset = load_dataset("hao-li/AIDev", "pr_task_type")

# Access the train split
repo_data = dataset['train']
print(f"Loaded {len(repo_data)} repositories")

# Convert to pandas DataFrame
df = pd.DataFrame(repo_data)

# Create the output DataFrame with renamed columns
output_df = pd.DataFrame({
    'PRID': df['id'],
    'PRTITLE': df['title'],
    'PRREASON': df['reason'],
    'PRTYPE': df['type'],
    'CONFIDENCE': df['confidence']
})

# Save to CSV
output_df.to_csv('task3_output.csv', index=False, encoding='utf-8')

print(f"\n✓ Task 3 Complete!")
print(f"Total repositories processed: {len(output_df)}")
print(f"CSV file saved as: task3_output.csv")
print(f"\nFirst 5 rows:")
print(output_df.head())