import pandas as pd
import numpy as np

def ts_rank(series, window):
    """
    Computes the time-series rank of the current value within the past 'window' days.
    Returns the percentile rank of the current value among the past window values.
    
    Args:
        series: pandas Series with time series data
        window: int, number of periods to look back
        
    Returns:
        pandas Series with time-series rank values (0-1)
    """
    def compute_ts_rank(x):
        if len(x) < 1:
            return np.nan
        current_value = x.iloc[-1]  # Current value (most recent)
        window_values = x.values    # All values in the window
        
        # Count how many values are less than current value
        rank_position = np.sum(window_values < current_value)
        # Add 0.5 for ties (average rank)
        rank_position += 0.5 * np.sum(window_values == current_value)
        
        # Convert to percentile rank (0-1)
        percentile_rank = rank_position / len(window_values)
        return percentile_rank
    
    return series.rolling(window=window, min_periods=1).apply(compute_ts_rank, raw=False)


def calculate_alpha4(df, ts_rank_window=9):
    """
    Calculates Alpha#4 based on the given formula.
    
    Alpha#4: (-1 * Ts_Rank(rank(low), 9))
    
    Args:
        df: DataFrame with columns ['date', 'asset_id', 'low', ...]
        ts_rank_window: int, window for time-series rank calculation (default=9)
        
    Returns:
        DataFrame with Alpha#4 values
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Step 1: rank(low) - Cross-sectional ranking of low prices each day
    df['rank_low'] = df.groupby('date')['low'].rank(pct=True, method='average')
    
    # Step 2: Ts_Rank(rank(low), 9) - Time-series ranking for each asset
    df['ts_rank_value'] = df.groupby('asset_id')['rank_low'].transform(
        lambda x: ts_rank(x, window=ts_rank_window).round(2)
    )
    
    # Step 3: (-1 * Ts_Rank(...)) - Apply negative sign
    df['alpha4'] = -1 * df['ts_rank_value']
    
    # Round to 4 decimal places for clarity
    df['alpha4'] = df['alpha4'].round(4)
    
    return df[['date', 'asset_id', 'low', 'rank_low', 'ts_rank_value', 'alpha4']]


if __name__ == "__main__":
    # Load mock data
    try:
        data_df = pd.read_csv("/Users/kuhung/roy/alpha-mining/data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: mock_data.csv not found. Please run generate_mock_data.py first.")
        exit()
    
    # Check if 'low' column exists
    if 'low' not in data_df.columns:
        print("Error: 'low' column not found in data. Please update generate_mock_data.py to include high/low prices.")
        exit()
    
    # Calculate Alpha#4
    alpha_df = calculate_alpha4(data_df.copy())
    
    # Save results
    alpha_df.to_csv("alpha4_results.csv", index=False)
    print("Alpha#4 calculated and results saved to alpha4_results.csv")
    print("\nFirst 5 rows of Alpha#4 results:")
    print(alpha_df.head())
    print("\nLast 5 rows of Alpha#4 results:")
    print(alpha_df.tail())
    print("\nDescriptive statistics of Alpha#4:")
    print(alpha_df['alpha4'].describe())
    
    # Additional analysis
    print("\nAlpha#4 distribution by asset:")
    print(alpha_df.groupby('asset_id')['alpha4'].agg(['mean', 'std', 'min', 'max']).round(4))
    
    print("\nDaily Alpha#4 statistics (last 10 days):")
    daily_stats = alpha_df.groupby('date')['alpha4'].agg(['mean', 'std']).tail(10).round(4)
    print(daily_stats) 