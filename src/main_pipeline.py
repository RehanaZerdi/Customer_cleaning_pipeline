"""
main_pipeline.py

This script runs the complete Customer Input Data Cleaning Pipeline.
It performs the following steps:

1. Load raw dataset from CSV (sample_comments.csv)
2. Clean all comments using the vectorized cleaning pipeline
3. Generate metadata (word counts, cleaning success flag)
4. Save cleaned results to cleaned_output.csv
5. Produce a summary report
6. Display before–after examples

This file acts as the main controller of the cleaning process.
"""

import pandas as pd
import os
import sys
import time
from pathlib import Path

# Import cleaning functions from cleaning_functions.py
from cleaning_functions import clean_comment, flag_cleaning_success, count_words

# Configuration Variables
INPUT_FILE = 'data/sample_comments.csv'  # Raw input file
OUTPUT_FILE = 'data/cleaned_output.csv' # Output cleaned file

# FUNCTION 1: Load Data
def load_data(file_path):
    """
    Load CSV file into a pandas DataFrame.
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    pd.DataFrame: DataFrame with comments

    Raises:
    Exits program if file is not found or unreadable.
    """
    try:
        df = pd.read_csv(file_path)
        print(f" Data loaded successfully from {file_path}")
        print(f" Total rows: {len(df)}")
        return df
    except FileNotFoundError:
        print(f" Error: File '{file_path}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f" Error loading data: {str(e)}")
        sys.exit(1)

# FUNCTION 2: Process Comments (Vectorized - FAST)
def process_comments_vectorized(df):
    """
    Apply the full cleaning pipeline to all comments using an optimized
    vectorized approach with pandas .apply().

    Parameters:
        df (pd.DataFrame): DataFrame containing a 'Comment' column.

    Returns:
        (pd.DataFrame, float): 
            - Cleaned DataFrame with metadata
            - Total processing time in seconds
    """
    print("\n" + "="*80)
    print("PROCESSING COMMENTS (OPTIMIZED VECTORIZED VERSION)...")
    print("="*80 + "\n")
    
    start_time = time.time()
    
    # Apply the cleaning pipeline to each row in the DataFrame
    results = df['Comment'].apply(lambda x: clean_comment(x))
    
    # Extract cleaned text and word statistics
    df['Cleaned_Comment'] = results.apply(lambda x: x[0])
    df['Words_Before'] = results.apply(lambda x: x[1])
    df['Words_After'] = results.apply(lambda x: x[2])
    df['Words_Removed'] = df['Words_Before'] - df['Words_After']

    # Flag success or failure
    df['Cleaning_Success'] = df.apply(
        lambda row: flag_cleaning_success(row['Comment'], row['Cleaned_Comment']), 
        axis=1
    )
    
    # Rename 'Comment' to 'Original_Comment' for clarity
    df = df.rename(columns={'Comment': 'Original_Comment'})
    
    # Reorder columns for better readability
    df = df[['Original_Comment', 'Cleaned_Comment', 'Words_Before', 
             'Words_After', 'Words_Removed', 'Cleaning_Success']]
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f" All {len(df)} comments processed successfully!")
    print(f" Processing time: {processing_time:.2f} seconds")
    
    return df, processing_time

