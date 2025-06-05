import pandas as pd
import numpy as np

def calculate_alpha17(df, ts_rank_close_window=10, adv_window=20, ts_rank_vol_window=5):
    """
    Calculate Alpha#17: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))

    Args:
        df (pd.DataFrame): DataFrame with 'date', 'asset_id', 'close', 'volume'.
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.
        ts_rank_close_window (int): Rolling window for ts_rank of close (default 10).
        adv_window (int): Rolling window for average daily volume (default 20).
        ts_rank_vol_window (int): Rolling window for ts_rank of (volume / adv) (default 5).

    Returns:
        pd.DataFrame: DataFrame with original data and calculated alpha and intermediate steps.
    """
    required_cols = ['close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted for groupby operations and ranks
    df = df.sort_values(by=['date', 'asset_id']).copy()

    # --- Component A: (-1 * rank(ts_rank(close, 10))) --- 
    # Sort by asset_id then date for rolling operations per asset
    df = df.sort_values(by=['asset_id', 'date'])
    df['ts_rank_close_10'] = df.groupby('asset_id')['close'].transform(
        lambda x: x.rolling(window=ts_rank_close_window, min_periods=ts_rank_close_window).rank(pct=True)
    )
    # Sort again by date, asset_id for the next cross-sectional rank
    df = df.sort_values(by=['date', 'asset_id'])
    df['rank_ts_rank_close_10'] = df.groupby('date')['ts_rank_close_10'].rank(method='average', pct=True)
    df['component_a'] = -1 * df['rank_ts_rank_close_10']

    # --- Component B: rank(delta(delta(close, 1), 1)) ---
    # Sort by asset_id then date for diff operations per asset
    df = df.sort_values(by=['asset_id', 'date'])
    df['delta_close_1'] = df.groupby('asset_id')['close'].diff(1)
    df['delta_delta_close_1_1'] = df.groupby('asset_id')['delta_close_1'].diff(1)
    # Sort again by date, asset_id for the next cross-sectional rank
    df = df.sort_values(by=['date', 'asset_id'])
    df['rank_delta_delta_close_1_1'] = df.groupby('date')['delta_delta_close_1_1'].rank(method='average', pct=True)
    df['component_b'] = df['rank_delta_delta_close_1_1']

    # --- Component C: rank(ts_rank((volume / adv20), 5)) ---
    # Sort by asset_id then date for rolling operations per asset
    df = df.sort_values(by=['asset_id', 'date'])
    df['adv20'] = df.groupby('asset_id')['volume'].transform(
        lambda x: x.rolling(window=adv_window, min_periods=adv_window).mean()
    )
    # Replace inf with NaN which can arise from adv20 being 0, though unlikely with min_periods=adv_window
    df['volume_adv20_ratio'] = (df['volume'] / df['adv20']).replace([np.inf, -np.inf], np.nan)
    
    df['ts_rank_vol_adv20_5'] = df.groupby('asset_id')['volume_adv20_ratio'].transform(
        lambda x: x.rolling(window=ts_rank_vol_window, min_periods=ts_rank_vol_window).rank(pct=True)
    )
    # Sort again by date, asset_id for the next cross-sectional rank
    df = df.sort_values(by=['date', 'asset_id'])
    df['rank_ts_rank_vol_adv20_5'] = df.groupby('date')['ts_rank_vol_adv20_5'].rank(method='average', pct=True)
    df['component_c'] = df['rank_ts_rank_vol_adv20_5']

    # --- Calculate Alpha#17 ---
    df['alpha17'] = df['component_a'] * df['component_b'] * df['component_c']

    # --- Round results ---
    cols_to_round = [
        'ts_rank_close_10', 'rank_ts_rank_close_10', 'component_a',
        'delta_close_1', 'delta_delta_close_1_1', 'rank_delta_delta_close_1_1', 'component_b',
        'adv20', 'volume_adv20_ratio', 'ts_rank_vol_adv20_5', 'rank_ts_rank_vol_adv20_5', 'component_c',
        'alpha17'
    ]
    for col in cols_to_round:
        if col in df.columns: # Check if column exists, e.g., adv20 might be all NaNs initially
            df[col] = df[col].round(2) 
    
    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)

    # Define columns to keep in the final output
    base_cols_present = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]
    alpha_cols = [
        'adv20', 'ts_rank_close_10', 'rank_ts_rank_close_10', 'component_a',
        'delta_close_1', 'delta_delta_close_1_1', 'rank_delta_delta_close_1_1', 'component_b',
        'volume_adv20_ratio', 'ts_rank_vol_adv20_5', 'rank_ts_rank_vol_adv20_5', 'component_c',
        'alpha17'
    ]
    output_columns = base_cols_present + [col for col in alpha_cols if col not in base_cols_present] 
    
    return df[output_columns]

