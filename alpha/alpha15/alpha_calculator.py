import pandas as pd
import numpy as np

def calculate_alpha15(df, correlation_window=3, sum_window=3):
    """
    Calculate Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))

    Args:
        df (pd.DataFrame): DataFrame with 'date', 'asset_id', 'high', 'volume'.
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.
        correlation_window (int): Rolling window for correlation calculation (default is 3).
        sum_window (int): Rolling window for sum calculation (default is 3).

    Returns:
        pd.DataFrame: DataFrame with original data and calculated alpha and intermediate steps.
    """
    required_cols = ['high', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted for groupby operations and ranks
    df = df.sort_values(by=['date', 'asset_id']).copy()

    # Step 1: Rank high and volume cross-sectionally (within each day)
    df['rank_high'] = df.groupby('date')['high'].rank(method='average', pct=True)
    df['rank_volume'] = df.groupby('date')['volume'].rank(method='average', pct=True)

    # df needs to be sorted by asset_id then date for rolling operations per asset
    df = df.sort_values(by=['asset_id', 'date'])

    # Step 2: Calculate rolling correlation for each asset
    # The .corr() method in pandas rolling applies to pairs of columns.
    # We need to group by asset_id first, then apply rolling correlation.
    def rolling_corr(data):
        return data['rank_high'].rolling(window=correlation_window, min_periods=correlation_window).corr(data['rank_volume'])

    df['correlation_high_volume_3'] = df.groupby('asset_id', group_keys=False).apply(rolling_corr)
    
    # Sort again by date, asset_id for the next cross-sectional rank
    df = df.sort_values(by=['date', 'asset_id'])

    # Step 3: Rank the correlation cross-sectionally
    df['rank_correlation'] = df.groupby('date')['correlation_high_volume_3'].rank(method='average', pct=True)

    # Sort again by asset_id, date for the final rolling sum per asset
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Step 4: Sum the rank_correlation over a rolling window for each asset
    df['sum_rank_correlation_3'] = df.groupby('asset_id')['rank_correlation'].transform(
        lambda x: x.rolling(window=sum_window, min_periods=sum_window).sum()
    )

    # Step 5: Calculate Alpha#15
    df['alpha15'] = -1 * df['sum_rank_correlation_3']

    # Round results
    cols_to_round = ['rank_high', 'rank_volume', 'correlation_high_volume_3', 
                       'rank_correlation', 'sum_rank_correlation_3', 'alpha15']
    for col in cols_to_round:
        df[col] = df[col].round(2) # Keep alpha15 with 2 decimal places as requested
    
    # Preserve original columns and add new ones
    # Determine original columns (excluding those we just created for calculation if they weren't already there)
    # This is a bit tricky, ideally we list them. For now, assume 'date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns' are base columns from mock data.
    # The prompt requires 'high' and 'volume' to be in the output, which they are.
    # The prompt says "代码处理的原始数据要包含在最后输出的csv中"
    # We will select all columns from the original df passed in, plus the new alpha related columns.
    # However, if rank_high etc. were somehow in original df, they'd be overwritten.
    # To be safe, we'll explicitly list the expected output columns.
    
    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)

    # Define columns to keep in the final output - include all original important columns and the new alpha columns
    # Check which of the typical base columns are present in the input df
    base_cols_present = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]
    alpha_cols = ['rank_high', 'rank_volume', 'correlation_high_volume_3', 'rank_correlation', 'sum_rank_correlation_3', 'alpha15']
    
    output_columns = base_cols_present + [col for col in alpha_cols if col not in base_cols_present] # ensure no duplicates if a name clashed
    
    return df[output_columns]

if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha15_results.csv"
    CORRELATION_WINDOW = 3
    SUM_WINDOW = 3
    NUM_ASSETS_TO_DISPLAY = 2
    ROWS_PER_ASSET_DISPLAY = 10

    # --- Load Data ---
    try:
        print(f"Loading data from {DATA_FILE_PATH}...")
        input_df = pd.read_csv(DATA_FILE_PATH)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE_PATH}.")
        exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

    # --- Data Preprocessing ---
    try:
        input_df['date'] = pd.to_datetime(input_df['date'])
        # Basic check for required columns for Alpha calculation itself
        if 'high' not in input_df.columns or 'volume' not in input_df.columns:
            print(f"Error: 'high' or 'volume' column not found in {DATA_FILE_PATH}.")
            exit(1)
        print("Data preprocessing (date conversion) complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)

    # --- Calculate Alpha ---
    try:
        print(f"Calculating Alpha#15 with correlation window {CORRELATION_WINDOW} and sum window {SUM_WINDOW}...")
        alpha_df = calculate_alpha15(input_df, correlation_window=CORRELATION_WINDOW, sum_window=SUM_WINDOW)
        print("Alpha#15 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        exit(1)

    # --- Save Results ---
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#15 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results ---
    print("\n--- Sample of Alpha#15 Results ---")
    if not alpha_df.empty:
        asset_ids = alpha_df['asset_id'].unique()
        if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY:
            selected_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY]
        else:
            selected_assets = asset_ids
        
        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
            print(f"\nAsset ID: {asset_id}")
            # Display more rows to see the effect of rolling windows
            print(f"First {ROWS_PER_ASSET_DISPLAY + CORRELATION_WINDOW + SUM_WINDOW -2} rows:") 
            print(asset_data.head(ROWS_PER_ASSET_DISPLAY + CORRELATION_WINDOW + SUM_WINDOW -2).to_string())
            if i < len(selected_assets) - 1:
                print("-" * 70) 
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df)}")
        print(f"Number of unique assets: {alpha_df['asset_id'].nunique()}")
        
        # NaN counts for key intermediate and final columns
        for col in ['correlation_high_volume_3', 'rank_correlation', 'sum_rank_correlation_3', 'alpha15']:
            if col in alpha_df.columns:
                nan_counts = alpha_df[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha15' in alpha_df.columns and len(alpha_df['alpha15'].dropna()) > 0:
            print("\nAlpha15 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df['alpha15'].dropna().describe())
        elif 'alpha15' in alpha_df.columns:
            print("\nAlpha15 column contains only NaN values or is not present after calculation.")
    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 