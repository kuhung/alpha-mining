import pandas as pd
import numpy as np

# 定义Alpha函数
def calculate_alpha6(df, window=10):
    """
    Calculate Alpha#6: (-1 * correlation(open, volume, 10))

    Args:
        df (pd.DataFrame): DataFrame with 'asset_id', 'date', 'open', 'volume'.
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.
        window (int): Rolling window size for correlation calculation.

    Returns:
        pd.DataFrame: DataFrame with 'date', 'asset_id', 'open', 'volume', 'alpha6'.
    """
    
    # Ensure required columns are present
    required_cols = ['open', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Calculate rolling correlation between 'open' and 'volume' for each asset
    # The min_periods ensures that we have enough data points to calculate correlation
    df['correlation_open_volume'] = df.groupby('asset_id', group_keys=False)[['open', 'volume']].apply(
        lambda x: x['open'].rolling(window=window, min_periods=window).corr(x['volume'])
    )
    
    # Calculate alpha6
    df['alpha6'] = -1 * df['correlation_open_volume']
    
    # Round alpha6 to two decimal places
    df['alpha6'] = df['alpha6'].round(2)
    
    # Select and return relevant columns, including raw data
    result_df = df[['date', 'asset_id', 'open', 'volume', 'alpha6']].copy()
    
    return result_df

if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"  # Path to the input data
    OUTPUT_FILE_PATH = "alpha6_results.csv"     # Path for the output CSV
    CORRELATION_WINDOW = 10
    NUM_ASSETS_TO_DISPLAY = 2 # Number of assets to show in head() and tail()
    ROWS_PER_ASSET_DISPLAY = 5 # Number of rows per asset to show

    # --- Load Data ---
    try:
        print(f"Loading data from {DATA_FILE_PATH}...")
        input_df = pd.read_csv(DATA_FILE_PATH)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE_PATH}. Please ensure the file exists.")
        exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

    # --- Data Preprocessing (ensure correct types and sort) ---
    try:
        input_df['date'] = pd.to_datetime(input_df['date'])
        # Ensure data is sorted correctly for rolling calculations
        input_df = input_df.sort_values(by=['asset_id', 'date']).reset_index(drop=True)
        print("Data preprocessing (date conversion and sorting) complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)

    # --- Calculate Alpha ---
    try:
        print(f"Calculating Alpha#6 with a window of {CORRELATION_WINDOW} days...")
        alpha_df = calculate_alpha6(input_df.copy(), window=CORRELATION_WINDOW) # Use .copy() to avoid SettingWithCopyWarning
        print("Alpha#6 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        exit(1)

    # --- Save Results ---
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False)
        print(f"Alpha#6 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results ---
    print("\n--- Sample of Alpha#6 Results ---")
    if not alpha_df.empty:
        # Display head and tail for a couple of assets to check NaN and calculations
        asset_ids = alpha_df['asset_id'].unique()
        if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY:
            selected_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY]
        else:
            selected_assets = asset_ids
        
        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
            print(f"\nAsset ID: {asset_id}")
            print(f"First {ROWS_PER_ASSET_DISPLAY} rows:")
            print(asset_data.head(ROWS_PER_ASSET_DISPLAY))
            if len(asset_data) > ROWS_PER_ASSET_DISPLAY:
                 print(f"\nLast {ROWS_PER_ASSET_DISPLAY} rows for {asset_id}:")
                 print(asset_data.tail(ROWS_PER_ASSET_DISPLAY))
            if i < len(selected_assets) - 1:
                print("-" * 30) 
        
        # Show general info
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df)}")
        print(f"Number of unique assets: {alpha_df['asset_id'].nunique()}")
        nan_alpha_counts = alpha_df['alpha6'].isna().sum()
        print(f"Number of NaN values in alpha6 column: {nan_alpha_counts} (expected due to initial window period)")
        if len(alpha_df) > 0:
            print("\nAlpha6 column statistics (excluding NaNs):")
            print(alpha_df['alpha6'].dropna().describe())

    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 