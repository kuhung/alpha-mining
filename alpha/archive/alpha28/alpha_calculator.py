import pandas as pd
import numpy as np

def scale(df):
    """
    Standardize a series to have zero mean and unit variance
    """
    return (df - df.mean()) / df.std()

def calculate_alpha28(df):
    """
    Calculates Alpha#28 based on the given formula:
    scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Calculate 20-day average volume (adv20)
    df['adv20'] = df.groupby('asset_id')['volume'].transform(
        lambda x: x.rolling(window=20, min_periods=1).mean()
    )
    
    # Calculate mid price
    df['mid_price'] = (df['high'] + df['low']) / 2
    
    # Calculate correlation between adv20 and low price
    df['correlation'] = df.groupby('asset_id').apply(
        lambda x: x['adv20'].rolling(window=5, min_periods=5).corr(x['low'])
    ).reset_index(level=0, drop=True)
    
    # Calculate combined result before scaling
    df['result'] = df['correlation'] + df['mid_price'] - df['close']
    
    # Apply scaling by group (date)
    df['alpha28'] = df.groupby('date')['result'].transform(lambda x: scale(x))
    
    # Round to 2 decimal places
    df['alpha28'] = round(df['alpha28'], 2)
    
    # Select and return relevant columns
    return df[['date', 'asset_id', 'volume', 'high', 'low', 'close', 'alpha28']]

if __name__ == "__main__":
    # Load data
    try:
        data_df = pd.read_csv("/Users/kuhung/roy/alpha-mining/data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: mock_data.csv not found. Please ensure the data file exists.")
        exit()

    # Calculate Alpha
    alpha_df = calculate_alpha28(data_df.copy())  # Use a copy to avoid modifying original df

    # Save results
    output_file = "alpha28_results.csv"
    alpha_df.to_csv(output_file, index=False)
    
    print(f"Alpha#28 calculated and results saved to {output_file}")
    print("\nFirst 5 rows of Alpha results:")
    print(alpha_df.head())
    print("\nLast 5 rows of Alpha results:")
    print(alpha_df.tail())
    print("\nDescriptive statistics of Alpha28:")
    print(alpha_df['alpha28'].describe()) 