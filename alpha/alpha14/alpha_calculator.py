import pandas as pd
import numpy as np

def calculate_alpha14(df):
    """
    Calculates Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))

    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'asset_id', 'open', 'volume', 'returns']
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.

    Returns:
        pd.DataFrame: DataFrame with Alpha#14 values and intermediate calculations.
    """
    # Ensure required columns are present
    required_cols = ['open', 'volume', 'returns']
    for col in required_cols:
        if col not in df.columns:
            # If returns is missing, try to calculate from close
            if col == 'returns' and 'close' in df.columns:
                df['returns'] = df.groupby('asset_id')['close'].pct_change().round(4)
            else:
                raise ValueError(f"Required column '{col}' not found in DataFrame and 'returns' could not be calculated from 'close'.")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Calculate delta(returns, 3)
    df['delta_returns_3'] = df.groupby('asset_id')['returns'].diff(3)

    # Calculate rank(delta(returns, 3))
    # Rank is calculated ascending, so lower value = lower rank (closer to 0 for pct=True)
    df['rank_delta_returns_3'] = df.groupby('date')['delta_returns_3'].rank(method='average', ascending=True, pct=True, na_option='keep')

    # Calculate -1 * rank(delta(returns, 3))
    df['neg_rank_delta_returns_3'] = -1 * df['rank_delta_returns_3']

    # Calculate correlation(open, volume, 10)
    # Using default pairwise=True for .corr() then unstacking is a standard way to get specific pair correlation.
    # Removed pairwise=False as it might have caused the length mismatch.
    s_corr = df.groupby('asset_id')[['open', 'volume']].rolling(window=10, min_periods=10).corr().unstack()['open']['volume']
    df['corr_open_volume_10'] = s_corr.reset_index(level=0, drop=True)

    # Calculate Alpha#14
    df['alpha14'] = df['neg_rank_delta_returns_3'] * df['corr_open_volume_10']

    # Round results
    df['delta_returns_3'] = df['delta_returns_3'].round(4) # returns delta can be small
    df['rank_delta_returns_3'] = df['rank_delta_returns_3'].round(4)
    df['neg_rank_delta_returns_3'] = df['neg_rank_delta_returns_3'].round(4)
    df['corr_open_volume_10'] = df['corr_open_volume_10'].round(4)
    # For alpha14, round to 2 significant figures
    # This is a bit more complex than a simple round. We'll format it during CSV writing.

    # Select and return relevant columns
    result_df = df[[
        'date', 'asset_id', 'open', 'volume', 'returns', 'close', # Include close if it was used
        'delta_returns_3', 'rank_delta_returns_3', 'neg_rank_delta_returns_3',
        'corr_open_volume_10', 'alpha14'
    ]].copy()
    
    # Remove 'close' if it wasn't in the original required_cols for calculation (i.e., 'returns' was provided)
    if 'close' not in required_cols and 'close' not in ['open', 'volume', 'returns'] and 'close' in result_df.columns:
        result_df = result_df.drop(columns=['close'])
        
    return result_df


def format_float_to_2_sig_figs(val):
    if pd.isna(val) or val == 0:
        return "{:.2f}".format(0.0) # Represent NaN or 0 as 0.00 for consistency in CSV
    return "{:.2g}".format(val)

if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha14_results.csv"
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
        # original_columns = input_df.columns.tolist() # Keep track of original cols
        if 'returns' not in input_df.columns and 'close' in input_df.columns:
            print("Calculating 'returns' from 'close' column.")
            input_df['returns'] = input_df.groupby('asset_id')['close'].pct_change().round(4)
        elif 'returns' not in input_df.columns and 'close' not in input_df.columns:
            print("Error: 'returns' column is missing and 'close' column is also missing, cannot calculate returns.")
            exit(1)
        elif 'returns' in input_df.columns:
            print("'returns' column already exists.")
            
        input_df = input_df.sort_values(by=['asset_id', 'date']).reset_index(drop=True)
        print("Data preprocessing complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)

    # --- Calculate Alpha ---
    try:
        print("Calculating Alpha#14...")
        alpha_df = calculate_alpha14(input_df.copy())
        print("Alpha#14 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        exit(1)

    # --- Save Results ---
    try:
        # Create a new df for saving with alpha14 specifically formatted
        save_df = alpha_df.copy()
        if 'alpha14' in save_df.columns:
             save_df['alpha14'] = save_df['alpha14'].apply(format_float_to_2_sig_figs)
        
        # Define a general formatter for other float columns
        def default_float_formatter(x):
            if pd.isna(x):
                return '' # Keep NaNs as empty strings
            return f"{x:.4f}" # Default to 4 decimal places for other floats

        formatters = {col: default_float_formatter for col in save_df.select_dtypes(include='float').columns if col != 'alpha14'}
        if 'volume' in save_df.columns and pd.api.types.is_float_dtype(save_df['volume']):
            formatters['volume'] = lambda x: f'{x:.0f}' if pd.notna(x) else '' # Format volume as integer-like if it's float
        elif 'volume' in save_df.columns and pd.api.types.is_integer_dtype(save_df['volume']):
             formatters['volume'] = lambda x: f'{x:.0f}' if pd.notna(x) else ''
        
        # alpha14 is already a string due to format_float_to_2_sig_figs
        formatters['alpha14'] = lambda x: x 

        # Convert columns to string using formatters before to_csv to ensure exact output
        for col, func in formatters.items():
            if col in save_df.columns:
                save_df[col] = save_df[col].apply(lambda x: func(x) if pd.notna(x) else '')
        
        # Special handling for boolean columns if any, convert to int 0/1 or string True/False
        for col in save_df.select_dtypes(include='bool').columns:
            save_df[col] = save_df[col].astype(str)

        save_df.to_csv(OUTPUT_FILE_PATH, index=False, header=True)
        print(f"Alpha#14 results saved to {OUTPUT_FILE_PATH} with alpha14 formatted to 2 significant figures and others to 4 decimal places.")

    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results ---
    print("\n--- Sample of Alpha#14 Results (unformatted alpha14) ---")
    if not alpha_df.empty:
        asset_ids = alpha_df['asset_id'].unique()
        display_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY] if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY else asset_ids
        
        for asset_id in display_assets:
            asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
            print(f"\nAsset ID: {asset_id}")
            print(f"First {ROWS_PER_ASSET_DISPLAY} rows:")
            print(asset_data.head(ROWS_PER_ASSET_DISPLAY).to_string(float_format="%.4f"))
            if len(asset_data) > ROWS_PER_ASSET_DISPLAY:
                 print(f"\nLast {ROWS_PER_ASSET_DISPLAY} rows for {asset_id}:")
                 print(asset_data.tail(ROWS_PER_ASSET_DISPLAY).to_string(float_format="%.4f"))
            print("-" * 70)
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df)}")
        print(f"Number of unique assets: {alpha_df['asset_id'].nunique()}")
        for col in ['delta_returns_3', 'rank_delta_returns_3', 'neg_rank_delta_returns_3', 'corr_open_volume_10', 'alpha14']:
            if col in alpha_df.columns:
                nan_counts = alpha_df[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha14' in alpha_df.columns and len(alpha_df['alpha14'].dropna()) > 0:
            print("\nAlpha14 column statistics (excluding NaNs, unformatted):")
            with pd.option_context('display.float_format', '{:.4f}'.format):
                 print(alpha_df['alpha14'].dropna().describe())
        else:
            print("\nAlpha14 column contains only NaN values or is missing.")
    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 