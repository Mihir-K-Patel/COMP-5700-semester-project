import pandas as pd
import os
import re

def create_task5_output():
    """
    Combines outputs from tasks 1-4 into a single CSV file with specified columns:
    ID, AGENT, TYPE, CONFIDENCE, SECURITY

    Column sources:
    - ID: PRID from task3/task4 (Pull Request ID)
    - AGENT: AGENTNAME from task1 (mapped via ID -> REPOID -> REPOURL)
    - TYPE: PRTYPE from task3
    - CONFIDENCE: CONFIDENCE from task3
    - SECURITY: Boolean flag determined by security-related keywords
    """

    # File paths
    task1_file = 'task1_output.csv'
    task2_file = 'task2_output.csv'
    task3_file = 'task3_output.csv'
    task4_file = 'task4_output.csv'
    output_file = 'task5_output.csv'

    print("Starting Task 5: Combining outputs from Tasks 1-4...")
    print("=" * 70)

    # Check if all input files exist
    missing_files = []
    for file in [task1_file, task2_file, task3_file, task4_file]:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"Error: The following files are missing: {', '.join(missing_files)}")
        return

    # Read CSV files with low_memory=False to handle large files
    print("\n[1/4] Reading task1_output.csv (622 MB)...")
    df1 = pd.read_csv(task1_file, low_memory=False)
    print(f"      Columns: {list(df1.columns)}")
    print(f"      Shape: {df1.shape}")

    print("\n[2/4] Reading task2_output.csv (8.7 MB)...")
    df2 = pd.read_csv(task2_file, low_memory=False)
    print(f"      Columns: {list(df2.columns)}")
    print(f"      Shape: {df2.shape}")

    print("\n[3/4] Reading task3_output.csv (6.9 MB)...")
    df3 = pd.read_csv(task3_file, low_memory=False)
    print(f"      Columns: {list(df3.columns)}")
    print(f"      Shape: {df3.shape}")

    print("\n[4/4] Reading task4_output.csv (1.67 GB)...")
    df4 = pd.read_csv(task4_file, low_memory=False)
    print(f"      Columns: {list(df4.columns)}")
    print(f"      Shape: {df4.shape}")

    print("\n" + "=" * 70)
    print("Merging and processing data...")
    print("=" * 70)

    # Start with task3 as it has PRID, PRTYPE, and CONFIDENCE
    print("\n[Step 1] Using task3 as base (has PRID, PRTYPE, CONFIDENCE)...")
    final_df = df3[['PRID', 'PRTYPE', 'CONFIDENCE']].copy()
    final_df.rename(columns={'PRID': 'ID', 'PRTYPE': 'TYPE'}, inplace=True)

    # Merge with task1 to get AGENTNAME
    # Task1's ID column = Task3's PRID column (both are PR IDs)
    print("[Step 2] Merging with task1 to get AGENT names...")
    df1_subset = df1[['ID', 'AGENTNAME']].copy()
    final_df = final_df.merge(df1_subset, on='ID', how='left')
    final_df.rename(columns={'AGENTNAME': 'AGENT'}, inplace=True)

    # Merge with task4 to get more PR details for security detection
    print("[Step 3] Merging with task4 to get PR commit details...")
    df4_subset = df4[['PRID', 'PRCOMMITMESSAGE']].copy()
    final_df = final_df.merge(df4_subset, left_on='ID', right_on='PRID', how='left')
    final_df.drop(columns=['PRID'], inplace=True, errors='ignore')

    # Fill missing AGENT values
    final_df['AGENT'] = final_df['AGENT'].fillna('Unknown')

    # Determine SECURITY flag based on keywords
    print("[Step 4] Determining SECURITY flag...")

    security_keywords = [
        'security', 'vulnerability', 'cve', 'exploit', 'patch',
        'auth', 'authentication', 'authorization', 'injection',
        'xss', 'csrf', 'sql injection', 'sanitize', 'encrypt',
        'secure', 'unsafe', 'threat', 'malicious', 'attack'
    ]

    def is_security_related(row):
        """Check if PR is security-related based on available text fields"""
        text_to_check = []

        if pd.notna(row.get('TYPE')):
            text_to_check.append(str(row['TYPE']).lower())
        if pd.notna(row.get('PRCOMMITMESSAGE')):
            text_to_check.append(str(row['PRCOMMITMESSAGE']).lower())
        if pd.notna(row.get('PRREASON')) and 'PRREASON' in row:
            text_to_check.append(str(row['PRREASON']).lower())

        combined_text = ' '.join(text_to_check)

        for keyword in security_keywords:
            if keyword in combined_text:
                return 1
        return 0

    final_df['SECURITY'] = final_df.apply(is_security_related, axis=1)

    # Select and order final columns
    print("[Step 5] Selecting final columns...")
    final_columns = ['ID', 'AGENT', 'TYPE', 'CONFIDENCE', 'SECURITY']
    final_df = final_df[final_columns]

    # Clean up any remaining issues
    final_df['AGENT'] = final_df['AGENT'].fillna('Unknown')
    final_df['CONFIDENCE'] = final_df['CONFIDENCE'].fillna(0)

    # Save to CSV
    print(f"\n[Step 6] Saving to {output_file}...")
    final_df.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print("TASK 5 COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nOutput file: {output_file}")
    print(f"Total rows: {len(final_df):,}")
    print(f"Columns: {list(final_df.columns)}")

    print(f"\n{'='*70}")
    print("SAMPLE DATA (First 10 rows):")
    print(f"{'='*70}")
    print(final_df.head(10).to_string())

    print(f"\n{'='*70}")
    print("SUMMARY STATISTICS:")
    print(f"{'='*70}")

    # Security breakdown
    security_count = final_df['SECURITY'].sum()
    non_security_count = (final_df['SECURITY'] == 0).sum()
    print(f"\nSecurity-related PRs: {security_count:,} ({security_count/len(final_df)*100:.2f}%)")
    print(f"Non-security PRs: {non_security_count:,} ({non_security_count/len(final_df)*100:.2f}%)")

    # Type distribution
    print(f"\nPull Request Types:")
    print(final_df['TYPE'].value_counts().head(10))

    # Agent distribution
    print(f"\nTop 10 Agents:")
    print(final_df['AGENT'].value_counts().head(10))

    # Confidence statistics
    print(f"\nConfidence Statistics:")
    print(final_df['CONFIDENCE'].describe())

    print(f"\n{'='*70}")
    print("Task 5 output saved successfully!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    create_task5_output()