import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

# --- Main Alpha Calculation Function ---

def calculate_alpha40(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#40:
    ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))
    """
    required_cols = ['high', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by asset_id then date for time-series operations
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Component 1: stddev(high, 10) ---
    df['stddev_high_10'] = df.groupby('asset_id')['high'].transform(lambda x: x.rolling(window=10, min_periods=10).std())

    # --- Component 2: rank(stddev(high, 10)) ---
    # Sort by date for cross-sectional ranking
    df = df.sort_values(by=['date', 'asset_id'])
    df['rank_stddev_high_10'] = df.groupby('date')['stddev_high_10'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index)
    )

    # --- Component 3: correlation(high, volume, 10) ---
    # Sort back by asset then date for time-series correlation
    df = df.sort_values(by=['asset_id', 'date'])
    df['corr_high_volume_10'] = df.groupby('asset_id').apply(
        lambda g: g['high'].rolling(window=10, min_periods=10).corr(g['volume'])
    ).reset_index(level=0, drop=True)


    # --- Final Alpha Calculation ---
    # Formula: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))
    df['alpha40'] = (-1 * df['rank_stddev_high_10']) * df['corr_high_volume_10']

    # Rounding to 2 decimal places for final alpha and relevant intermediates
    alpha_related_cols_to_round = [
        'stddev_high_10', 'rank_stddev_high_10', 'corr_high_volume_10', 'alpha40'
    ]

    for col in alpha_related_cols_to_round:
        if col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df.loc[:, col] = df[col].round(2)

    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)

    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]

    intermediate_cols_for_output = [
        'stddev_high_10', 'rank_stddev_high_10', 'corr_high_volume_10'
    ]
    final_alpha_col = ['alpha40']

    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha/alpha40/alpha40_results.csv"

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
        print("Calculating Alpha#40...")
        alpha_df_output = calculate_alpha40(input_df.copy())
        print("Alpha#40 calculation complete.")
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
        # Filter out rows where 'alpha40' is NaN before saving
        alpha_df_output = alpha_df_output.dropna(subset=['alpha40'])

        # Use float_format to ensure 2 decimal places for floats in the CSV
        alpha_df_output.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#40 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#40 Results ---")
    if not alpha_df_output.empty:
        with pd.option_context('display.max_columns', None, 'display.float_format', '{:.2f}'.format):
            print(alpha_df_output.head().to_string())

        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")

        key_cols_for_nan_check = [
            'stddev_high_10', 'rank_stddev_high_10', 'corr_high_volume_10', 'alpha40'
        ]
        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha40' in alpha_df_output.columns and len(alpha_df_output['alpha40'].dropna()) > 0:
            print("\nAlpha40 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha40'].dropna().describe())
        elif 'alpha40' in alpha_df_output.columns:
            print("\nAlpha40 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.") 