import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_stddev(series: pd.Series, period: int) -> pd.Series:
    """Time-series standard deviation over the past period."""
    return series.rolling(window=period, min_periods=period).std()

def ts_delta(series: pd.Series, period: int) -> pd.Series:
    """Time-series delta: current value minus value 'period' days ago."""
    return series - series.shift(period)

# --- Main Alpha Calculation Function ---

def calculate_alpha34(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#34:
    rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))
    """
    required_cols = ['returns', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by asset_id then date for time-series operations
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Part 1: stddev(returns, 2) ---
    df['stddev_returns_2'] = df.groupby('asset_id')['returns'].transform(lambda x: ts_stddev(x, 2))

    # --- Part 2: stddev(returns, 5) ---
    df['stddev_returns_5'] = df.groupby('asset_id')['returns'].transform(lambda x: ts_stddev(x, 5))

    # --- Part 3: (stddev(returns, 2) / stddev(returns, 5)) ---
    # Handle division by zero: if stddev_returns_5 is 0 or NaN, the ratio should be NaN or 0,
    # depending on desired behavior. Here, we'll let pandas handle NaN propagate,
    # and if denominator is 0, result will be inf (which rank will handle).
    # It's better to explicitly handle zero division to avoid inf/NaN propagating unexpectedly
    df['stddev_ratio'] = df['stddev_returns_2'] / df['stddev_returns_5'].replace(0, np.nan)

    # --- Part 4: 1 - rank(stddev_ratio) - Cross-sectional operation, re-sort by date ---
    df = df.sort_values(by=['date', 'asset_id'])
    df['part_A'] = df.groupby('date')['stddev_ratio'].transform(
        lambda x: 1 - cs_rank(x) if x.notna().sum() > 1 else pd.Series(0.0, index=x.index)
    )

    # --- Part 5: delta(close, 1) - Time-series operation, re-sort by asset_id ---
    df = df.sort_values(by=['asset_id', 'date'])
    df['delta_close_1'] = df.groupby('asset_id')['close'].transform(lambda x: ts_delta(x, 1))

    # --- Part 6: 1 - rank(delta_close_1) - Cross-sectional operation, re-sort by date ---
    df = df.sort_values(by=['date', 'asset_id'])
    df['part_B'] = df.groupby('date')['delta_close_1'].transform(
        lambda x: 1 - cs_rank(x) if x.notna().sum() > 1 else pd.Series(0.0, index=x.index)
    )

    # --- Part 7: Sum of Part A and Part B ---
    df['sum_parts_AB'] = df['part_A'] + df['part_B']

    # --- Final Alpha Calculation: rank(sum_parts_AB) - Cross-sectional operation, re-sort by date ---
    df['alpha34'] = df.groupby('date')['sum_parts_AB'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(0.0, index=x.index)
    )

    # Rounding to 2 decimal places as required for final alpha
    alpha_related_cols_to_round = [
        'stddev_returns_2', 'stddev_returns_5', 'stddev_ratio', 'part_A',
        'delta_close_1', 'part_B', 'sum_parts_AB', 'alpha34'
    ]

    for col in alpha_related_cols_to_round:
        if col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].round(2)
            
    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)
    
    # Define columns to keep, ensuring original data + new alpha + key intermediates
    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]
    
    intermediate_cols_for_output = ['part_A', 'part_B', 'sum_parts_AB'] # Keep relevant intermediates
    final_alpha_col = ['alpha34']
    
    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha34_results.csv"

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
        print("Calculating Alpha#34...")
        # Make a copy to avoid modifying the original input_df if needed elsewhere
        alpha_df_output = calculate_alpha34(input_df.copy()) 
        print("Alpha#34 calculation complete.")
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
        print(f"Alpha#34 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#34 Results ---")
    if not alpha_df_output.empty:
        # Display head with all columns and proper float formatting
        with pd.option_context('display.max_columns', None, 'display.float_format', '{:.2f}'.format):
            print(alpha_df_output.head().to_string())
        
        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")
        
        key_cols_for_nan_check = ['part_A', 'part_B', 'sum_parts_AB', 'alpha34']
        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha34' in alpha_df_output.columns and len(alpha_df_output['alpha34'].dropna()) > 0:
            print("\nAlpha34 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha34'].dropna().describe())
        elif 'alpha34' in alpha_df_output.columns:
            print("\nAlpha34 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.") 