if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha17_results.csv"
    TS_RANK_CLOSE_WINDOW = 10
    ADV_WINDOW = 20
    TS_RANK_VOL_WINDOW = 5
    NUM_ASSETS_TO_DISPLAY = 2
    # Adjust display rows based on max NaN period for alpha17 (adv_window + ts_rank_vol_window - 1 - 1)
    # max_nan_period = ADV_WINDOW + TS_RANK_VOL_WINDOW - 1 -1 = 20 + 5 - 2 = 23
    # To see the first alpha value, we need at least max_nan_period + 1 rows.
    # Let's display a few more to see some trend: max_nan_period + 5
    ROWS_PER_ASSET_DISPLAY = ADV_WINDOW + TS_RANK_VOL_WINDOW - 2 + 5 # approx 23 + 5 = 28

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
        required_calc_cols = ['close', 'volume']
        for col in required_calc_cols:
            if col not in input_df.columns:
                print(f"Error: Required column '{col}' not found in {DATA_FILE_PATH}.")
                exit(1)
        print("Data preprocessing (date conversion) complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)

    # --- Calculate Alpha ---
    try:
        print(f"Calculating Alpha#17 with ts_rank_close_window={TS_RANK_CLOSE_WINDOW}, adv_window={ADV_WINDOW}, ts_rank_vol_window={TS_RANK_VOL_WINDOW}...")
        alpha_df = calculate_alpha17(input_df.copy(), 
                                     ts_rank_close_window=TS_RANK_CLOSE_WINDOW, 
                                     adv_window=ADV_WINDOW, 
                                     ts_rank_vol_window=TS_RANK_VOL_WINDOW)
        print("Alpha#17 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        exit(1)

    # --- Save Results ---
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#17 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results ---
    print("\n--- Sample of Alpha#17 Results ---")
    if not alpha_df.empty:
        asset_ids = alpha_df['asset_id'].unique()
        if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY:
            selected_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY]
        else:
            selected_assets = asset_ids
        
        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
            print(f"\nAsset ID: {asset_id}")
            print(f"First {ROWS_PER_ASSET_DISPLAY} rows to observe rolling window effects:") 
            print(asset_data.head(ROWS_PER_ASSET_DISPLAY).to_string())
            if i < len(selected_assets) - 1:
                print("-" * 70) 
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df)}")
        print(f"Number of unique assets: {alpha_df['asset_id'].nunique()}")
        
        # NaN counts for key intermediate and final columns
        nan_check_cols = [
            'adv20', 'ts_rank_close_10', 'rank_ts_rank_close_10', 'component_a',
            'delta_close_1', 'delta_delta_close_1_1', 'rank_delta_delta_close_1_1', 'component_b',
            'volume_adv20_ratio', 'ts_rank_vol_adv20_5', 'rank_ts_rank_vol_adv20_5', 'component_c',
            'alpha17'
        ]
        for col in nan_check_cols:
            if col in alpha_df.columns:
                nan_counts = alpha_df[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha17' in alpha_df.columns and len(alpha_df['alpha17'].dropna()) > 0:
            print("\nAlpha17 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df['alpha17'].dropna().describe())
        elif 'alpha17' in alpha_df.columns:
            print("\nAlpha17 column contains only NaN values or is not present after calculation.")
        else:
            print("Alpha17 column not found in results.")
    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 