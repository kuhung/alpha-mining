import pandas as pd
import numpy as np

def calculate_adv(series, window):
    """Helper to calculate rolling average, ensuring enough periods or NaN."""
    if len(series) < window:
        return pd.Series([np.nan] * len(series), index=series.index)
    return series.rolling(window=window, min_periods=window).mean()

def calculate_delta(series, period):
    """Helper to calculate difference, ensuring enough periods or NaN."""
    if len(series) < period:
        return pd.Series([np.nan] * len(series), index=series.index)
    return series.diff(periods=period)

def ts_rank(series, window):
    """Helper for time-series rank (percentile) over a rolling window."""
    if len(series) < window:
        return pd.Series([np.nan] * len(series), index=series.index)
    # rank(pct=True) ranks from 0 to 1. Formula requires 1-N, then scaled.
    # We use pct=True to get percentile rank directly (0 to 1)
    return series.rolling(window=window, min_periods=window).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=True)

def calculate_alpha7(df, adv_window=20, delta_period=7, ts_rank_window=60):
    """
    Calculates Alpha#7 based on the formula:
    ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1*1))

    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'asset_id', 'close', 'volume']
        adv_window (int): Window for average daily volume (adv20)
        delta_period (int): Period for delta(close, 7)
        ts_rank_window (int): Window for ts_rank

    Returns:
        pd.DataFrame: DataFrame with Alpha#7 values and intermediate calculations.
    """
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Calculate adv20 (average daily volume over 20 days)
    # Using .transform() to align results properly after groupby
    df['adv20'] = df.groupby('asset_id')['volume'].transform(
        lambda x: calculate_adv(x, adv_window)
    )

    # Calculate delta(close, 7)
    df['delta_close_7'] = df.groupby('asset_id')['close'].transform(
        lambda x: calculate_delta(x, delta_period)
    )

    # Calculate abs(delta(close, 7))
    df['abs_delta_close_7'] = np.abs(df['delta_close_7'])

    # Calculate ts_rank(abs(delta(close, 7)), 60)
    df['ts_rank_abs_delta_close_7'] = df.groupby('asset_id')['abs_delta_close_7'].transform(
        lambda x: ts_rank(x, ts_rank_window)
    )

    # Calculate sign(delta(close, 7))
    df['sign_delta_close_7'] = np.sign(df['delta_close_7'])

    # Condition: adv20 < volume
    condition = df['adv20'] < df['volume']

    # Calculate alpha based on condition
    # Part 1: When condition is true
    alpha_part1 = (-1 * df['ts_rank_abs_delta_close_7']) * df['sign_delta_close_7']
    
    # Part 2: When condition is false (-1*1 = -1)
    alpha_part2 = -1.0

    df['alpha7'] = np.where(condition, alpha_part1, alpha_part2)
    
    # Handle cases where intermediate values might be NaN, leading to NaN in alpha7
    # If adv20 is NaN, condition is False, so alpha7 becomes -1. This is acceptable by formula.
    # If ts_rank or sign is NaN, alpha_part1 is NaN. np.where handles this by assigning NaN.
    # We want to ensure that if any component of alpha_part1 is NaN, alpha7 is NaN IF the condition was true.
    # If the condition is true AND alpha_part1 is NaN, then alpha7 should be NaN.
    # If the condition is false, alpha7 is always -1, regardless of other NaNs.
    mask_condition_true_and_nan = condition & (df['ts_rank_abs_delta_close_7'].isna() | df['sign_delta_close_7'].isna())
    df.loc[mask_condition_true_and_nan, 'alpha7'] = np.nan

    # Round final alpha and intermediate steps for clarity in output
    df['alpha7'] = df['alpha7'].round(2) # As per user request
    df['adv20'] = df['adv20'].round(2)
    df['delta_close_7'] = df['delta_close_7'].round(2)
    df['abs_delta_close_7'] = df['abs_delta_close_7'].round(2)
    df['ts_rank_abs_delta_close_7'] = df['ts_rank_abs_delta_close_7'].round(4)
    # sign_delta_close_7 is already -1, 0, or 1

    return df[['date', 'asset_id', 'close', 'volume', 'adv20', 
               'delta_close_7', 'abs_delta_close_7', 'ts_rank_abs_delta_close_7', 
               'sign_delta_close_7', 'alpha7']]

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha7_results.csv"

    try:
        input_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['date'])
    except FileNotFoundError:
        print(f"错误: 数据文件 {DATA_FILE_PATH} 未找到. 请先运行位于 data 目录的 mock 数据生成脚本。")
        exit(1)
    except Exception as e:
        print(f"加载数据时出错: {e}")
        exit(1)

    required_columns = ['close', 'volume']
    missing_columns = [col for col in required_columns if col not in input_df.columns]
    if missing_columns:
        print(f"错误: 数据文件缺少必需列: {missing_columns}. 请检查 {DATA_FILE_PATH} 或更新生成脚本。")
        exit(1)

    print("成功加载数据文件...")
    print(f"数据包含 {len(input_df)} 行，{len(input_df.columns)} 列.")
    print(f"日期范围从 {input_df['date'].min().strftime('%Y-%m-%d')} 到 {input_df['date'].max().strftime('%Y-%m-%d')}.")
    print(f"资产数量: {input_df['asset_id'].nunique()}.")

    print("\n开始计算 Alpha#7...")
    alpha_df = calculate_alpha7(input_df.copy()) 
    # .copy() is used to avoid SettingWithCopyWarning on the original DataFrame

    alpha_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f') # Ensure alpha7 is saved with 2 decimal places
    print(f"Alpha#7 计算完成，结果已保存到 {OUTPUT_FILE_PATH}")

    print("\nAlpha#7 结果预览:")
    # Display head and tail for a couple of assets to check NaN and calculations
    num_assets_to_display = 2
    rows_per_asset_display = 5
    asset_ids = alpha_df['asset_id'].unique()
    if len(asset_ids) >= num_assets_to_display:
        selected_assets = asset_ids[:num_assets_to_display]
    else:
        selected_assets = asset_ids
    
    for i, asset_id in enumerate(selected_assets):
        asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
        print(f"\n资产ID: {asset_id}")
        print(f"前 {rows_per_asset_display} 行数据:")
        print(asset_data.head(rows_per_asset_display).to_string())
        if len(asset_data) > rows_per_asset_display:
                print(f"\n后 {rows_per_asset_display} 行数据 ({asset_id}):")
                print(asset_data.tail(rows_per_asset_display).to_string())
        if i < len(selected_assets) - 1:
            print("-" * 50)

    print("\nAlpha#7 列统计信息 (不含 NaN):")
    # Forcing float_format here as well for describe()
    with pd.option_context('display.float_format', '{:.2f}'.format):
        print(alpha_df['alpha7'].dropna().describe())
    
    nan_alpha_counts = alpha_df['alpha7'].isna().sum()
    print(f"Alpha#7 列中 NaN 值数量: {nan_alpha_counts} (预期由初始计算窗口期导致)")

    print("\n脚本执行完毕。") 