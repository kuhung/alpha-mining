import pandas as pd
import numpy as np

# --- Helper Functions ---
# Reusing cs_rank, ts_delta, ts_correlation, cs_scale from alpha31 as they are generic

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_delay(series: pd.Series, period: int) -> pd.Series:
    """Time-series delay."""
    return series.shift(period)

def ts_sum(series: pd.Series, period: int) -> pd.Series:
    """Time-series sum over the past period."""
    return series.rolling(window=period, min_periods=period).sum()

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
        return pd.Series(0.0, index=series.index) # Return 0.0 for constant series
    return (series - mean) / std

# --- Main Alpha Calculation Function ---

def calculate_alpha32(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#32:
    (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5), 230))))
    """
    required_cols = ['close', 'vwap']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by asset_id then date for time-series operations
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Part A: scale(((sum(close, 7) / 7) - close)) ---
    # sum(close, 7)
    df['sum_close_7'] = df.groupby('asset_id')['close'].transform(lambda x: ts_sum(x, 7))
    
    # (sum(close, 7) / 7)
    df['avg_close_7'] = df['sum_close_7'] / 7
    
    # (sum(close, 7) / 7) - close
    df['diff_avg_close'] = df['avg_close_7'] - df['close']
    
    # scale(...) - cross-sectional operation, so re-sort by date
    df = df.sort_values(by=['date', 'asset_id'])
    df['part_A'] = df.groupby('date')['diff_avg_close'].transform(
        lambda x: cs_scale(x) if x.notna().sum() > 1 else pd.Series(0.0, index=x.index) # Handle fully NaN or single value slices
    )
    
    # --- Part B: (20 * scale(correlation(vwap, delay(close, 5), 230))) ---
    # delay(close, 5) - time-series operation, so ensure sorted by asset_id
    df = df.sort_values(by=['asset_id', 'date'])
    df['delay_close_5'] = df.groupby('asset_id')['close'].transform(lambda x: ts_delay(x, 5))
    
    # correlation(vwap, delay(close, 5), 230) - time-series operation
    df['corr_vwap_delay_close_230'] = df.groupby('asset_id', group_keys=False).apply(
        lambda x: ts_correlation(x['vwap'], x['delay_close_5'], 230)
    )
    
    # scale(...) - cross-sectional operation, so re-sort by date
    df = df.sort_values(by=['date', 'asset_id'])
    df['scaled_corr_B'] = df.groupby('date')['corr_vwap_delay_close_230'].transform(
        lambda x: cs_scale(x) if x.notna().sum() > 1 else pd.Series(0.0, index=x.index) # Handle fully NaN or single value slices
    )
    
    # 20 * scaled_corr_B
    df['part_B'] = 20 * df['scaled_corr_B']

    # --- Final Alpha Calculation ---
    df['alpha32'] = df['part_A'] + df['part_B']

    # Rounding to 2 decimal places as required
    alpha_related_cols_to_round = [
        'sum_close_7', 'avg_close_7', 'diff_avg_close', 'part_A',
        'delay_close_5', 'corr_vwap_delay_close_230', 'scaled_corr_B', 'part_B', 'alpha32'
    ]

    for col in alpha_related_cols_to_round:
        if col in df.columns:
            # Only round if the column contains numeric data that can be rounded
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].round(2)
            
    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)
    
    # Define columns to keep, ensuring original data + new alpha + key intermediates
    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in input_df.columns]
    
    intermediate_cols_for_output = ['part_A', 'part_B']
    final_alpha_col = ['alpha32']
    
    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha32_results.csv"

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
        if 'asset_id' in input_df.columns:
            input_df['asset_id'] = input_df['asset_id'].astype(str)

        print("Data preprocessing (date conversion, asset_id type) complete.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        exit(1)
    
    # --- Calculate Alpha ---
    try:
        print("Calculating Alpha#32...")
        alpha_df_output = calculate_alpha32(input_df.copy()) 
        print("Alpha#32 calculation complete.")
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
        alpha_df_output.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#32 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#32 Results ---")
    if not alpha_df_output.empty:
        print(alpha_df_output.head().to_string())
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")
        
        key_cols_for_nan_check = ['part_A', 'part_B', 'alpha32']
        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha32' in alpha_df_output.columns and len(alpha_df_output['alpha32'].dropna()) > 0:
            print("\nAlpha32 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha32'].dropna().describe())
        elif 'alpha32' in alpha_df_output.columns:
            print("\nAlpha32 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.") 