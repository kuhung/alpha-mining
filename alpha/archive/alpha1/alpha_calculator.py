import pandas as pd
import numpy as np

def signed_power(series, exponent):
    """
    Computes sign(series) * (abs(series) ** exponent).
    """
    return np.sign(series) * (np.abs(series) ** exponent)

def ts_arg_max(series, window):
    """
    对每一天，返回过去window天内最大值出现的位置（0为今天，1为昨天，依此类推）。
    """
    def argmax_pos(x):
        # x为长度window的Series
        return window - 1 - np.argmax(x.values[::-1])
    return series.rolling(window=window, min_periods=1).apply(argmax_pos, raw=False)


def calculate_alpha1(df, stddev_window=20, ts_argmax_window=5):
    """
    Calculates Alpha#1 based on the given formula.

    Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)
    其中 Ts_ArgMax 返回最大值出现的相对天数（0为今天，1为昨天...）
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])

    # Calculate stddev_returns for each asset
    df['stddev_returns'] = df.groupby('asset_id')['returns'].transform(
        lambda x: x.rolling(window=stddev_window, min_periods=1).std()
    )

    # Condition: (returns < 0) ? stddev(returns, 20) : close
    df['conditional_value'] = np.where(df['returns'] < 0, df['stddev_returns'], df['close'])

    # SignedPower(conditional_value, 2.)
    df['signed_power_value'] = df.groupby('asset_id')['conditional_value'].transform(
        lambda x: signed_power(x, 2.0)
    )
    # Fill NaNs that might result from signed_power if conditional_value was NaN (e.g. early stddev)
    df['signed_power_value'] = df['signed_power_value'].fillna(0)

    # Ts_ArgMax(SignedPower_value, 5)
    # 返回最大值出现的相对天数
    df['ts_argmax_value'] = df.groupby('asset_id')['signed_power_value'].transform(
        lambda x: ts_arg_max(x, window=ts_argmax_window)
    )

    # rank(ts_argmax_value)
    # Rank is calculated daily across all assets
    df['rank_ts_argmax'] = df.groupby('date')['ts_argmax_value'].rank(pct=True, method='average')

    # Final Alpha: (rank - 0.5)
    df['alpha1'] = round(df['rank_ts_argmax'] - 0.5, 2)

    return df[['date', 'asset_id', 'close', 'returns', 'alpha1']]

if __name__ == "__main__":
    # Load mock data
    try:
        data_df = pd.read_csv("/Users/kuhung/roy/alpha-mining/data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("Error: mock_data.csv not found. Please run generate_mock_data.py first.")
        exit()

    # Calculate Alpha
    alpha_df = calculate_alpha1(data_df.copy()) # Use a copy to avoid modifying original df in some pandas versions

    # Save results
    alpha_df.to_csv("alpha1_results.csv", index=False)
    print("Alpha#1 calculated and results saved to alpha1_results.csv")
    print("\nFirst 5 rows of Alpha results:")
    print(alpha_df.head())
    print("\nLast 5 rows of Alpha results:")
    print(alpha_df.tail())
    print("\nDescriptive statistics of Alpha1:")
    print(alpha_df['alpha1'].describe()) 