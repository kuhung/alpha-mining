import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_delay(series: pd.Series, period: int) -> pd.Series:
    """Time-series delay: value of series 'period' days ago."""
    return series.shift(period)

def ts_correlation(series_x: pd.Series, series_y: pd.Series, period: int) -> pd.Series:
    """Time-series correlation of series_x and series_y over the past period."""
    # Ensure both series are aligned for correlation calculation
    # The rolling correlation function inherently handles alignment based on index
    return series_x.rolling(window=period, min_periods=period).corr(series_y)

# --- Main Alpha Calculation Function ---

def calculate_alpha37(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#37:
    (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))
    """
    required_cols = ['open', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by asset_id then date for time-series operations
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Part 1: (open - close) ---
    df['oc_diff'] = df['open'] - df['close']

    # --- Part 2: delay((open - close), 1) ---
    df['oc_diff_delay1'] = df.groupby('asset_id')['oc_diff'].transform(lambda x: ts_delay(x, 1))

    # --- Part 3: correlation(delay((open - close), 1), close, 200) ---
    # Group by asset_id and apply rolling correlation
    # For rolling correlation, ensure both series are passed to corr, not just one.
    # The `transform` applies the grouped operation back to the original DataFrame's shape.
    df['corr_oc_delay1_close_200'] = df.groupby('asset_id').apply(
        lambda x: ts_correlation(x['oc_diff_delay1'], x['close'], 200)
    ).reset_index(level=0, drop=True) # Reset index from apply to merge back correctly

    # --- Part 4: rank(correlation(delay((open - close), 1), close, 200)) - Cross-sectional operation ---
    df = df.sort_values(by=['date', 'asset_id'])
    df['ranked_corr'] = df.groupby('date')['corr_oc_delay1_close_200'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index) # Use NaN for insufficient data
    )

    # --- Part 5: rank((open - close)) - Cross-sectional operation ---
    df['ranked_oc_diff'] = df.groupby('date')['oc_diff'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index) # Use NaN for insufficient data
    )

    # --- Final Alpha Calculation: sum of ranks ---
    df['alpha37'] = df['ranked_corr'] + df['ranked_oc_diff']

    # Rounding to 2 decimal places as required for final alpha and relevant intermediates
    alpha_related_cols_to_round = [
        'oc_diff', 'oc_diff_delay1', 'corr_oc_delay1_close_200',
        'ranked_corr', 'ranked_oc_diff', 'alpha37'
    ]

    for col in alpha_related_cols_to_round:
        if col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Use .loc to avoid SettingWithCopyWarning, especially with chained operations
                df.loc[:, col] = df[col].round(2)
            
    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)
    
    # Define columns to keep, ensuring original data + new alpha + key intermediates
    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]
    
    intermediate_cols_for_output = ['oc_diff', 'corr_oc_delay1_close_200', 'ranked_corr', 'ranked_oc_diff']
    final_alpha_col = ['alpha37']
    
    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha37_results.csv"

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
        print("Calculating Alpha#37...")
        # Make a copy to avoid modifying the original input_df if needed elsewhere
        alpha_df_output = calculate_alpha37(input_df.copy()) 
        print("Alpha#37 calculation complete.")
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
        # Use float_format to ensure 2 decimal places for floats in the CSV
        alpha_df_output.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#37 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#37 Results ---")
    if not alpha_df_output.empty:
        # Display head with all columns and proper float formatting
        with pd.option_context('display.max_columns', None, 'display.float_format', '{:.2f}'.format):
            print(alpha_df_output.head().to_string())
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")
        
        key_cols_for_nan_check = ['oc_diff', 'corr_oc_delay1_close_200', 'ranked_corr', 'ranked_oc_diff', 'alpha37']
        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha37' in alpha_df_output.columns and len(alpha_df_output['alpha37'].dropna()) > 0:
            print("\nAlpha37 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha37'].dropna().describe())
        elif 'alpha37' in alpha_df_output.columns:
            print("\nAlpha37 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.") 