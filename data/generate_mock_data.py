import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(num_assets=5, num_days=100):
    """
    Generates mock financial data for multiple assets.

    Args:
        num_assets (int): Number of assets.
        num_days (int): Number of trading days.

    Returns:
        pandas.DataFrame: DataFrame with columns ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'returns'].
    """
    data = []
    start_date = datetime(2025, 1, 1)

    for asset_idx in range(num_assets):
        asset_id = f"asset_{asset_idx + 1}"
        # Simulate closing prices with a random walk
        prices = [100.0]  # Initial price
        for _ in range(1, num_days):
            change = round(np.random.normal(0, 1.5), 1)  
            prices.append(round(max(1, prices[-1] + change), 1)) # Ensure price is positive

        for day_idx in range(num_days):
            date = start_date + timedelta(days=day_idx)
            close_price = prices[day_idx]
            
            # Generate open price (usually close to previous close or current close)
            if day_idx == 0:
                open_price = round(close_price + np.random.normal(0, 0.5), 2)
            else:
                # Open price is usually close to previous close with some gap
                gap = np.random.normal(0, 0.8)  # Random gap up/down
                open_price = round(max(1, prices[day_idx-1] + gap), 2)
            
            # Generate high and low prices
            # High should be >= max(open, close)
            # Low should be <= min(open, close)
            base_high = max(open_price, close_price)
            base_low = min(open_price, close_price)
            
            # Add some random variations for high and low
            high_variation = abs(np.random.normal(0, 0.5))  # Always positive
            low_variation = abs(np.random.normal(0, 0.5))   # Always positive
            
            high_price = round(base_high + high_variation, 2)
            low_price = round(max(0.01, base_low - low_variation), 2)  # Ensure positive
            
            # Generate volume (log-normal distribution for realistic volume patterns)
            base_volume = 1000000  # 1 million base volume
            volume_multiplier = np.random.lognormal(0, 0.5)  # Log-normal for realistic volume distribution
            volume = int(base_volume * volume_multiplier)
            
            # Calculate VWAP (Volume Weighted Average Price)
            # Simplified VWAP calculation: average of high, low, close weighted equally
            # In reality, VWAP is calculated as cumulative(price * volume) / cumulative(volume) throughout the day
            # For simplicity, we'll approximate it as a weighted average of key price points
            typical_price = (high_price + low_price + close_price) / 3
            # Add some random variation to make it more realistic (±0.5% of typical price)
            vwap_noise = np.random.normal(0, typical_price * 0.005)
            vwap = round(typical_price + vwap_noise, 2)
            # Ensure VWAP is within reasonable bounds (between low and high)
            vwap = round(max(low_price, min(high_price, vwap)), 2)

            # Calculate returns based on close prices
            if day_idx == 0:
                daily_return = round(np.random.normal(0, 0.05), 4) # Small random return for the first day
            else:
                daily_return = round(((prices[day_idx] / prices[day_idx-1]) - 1) , 4)

            data.append({
                "date": date.strftime('%Y-%m-%d'),
                "asset_id": asset_id,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
                "vwap": vwap,
                "returns": daily_return
            })

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['asset_id', 'date']).reset_index(drop=True)
    return df

if __name__ == "__main__":
    mock_df = generate_data(num_assets=5, num_days=100)
    mock_df.to_csv("mock_data.csv", index=False)
    print("mock_data.csv generated successfully with open, high, low, close, volume, vwap and returns data.")
    print("\nFirst 5 rows of generated data:")
    print(mock_df.head())
    print("\nData columns:", list(mock_df.columns)) 