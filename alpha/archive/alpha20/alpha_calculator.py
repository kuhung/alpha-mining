import pandas as pd
import numpy as np

def format_float_to_2_sig_figs(val):
    """Formats a float to two significant figures, handling NaN and 0."""
    if pd.isna(val):
        return ""  # Keep NaN as empty string for CSV
    if val == 0:
        return "0.00"
    try:
        float_val = float(val)
        return f"{float_val:.2g}"
    except (ValueError, TypeError):
        return str(val) # Return original if not formattable as float

def calculate_alpha20(df, delay_n=1):
    """
    Calculates Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))

    Args:
        df (pd.DataFrame): DataFrame with 'date', 'asset_id', 'open', 'high', 'low', 'close'.
        delay_n (int): Period for delay function (default is 1 for Alpha#20).

    Returns:
        pd.DataFrame: DataFrame with original data and calculated alpha and intermediate steps.
    """
    required_cols = ['open', 'high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"错误: 数据文件缺少必需列: '{col}'. Alpha#20 无法计算。")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Calculate delayed values for high, close, low
    df['prev_high'] = df.groupby('asset_id', group_keys=False)['high'].transform(lambda x: x.shift(delay_n))
    df['prev_close'] = df.groupby('asset_id', group_keys=False)['close'].transform(lambda x: x.shift(delay_n))
    df['prev_low'] = df.groupby('asset_id', group_keys=False)['low'].transform(lambda x: x.shift(delay_n))

    # Calculate differences: (open - delay(X, 1))
    df['diff_open_prev_high'] = df['open'] - df['prev_high']
    df['diff_open_prev_close'] = df['open'] - df['prev_close']
    df['diff_open_prev_low'] = df['open'] - df['prev_low']

    # Sort for cross-sectional ranking
    df = df.sort_values(by=['date', 'asset_id'])

    # Calculate ranks of these differences cross-sectionally
    df['rank_diff_oph'] = df.groupby('date')['diff_open_prev_high'].rank(method='average', pct=True)
    df['rank_diff_opc'] = df.groupby('date')['diff_open_prev_close'].rank(method='average', pct=True)
    df['rank_diff_opl'] = df.groupby('date')['diff_open_prev_low'].rank(method='average', pct=True)

    # Calculate components for Alpha#20 formula
    comp1 = -1 * df['rank_diff_oph']
    comp2 = df['rank_diff_opc']
    comp3 = df['rank_diff_opl']

    # Final Alpha#20 calculation
    df['alpha20'] = comp1 * comp2 * comp3

    # Define columns for output
    base_cols_present = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'returns'] if col in df.columns]
    intermediate_cols = [
        'prev_high', 'prev_close', 'prev_low',
        'diff_open_prev_high', 'diff_open_prev_close', 'diff_open_prev_low',
        'rank_diff_oph', 'rank_diff_opc', 'rank_diff_opl'
    ]
    alpha_final_col = ['alpha20']
    
    output_columns = base_cols_present + [col for col in intermediate_cols if col not in base_cols_present] + alpha_final_col
    output_columns = [col for i, col in enumerate(output_columns) if col not in output_columns[:i]] # Preserve order, remove duplicates

    df_output = df[output_columns].copy()

    cols_to_round_display = intermediate_cols # Rank columns are already 0-1, diffs can be rounded
    for col in cols_to_round_display:
        if col in df_output.columns and ('prev_' in col or 'diff_' in col): # Only round price diffs and prev prices
             df_output[col] = df_output[col].round(4) # Round to 4 for display of these
        elif col in df_output.columns and 'rank_' in col:
            df_output[col] = df_output[col].round(6) # Ranks can have more precision
            
    return df_output

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha20_results.csv"
    DELAY_N = 1
    NUM_ASSETS_TO_DISPLAY = 2
    ROWS_PER_ASSET_DISPLAY = 5 # Show first few rows where NaNs are expected

    try:
        print(f"从 {DATA_FILE_PATH} 加载数据中...")
        input_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['date'])
        print("数据加载成功。")
    except FileNotFoundError:
        print(f"错误: 数据文件 {DATA_FILE_PATH} 未找到。")
        exit(1)
    except Exception as e:
        print(f"加载数据时出错: {e}")
        exit(1)

    print(f"输入数据包含 {len(input_df)} 行和 {len(input_df.columns)} 列。")
    required_check = ['open', 'high', 'low', 'close']
    if not all(col in input_df.columns for col in required_check):
        missing_cols = [col for col in required_check if col not in input_df.columns]
        print(f"错误: {DATA_FILE_PATH} 中缺少必需列: {missing_cols}。Alpha#20 无法计算。")
        exit(1)
    
    print(f"开始计算 Alpha#20 (delay_n={DELAY_N})...")
    try:
        alpha_df_calculated = calculate_alpha20(input_df.copy(), delay_n=DELAY_N)
        print("Alpha#20 计算完成。")
    except ValueError as ve:
        print(f"Alpha 计算过程中发生错误: {ve}")
        exit(1)
    except Exception as e:
        print(f"Alpha 计算过程中发生意外错误: {e}")
        exit(1)

    save_df = alpha_df_calculated.copy()
    if 'alpha20' in save_df.columns:
        save_df['alpha20_formatted'] = save_df['alpha20'].apply(format_float_to_2_sig_figs)
        save_df['alpha20'] = save_df['alpha20_formatted']
        save_df = save_df.drop(columns=['alpha20_formatted'])
    
    csv_formatters = {}
    original_data_cols = ['open', 'high', 'low', 'close', 'volume', 'returns']
    intermediate_output_cols = [
        'prev_high', 'prev_close', 'prev_low',
        'diff_open_prev_high', 'diff_open_prev_close', 'diff_open_prev_low',
        'rank_diff_oph', 'rank_diff_opc', 'rank_diff_opl'
    ]

    for col in save_df.columns:
        if col in original_data_cols:
            if save_df[col].dtype == 'float64' or save_df[col].dtype == 'int64':
                if col == 'volume': 
                     csv_formatters[col] = lambda x: f"{x:.0f}" if pd.notnull(x) else ''
                elif col == 'returns':
                     csv_formatters[col] = lambda x: f"{x:.4f}" if pd.notnull(x) else ''
                else: 
                     csv_formatters[col] = lambda x: f"{x:.2f}" if pd.notnull(x) else ''
        elif col in intermediate_output_cols:
            if save_df[col].dtype == 'float64' or save_df[col].dtype == 'int64':
                 csv_formatters[col] = lambda x: f"{x:.6f}" if pd.notnull(x) else ''

    for col_name, formatter_func in csv_formatters.items():
        if col_name in save_df.columns:
            save_df[col_name] = save_df[col_name].apply(formatter_func)

    if 'alpha20' in save_df.columns:
         save_df['alpha20'] = save_df['alpha20'].apply(lambda x: '' if (pd.isna(x) or x is None or str(x).lower()=='nan') else x)

    try:
        save_df.to_csv(OUTPUT_FILE_PATH, index=False, na_rep='')
        print(f"Alpha#20 结果已保存到 {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"保存结果到 CSV 时出错: {e}")
        exit(1)

    print("\n--- Alpha#20 结果样本 (控制台预览使用原始计算精度) ---")
    if not alpha_df_calculated.empty:
        asset_ids = alpha_df_calculated['asset_id'].unique()
        preview_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY] if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY else asset_ids
        
        cols_for_console_preview = [col for col in alpha_df_calculated.columns if col in ['date', 'asset_id', 'open', 'prev_high', 'prev_close', 'prev_low', 'diff_open_prev_high', 'diff_open_prev_close', 'diff_open_prev_low', 'rank_diff_oph', 'rank_diff_opc', 'rank_diff_opl', 'alpha20']]
        alpha_df_preview = alpha_df_calculated[cols_for_console_preview].copy()

        for col_preview in alpha_df_preview.columns:
            if alpha_df_preview[col_preview].dtype == 'float64':
                alpha_df_preview[col_preview] = alpha_df_preview[col_preview].round(4)

        for i, asset_id_val in enumerate(preview_assets):
            asset_data_preview = alpha_df_preview[alpha_df_preview['asset_id'] == asset_id_val]
            print(f"\n资产 ID: {asset_id_val}")
            print(f"前 {ROWS_PER_ASSET_DISPLAY + DELAY_N} 行数据:") 
            print(asset_data_preview.head(ROWS_PER_ASSET_DISPLAY + DELAY_N).to_string(index=False))
            if i < len(preview_assets) - 1:
                print("-" * 100)
        
        print("\n--- 总体信息 ---")
        print(f"结果总行数: {len(alpha_df_calculated)}")
        print(f"独立资产数量: {alpha_df_calculated['asset_id'].nunique()}")
        
        nan_info_cols = ['prev_high', 'diff_open_prev_high', 'rank_diff_oph', 'alpha20']
        for col in nan_info_cols:
            if col in alpha_df_calculated.columns:
                nan_counts = alpha_df_calculated[col].isna().sum()
                print(f"列 '{col}' 中的 NaN 值数量: {nan_counts}")

        if 'alpha20' in alpha_df_calculated.columns and len(alpha_df_calculated['alpha20'].dropna()) > 0:
            print("\nAlpha20 列统计信息 (不含 NaN):")
            with pd.option_context('display.float_format', '{:.4f}'.format):
                 print(alpha_df_calculated['alpha20'].dropna().describe())
        elif 'alpha20' in alpha_df_calculated.columns:
            print("\nAlpha20 列不包含有效数据 (可能全部为 NaN)。")
    else:
        print("结果 DataFrame 为空。")

    print("\n脚本执行完毕。") 