import pandas as pd
import json
import re
import os

def process_viewing_history(input_file, output_file):
    print(f"Reading viewing history from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        # Standardize dates
        df['Date Watched'] = pd.to_datetime(df['Date Watched'], format='%d/%m/%Y')
        df['Date'] = df['Date Watched'].dt.strftime('%Y-%m-%d')
        df['Year'] = df['Date Watched'].dt.year
        df['Month'] = df['Date Watched'].dt.month_name()
        df['Is_Weekend'] = df['Day'].isin(['Saturday', 'Sunday'])
        df['Season'] = df['Title'].str.extract(r'Season (\d+)').fillna('N/A')
        
        # Keep only necessary columns and handle missing data
        columns_to_keep = ['Title', 'Show Name', 'Episode Title', 'Category', 'Date', 'Day', 'Year', 'Month', 'Is_Weekend', 'Season']
        df_clean = df[[col for col in columns_to_keep if col in df.columns]].fillna("")
        df_clean = df_clean.sort_values('Date')
        
        json_data = df_clean.to_dict(orient='records')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)
        
        print(f"Success! Processed {len(df_clean)} viewing records.")
    except Exception as e:
        print(f"Error processing viewing history: {e}")

def process_watchlist(input_file, output_file):
    print(f"Reading watchlist data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        # Fill missing values to avoid NaN issues
        df = df.fillna("")
        json_data = df.to_dict(orient='records')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)
        print(f"Success! Processed {len(df)} watchlist records.")
    except Exception as e:
        print(f"Error processing watchlist: {e}")

if __name__ == "__main__":
    # INSTRUCTIONS:
    # 1. Ensure 'netflix_history.csv' and 'watchlist.csv' are in this folder.
    
    INPUT_FILE = 'netflix_history.csv'
    OUTPUT_FILE = 'data.json'
    WATCHLIST_INPUT = 'watchlist.csv'
    WATCHLIST_OUTPUT = 'watchlist.json'
    
    # Process History
    if os.path.exists(INPUT_FILE):
        process_viewing_history(INPUT_FILE, OUTPUT_FILE)
    else:
        print(f"Notice: {INPUT_FILE} not found. Skipping history.")

    # Process Watchlist
    if os.path.exists(WATCHLIST_INPUT):
        process_watchlist(WATCHLIST_INPUT, WATCHLIST_OUTPUT)
    else:
        print(f"Notice: {WATCHLIST_INPUT} not found. Skipping watchlist.")