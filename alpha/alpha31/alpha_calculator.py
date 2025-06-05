import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_delta(series: pd.Series, period: int) -> pd.Series:
    """Time-series delta (difference)."""
    return series.diff(period)

def ts_decay_linear(series: pd.Series, period: int) -> pd.Series:
    """Time-series linear decay sum.
    Assigns linearly decaying weights to the series over the given period.
    Example for period=3, weights are [3, 2, 1] (normalized).
    """
    weights = np.arange(period, 0, -1)
    # Normalize weights
    weights = weights / weights.sum() 
    
    # Pad with NaNs for elements that don't have a full window
    # Rolling apply will handle min_periods. If series length is less than period, result is NaN.
    return series.rolling(window=period, min_periods=period).apply(lambda x: np.sum(weights * x), raw=True)

def ts_correlation(series1: pd.Series, series2: pd.Series, period: int) -> pd.Series:
    """Time-series correlation."""
    return series1.rolling(window=period, min_periods=period).corr(series2)

def cs_scale(series: pd.Series) -> pd.Series:
    """Cross-sectional scale (z-score).
    (value - mean) / std_dev.
    Handles cases where std_dev is zero to avoid division by zero.
    """
    mean = series.mean()
    std = series.std()
    if std == 0:
        return pd.Series(0.0, index=series.index) # or np.nan, depending on desired behavior
    return (series - mean) / std

# --- Main Alpha Calculation Function ---

