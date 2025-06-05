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

def calculate_alpha19(df, delay_period=7, sum_returns_period=250):
    """
    Calculates Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))
    Assuming delta(close, 7) means close - delay(close, 7).

    Args:
        df (pd.DataFrame): DataFrame with 'date', 'asset_id', 'close', 'returns'.
        delay_period (int): Window for delay and delta (default is 7).
        sum_returns_period (int): Window for sum of returns (default is 250).

    Returns:
        pd.DataFrame: DataFrame with original data and calculated alpha and intermediate steps.
    """
    required_cols = ['close', 'returns']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"错误: 数据文件缺少必需列: '{col}'. Alpha#19 无法计算。")

    df = df.sort_values(by=['asset_id', 'date']).copy()

    # Component 1: Trend signal
    # delay(close, 7)
    df['close_delay_7'] = df.groupby('asset_id', group_keys=False)['close'].transform(
        lambda x: x.shift(delay_period)
    )
    # (close - delay(close, 7))
    df['price_change_7d'] = df['close'] - df['close_delay_7']
    
    # delta(close, 7) is assumed to be price_change_7d
    # So, ((close - delay(close, 7)) + delta(close, 7)) = 2 * price_change_7d
    df['double_price_change_7d'] = 2 * df['price_change_7d']
    
    # sign(...)
    df['sign_double_price_change'] = np.sign(df['double_price_change_7d'])
    
    # -1 * sign(...)
    df['trend_signal_component'] = -1 * df['sign_double_price_change']

    # Component 2: Long-term return rank factor
    # sum(returns, 250)
    df['sum_returns_250'] = df.groupby('asset_id', group_keys=False)['returns'].transform(
        lambda x: x.rolling(window=sum_returns_period, min_periods=sum_returns_period).sum()
    )
    
    df['one_plus_sum_returns'] = 1 + df['sum_returns_250']
    
    # rank(1 + sum(returns, 250)) - cross-sectional rank
    df = df.sort_values(by=['date', 'asset_id']) # Sort for cross-sectional rank
    df['rank_sum_returns'] = df.groupby('date')['one_plus_sum_returns'].rank(method='average', pct=True)
    
    # (1 + rank(...))
    df['return_rank_factor'] = 1 + df['rank_sum_returns']

    # Final Alpha#19
    df['alpha19'] = df['trend_signal_component'] * df['return_rank_factor']

    # Define columns for output
    base_cols_present = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume', 'returns'] if col in df.columns]
    intermediate_cols = [
        'close_delay_7', 'price_change_7d', 'double_price_change_7d', 'sign_double_price_change', 'trend_signal_component',
        'sum_returns_250', 'one_plus_sum_returns', 'rank_sum_returns', 'return_rank_factor'
    ]
    alpha_final_col = ['alpha19']
    
    output_columns = base_cols_present + [col for col in intermediate_cols if col not in base_cols_present] + alpha_final_col
    output_columns = [col for i, col in enumerate(output_columns) if col not in output_columns[:i]]

    df_output = df[output_columns].copy()

    # Round intermediate financial calculations for display consistency if needed
    cols_to_round_display = ['close_delay_7', 'price_change_7d', 'double_price_change_7d',
                               'sum_returns_250', 'one_plus_sum_returns', 'rank_sum_returns', 'return_rank_factor']
    for col in cols_to_round_display:
        if col in df_output.columns:
            df_output[col] = df_output[col].round(6)

    return df_output

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha19_results.csv"
    DELAY_PERIOD = 7
    SUM_RETURNS_PERIOD = 250
    NUM_ASSETS_TO_DISPLAY = 1 # Display one asset to trace NaNs better
    ROWS_TO_DISPLAY_INITIAL = SUM_RETURNS_PERIOD + DELAY_PERIOD + 5 # Enough to see first non-NaNs

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
    if 'close' not in input_df.columns or 'returns' not in input_df.columns:
        print(f"错误: {DATA_FILE_PATH} 中缺少 'close' 或 'returns' 列。Alpha#19 无法计算。")
        exit(1)
    
    print(f"开始计算 Alpha#19 (delay_period={DELAY_PERIOD}, sum_returns_period={SUM_RETURNS_PERIOD})...")
    try:
        alpha_df_calculated = calculate_alpha19(input_df.copy(), delay_period=DELAY_PERIOD, sum_returns_period=SUM_RETURNS_PERIOD)
        print("Alpha#19 计算完成。")
    except ValueError as ve:
        print(f"Alpha 计算过程中发生错误: {ve}")
        exit(1)
    except Exception as e:
        print(f"Alpha 计算过程中发生意外错误: {e}")
        exit(1)

    save_df = alpha_df_calculated.copy()
    if 'alpha19' in save_df.columns:
        save_df['alpha19_formatted'] = save_df['alpha19'].apply(format_float_to_2_sig_figs)
        save_df['alpha19'] = save_df['alpha19_formatted']
        save_df = save_df.drop(columns=['alpha19_formatted'])

    csv_formatters = {}
    original_data_cols = ['open', 'high', 'low', 'close', 'volume', 'returns']
    intermediate_output_cols = [
        'close_delay_7', 'price_change_7d', 'double_price_change_7d', 'sign_double_price_change', 'trend_signal_component',
        'sum_returns_250', 'one_plus_sum_returns', 'rank_sum_returns', 'return_rank_factor'
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
            
    if 'alpha19' in save_df.columns:
         save_df['alpha19'] = save_df['alpha19'].apply(lambda x: '' if (pd.isna(x) or x is None or str(x).lower()=='nan') else x)

    try:
        save_df.to_csv(OUTPUT_FILE_PATH, index=False, na_rep='')
        print(f"Alpha#19 结果已保存到 {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"保存结果到 CSV 时出错: {e}")
        exit(1)

    print("\n--- Alpha#19 结果样本 (控制台预览使用原始计算精度) ---")
    if not alpha_df_calculated.empty:
        asset_ids = alpha_df_calculated['asset_id'].unique()
        if len(asset_ids) >= NUM_ASSETS_TO_DISPLAY:
            selected_assets = asset_ids[:NUM_ASSETS_TO_DISPLAY]
        else:
            selected_assets = asset_ids
        
        cols_for_console_preview = [col for col in alpha_df_calculated.columns if col in ['date', 'asset_id', 'close', 'returns', 'price_change_7d', 'trend_signal_component', 'sum_returns_250', 'rank_sum_returns', 'return_rank_factor', 'alpha19']]
        alpha_df_preview = alpha_df_calculated[cols_for_console_preview].copy()
        
        for col_preview in alpha_df_preview.columns:
            if alpha_df_preview[col_preview].dtype == 'float64':
                alpha_df_preview[col_preview] = alpha_df_preview[col_preview].round(4)

        for i, asset_id in enumerate(selected_assets):
            asset_data = alpha_df_preview[alpha_df_preview['asset_id'] == asset_id]
            print(f"\n资产 ID: {asset_id}")
            print(f"前 {ROWS_TO_DISPLAY_INITIAL} 行数据:") 
            print(asset_data.head(ROWS_TO_DISPLAY_INITIAL).to_string(index=False))
            if i < len(selected_assets) - 1:
                print("-" * 90)        
        
        print("\n--- 总体信息 ---")
        print(f"结果总行数: {len(alpha_df_calculated)}")
        print(f"独立资产数量: {alpha_df_calculated['asset_id'].nunique()}")
        
        nan_info_cols = ['close_delay_7', 'price_change_7d', 'sum_returns_250', 'rank_sum_returns', 'alpha19']
        for col in nan_info_cols:
            if col in alpha_df_calculated.columns:
                nan_counts = alpha_df_calculated[col].isna().sum()
                print(f"列 '{col}' 中的 NaN 值数量: {nan_counts}")

        if 'alpha19' in alpha_df_calculated.columns and len(alpha_df_calculated['alpha19'].dropna()) > 0:
            print("\nAlpha19 列统计信息 (不含 NaN):")
            with pd.option_context('display.float_format', '{:.4f}'.format):
                 print(alpha_df_calculated['alpha19'].dropna().describe())
        elif 'alpha19' in alpha_df_calculated.columns:
            print("\nAlpha19 列不包含有效数据 (可能全部为 NaN)。")
    else:
        print("结果 DataFrame 为空。")

    print("\n脚本执行完毕。") 