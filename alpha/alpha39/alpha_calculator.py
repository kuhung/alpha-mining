import pandas as pd
import numpy as np

# --- Helper Functions ---

def cs_rank(series: pd.Series) -> pd.Series:
    """Cross-sectional rank (percentage)."""
    return series.rank(method='average', pct=True)

def ts_rank(series: pd.Series, period: int) -> pd.Series:
    """Time-series rank over the past period."""
    return series.rolling(window=period, min_periods=period).apply(lambda x: x.rank(method='average', pct=True).iloc[-1], raw=False)

def ts_delta(series: pd.Series, period: int) -> pd.Series:
    """Time-series delta (difference) over the past period."""
    return series.diff(period)

def ts_sum(series: pd.Series, period: int) -> pd.Series:
    """Time-series sum over the past period."""
    return series.rolling(window=period, min_periods=period).sum()

def decay_linear(series: pd.Series, period: int) -> pd.Series:
    """
    Applies a linear decay to a time series over the specified period.
    More recent observations have higher weights.
    Weights are (period), (period-1), ..., 1.
    """
    if series.empty:
        return pd.Series(np.nan, index=series.index)

    if not pd.api.types.is_numeric_dtype(series):
        try:
            series = pd.to_numeric(series)
        except ValueError:
            raise TypeError("Input series for decay_linear must be numeric.")

    decayed_values = []
    weights = np.arange(1, period + 1) # [1, 2, ..., period]
    sum_weights = weights.sum()

    for i in range(len(series)):
        if i >= period - 1:
            window = series.iloc[i - period + 1 : i + 1]
            if len(window) == period and not window.isnull().all():
                # Apply weights in reverse order: latest * period, oldest * 1
                weighted_sum = (window * weights[::-1]).sum()
                decayed_values.append(weighted_sum / sum_weights)
            else:
                decayed_values.append(np.nan)
        else:
            decayed_values.append(np.nan)

    return pd.Series(decayed_values, index=series.index)

# --- Main Alpha Calculation Function ---

