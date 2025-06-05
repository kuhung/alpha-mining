import pandas as pd
import numpy as np

def rank_pct(series):
    """Helper for cross-sectional rank (percentile)."""
    return series.rank(pct=True)

def rolling_covariance(series1, series2, window):
    """Helper to calculate rolling covariance between two series for each asset."""
    s1 = pd.Series(series1)
    s2 = pd.Series(series2)
    return s1.rolling(window=window, min_periods=max(2, window)).cov(s2)

def format_float_to_2_sig_figs(val):
    """Formats a float to two significant figures, handling NaN and 0."""
    if pd.isna(val):
        return ""  # Keep NaN as empty string for CSV
    if val == 0:
        return "0.00" # Represent 0 as 0.00
    # Format to 2 significant figures
    return f"{val:.2g}"

def calculate_alpha16(df, cov_window=5):
    """
    Calculates Alpha#16 based on the formula:
    (-1 * rank(covariance(rank(high), rank(volume), 5)))

    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'asset_id', 'high', 'volume']
                           May also contain 'open', 'close', 'returns' for output consistency.
        cov_window (int): Window for covariance calculation, typically 5.

    Returns:
        pd.DataFrame: DataFrame with Alpha#16 values and intermediate calculations.
    """
    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Check for required columns
    required_cols = ['high', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"错误: 数据文件缺少必需列: '{col}'. Alpha#16 无法计算。请检查 mock_data.csv 或更新生成脚本。")

    # Step 1: Calculate rank(high) cross-sectionally for each day
    df['rank_high'] = df.groupby('date')['high'].transform(rank_pct)

    # Step 2: Calculate rank(volume) cross-sectionally for each day
    df['rank_volume'] = df.groupby('date')['volume'].transform(rank_pct)

    # Step 3 & 4: Calculate covariance(rank(high), rank(volume), 5) for each asset over time
    df['cov_rank_high_rank_volume_5'] = df.groupby('asset_id', group_keys=False).apply(
        lambda x: rolling_covariance(x['rank_high'], x['rank_volume'], cov_window)
    ) # No rounding here, keep precision for rank_cov

    # Step 5: Calculate rank of the covariance (cross-sectional rank for each day)
    df['rank_cov'] = df.groupby('date')['cov_rank_high_rank_volume_5'].transform(rank_pct)

    # Step 6: Final Alpha#16 value
    df['alpha16'] = -1 * df['rank_cov']

    # Select columns for output, including original data and intermediate steps
    output_columns = ['date', 'asset_id']
    # Add original data columns that are present in the input df
    # Common original columns seen in other alphas.
    # We prioritize 'high' and 'volume' as they are core to this alpha.
    original_data_cols_to_include = ['open', 'high', 'low', 'close', 'volume', 'returns']
    for col in original_data_cols_to_include:
        if col in df.columns and col not in output_columns:
            output_columns.append(col)
    
    intermediate_and_alpha_cols = [
        'rank_high', 'rank_volume',
        'cov_rank_high_rank_volume_5', 'rank_cov', 'alpha16'
    ]
    output_columns.extend(intermediate_and_alpha_cols)
    
    # Ensure no duplicate columns and preserve order
    final_output_columns = []
    for col in output_columns:
        if col not in final_output_columns:
            final_output_columns.append(col)
            
    return df[final_output_columns]

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha16_results.csv"

    try:
        input_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['date'])
    except FileNotFoundError:
        print(f"错误: 数据文件 {DATA_FILE_PATH} 未找到. 请先运行位于 data 目录的 mock 数据生成脚本。")
        exit(1)
    except Exception as e:
        print(f"加载数据时出错: {e}")
        exit(1)

    print("成功加载数据文件...")
    print(f"数据包含 {len(input_df)} 行，{len(input_df.columns)} 列.")
    print(f"日期范围从 {input_df['date'].min().strftime('%Y-%m-%d')} 到 {input_df['date'].max().strftime('%Y-%m-%d')}.")
    print(f"资产数量: {input_df['asset_id'].nunique()}.")
    print(f"数据列: {input_df.columns.tolist()}")

    # Check for 'high' column specifically, as it's crucial and not always in mock data
    if 'high' not in input_df.columns:
        print(f"错误: 必需的 'high' 列在 {DATA_FILE_PATH} 中缺失。Alpha#16 无法计算。")
        print("请确保您的 mock_data.csv 包含 'high' 列，或修改 data/generate_mock_data.py 以生成此列。")
        exit(1)
    if 'volume' not in input_df.columns: # Also check volume, though it's usually present
        print(f"错误: 必需的 'volume' 列在 {DATA_FILE_PATH} 中缺失。Alpha#16 无法计算。")
        exit(1)

    print("开始计算 Alpha#16...")
    try:
        alpha_df = calculate_alpha16(input_df.copy())
    except ValueError as ve:
        print(ve) # Print the specific ValueError from calculate_alpha16
        exit(1)
    except Exception as e:
        print(f"计算 Alpha#16 时发生意外错误: {e}")
        exit(1)

    # Prepare a copy for saving with specific formatting
    save_df = alpha_df.copy()

    # Format alpha16 to two significant figures
    if 'alpha16' in save_df.columns:
        save_df['alpha16_formatted'] = save_df['alpha16'].apply(format_float_to_2_sig_figs)
        # Overwrite original alpha16 col for saving, or keep original and save formatted as new
        # For consistency with request "新alpha保留两位有效数字", we will save the formatted one.
        save_df['alpha16'] = save_df['alpha16_formatted']
        save_df = save_df.drop(columns=['alpha16_formatted'])

    # Define formatters for other columns for CSV output
    csv_formatters = {}
    float_cols_to_format = ['rank_high', 'rank_volume', 'rank_cov']
    for col in float_cols_to_format:
        if col in save_df.columns:
            csv_formatters[col] = lambda x: f"{x:.4f}" if pd.notnull(x) else ''
    
    if 'cov_rank_high_rank_volume_5' in save_df.columns:
        csv_formatters['cov_rank_high_rank_volume_5'] = lambda x: f"{x:.6f}" if pd.notnull(x) else ''

    # Original data formatting
    original_numeric_cols = ['open', 'high', 'low', 'close', 'returns', 'volume']
    for col in original_numeric_cols:
        if col in save_df.columns:
            if col == 'volume': # Volume typically integer
                csv_formatters[col] = lambda x, c=col: f"{x:.0f}" if pd.notnull(x) else ''
            elif col == 'returns':
                 csv_formatters[col] = lambda x, c=col: f"{x:.4f}" if pd.notnull(x) else '' # returns often needs more precision
            else: # open, high, low, close
                 csv_formatters[col] = lambda x, c=col: f"{x:.2f}" if pd.notnull(x) else ''
    
    # Apply formatters by converting columns to string before to_csv
    # This gives more control over NaN representation (empty string)
    for col_name, formatter in csv_formatters.items():
        if col_name in save_df.columns:
            save_df[col_name] = save_df[col_name].apply(formatter)
    
    # For alpha16, it's already string formatted by format_float_to_2_sig_figs
    # Ensure NaN in alpha16 becomes empty string if not already handled
    if 'alpha16' in save_df.columns:
        save_df['alpha16'] = save_df['alpha16'].apply(lambda x: '' if pd.isna(x) or x is None else x)

    save_df.to_csv(OUTPUT_FILE_PATH, index=False, na_rep='') # Save NaN as empty string
    print(f"Alpha#16 计算完成，结果已保存到 {OUTPUT_FILE_PATH}")

    print("Alpha#16 结果预览 (alpha16 列为CSV中的格式):")
    num_assets_to_display = min(2, alpha_df['asset_id'].nunique())
    rows_per_asset_display = 5
    asset_ids = alpha_df['asset_id'].unique()

    # Display columns for console output, use original alpha16 for stats, but formatted for display
    console_display_columns = [
        'date', 'asset_id', 'high', 'volume', 
        'rank_high', 'rank_volume', 
        'cov_rank_high_rank_volume_5', 'alpha16' # Show the formatted alpha16 for preview
    ]
    # Ensure all requested display columns are actually in save_df
    console_display_columns = [col for col in console_display_columns if col in save_df.columns]

    if len(asset_ids) > 0:
        selected_assets = asset_ids[:num_assets_to_display]
        for i, asset_id_val in enumerate(selected_assets):
            # Use save_df for previewing CSV-like output
            asset_data_display = save_df[save_df['asset_id'] == asset_id_val]
            print(f"资产ID: {asset_id_val}")
            
            # For console display, we can re-apply a simpler to_string formatting
            # or use the already string-formatted save_df
            print(f"前 {rows_per_asset_display} 行数据:")
            print(asset_data_display.head(rows_per_asset_display)[console_display_columns].to_string(index=False))
            if len(asset_data_display) > rows_per_asset_display:
                print(f"后 {rows_per_asset_display} 行数据 ({asset_id_val}):")
                print(asset_data_display.tail(rows_per_asset_display)[console_display_columns].to_string(index=False))
            if i < len(selected_assets) - 1:
                print("-" * 70)
    else:
        print("没有可供预览的资产数据。")

    print("Alpha#16 列统计信息 (原始 alpha16 值, 不含 NaN):")
    # For statistics, use the original, unformatted alpha_df['alpha16']
    if 'alpha16' in alpha_df.columns and not alpha_df['alpha16'].dropna().empty:
        with pd.option_context('display.float_format', '{:.4f}'.format): # Stats with more precision
            print(alpha_df['alpha16'].dropna().describe())
        nan_alpha_counts = alpha_df['alpha16'].isna().sum()
        total_counts = len(alpha_df['alpha16'])
        print(f"Alpha#16 列中 NaN 值数量: {nan_alpha_counts} (总计 {total_counts} 行)")
        print("(NaN 值预期由初始计算窗口期和协方差/排名计算时组内数量不足导致)")
    else:
        print("Alpha#16 列不包含有效数据进行统计。")

    print("脚本执行完毕。") 