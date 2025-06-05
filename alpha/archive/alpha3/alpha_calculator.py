import pandas as pd
import numpy as np

def rolling_correlation(x, y, window):
    """
    Computes rolling correlation between two series over a specified window.
    """
    correlation = x.rolling(window=window, min_periods=1).corr(y)
    # Handle infinite values and replace with 0
    correlation = correlation.replace([np.inf, -np.inf], 0)
    return correlation

def calculate_alpha3(df, correlation_window=10):
    """
    Calculates Alpha#3 based on the given formula.

    Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))
    
    Args:
        df: DataFrame containing date, asset_id, open, volume columns
        correlation_window: Window size for correlation calculation (default: 10)
    
    Returns:
        DataFrame with Alpha#3 values
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Check if required columns exist
    required_columns = ['date', 'asset_id', 'open', 'volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Calculate daily cross-sectional ranks
    # rank(open): rank of opening price across all assets on each day
    df['rank_open'] = df.groupby('date')['open'].rank(pct=True, method='average')
    
    # rank(volume): rank of volume across all assets on each day  
    df['rank_volume'] = df.groupby('date')['volume'].rank(pct=True, method='average')
    
    # Calculate rolling correlation for each asset
    def calculate_correlation_for_group(group):
        correlation = rolling_correlation(
            group['rank_open'], 
            group['rank_volume'], 
            correlation_window
        )
        return correlation
    
    df['correlation'] = df.groupby('asset_id', group_keys=False).apply(
        calculate_correlation_for_group
    )
    
    # Final Alpha#3: -1 * correlation
    df['alpha3'] = -1 * df['correlation']
    
    # Handle infinite and NaN values
    df['alpha3'] = df['alpha3'].replace([np.inf, -np.inf], 0)
    df['alpha3'] = df['alpha3'].fillna(0)
    
    # Round to 4 decimal places for better readability
    df['alpha3'] = df['alpha3'].round(4)
    
    return df[['date', 'asset_id', 'open', 'volume', 'alpha3']]

if __name__ == "__main__":
    # Load mock data
    try:
        data_df = pd.read_csv("../../data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: ../../data/mock_data.csv not found. Please ensure the mock data file exists.")
        print("The file should contain columns: date, asset_id, open, volume")
        exit()
    
    # Check if required columns exist
    required_columns = ['date', 'asset_id', 'open', 'volume']
    missing_columns = [col for col in required_columns if col not in data_df.columns]
    if missing_columns:
        print(f"Error: Missing required columns in mock_data.csv: {missing_columns}")
        print("Required columns: date, asset_id, open, volume")
        exit()

    # Calculate Alpha#3
    try:
        alpha_df = calculate_alpha3(data_df.copy())
        
        # Save results
        alpha_df.to_csv("alpha3_results.csv", index=False)
        print("Alpha#3 calculated and results saved to alpha3_results.csv")
        print("\nFirst 5 rows of Alpha#3 results:")
        print(alpha_df.head())
        print("\nLast 5 rows of Alpha#3 results:")
        print(alpha_df.tail())
        print("\nDescriptive statistics of Alpha#3:")
        print(alpha_df['alpha3'].describe())
        
        # Additional statistics
        print(f"\nNumber of non-zero Alpha#3 values: {(alpha_df['alpha3'] != 0).sum()}")
        print(f"Number of NaN Alpha#3 values: {alpha_df['alpha3'].isna().sum()}")
        
        # Correlation analysis
        print(f"\nCorrelation statistics:")
        print(f"Mean Alpha#3: {alpha_df['alpha3'].mean():.4f}")
        print(f"Std Alpha#3: {alpha_df['alpha3'].std():.4f}")
        print(f"Min Alpha#3: {alpha_df['alpha3'].min():.4f}")
        print(f"Max Alpha#3: {alpha_df['alpha3'].max():.4f}")
        
        # Check for extreme values
        extreme_values = alpha_df[(alpha_df['alpha3'] > 1) | (alpha_df['alpha3'] < -1)]
        if len(extreme_values) > 0:
            print(f"\nNumber of extreme values (|alpha3| > 1): {len(extreme_values)}")
        
    except Exception as e:
        print(f"Error calculating Alpha#3: {str(e)}")
        exit() 