# FUNCTION 3: Save Cleaned Data
def save_cleaned_data(df, output_file):
    """
    Save cleaned results to a CSV file.

    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        output_file (str): Output path for cleaned CSV
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"\n Cleaned data saved to {output_file}")
        print(f"  Total rows saved: {len(df)}")
    except Exception as e:
        print(f"\n Error saving data: {str(e)}")
        sys.exit(1)

# FUNCTION 4: Generate Summary Report
def generate_summary_report(df, processing_time):
    """
    Generate a summary report of pipeline performance and cleaning results.

    Parameters:
        df (pd.DataFrame): Cleaned data with metadata
        processing_time (float): Total processing time in seconds
    """
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)
    
    #basic statistics
    total_comments = len(df)
    successful = len(df[df['Cleaning_Success'] == 'Success'])
    failed = len(df[df['Cleaning_Success'] == 'Failed'])
    
    avg_words_before = df['Words_Before'].mean()
    avg_words_after = df['Words_After'].mean()
    avg_words_removed = df['Words_Removed'].mean()
    
    total_words_removed = df['Words_Removed'].sum()
    
    # Display summary
    print(f"\nTotal Comments Processed: {total_comments}")
    print(f"Successfully Cleaned: {successful} ({successful/total_comments*100:.1f}%)")
    print(f"Failed to Clean: {failed} ({failed/total_comments*100:.1f}%)")
    
    print(f"\nWord Statistics:")
    print(f"  Average Words Before: {avg_words_before:.2f}")
    print(f"  Average Words After: {avg_words_after:.2f}")
    print(f"  Average Words Removed: {avg_words_removed:.2f}")
    print(f"  Total Words Removed: {total_words_removed}")
    
    print(f"\nPerformance Metrics:")
    print(f"  Total Time: {processing_time:.2f} seconds")
    print(f"  Time per Comment: {processing_time/total_comments*1000:.2f} ms")
    print(f"  Comments per Second: {total_comments/processing_time:.2f}")
    
    # Check if meets company requirement
    if processing_time <= 120 and total_comments >= 1000:
        print(f"\n PASSED: Processed {total_comments} comments in {processing_time:.2f}s (under 2 mins)")
    elif total_comments < 1000:
        print(f"\n INFO: Dataset has {total_comments} comments (test with 1000+ for benchmark)")
    else:
        print(f"\n FAILED: Processing took {processing_time:.2f}s (exceeds 2 min limit)")
    
    print("\n" + "="*80)

# FUNCTION 5: Display Sample Results
def display_sample_results(df, num_samples=5):
    """
   Print sample before - after cleaning examples to the console.

    Parameters:
        df (pd.DataFrame): Cleaned data
        num_samples (int): Number of samples to display
    """
    print("\n" + "="*80)
    print(f"SAMPLE BEFORE-AFTER EXAMPLES (First {num_samples}):")
    print("="*80)
    
    for idx in range(min(num_samples, len(df))):
        row = df.iloc[idx]
        print(f"\nExample {idx + 1}:")
        print(f"  BEFORE: {row['Original_Comment'][:80]}")
        print(f"  AFTER:  {row['Cleaned_Comment'][:80]}")
        print(f"  Words: {row['Words_Before']} → {row['Words_After']} | Status: {row['Cleaning_Success']}")
    
    print("\n" + "="*80)

# MAIN PIPELINE EXECUTION
def main():
    """
     Execute the complete optimized cleaning pipeline from start to finish.
    """
    print("\n" + "="*80)
    print("CUSTOMER INPUT DATA CLEANING PIPELINE (OPTIMIZED)")
    print("="*80)
    
    # Step 1: Load raw CSV
    print("\nSTEP 1: Loading Data...")
    df_input = load_data(INPUT_FILE)
    
    # Step 2: Clean all comments
    print("\nSTEP 2: Processing Comments...")
    df_cleaned, processing_time = process_comments_vectorized(df_input)
    
    # Step 3: Save cleaned data
    print("\nSTEP 3: Saving Cleaned Data...")
    save_cleaned_data(df_cleaned, OUTPUT_FILE)
    
    # Step 4: Generate summary report
    print("\nSTEP 4: Generating Summary Report...")
    generate_summary_report(df_cleaned, processing_time)
    
    # Step 5: Display sample results
    print("\nSTEP 5: Displaying Sample Results...")
    display_sample_results(df_cleaned, num_samples=5)
    
    print("\n✓ Pipeline execution completed successfully!")
    print(f"✓ Output file: {OUTPUT_FILE}")

# Run Pipeline
if __name__ == "__main__":
    main()
