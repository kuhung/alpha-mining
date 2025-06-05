import pandas as pd
import numpy as np

def scale(df):
    """
    Standardize a series to have zero mean and unit variance
    """
    return (df - df.mean()) / df.std()

def delta(series, window):
    """
    Calculate the difference between the current value and the value 'window' days ago
    """
    return series - series.shift(window)

def ts_rank(series, window):
    """
    Calculate the rolling rank for a time series
    """
    return series.rolling(window=window).rank(pct=True)

def calculate_alpha29(df):
    """
    Calculates Alpha#29 based on the given formula:
    (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1),
    5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Part 1 calculation
    # Calculate initial difference
    df['diff'] = df.groupby('asset_id').apply(
        lambda x: delta(x['close'] - 1, 5)
    ).reset_index(level=0, drop=True)
    
    # Multiple rank operations
    df['part1'] = df.groupby('date')['diff'].rank(pct=True)  # First rank
    df['part1'] = -1 * df['part1']  # Negative
    df['part1'] = df.groupby('date')['part1'].rank(pct=True)  # Second rank
    df['part1'] = df.groupby('date')['part1'].rank(pct=True)  # Third rank
    
    # Time series operations
    df['part1'] = df.groupby('asset_id')['part1'].transform(
        lambda x: x.rolling(window=2, min_periods=2).min()  # ts_min
    )
    df['part1'] = df.groupby('asset_id')['part1'].transform(
        lambda x: x.rolling(window=1, min_periods=1).sum()  # sum
    )
    
    # Mathematical transformations
    df['part1'] = np.log(df['part1'].abs())  # log of absolute value to handle negative numbers
    df['part1'] = df.groupby('date')['part1'].transform(lambda x: scale(x))  # scale
    
    # Final transformations for part1
    df['part1'] = df.groupby('date')['part1'].rank(pct=True)  # rank
    df['part1'] = df.groupby('date')['part1'].rank(pct=True)  # rank again
    df['part1'] = df.groupby('asset_id')['part1'].transform(
        lambda x: x.rolling(window=1, min_periods=1).apply(np.prod)  # product
    )
    df['part1'] = df.groupby('asset_id')['part1'].transform(
        lambda x: x.rolling(window=5, min_periods=5).min()  # min
    )
    
    # Part 2 calculation
    df['part2'] = -1 * df['returns']  # Negative returns
    df['part2'] = df.groupby('asset_id')['part2'].shift(6)  # delay
    df['part2'] = df.groupby('asset_id')['part2'].transform(
        lambda x: ts_rank(x, 5)  # ts_rank
    )
    
    # Combine parts and calculate final alpha
    df['alpha29'] = df['part1'] + df['part2']
    
    # Round to 2 decimal places
    df['alpha29'] = round(df['alpha29'], 2)
    
    # Select and return relevant columns
    return df[['date', 'asset_id', 'close', 'returns', 'alpha29']]

if __name__ == "__main__":
    # Load data
    try:
        data_df = pd.read_csv("/Users/kuhung/roy/alpha-mining/data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: mock_data.csv not found. Please ensure the data file exists.")
        exit()

    # Calculate Alpha
    alpha_df = calculate_alpha29(data_df.copy())  # Use a copy to avoid modifying original df

    # Save results
    output_file = "alpha29_results.csv"
    alpha_df.to_csv(output_file, index=False)
    
    print(f"Alpha#29 calculated and results saved to {output_file}")
    print("\nFirst 5 rows of Alpha results:")
    print(alpha_df.head())
    print("\nLast 5 rows of Alpha results:")
    print(alpha_df.tail())
    print("\nDescriptive statistics of Alpha29:")
    print(alpha_df['alpha29'].describe()) 