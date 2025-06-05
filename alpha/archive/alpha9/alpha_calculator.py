import pandas as pd
import numpy as np

# 定义Alpha函数
def calculate_alpha9(df, window=5):
    """
    Calculate Alpha#9: 
    ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))

    Args:
        df (pd.DataFrame): DataFrame with 'asset_id', 'date', 'close'.
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.
        window (int): Rolling window size for ts_min and ts_max calculation (default is 5).

    Returns:
        pd.DataFrame: DataFrame with 'date', 'asset_id', 'close', 
                      'delta_close_1', 'ts_min_delta_close_1_5', 
                      'ts_max_delta_close_1_5', 'alpha9'.
    """
    
    # Ensure required columns are present
    required_cols = ['close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Calculate delta(close, 1)
    df['delta_close_1'] = df.groupby('asset_id')['close'].diff(1)

    # Calculate ts_min(delta(close, 1), window)
    df['ts_min_delta_close_1_5'] = df.groupby('asset_id')['delta_close_1'].transform(
        lambda x: x.rolling(window=window, min_periods=window).min()
    )

    # Calculate ts_max(delta(close, 1), window)
    df['ts_max_delta_close_1_5'] = df.groupby('asset_id')['delta_close_1'].transform(
        lambda x: x.rolling(window=window, min_periods=window).max()
    )

    # Conditions for Alpha#9 calculation
    cond1 = 0 < df['ts_min_delta_close_1_5']
    cond2 = df['ts_max_delta_close_1_5'] < 0

    # Apply conditions
    df['alpha9'] = np.select(
        [cond1, cond2],
        [df['delta_close_1'], df['delta_close_1']],
        default=-1 * df['delta_close_1']
    )
    
    # Round alpha9 and intermediate results to two decimal places for consistency, though delta might be better with more
    df['delta_close_1'] = df['delta_close_1'].round(2)
    df['ts_min_delta_close_1_5'] = df['ts_min_delta_close_1_5'].round(2)
    df['ts_max_delta_close_1_5'] = df['ts_max_delta_close_1_5'].round(2)
    df['alpha9'] = df['alpha9'].round(2)
    
    # Select and return relevant columns
    result_df = df[['date', 'asset_id', 'close', 'delta_close_1', 
                    'ts_min_delta_close_1_5', 'ts_max_delta_close_1_5', 'alpha9']].copy()
    
    return result_df

if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"  # Path to the input data
    OUTPUT_FILE_PATH = "alpha9_results.csv"     # Path for the output CSV
    ROLLING_WINDOW = 5
    NUM_ASSETS_TO_DISPLAY = 2 # Number of assets to show in head() and tail()
    ROWS_PER_ASSET_DISPLAY = 10 # Number of rows per asset to show (increased to see window effect)

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
    
    # --- Check for 'close' column ---
    if 'close' not in input_df.columns:
        print(f"Error: 'close' column not found in {DATA_FILE_PATH}. This Alpha requires 'close' prices.")
        print("Please ensure your data generation script includes the 'close' column.")
        exit(1)

    # --- Calculate Alpha ---
    try:
        print(f"Calculating Alpha#9 with a window of {ROLLING_WINDOW} days...")
        # Use .copy() to avoid SettingWithCopyWarning if input_df is used elsewhere
        alpha_df = calculate_alpha9(input_df.copy(), window=ROLLING_WINDOW)
        print("Alpha#9 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        exit(1)

    # --- Save Results ---
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#9 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results ---
    print("\n--- Sample of Alpha#9 Results ---")
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
        
        nan_delta_counts = alpha_df['delta_close_1'].isna().sum()
        print(f"Number of NaN values in delta_close_1: {nan_delta_counts} (expected for first day of each asset)")
        nan_ts_min_counts = alpha_df['ts_min_delta_close_1_5'].isna().sum()
        print(f"Number of NaN values in ts_min_delta_close_1_5: {nan_ts_min_counts} (expected due to initial window)")
        nan_ts_max_counts = alpha_df['ts_max_delta_close_1_5'].isna().sum()
        print(f"Number of NaN values in ts_max_delta_close_1_5: {nan_ts_max_counts} (expected due to initial window)")
        nan_alpha_counts = alpha_df['alpha9'].isna().sum()
        print(f"Number of NaN values in alpha9: {nan_alpha_counts} (expected due to initial window and delta)")

        if len(alpha_df['alpha9'].dropna()) > 0:
            print("\nAlpha9 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df['alpha9'].dropna().describe())
        else:
            print("\nAlpha9 column contains only NaN values after dropping NaNs.")

    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 