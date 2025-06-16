import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    # Ensure only non-NaN values are ranked. NaNs will remain NaN.
    return series.rank(method='average', pct=True)

# --- Main Alpha Calculation Function ---

def calculate_alpha33(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#33:
    rank((-1 * ((1 - (open / close))^1)))
    """
    required_cols = ['open', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by date first for cross-sectional operations
    df = df.sort_values(by=['date', 'asset_id']).copy()

    # Calculate (1 - (open / close))
    # Handle division by zero for 'close' price
    # If close is 0, the ratio will be inf, and (1 - inf) will be -inf, which will propagate to NaN after rank
    # We'll let pandas handle inf/-inf and resulting NaNs. Rank handles NaNs by default.
    df['intermediate_ratio'] = (1 - (df['open'] / df['close']))

    # Calculate -1 * (1 - (open / close))
    df['intermediate_negated'] = -1 * df['intermediate_ratio']

    # Apply cross-sectional rank
    df['alpha33'] = df.groupby('date')['intermediate_negated'].transform(cs_rank)

    # Rounding alpha33 to two decimal places
    df['alpha33'] = df['alpha33'].round(2)

    # Define columns to keep, ensuring original data + new alpha
    # Use a set to avoid duplicates and preserve order for original columns
    original_cols_ordered = ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns']
    output_cols = [col for col in original_cols_ordered if col in df.columns]

    # Add alpha33 to the end, if not already present
    if 'alpha33' not in output_cols:
        output_cols.append('alpha33')
    
    # Re-sort by date and asset_id for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    # Assuming mock_data.csv is in ../../data/ relative to this script's location (alpha/alpha33/)
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha33_results.csv"

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
        print("Calculating Alpha#33...")
        # Pass a copy to avoid modifying the original input_df in memory if it's used elsewhere
        results_df = calculate_alpha33(input_df.copy())
        print("Alpha#33 calculation complete.")
    except Exception as e:
        print(f"Error calculating Alpha#33: {e}")
        exit(1)

    # --- Save Results ---
    try:
        results_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#33 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results: {e}")
        exit(1) 