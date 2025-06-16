import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_delay(series: pd.Series, period: int) -> pd.Series:
    """Time-series delay."""
    return series.shift(period)

def ts_correlation(series1: pd.Series, series2: pd.Series, period: int) -> pd.Series:
    """Time-series correlation."""
    return series1.rolling(window=period).corr(series2)

def ts_rank(series: pd.Series, period: int) -> pd.Series:
    """Time-series rank."""
    return series.rolling(window=period).apply(lambda x: x.rank(pct=True).iloc[-1], raw=False)

def ts_sum(series: pd.Series, period: int) -> pd.Series:
    """Time-series sum."""
    return series.rolling(window=period).sum()

def ts_mean(series: pd.Series, period: int) -> pd.Series:
    """Time-series mean."""
    return series.rolling(window=period).mean()

# --- Main Alpha Calculation Function ---

def calculate_alpha36(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Alpha#36.
    """
    required_cols = ['open', 'close', 'volume', 'vwap', 'returns']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Pre-calculations ---
    # adv20: 20-day average daily dollar volume
    df['dollar_volume'] = df['close'] * df['volume']
    df['adv20'] = df.groupby('asset_id')['dollar_volume'].transform(lambda x: ts_mean(x, 20))

    # --- Term 1 ---
    df['close_minus_open'] = df['close'] - df['open']
    df['delayed_volume_1'] = df.groupby('asset_id')['volume'].transform(lambda x: ts_delay(x, 1))
    df['corr_15d'] = df.groupby('asset_id').apply(
        lambda x: ts_correlation(x['close_minus_open'], x['delayed_volume_1'], 15)
    ).reset_index(level=0, drop=True)
    
    df = df.sort_values(by=['date', 'asset_id'])
    df['term1'] = 2.21 * df.groupby('date')['corr_15d'].transform(cs_rank)

    # --- Term 2 ---
    df['open_minus_close'] = df['open'] - df['close']
    df['term2'] = 0.7 * df.groupby('date')['open_minus_close'].transform(cs_rank)

    # --- Term 3 ---
    df = df.sort_values(by=['asset_id', 'date'])
    df['neg_returns_delayed_6'] = df.groupby('asset_id')['returns'].transform(lambda x: ts_delay(-1 * x, 6))
    df['ts_rank_5d'] = df.groupby('asset_id')['neg_returns_delayed_6'].transform(lambda x: ts_rank(x, 5))
    
    df = df.sort_values(by=['date', 'asset_id'])
    df['term3'] = 0.73 * df.groupby('date')['ts_rank_5d'].transform(cs_rank)

    # --- Term 4 ---
    df = df.sort_values(by=['asset_id', 'date'])
    df['corr_vwap_adv20_6d'] = df.groupby('asset_id').apply(
        lambda x: ts_correlation(x['vwap'], x['adv20'], 6)
    ).reset_index(level=0, drop=True)
    df['abs_corr'] = df['corr_vwap_adv20_6d'].abs()
    
    df = df.sort_values(by=['date', 'asset_id'])
    df['term4'] = df.groupby('date')['abs_corr'].transform(cs_rank)

    # --- Term 5 ---
    df = df.sort_values(by=['asset_id', 'date'])
    df['sum_close_200'] = df.groupby('asset_id')['close'].transform(lambda x: ts_sum(x, 200))
    df['avg_close_200'] = df['sum_close_200'] / 200
    df['value_momentum_interaction'] = (df['avg_close_200'] - df['open']) * (df['close'] - df['open'])
    
    df = df.sort_values(by=['date', 'asset_id'])
    df['term5'] = 0.6 * df.groupby('date')['value_momentum_interaction'].transform(cs_rank)
    
    # --- Final Alpha Calculation ---
    df['alpha36'] = df['term1'] + df['term2'] + df['term3'] + df['term4'] + df['term5']

    # --- Output Formatting ---
    # Rounding to 2 decimal places as required
    alpha_related_cols_to_round = [
        'term1', 'term2', 'term3', 'term4', 'term5', 'alpha36'
    ]
    for col in alpha_related_cols_to_round:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].round(2)
            
    # Re-sort for final output consistency
    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)
    
    # Define columns to keep
    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]
    intermediate_cols_for_output = ['term1', 'term2', 'term3', 'term4', 'term5']
    final_alpha_col = ['alpha36']
    
    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha36_results.csv"

    try:
        input_df = pd.read_csv(DATA_FILE_PATH)
        input_df['date'] = pd.to_datetime(input_df['date'])
        if 'asset_id' in input_df.columns:
            input_df['asset_id'] = input_df['asset_id'].astype(str)
        print("Data loaded and preprocessed successfully.")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE_PATH}.")
        exit(1)
    except Exception as e:
        print(f"Error loading or preprocessing data: {e}")
        exit(1)

    try:
        print("Calculating Alpha#36...")
        alpha_df_output = calculate_alpha36(input_df.copy())
        print("Alpha#36 calculation complete.")
    except Exception as e:
        print(f"An unexpected error occurred during Alpha calculation: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    try:
        alpha_df_output.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#36 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    print("\n--- Sample of Alpha#36 Results ---")
    if not alpha_df_output.empty:
        with pd.option_context('display.max_columns', None, 'display.float_format', '{:.2f}'.format):
            print(alpha_df_output.head().to_string())
    else:
        print("Resulting DataFrame is empty.") 