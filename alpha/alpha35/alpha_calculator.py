import pandas as pd
import numpy as np
import os

def ts_rank(series, window):
    """
    Calculates the time-series rank of a series over a specified window.
    For each element, it ranks the current value against the values in the preceding window,
    and then normalizes it to a [0, 1] range (percentile rank).
    """
    return series.rolling(window=window).apply(lambda x: pd.Series(x).rank(method='average').iloc[-1] / len(x), raw=False)

def calculate_alpha35(df):
    """
    Calculates Alpha#35 based on the given DataFrame.
    Formula: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))
    """
    # Ensure necessary columns exist
    required_cols = ['close', 'high', 'low', 'volume', 'returns']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns. Ensure {required_cols} are in the DataFrame.")

    # Calculate intermediate terms
    df['price_term'] = (df['close'] + df['high'] - df['low'])

    # Apply Ts_Rank
    df['ts_rank_volume_32'] = ts_rank(df['volume'], 32)
    df['ts_rank_price_term_16'] = ts_rank(df['price_term'], 16)
    df['ts_rank_returns_32'] = ts_rank(df['returns'], 32)

    # Calculate Alpha#35
    alpha35_values = (df['ts_rank_volume_32'] *
                      (1 - df['ts_rank_price_term_16']) *
                      (1 - df['ts_rank_returns_32']))

    return alpha35_values

def main():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'data', 'mock_data.csv')
    output_path = os.path.join(script_dir, 'alpha35_results.csv')

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}. Please ensure mock_data.csv exists in the data/ directory.")
        return

    # Assuming 'returns' needs to be calculated if not present
    if 'returns' not in df.columns:
        if 'close' in df.columns:
            df['returns'] = df['close'].pct_change()
            print("Note: 'returns' column was calculated from 'close' prices.")
        else:
            print("Error: 'close' column not found to calculate 'returns'. Please ensure 'close' or 'returns' is in the data.")
            return

    # Calculate Alpha#35
    df['Alpha#35'] = calculate_alpha35(df)

    # Keep original data and Alpha#35, drop intermediate columns
    final_df = df.drop(columns=['price_term', 'ts_rank_volume_32', 'ts_rank_price_term_16', 'ts_rank_returns_32'], errors='ignore')

    # Round Alpha#35 to two decimal places
    final_df['Alpha#35'] = final_df['Alpha#35'].round(2)

    # Save results
    final_df.to_csv(output_path, index=False)
    print(f"Alpha#35 calculated and saved to {output_path}")

if __name__ == "__main__":
    main() 