def calculate_alpha39(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Alpha#39:
    ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 + rank(sum(returns, 250))))
    """
    required_cols = ['close', 'volume', 'returns']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame.")

    # Ensure data is sorted by asset_id then date for time-series operations
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # --- Component 1: adv20 (Average Daily Volume over 20 periods) ---
    df['adv20'] = df.groupby('asset_id')['volume'].transform(lambda x: x.rolling(window=20, min_periods=20).mean())

    # --- Component 2: delta(close, 7) ---
    df['delta_close_7'] = df.groupby('asset_id')['close'].transform(lambda x: ts_delta(x, 7))

    # --- Component 3: volume / adv20 ---
    df['volume_div_adv20'] = df['volume'] / df['adv20']
    df.loc[df['adv20'] == 0, 'volume_div_adv20'] = np.nan

    # --- Component 4: decay_linear((volume / adv20), 9) ---
    df['decay_linear_volume_adv20_9'] = df.groupby('asset_id')['volume_div_adv20'].transform(lambda x: decay_linear(x, 9))

    # --- Component 5: 1 - rank(decay_linear((volume / adv20), 9)) ---
    df = df.sort_values(by=['date', 'asset_id'])
    df['ranked_decay_linear_volume_adv20'] = df.groupby('date')['decay_linear_volume_adv20_9'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index)
    )
    df['one_minus_ranked_decay_linear'] = 1 - df['ranked_decay_linear_volume_adv20']

    # --- Component 6: (delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))) ---
    df['momentum_volume_component'] = df['delta_close_7'] * df['one_minus_ranked_decay_linear']

    # --- Component 7: -1 * rank(momentum_volume_component) ---
    df = df.sort_values(by=['date', 'asset_id'])
    df['ranked_momentum_volume_component'] = df.groupby('date')['momentum_volume_component'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index)
    )
    df['neg_ranked_momentum_volume_component'] = -1 * df['ranked_momentum_volume_component']

    # --- Component 8: 1 + rank(sum(returns, 250)) ---
    df = df.sort_values(by=['asset_id', 'date']).copy()
    df['sum_returns_250'] = df.groupby('asset_id')['returns'].transform(lambda x: ts_sum(x, 250))

    df = df.sort_values(by=['date', 'asset_id'])
    df['ranked_sum_returns_250'] = df.groupby('date')['sum_returns_250'].transform(
        lambda x: cs_rank(x) if x.notna().sum() > 1 else pd.Series(np.nan, index=x.index)
    )
    df['one_plus_ranked_sum_returns'] = 1 + df['ranked_sum_returns_250']

    # --- Final Alpha Calculation ---
    df['alpha39'] = df['neg_ranked_momentum_volume_component'] * df['one_plus_ranked_sum_returns']

    # Rounding to 2 decimal places as required for final alpha and relevant intermediates
    alpha_related_cols_to_round = [
        'adv20', 'delta_close_7', 'volume_div_adv20', 'decay_linear_volume_adv20_9',
        'ranked_decay_linear_volume_adv20', 'one_minus_ranked_decay_linear',
        'momentum_volume_component', 'ranked_momentum_volume_component',
        'neg_ranked_momentum_volume_component', 'sum_returns_250',
        'ranked_sum_returns_250', 'one_plus_ranked_sum_returns', 'alpha39'
    ]

    for col in alpha_related_cols_to_round:
        if col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df.loc[:, col] = df[col].round(2)

    df = df.sort_values(by=['date', 'asset_id']).reset_index(drop=True)

    original_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'] if col in df.columns]

    intermediate_cols_for_output = [
        'adv20', 'delta_close_7', 'volume_div_adv20', 'decay_linear_volume_adv20_9',
        'ranked_decay_linear_volume_adv20', 'one_minus_ranked_decay_linear',
        'momentum_volume_component', 'ranked_momentum_volume_component',
        'neg_ranked_momentum_volume_component', 'sum_returns_250',
        'ranked_sum_returns_250', 'one_plus_ranked_sum_returns'
    ]
    final_alpha_col = ['alpha39']

    output_cols = original_cols + [col for col in intermediate_cols_for_output + final_alpha_col if col not in original_cols and col in df.columns]

    return df[output_cols]


if __name__ == "__main__":
    # --- Configuration ---
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha39_results.csv"

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
        print("Calculating Alpha#39...")
        alpha_df_output = calculate_alpha39(input_df.copy())
        print("Alpha#39 calculation complete.")
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
        # Filter out rows where 'alpha39' is NaN before saving
        alpha_df_output = alpha_df_output.dropna(subset=['alpha39'])

        # Use float_format to ensure 2 decimal places for floats in the CSV
        alpha_df_output.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
        print(f"Alpha#39 results saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")
        exit(1)

    # --- Display Sample Results (Optional) ---
    print("\n--- Sample of Alpha#39 Results ---")
    if not alpha_df_output.empty:
        with pd.option_context('display.max_columns', None, 'display.float_format', '{:.2f}'.format):
            print(alpha_df_output.head().to_string())

        print("\n--- General Information ---")
        print(f"Total rows in result: {len(alpha_df_output)}")
        if 'asset_id' in alpha_df_output.columns:
            print(f"Number of unique assets: {alpha_df_output['asset_id'].nunique()}")

        key_cols_for_nan_check = [
            'adv20', 'delta_close_7', 'volume_div_adv20', 'decay_linear_volume_adv20_9',
            'ranked_decay_linear_volume_adv20', 'one_minus_ranked_decay_linear',
            'momentum_volume_component', 'ranked_momentum_volume_component',
            'neg_ranked_momentum_volume_component', 'sum_returns_250',
            'ranked_sum_returns_250', 'one_plus_ranked_sum_returns', 'alpha39'
        ]
        for col in key_cols_for_nan_check:
            if col in alpha_df_output.columns:
                nan_counts = alpha_df_output[col].isna().sum()
                print(f"Number of NaN values in {col}: {nan_counts}")

        if 'alpha39' in alpha_df_output.columns and len(alpha_df_output['alpha39'].dropna()) > 0:
            print("\nAlpha39 column statistics (excluding NaNs):")
            with pd.option_context('display.float_format', '{:.2f}'.format):
                 print(alpha_df_output['alpha39'].dropna().describe())
        elif 'alpha39' in alpha_df_output.columns:
            print("\nAlpha39 column contains only NaN values.")
    else:
        print("Resulting DataFrame is empty.") 