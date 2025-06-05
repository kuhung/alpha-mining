import pandas as pd
import numpy as np

def calculate_alpha12(df):
    """
    Calculates Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))

    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'asset_id', 'close', 'volume']
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.

    Returns:
        pd.DataFrame: DataFrame with Alpha#12 values and intermediate calculations.
    """
    # Ensure required columns are present
    required_cols = ['close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Calculate delta(close, 1)
    df['delta_close_1'] = df.groupby('asset_id')['close'].diff(1)

    # Calculate delta(volume, 1)
    df['delta_volume_1'] = df.groupby('asset_id')['volume'].diff(1)

    # Calculate sign(delta(volume, 1))
    df['sign_delta_volume_1'] = np.sign(df['delta_volume_1'])

    # Calculate Alpha#12
    df['alpha12'] = df['sign_delta_volume_1'] * (-1 * df['delta_close_1'])

    # Round alpha12 and intermediate results
    df['delta_close_1'] = df['delta_close_1'].round(2)
    df['delta_volume_1'] = df['delta_volume_1'].round(0) # Volume delta can be integer
    df['sign_delta_volume_1'] = df['sign_delta_volume_1'].round(0)
    df['alpha12'] = df['alpha12'].round(2)

    # Select and return relevant columns
    result_df = df[['date', 'asset_id', 'close', 'volume', 
                    'delta_close_1', 'delta_volume_1', 
                    'sign_delta_volume_1', 'alpha12']].copy()

    return result_df

if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"  # Path to the input data
    OUTPUT_FILE_PATH = "alpha12_results.csv"     # Path for the output CSV
    NUM_ASSETS_TO_DISPLAY = 2 # Number of assets to show in head() and tail()
    ROWS_PER_ASSET_DISPLAY = 10 # Number of rows per asset to show

    # --- Load Data ---
    try:
        print(f"Loading data from {DATA_FILE_PATH}...")
        input_df = pd.read_csv(DATA_FILE_PATH)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE_PATH}. Please ensure the file exists or run generate_mock_data.py.")
        exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

    # --- Data Preprocessing (ensure correct types and sort) ---
    try:
        input_df['date'] = pd.to_datetime(input_df['date'])
        # Ensure data is sorted correctly for rolling calculations and diff
        input_df = input_df.sort_values(by=['asset_id', 'date']).reset_index(drop=True)
        print("Data preprocessing (date conversion and sorting) complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)
    
    # --- Check for required columns 'close' and 'volume' ---
    required_data_cols = ['close', 'volume']
    missing_cols = [col for col in required_data_cols if col not in input_df.columns]
    if missing_cols:
        print(f"Error: Missing required column(s) for Alpha#12: {missing_cols} in {DATA_FILE_PATH}.")
        print("Please ensure your data generation script includes these columns or that the CSV file is correct.")
        # Check if generate_mock_data.py needs to be updated or run
        # For now, we'll exit. In a more robust system, you might try to generate them.
        exit(1)

    # --- Calculate Alpha ---
    try:
        print(f"Calculating Alpha#12...")
        alpha_df = calculate_alpha12(input_df.copy()) # Use .copy() to avoid SettingWithCopyWarning
        print("Alpha#12 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        exit(1)

    # --- Save Results ---
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#12 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results ---
    print("\n--- Sample of Alpha#12 Results ---")
    if not alpha_df.empty:
        asset_ids = alpha_df['asset_id'].unique()
        if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY:
            selected_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY]
        else:
            selected_assets = asset_ids
        
        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
            print(f"\nAsset ID: {asset_id}")
            print(f"First {ROWS_PER_ASSET_DISPLAY} rows:")
            print(asset_data.head(ROWS_PER_ASSET_DISPLAY).to_string())
            if len(asset_data) > ROWS_PER_ASSET_DISPLAY:
                 print(f"\nLast {ROWS_PER_ASSET_DISPLAY} rows for {asset_id}:")
                 print(asset_data.tail(ROWS_PER_ASSET_DISPLAY).to_string())
            if i < len(selected_assets) - 1:
                print("-" * 70) 
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df)}")
        print(f"Number of unique assets: {alpha_df['asset_id'].nunique()}")
        
        nan_delta_close_counts = alpha_df['delta_close_1'].isna().sum()
        print(f"Number of NaN values in delta_close_1: {nan_delta_close_counts} (expected for first day of each asset)")
        nan_delta_volume_counts = alpha_df['delta_volume_1'].isna().sum()
        print(f"Number of NaN values in delta_volume_1: {nan_delta_volume_counts} (expected for first day of each asset)")
        nan_sign_delta_volume_counts = alpha_df['sign_delta_volume_1'].isna().sum()
        print(f"Number of NaN values in sign_delta_volume_1: {nan_sign_delta_volume_counts} (can happen if delta_volume_1 is NaN)")
        nan_alpha_counts = alpha_df['alpha12'].isna().sum()
        print(f"Number of NaN values in alpha12: {nan_alpha_counts} (expected due to deltas or if delta_volume_1 is zero then sign is zero)")

        if len(alpha_df['alpha12'].dropna()) > 0:
            print("\nAlpha12 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df['alpha12'].dropna().describe())
        else:
            print("\nAlpha12 column contains only NaN values or all zeros after dropping NaNs.")

    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 