import pandas as pd
import numpy as np

def calculate_alpha5(df, vwap_window=10):
    """
    Calculates Alpha#5 based on the given formula.
    
    Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
    
    Args:
        df: DataFrame with columns ['date', 'asset_id', 'open', 'close', 'vwap', ...]
        vwap_window: int, window for VWAP moving average calculation (default=10)
        
    Returns:
        DataFrame with Alpha#5 values
    """
    # Ensure data is sorted by date for rolling calculations
    df = df.sort_values(by=['asset_id', 'date'])
    
    # Step 1: Calculate VWAP moving average (sum(vwap, 10) / 10)
    df['vwap_ma_10'] = df.groupby('asset_id')['vwap'].transform(
        lambda x: x.rolling(window=vwap_window, min_periods=1).mean().round(2)
    )
    
    # Step 2: Calculate open price difference from VWAP moving average
    df['open_vwap_diff'] = (df['open'] - df['vwap_ma_10']).round(2)
    
    # Step 3: Calculate close price difference from current VWAP
    df['close_vwap_diff'] = (df['close'] - df['vwap']).round(2)
    
    # Step 4: Cross-sectional ranking for each component
    # rank(open - vwap_ma_10)
    df['rank_open_diff'] = df.groupby('date')['open_vwap_diff'].rank(pct=True, method='average')
    
    # rank(close - vwap)
    df['rank_close_diff'] = df.groupby('date')['close_vwap_diff'].rank(pct=True, method='average')
    
    # Step 5: Calculate Alpha#5
    # (rank(open_diff) * (-1 * abs(rank(close_diff))))
    df['alpha5'] = df['rank_open_diff'] * (-1 * np.abs(df['rank_close_diff']))
    
    # Round to 4 decimal places for clarity
    df['alpha5'] = df['alpha5'].round(4)
    df['rank_open_diff'] = df['rank_open_diff'].round(4)
    df['rank_close_diff'] = df['rank_close_diff'].round(4)
    
    return df[['date', 'asset_id', 'open', 'close', 'vwap', 'vwap_ma_10', 
               'open_vwap_diff', 'close_vwap_diff', 'rank_open_diff', 'rank_close_diff', 'alpha5']]


def analyze_alpha5_results(df):
    """
    Performs additional analysis on Alpha#5 results.
    
    Args:
        df: DataFrame with Alpha#5 results
        
    Returns:
        None (prints analysis results)
    """
    print("=== Alpha#5 分析报告 ===")
    
    # Basic statistics
    print("\n1. Alpha#5 基础统计:")
    print(df['alpha5'].describe())
    
    # Distribution by asset
    print("\n2. 各资产Alpha#5统计:")
    asset_stats = df.groupby('asset_id')['alpha5'].agg(['count', 'mean', 'std', 'min', 'max']).round(4)
    print(asset_stats)
    
    # Recent performance
    print("\n3. 最近10天Alpha#5表现:")
    recent_dates = df['date'].nlargest(10).unique()
    recent_data = df[df['date'].isin(recent_dates)]
    daily_stats = recent_data.groupby('date')['alpha5'].agg(['mean', 'std', 'min', 'max']).round(4)
    print(daily_stats)
    
    # Correlation analysis
    print("\n4. 各组件相关性分析:")
    correlation_cols = ['open_vwap_diff', 'close_vwap_diff', 'rank_open_diff', 'rank_close_diff', 'alpha5']
    corr_matrix = df[correlation_cols].corr().round(3)
    print(corr_matrix)
    
    # Extreme values
    print("\n5. 极值分析:")
    print("Alpha#5最大值记录:")
    max_idx = df['alpha5'].idxmax()
    print(df.loc[max_idx, ['date', 'asset_id', 'alpha5', 'rank_open_diff', 'rank_close_diff']])
    
    print("\nAlpha#5最小值记录:")
    min_idx = df['alpha5'].idxmin()
    print(df.loc[min_idx, ['date', 'asset_id', 'alpha5', 'rank_open_diff', 'rank_close_diff']])


if __name__ == "__main__":
    # Load mock data
    try:
        data_df = pd.read_csv("/Users/kuhung/roy/alpha-mining/data/mock_data.csv", parse_dates=['date'])
    except FileNotFoundError:
        print("错误: 未找到mock_data.csv文件。请先运行generate_mock_data.py生成数据。")
        exit()
    
    # Check if required columns exist
    required_columns = ['open', 'close', 'vwap']
    missing_columns = [col for col in required_columns if col not in data_df.columns]
    
    if missing_columns:
        print(f"错误: 数据中缺少必要字段: {missing_columns}")
        print("请更新generate_mock_data.py脚本以包含所需字段。")
        exit()
    
    print("成功加载数据文件...")
    print(f"数据包含 {len(data_df)} 行，{len(data_df.columns)} 列")
    print(f"日期范围: {data_df['date'].min()} 到 {data_df['date'].max()}")
    print(f"资产数量: {data_df['asset_id'].nunique()}")
    
    # Calculate Alpha#5
    print("\n开始计算Alpha#5...")
    alpha_df = calculate_alpha5(data_df.copy())
    
    # Save results
    alpha_df.to_csv("alpha5_results.csv", index=False)
    print("Alpha#5计算完成，结果已保存到alpha5_results.csv")
    
    # Display sample results
    print("\nAlpha#5结果前5行:")
    print(alpha_df.head())
    print("\nAlpha#5结果后5行:")
    print(alpha_df.tail())
    
    # Perform detailed analysis
    analyze_alpha5_results(alpha_df)
    
    print("\n=== 计算示例 (最新日期) ===")
    latest_date = alpha_df['date'].max()
    latest_data = alpha_df[alpha_df['date'] == latest_date].copy()
    
    print(f"\n{latest_date.strftime('%Y-%m-%d')} 的计算示例:")
    print("资产ID | 开盘价 | 收盘价 | VWAP | VWAP_MA10 | 开盘差值 | 收盘差值 | 开盘排名 | 收盘排名 | Alpha#5")
    print("-" * 100)
    
    for _, row in latest_data.iterrows():
        print(f"{row['asset_id']:>7} | {row['open']:>6.2f} | {row['close']:>6.2f} | {row['vwap']:>6.2f} | "
              f"{row['vwap_ma_10']:>8.2f} | {row['open_vwap_diff']:>8.2f} | {row['close_vwap_diff']:>8.2f} | "
              f"{row['rank_open_diff']:>8.4f} | {row['rank_close_diff']:>8.4f} | {row['alpha5']:>7.4f}") 