def calculate_alpha31(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#31: 
    ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + 
      rank((-1 * delta(close, 3)))) + 
      sign(scale(correlation(adv20, low, 12))))
    """
    required_cols = ['close', 'low', 'adv20'] # Assuming adv20 is provided
    for col in required_cols:
        if col not in df.columns:
            # If adv20 is not present, try to calculate it from 'volume'
            if col == 'adv20' and 'volume' in df.columns:
                print("Column 'adv20' not found, calculating as 20-day rolling mean of 'volume'.")
                # Sort by asset, then date for rolling volume mean
                df_sorted_for_adv = df.sort_values(by=['asset_id', 'date']).copy()
                df_sorted_for_adv['adv20'] = df_sorted_for_adv.groupby('asset_id')['volume'].transform(
                    lambda x: x.rolling(window=20, min_periods=15).mean() # min_periods can be adjusted
                )
                # Merge back or assign carefully if original df index is important
                df = df_sorted_for_adv.sort_values(by=['date', 'asset_id']) # Resort for cs operations
            else:
                raise ValueError(f"Required column '{col}' not found in DataFrame and cannot be derived.")

    # Ensure data is sorted by date first for cross-sectional operations
    df = df.sort_values(by=['date', 'asset_id']).copy()
    
    # --- Part A: rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) ---
    # delta(close, 10) - needs asset grouping for delta
    df['delta_close_10'] = df.groupby('asset_id')['close'].transform(lambda x: ts_delta(x, 10))
    
    # rank(delta(close,10))
    df['rank_delta_close_10'] = df.groupby('date')['delta_close_10'].transform(cs_rank)
    
    # rank(rank(delta(close,10)))
    df['rank_rank_delta_close_10'] = df.groupby('date')['rank_delta_close_10'].transform(cs_rank)
    
    df['neg_rank_rank_delta_close_10'] = -1 * df['rank_rank_delta_close_10']
    
    # decay_linear requires time-series context per asset
    df = df.sort_values(by=['asset_id', 'date']) # Sort for ts_decay_linear
    df['decayed_val_A'] = df.groupby('asset_id')['neg_rank_rank_delta_close_10'].transform(
        lambda x: ts_decay_linear(x, 10)
    )
    df = df.sort_values(by=['date', 'asset_id']) # Re-sort for cs_rank

    df['rank_decayed_A1'] = df.groupby('date')['decayed_val_A'].transform(cs_rank)
    df['rank_decayed_A2'] = df.groupby('date')['rank_decayed_A1'].transform(cs_rank)
    df['part_A'] = df.groupby('date')['rank_decayed_A2'].transform(cs_rank)

    # --- Part B: rank((-1 * delta(close, 3))) ---
    df['delta_close_3'] = df.groupby('asset_id')['close'].transform(lambda x: ts_delta(x, 3))
    df['neg_delta_close_3'] = -1 * df['delta_close_3']
    df['part_B'] = df.groupby('date')['neg_delta_close_3'].transform(cs_rank)

    # --- Part C: sign(scale(correlation(adv20, low, 12))) ---
    # correlation requires time-series context per asset
    df = df.sort_values(by=['asset_id', 'date']) # Sort for ts_correlation
    df['corr_adv20_low_12'] = df.groupby('asset_id', group_keys=False).apply(
        lambda x: ts_correlation(x['adv20'], x['low'], 12)
    )
    df = df.sort_values(by=['date', 'asset_id']) # Re-sort for cs_scale

    df['scaled_corr_C'] = df.groupby('date')['corr_adv20_low_12'].transform(
         lambda x: cs_scale(x) if x.notna().sum() > 1 else pd.Series(0.0, index=x.index) # Handle fully NaN or single value slices for scale
    )
    df['part_C'] = np.sign(df['scaled_corr_C'])
    
    # Handle potential -0.0 from np.sign by converting to 0.0
    df['part_C'] = df['part_C'].replace(-0.0, 0.0)


    # --- Final Alpha Calculation ---
    df['alpha31'] = df['part_A'] + df['part_B'] + df['part_C']

    # Rounding (as per user request for final alpha, and good practice for intermediate)
    # Select only key intermediate and final alpha columns for explicit rounding here
    # This ensures original data precision is not altered unless intended.
    alpha_related_cols_to_round = [
        'delta_close_10', 'rank_delta_close_10', 'rank_rank_delta_close_10', 
        'neg_rank_rank_delta_close_10', 'decayed_val_A', 'rank_decayed_A1', 
        'rank_decayed_A2', 'part_A', 'delta_close_3', 'neg_delta_close_3', 'part_B',
        'corr_adv20_low_12', 'scaled_corr_C', 'part_C', 'alpha31'
    ]
    if 'adv20' in df.columns and df['adv20'].dtype == np.float64 : # If adv20 was calculated, it might be float
         alpha_related_cols_to_round.append('adv20')


    for col in alpha_related_cols_to_round:
        if col in df.columns: # Check if column exists (e.g. adv20 might not be if it was input int)
            df[col] = df[col].round(2) # User requested final alpha with 2 decimal places
                                       # README mentioned "all numerical alpha related columns"

    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)
    
    # Define columns to keep, ensuring original data + new alpha + key intermediates
    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns', 'adv20'] if col in input_df.columns]
    # Add newly created intermediate columns and final alpha, avoid duplicates
    # Using a list of important intermediate columns explicitly from README/User context
    intermediate_cols_for_output = ['part_A', 'part_B', 'part_C'] 
    final_alpha_col = ['alpha31']
    
    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    # If 'adv20' was calculated and not in original_cols list from input_df, add it
    if 'adv20' in df.columns and 'adv20' not in output_cols:
        # Find a suitable position, e.g., after 'volume' or 'close'
        try:
            vol_idx = output_cols.index('volume')
            output_cols.insert(vol_idx + 1, 'adv20')
        except ValueError:
            try:
                close_idx = output_cols.index('close')
                output_cols.insert(close_idx + 1, 'adv20')
            except ValueError:
                 output_cols.append('adv20') # Append if preferred position not found

    # Ensure all df columns are string for to_csv if any are problematic (e.g. exotic objects)
    # df = df.astype(str) # This is too aggressive, usually not needed.

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    # Assuming mock_data.csv is in ../../data/ relative to this script's location (alpha/alpha31/)
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha31_results.csv"

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
        # Ensure asset_id is treated as object/string to avoid issues with numeric IDs being misinterpreted
        if 'asset_id' in input_df.columns:
            input_df['asset_id'] = input_df['asset_id'].astype(str)

        print("Data preprocessing (date conversion, asset_id type) complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)
    
    # --- Calculate Alpha ---
    try:
        print("Calculating Alpha#31...")
        # Pass a copy to avoid modifying the original input_df in memory if it's used elsewhere
        alpha_df_output = calculate_alpha31(input_df.copy()) 
        print("Alpha#31 calculation complete.")
    except ValueError as ve:
        print(f"Error during Alpha calculation: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    # --- Save Results ---
    try:
        # Ensure float_format applies to all floats, not just alpha31
        alpha_df_output.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#31 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#31 Results ---")
    if not alpha_df_output.empty:
        # Display first few rows of the output for a quick check
        print(alpha_df_output.head().to_string())
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")
        
        # NaN counts for key columns
        key_cols_for_nan_check = ['part_A', 'part_B', 'part_C', 'alpha31']
        if 'adv20' in alpha_df_output.columns: # If adv20 was generated/used
            key_cols_for_nan_check.insert(0, 'adv20')

        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha31' in alpha_df_output.columns and len(alpha_df_output['alpha31'].dropna()) > 0:
            print("\nAlpha31 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha31'].dropna().describe())
        elif 'alpha31' in alpha_df_output.columns:
            print("\nAlpha31 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.")

    print("\nScript execution finished.") 