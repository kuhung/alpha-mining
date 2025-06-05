import pandas as pd
import numpy as np

def calculate_alpha30(df):
    """
    Calculates Alpha#30 based on the given formula:
    (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +
    sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Calculate price differences
    df['diff1'] = df.groupby('asset_id')['close'].transform(lambda x: x - x.shift(1))
    df['diff2'] = df.groupby('asset_id')['close'].transform(lambda x: x.shift(1) - x.shift(2))
    df['diff3'] = df.groupby('asset_id')['close'].transform(lambda x: x.shift(2) - x.shift(3))
    
    # Calculate signs
    df['sign1'] = np.sign(df['diff1'])
    df['sign2'] = np.sign(df['diff2'])
    df['sign3'] = np.sign(df['diff3'])
    
    # Sum signs and calculate rank
    df['sign_sum'] = df['sign1'] + df['sign2'] + df['sign3']
    df['rank_result'] = 1.0 - df.groupby('date')['sign_sum'].rank(pct=True)
    
    # Calculate volume sums
    df['vol_5'] = df.groupby('asset_id')['volume'].transform(
        lambda x: x.rolling(window=5, min_periods=5).sum()
    )
    df['vol_20'] = df.groupby('asset_id')['volume'].transform(
        lambda x: x.rolling(window=20, min_periods=20).sum()
    )
    
    # Calculate final alpha
    # Handle potential division by zero
    df['alpha30'] = np.where(
        df['vol_20'] != 0,
        (df['rank_result'] * df['vol_5']) / df['vol_20'],
        0
    )
    
    # Round to 2 decimal places
    df['alpha30'] = round(df['alpha30'], 2)
    
    # Select and return relevant columns
    return df[['date', 'asset_id', 'close', 'volume', 'alpha30']]

if __name__ == "__main__":
    # Load data
    try:
        data_df = pd.read_csv("/Users/kuhung/roy/alpha-mining/data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: mock_data.csv not found. Please ensure the data file exists.")
        exit()

    # Calculate Alpha
    alpha_df = calculate_alpha30(data_df.copy())  # Use a copy to avoid modifying original df

    # Save results
    output_file = "alpha30_results.csv"
    alpha_df.to_csv(output_file, index=False)
    
    print(f"Alpha#30 calculated and results saved to {output_file}")
    print("\nFirst 5 rows of Alpha results:")
    print(alpha_df.head())
    print("\nLast 5 rows of Alpha results:")
    print(alpha_df.tail())
    print("\nDescriptive statistics of Alpha30:")
    print(alpha_df['alpha30'].describe()) 