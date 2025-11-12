"""
Task-1: Extract specific fields from the all_pull_request table
from the AIDev dataset and save to CSV
"""

from datasets import load_dataset
import pandas as pd

def extract_pull_request_data():
    """
    Load the AIDev dataset and extract specified fields from all_pull_request table
    """
    print("Loading dataset from HuggingFace...")

    try:
        # Load the dataset
        dataset = load_dataset("hao-li/AIDev")

        # Print available splits to debug
        print(f"Available splits: {list(dataset.keys())}")

        # Access the train split (which contains all_pull_request data)
        pull_requests = dataset['train']

        print(f"Loaded {len(pull_requests)} pull requests")

        # Print column names to see what fields are available
        print(f"Available columns: {pull_requests.column_names}")

        # Extract the required fields
        data = {
            'TITLE': [],
            'ID': [],
            'AGENTNAME': [],
            'BODYSTRING': [],
            'REPOID': [],
            'REPOURL': []
        }

        print("Extracting data...")
        for pr in pull_requests:
            data['TITLE'].append(pr.get('title', ''))
            data['ID'].append(pr.get('id', ''))
            data['AGENTNAME'].append(pr.get('agent', ''))
            data['BODYSTRING'].append(pr.get('body', ''))
            data['REPOID'].append(pr.get('repo_id', ''))
            data['REPOURL'].append(pr.get('repo_url', ''))

        # Create DataFrame
        df = pd.DataFrame(data)

        # Save to CSV
        output_file = 'task1_output.csv'
        df.to_csv(output_file, index=False)

        print(f"\n✓ Successfully created CSV file: {output_file}")
        print(f"✓ Total records: {len(df)}")
        print(f"\nFirst few rows:")
        print(df.head())

        # Display basic statistics
        print(f"\nDataset Statistics:")
        print(f"- Total Pull Requests: {len(df)}")
        print(f"- Unique Agents: {df['AGENTNAME'].nunique()}")
        print(f"- Unique Repositories: {df['REPOID'].nunique()}")

        return df

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure you have installed required packages:")
        print("   pip install datasets pandas")
        print("2. Check your internet connection")
        print("3. Verify the dataset name is correct")
        return None

if __name__ == "__main__":
    print("="*60)
    print("Task-1: AIDev Dataset - Pull Request Data Extraction")
    print("="*60)

    df = extract_pull_request_data()

    if df is not None:
        print("\n" + "="*60)
        print("Task completed successfully!")
        print("="*60)