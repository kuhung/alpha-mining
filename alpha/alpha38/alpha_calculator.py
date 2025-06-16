import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_rank(series: pd.Series, period: int) -> pd.Series:
    """Time-series rank over the past period."""
    return series.rolling(window=period, min_periods=period).apply(lambda x: x.rank(method='average', pct=True).iloc[-1], raw=False)

# --- Main Alpha Calculation Function ---

def calculate_alpha38(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#38:
    ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))
    """
    required_cols = ['open', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by asset_id then date for time-series operations
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Part 1: (close / open) ---
    df['close_over_open'] = df['close'] / df['open']
    # Handle division by zero or very small open values if they exist by replacing with NaN or inf
    df.loc[df['open'] == 0, 'close_over_open'] = np.nan # Or np.inf if that's desired behavior

    # --- Part 2: Ts_Rank(close, 10) ---
    df['ts_rank_close_10'] = df.groupby('asset_id')['close'].transform(lambda x: ts_rank(x, 10))

    # --- Part 3: rank(Ts_Rank(close, 10)) - Cross-sectional operation ---
    df = df.sort_values(by=['date', 'asset_id'])
    df['ranked_ts_rank_close_10'] = df.groupby('date')['ts_rank_close_10'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index) # Use NaN for insufficient data
    )

    # --- Part 4: (-1 * rank(Ts_Rank(close, 10))) ---
    df['neg_ranked_ts_rank'] = -1 * df['ranked_ts_rank_close_10']

    # --- Part 5: rank((close / open)) - Cross-sectional operation ---
    df['ranked_close_over_open'] = df.groupby('date')['close_over_open'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index) # Use NaN for insufficient data
    )

    # --- Final Alpha Calculation: Multiplication of ranks ---
    df['alpha38'] = df['neg_ranked_ts_rank'] * df['ranked_close_over_open']

    # Rounding to 2 decimal places as required for final alpha and relevant intermediates
    alpha_related_cols_to_round = [
        'close_over_open', 'ts_rank_close_10', 'ranked_ts_rank_close_10',
        'neg_ranked_ts_rank', 'ranked_close_over_open', 'alpha38'
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
    
    intermediate_cols_for_output = [
        'close_over_open', 'ts_rank_close_10', 'ranked_ts_rank_close_10',
        'neg_ranked_ts_rank', 'ranked_close_over_open'
    ]
    final_alpha_col = ['alpha38']
    
    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha38_results.csv"

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
        print("Calculating Alpha#38...")
        # Make a copy to avoid modifying the original input_df if needed elsewhere
        alpha_df_output = calculate_alpha38(input_df.copy()) 
        print("Alpha#38 calculation complete.")
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
        print(f"Alpha#38 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#38 Results ---")
    if not alpha_df_output.empty:
        # Display head with all columns and proper float formatting
        with pd.option_context('display.max_columns', None, 'display.float_format', '{:.2f}'.format):
            print(alpha_df_output.head().to_string())
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")
        
        key_cols_for_nan_check = [
            'close_over_open', 'ts_rank_close_10', 'ranked_ts_rank_close_10',
            'neg_ranked_ts_rank', 'ranked_close_over_open', 'alpha38'
        ]
        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha38' in alpha_df_output.columns and len(alpha_df_output['alpha38'].dropna()) > 0:
            print("\nAlpha38 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha38'].dropna().describe())
        elif 'alpha38' in alpha_df_output.columns:
            print("\nAlpha38 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.") 