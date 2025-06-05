import pandas as pd
import numpy as np

def format_float_to_2_sig_figs(val):
    """Formats a float to two significant figures, handling NaN and 0."""
    if pd.isna(val):
        return ""  # Keep NaN as empty string for CSV
    if val == 0:
        return "0.00"
    try:
        # Attempt to format, ensuring it's a float first
        float_val = float(val)
        return f"{float_val:.2g}"
    except (ValueError, TypeError):
        return str(val) # Return original if not formattable as float

def calculate_alpha18(df, stddev_window=5, corr_window=10):
    """
    Calculates Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))

    Args:
        df (pd.DataFrame): DataFrame with 'date', 'asset_id', 'open', 'close'.
                           It's assumed that the DataFrame is sorted by 'asset_id' and 'date'.
        stddev_window (int): Rolling window for stddev calculation (default is 5).
        corr_window (int): Rolling window for correlation calculation (default is 10).

    Returns:
        pd.DataFrame: DataFrame with original data and calculated alpha and intermediate steps.
    """
    required_cols = ['open', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"错误: 数据文件缺少必需列: '{col}'. Alpha#18 无法计算。")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Step 1: abs((close - open))
    df['abs_close_minus_open'] = (df['close'] - df['open']).abs()

    # Step 2: stddev(abs((close - open)), 5)
    df['stddev_abs_co_5'] = df.groupby('asset_id', group_keys=False)['abs_close_minus_open']\
                               .transform(lambda x: x.rolling(window=stddev_window, min_periods=stddev_window).std())

    # Step 3: (close - open)
    df['co_diff'] = df['close'] - df['open']

    # Step 4: correlation(close, open, 10)
    # Pandas rolling.corr() calculates correlation between two Series within a group.
    def rolling_corr(data_group):
        return data_group['close'].rolling(window=corr_window, min_periods=corr_window).corr(data_group['open'])

    df['corr_close_open_10'] = df.groupby('asset_id', group_keys=False).apply(rolling_corr)

    # Step 5: Combined value: (stddev_abs_co_5 + co_diff + corr_close_open_10)
    df['combined_value'] = df['stddev_abs_co_5'] + df['co_diff'] + df['corr_close_open_10']

    # Ensure data is sorted by date, asset_id for cross-sectional rank
    df = df.sort_values(by=['date', 'asset_id'])

    # Step 6: rank(combined_value)
    df['rank_combined_value'] = df.groupby('date')['combined_value'].rank(method='average', pct=True)

    # Step 7: Final Alpha#18
    df['alpha18'] = -1 * df['rank_combined_value']

    # Define columns to keep in the final output
    base_cols_present = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'returns'] if col in df.columns]
    alpha_intermediate_cols = ['abs_close_minus_open', 'stddev_abs_co_5', 'co_diff', 'corr_close_open_10', 'combined_value', 'rank_combined_value']
    alpha_final_col = ['alpha18']
    
    output_columns = base_cols_present + [col for col in alpha_intermediate_cols if col not in base_cols_present] + alpha_final_col
    output_columns = [col for i, col in enumerate(output_columns) if col not in output_columns[:i]] # Preserve order, remove duplicates
    
    df_output = df[output_columns].copy() # Create a copy for formatting

    # Round intermediate financial calculations to a reasonable precision for display if needed, e.g., 4-6 decimal places
    # Alpha value itself will be formatted to 2 significant figures before saving CSV.
    cols_to_round_display = ['abs_close_minus_open', 'stddev_abs_co_5', 'co_diff', 'corr_close_open_10', 'combined_value', 'rank_combined_value']
    for col in cols_to_round_display:
        if col in df_output.columns:
            df_output[col] = df_output[col].round(6) 
            
    return df_output

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha18_results.csv"
    STDDEV_WINDOW = 5
    CORR_WINDOW = 10
    NUM_ASSETS_TO_DISPLAY = 2
    ROWS_PER_ASSET_DISPLAY = 10 # Display more to see window effects

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
    if 'open' not in input_df.columns or 'close' not in input_df.columns:
        print(f"错误: {DATA_FILE_PATH} 中缺少 'open' 或 'close' 列。Alpha#18 无法计算。")
        exit(1)
    
    print(f"开始计算 Alpha#18 (stddev_window={STDDEV_WINDOW}, corr_window={CORR_WINDOW})...")
    try:
        alpha_df_calculated = calculate_alpha18(input_df.copy(), stddev_window=STDDEV_WINDOW, corr_window=CORR_WINDOW)
        print("Alpha#18 计算完成。")
    except ValueError as ve:
        print(f"Alpha 计算过程中发生错误: {ve}")
        exit(1)
    except Exception as e:
        print(f"Alpha 计算过程中发生意外错误: {e}")
        exit(1)

    # Prepare a copy for saving with specific formatting for alpha18
    save_df = alpha_df_calculated.copy()
    if 'alpha18' in save_df.columns:
        save_df['alpha18_formatted'] = save_df['alpha18'].apply(format_float_to_2_sig_figs)
        save_df['alpha18'] = save_df['alpha18_formatted'] # Overwrite with formatted string
        save_df = save_df.drop(columns=['alpha18_formatted'])
    
    # Formatting other numeric columns for CSV output (e.g., 4-6 decimal places or original if already suitable)
    csv_formatters = {}
    original_data_cols = ['open', 'high', 'low', 'close', 'volume', 'returns']
    intermediate_cols = ['abs_close_minus_open', 'stddev_abs_co_5', 'co_diff', 'corr_close_open_10', 'combined_value', 'rank_combined_value']

    for col in save_df.columns:
        if col in original_data_cols:
            if save_df[col].dtype == 'float64':
                if col == 'volume': # Volume typically integer like
                     csv_formatters[col] = lambda x: f"{x:.0f}" if pd.notnull(x) else ''
                elif col == 'returns':
                     csv_formatters[col] = lambda x: f"{x:.4f}" if pd.notnull(x) else ''
                else: # open, high, low, close
                     csv_formatters[col] = lambda x: f"{x:.2f}" if pd.notnull(x) else ''
        elif col in intermediate_cols:
            if save_df[col].dtype == 'float64':
                 csv_formatters[col] = lambda x: f"{x:.6f}" if pd.notnull(x) else ''
        # alpha18 is already string formatted

    # Apply formatters by converting columns to string before to_csv for better NaN handling
    for col_name, formatter_func in csv_formatters.items():
        if col_name in save_df.columns:
            save_df[col_name] = save_df[col_name].apply(formatter_func)
    
    # Ensure NaN in alpha18 becomes empty string (if not already handled by format_float_to_2_sig_figs)
    if 'alpha18' in save_df.columns:
         save_df['alpha18'] = save_df['alpha18'].apply(lambda x: '' if (pd.isna(x) or x is None or str(x).lower()=='nan') else x)

    try:
        save_df.to_csv(OUTPUT_FILE_PATH, index=False, na_rep='') # Save NaN as empty string
        print(f"Alpha#18 结果已保存到 {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"保存结果到 CSV 时出错: {e}")
        exit(1)

    print("\n--- Alpha#18 结果样本 (控制台预览使用原始计算精度) ---")
    if not alpha_df_calculated.empty:
        asset_ids = alpha_df_calculated['asset_id'].unique()
        if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY:
            selected_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY]
        else:
            selected_assets = asset_ids
        
        # For console display, use the unformatted (but rounded for display) alpha_df_calculated
        cols_for_console_preview = [col for col in alpha_df_calculated.columns if col in ['date', 'asset_id', 'open', 'close', 'abs_close_minus_open', 'stddev_abs_co_5', 'co_diff', 'corr_close_open_10', 'combined_value', 'rank_combined_value', 'alpha18']]
        alpha_df_preview = alpha_df_calculated[cols_for_console_preview].copy()
        
        # Round floats in preview for better readability in console
        for col_preview in alpha_df_preview.columns:
            if alpha_df_preview[col_preview].dtype == 'float64':
                alpha_df_preview[col_preview] = alpha_df_preview[col_preview].round(4)

        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df_preview[alpha_df_preview['asset_id'] == asset_id]
            print(f"\n资产 ID: {asset_id}")
            # Display more rows to see the effect of rolling windows
            # Max window is corr_window (10), so need at least 10 + few more rows
            print(f"前 {CORR_WINDOW + ROWS_PER_ASSET_DISPLAY -1} 行数据:") 
            print(asset_data.head(CORR_WINDOW + ROWS_PER_ASSET_DISPLAY -1).to_string(index=False))
            if i < len(selected_assets) - 1:
                print("-" * 90)
        
        print("\n--- 总体信息 ---")
        print(f"结果总行数: {len(alpha_df_calculated)}")
        print(f"独立资产数量: {alpha_df_calculated['asset_id'].nunique()}")
        
        nan_info_cols = ['stddev_abs_co_5', 'corr_close_open_10', 'combined_value', 'rank_combined_value', 'alpha18']
        for col in nan_info_cols:
            if col in alpha_df_calculated.columns:
                nan_counts = alpha_df_calculated[col].isna().sum()
                print(f"列 '{col}' 中的 NaN 值数量: {nan_counts}")

        if 'alpha18' in alpha_df_calculated.columns and len(alpha_df_calculated['alpha18'].dropna()) > 0:
            print("\nAlpha18 列统计信息 (不含 NaN):")
            with pd.option_context('display.float_format', '{:.4f}'.format):
                 print(alpha_df_calculated['alpha18'].dropna().describe())
        elif 'alpha18' in alpha_df_calculated.columns:
            print("\nAlpha18 列不包含有效数据 (可能全部为 NaN)。")
    else:
        print("结果 DataFrame 为空。")

    print("\n脚本执行完毕。") 