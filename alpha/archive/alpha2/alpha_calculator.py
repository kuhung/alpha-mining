import pandas as pd
import numpy as np

def delta(series, period):
    """
    Computes the difference between current value and value 'period' periods ago.
    delta(series, N) = series[t] - series[t-N]
    """
    return series - series.shift(period)

def rolling_correlation(x, y, window):
    """
    Computes rolling correlation between two series over a specified window.
    """
    return x.rolling(window=window, min_periods=1).corr(y)

def calculate_alpha2(df, delta_period=2, correlation_window=6):
    """
    Calculates Alpha#2 based on the given formula.

    Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Check if required columns exist
    required_columns = ['date', 'asset_id', 'close', 'open', 'volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Calculate log(volume)
    df['log_volume'] = np.log(df['volume'])
    
    # Calculate delta(log(volume), 2) for each asset
    df['delta_log_volume'] = df.groupby('asset_id')['log_volume'].transform(
        lambda x: delta(x, delta_period)
    )
    
    # Calculate intraday return: (close - open) / open
    df['intraday_return'] = (df['close'] - df['open']) / df['open']
    
    # Calculate daily cross-sectional ranks
    df['rank_delta_log_volume'] = df.groupby('date')['delta_log_volume'].rank(pct=True, method='average')
    df['rank_intraday_return'] = df.groupby('date')['intraday_return'].rank(pct=True, method='average')
    
    # Calculate rolling correlation for each asset
    def calculate_correlation_for_group(group):
        return rolling_correlation(
            group['rank_delta_log_volume'], 
            group['rank_intraday_return'], 
            correlation_window
        )
    
    df['correlation'] = df.groupby('asset_id').apply(
        calculate_correlation_for_group
    ).reset_index(level=0, drop=True)
    
    # Final Alpha#2: -1 * correlation
    df['alpha2'] = -1 * df['correlation']
    
    # Round to 4 decimal places for better readability
    df['alpha2'] = df['alpha2'].round(4)
    
    # Handle NaN values (set to 0 for early periods where correlation cannot be calculated)
    df['alpha2'] = df['alpha2'].fillna(0)
    
    return df[['date', 'asset_id', 'open', 'close', 'volume', 'alpha2']]

if __name__ == "__main__":
    # Load mock data
    try:
        data_df = pd.read_csv("../../data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: ../../data/mock_data.csv not found. Please ensure the mock data file exists.")
        print("The file should contain columns: date, asset_id, open, close, volume")
        exit()
    
    # Check if required columns exist
    required_columns = ['date', 'asset_id', 'close', 'open', 'volume']
    missing_columns = [col for col in required_columns if col not in data_df.columns]
    if missing_columns:
        print(f"Error: Missing required columns in mock_data.csv: {missing_columns}")
        print("Required columns: date, asset_id, open, close, volume")
        exit()

    # Calculate Alpha#2
    try:
        alpha_df = calculate_alpha2(data_df.copy())
        
        # Save results
        alpha_df.to_csv("alpha2_results.csv", index=False)
        print("Alpha#2 calculated and results saved to alpha2_results.csv")
        print("\nFirst 5 rows of Alpha#2 results:")
        print(alpha_df.head())
        print("\nLast 5 rows of Alpha#2 results:")
        print(alpha_df.tail())
        print("\nDescriptive statistics of Alpha#2:")
        print(alpha_df['alpha2'].describe())
        
        # Additional statistics
        print(f"\nNumber of non-zero Alpha#2 values: {(alpha_df['alpha2'] != 0).sum()}")
        print(f"Number of NaN Alpha#2 values: {alpha_df['alpha2'].isna().sum()}")
        
    except Exception as e:
        print(f"Error calculating Alpha#2: {str(e)}")
        exit() 