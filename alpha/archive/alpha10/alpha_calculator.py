import pandas as pd
import numpy as np

def calculate_delta(series, period=1):
    """Helper to calculate difference, ensuring enough periods or NaN."""
    if len(series) < period + 1: # Need period+1 observations for one difference
        return pd.Series([np.nan] * len(series), index=series.index)
    return series.diff(periods=period)

def ts_min(series, window):
    """Helper for time-series min over a rolling window."""
    if len(series) < window:
        return pd.Series([np.nan] * len(series), index=series.index)
    return series.rolling(window=window, min_periods=window).min()

def ts_max(series, window):
    """Helper for time-series max over a rolling window."""
    if len(series) < window:
        return pd.Series([np.nan] * len(series), index=series.index)
    return series.rolling(window=window, min_periods=window).max()

def rank_pct(series):
    """Helper for cross-sectional rank (percentile)."""
    return series.rank(pct=True)

def calculate_alpha10(df, delta_period=1, ts_window=4):
    """
    Calculates Alpha#10 based on the formula:
    rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))

    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'asset_id', 'close']
        delta_period (int): Period for delta(close, 1), typically 1.
        ts_window (int): Window for ts_min and ts_max, typically 4.

    Returns:
        pd.DataFrame: DataFrame with Alpha#10 values and intermediate calculations.
    """
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Calculate delta(close, 1)
    df['delta_close_1'] = df.groupby('asset_id')['close'].transform(
        lambda x: calculate_delta(x, delta_period)
    )

    # Calculate ts_min(delta(close, 1), 4)
    df['ts_min_delta_close_1_4'] = df.groupby('asset_id')['delta_close_1'].transform(
        lambda x: ts_min(x, ts_window)
    )

    # Calculate ts_max(delta(close, 1), 4)
    df['ts_max_delta_close_1_4'] = df.groupby('asset_id')['delta_close_1'].transform(
        lambda x: ts_max(x, ts_window)
    )

    # Apply the conditional logic to determine the intermediate value
    condition1 = 0 < df['ts_min_delta_close_1_4']
    condition2 = df['ts_max_delta_close_1_4'] < 0

    df['intermediate_value'] = np.select(
        [condition1, condition2],
        [df['delta_close_1'], df['delta_close_1']],
        default=(-1 * df['delta_close_1'])
    )
    
    # Handle NaNs from conditions or inputs propagating to intermediate_value
    # If delta_close_1 is NaN, intermediate_value will be NaN.
    # If ts_min or ts_max is NaN, the conditions might evaluate in an unexpected way for np.select if not careful.
    # However, np.select propagates NaNs from the choicelist correctly.
    # NaNs in condition arrays: condition1/2 will be False if ts_min/ts_max is NaN. This leads to default.
    # If default's component (-1 * delta_close_1) is NaN, then intermediate is NaN.
    # This seems to handle NaN propagation correctly based on np.select behavior.

    # Calculate rank of the intermediate value (cross-sectional rank for each day)
    df['alpha10'] = df.groupby('date')['intermediate_value'].transform(rank_pct)

    # Round final alpha and intermediate steps for clarity in output
    df['alpha10'] = df['alpha10'].round(2)
    df['delta_close_1'] = df['delta_close_1'].round(4) # Keep more precision for intermediate calcs
    df['ts_min_delta_close_1_4'] = df['ts_min_delta_close_1_4'].round(4)
    df['ts_max_delta_close_1_4'] = df['ts_max_delta_close_1_4'].round(4)
    df['intermediate_value'] = df['intermediate_value'].round(4)

    return df[['date', 'asset_id', 'close', 'delta_close_1', 
               'ts_min_delta_close_1_4', 'ts_max_delta_close_1_4', 
               'intermediate_value', 'alpha10']]

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha10_results.csv"

    try:
        input_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['date'])
    except FileNotFoundError:
        print(f"错误: 数据文件 {DATA_FILE_PATH} 未找到. 请先运行位于 data 目录的 mock 数据生成脚本。")
        exit(1)
    except Exception as e:
        print(f"加载数据时出错: {e}")
        exit(1)

    required_columns = ['close'] # Alpha10 only needs 'close'
    # Include 'volume' just for consistency with other alphas' data loading and initial checks, though not used by Alpha10 itself
    # This way, the same mock_data.csv can be used without modification worries if other alphas need 'volume'.
    all_checked_columns = ['close', 'volume'] 
    missing_columns = [col for col in all_checked_columns if col not in input_df.columns]
    if 'close' not in input_df.columns:
        print(f"错误: 数据文件缺少核心必需列: ['close']. 请检查 {DATA_FILE_PATH} 或更新生成脚本。")
        exit(1)
    elif missing_columns:
        print(f"警告: 数据文件缺少一些列: {missing_columns}, 但 Alpha#10 核心计算仅需 'close'。")


    print("成功加载数据文件...")
    print(f"数据包含 {len(input_df)} 行，{len(input_df.columns)} 列.")
    print(f"日期范围从 {input_df['date'].min().strftime('%Y-%m-%d')} 到 {input_df['date'].max().strftime('%Y-%m-%d')}.")
    print(f"资产数量: {input_df['asset_id'].nunique()}.")

    print("\n开始计算 Alpha#10...")
    alpha_df = calculate_alpha10(input_df.copy())

    alpha_df.to_csv(OUTPUT_FILE_PATH, index=False, float_format='%.2f')
    print(f"Alpha#10 计算完成，结果已保存到 {OUTPUT_FILE_PATH}")

    print("\nAlpha#10 结果预览:")
    num_assets_to_display = min(2, alpha_df['asset_id'].nunique()) # Display min of 2 assets or total if less
    rows_per_asset_display = 5
    asset_ids = alpha_df['asset_id'].unique()
    
    if len(asset_ids) > 0:
        selected_assets = asset_ids[:num_assets_to_display]
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
    else:
        print("没有可供预览的资产数据。")

    print("\nAlpha#10 列统计信息 (不含 NaN):")
    if not alpha_df['alpha10'].dropna().empty:
        with pd.option_context('display.float_format', '{:.2f}'.format):
            print(alpha_df['alpha10'].dropna().describe())
        nan_alpha_counts = alpha_df['alpha10'].isna().sum()
        print(f"Alpha#10 列中 NaN 值数量: {nan_alpha_counts} (预期由初始计算窗口期和排名时组内数量不足导致)")
    else:
        print("Alpha#10 列不包含有效数据进行统计。")

    print("\n脚本执行完毕。") 