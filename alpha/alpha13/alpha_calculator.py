import pandas as pd
import numpy as np

def rank_pct(series):
    """Helper for cross-sectional rank (percentile)."""
    return series.rank(pct=True)

def rolling_covariance(series1, series2, window):
    """Helper to calculate rolling covariance between two series for each asset."""
    # Ensure inputs are Series
    s1 = pd.Series(series1)
    s2 = pd.Series(series2)
    
    # Calculate rolling covariance
    # Need to handle cases where window size is not met, pandas rolling.cov handles this by returning NaN
    # min_periods is crucial for covariance calculation; pandas default for .cov() is window size.
    # For a pair of series, cov requires at least 2 observations for a non-NaN result.
    # So, min_periods for the rolling window should be at least 2.
    # If we want to ensure a full window for cov, set min_periods=window.
    return s1.rolling(window=window, min_periods=max(2, window)).cov(s2) # Ensure at least 2 periods for cov, or full window

def calculate_alpha13(df, cov_window=5):
    """
    Calculates Alpha#13 based on the formula:
    (-1 * rank(covariance(rank(close), rank(volume), 5)))

    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'asset_id', 'close', 'volume']
        cov_window (int): Window for covariance calculation, typically 5.

    Returns:
        pd.DataFrame: DataFrame with Alpha#13 values and intermediate calculations.
    """
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Step 1: Calculate rank(close) cross-sectionally for each day
    df['rank_close'] = df.groupby('date')['close'].transform(rank_pct)

    # Step 2: Calculate rank(volume) cross-sectionally for each day
    df['rank_volume'] = df.groupby('date')['volume'].transform(rank_pct)

    # Step 3 & 4: Calculate covariance(rank(close), rank(volume), 5) for each asset over time
    # We need to group by asset_id and then apply the rolling covariance
    df['cov_rank_close_rank_volume_5'] = df.groupby('asset_id', group_keys=False).apply(
        lambda x: rolling_covariance(x['rank_close'], x['rank_volume'], cov_window).round(4)
    )

    # Step 5: Calculate rank of the covariance (cross-sectional rank for each day)
    df['rank_cov'] = df.groupby('date')['cov_rank_close_rank_volume_5'].transform(rank_pct)

    # Step 6: Final Alpha#13 value
    df['alpha13'] = -1 * df['rank_cov']

    return df[['date', 'asset_id', 'close', 'volume', 
               'rank_close', 'rank_volume', 
               'cov_rank_close_rank_volume_5', 'rank_cov', 'alpha13']]

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha13_results.csv"

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

    print("\n开始计算 Alpha#13...")
    alpha_df = calculate_alpha13(input_df.copy())

    # Save with specific float format for the alpha column
    formatters = {'alpha13': lambda x: f"{x:.2f}" if pd.notnull(x) else ''}
    for col in ['rank_close', 'rank_volume', 'rank_cov']:
        formatters[col] = lambda x, col_name=col: f"{x:.4f}" if pd.notnull(x) else ''
    formatters['cov_rank_close_rank_volume_5'] = lambda x: f"{x:.6f}" if pd.notnull(x) else ''
    
    # Ensure original data (close, volume) is also preserved with reasonable formatting
    formatters['close'] = lambda x: f"{x:.2f}" if pd.notnull(x) else ''
    formatters['volume'] = lambda x: f"{x:.0f}" if pd.notnull(x) else '' # Volume typically integer

    alpha_df.to_csv(OUTPUT_FILE_PATH, index=False)
    print(f"Alpha#13 计算完成，结果已保存到 {OUTPUT_FILE_PATH}")

    print("\nAlpha#13 结果预览:")
    num_assets_to_display = min(2, alpha_df['asset_id'].nunique()) 
    rows_per_asset_display = 5
    asset_ids = alpha_df['asset_id'].unique()
    
    display_columns = ['date', 'asset_id', 'close', 'volume', 'rank_close', 'rank_volume', 'cov_rank_close_rank_volume_5', 'alpha13']

    if len(asset_ids) > 0:
        selected_assets = asset_ids[:num_assets_to_display]
        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df[alpha_df['asset_id'] == asset_id]
            print(f"\n资产ID: {asset_id}")
            print(f"前 {rows_per_asset_display} 行数据:")
            # Apply formatters for display
            print(asset_data.head(rows_per_asset_display)[display_columns].to_string(formatters=formatters))
            if len(asset_data) > rows_per_asset_display:
                print(f"\n后 {rows_per_asset_display} 行数据 ({asset_id}):")
                print(asset_data.tail(rows_per_asset_display)[display_columns].to_string(formatters=formatters))
            if i < len(selected_assets) - 1:
                print("-" * 70) # Adjusted separator width
    else:
        print("没有可供预览的资产数据。")

    print("\nAlpha#13 列统计信息 (不含 NaN):")
    if not alpha_df['alpha13'].dropna().empty:
        # Use pandas option for describe formatting
        with pd.option_context('display.float_format', '{:.2f}'.format): 
            print(alpha_df['alpha13'].dropna().describe())
        nan_alpha_counts = alpha_df['alpha13'].isna().sum()
        total_counts = len(alpha_df['alpha13'])
        print(f"Alpha#13 列中 NaN 值数量: {nan_alpha_counts} (总计 {total_counts} 行)")
        print("(NaN 值预期由初始计算窗口期和协方差/排名计算时组内数量不足导致)")
    else:
        print("Alpha#13 列不包含有效数据进行统计。")

    print("\n脚本执行完毕。") 