import pandas as pd
import numpy as np

def format_float_to_2_sig_figs(val):
    if pd.isna(val):
        return ""
    if val == 0:
        return "0.00"
    try:
        float_val = float(val)
        return f"{float_val:.2g}"
    except (ValueError, TypeError):
        return str(val)

def calculate_alpha21(df):
    required_cols = ['close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"数据缺少必要列: {col}")
    df = df.sort_values(['asset_id', 'date']).copy()
    # 8日均价
    df['close_mean_8'] = df.groupby('asset_id')['close'].transform(lambda x: x.rolling(8, min_periods=8).mean())
    # 8日波动率
    df['close_std_8'] = df.groupby('asset_id')['close'].transform(lambda x: x.rolling(8, min_periods=8).std())
    # 2日均价
    df['close_mean_2'] = df.groupby('asset_id')['close'].transform(lambda x: x.rolling(2, min_periods=2).mean())
    # 20日均量
    df['adv20'] = df.groupby('asset_id')['volume'].transform(lambda x: x.rolling(20, min_periods=20).mean())
    # volume/adv20
    df['volume_over_adv20'] = df['volume'] / df['adv20']
    # 条件判断
    df['cond1'] = (df['close_mean_8'] + df['close_std_8']) < df['close_mean_2']
    df['cond2'] = df['close_mean_2'] < (df['close_mean_8'] - df['close_std_8'])
    df['cond3'] = (df['volume_over_adv20'] > 1) | (np.isclose(df['volume_over_adv20'], 1))
    # 公式实现
    df['alpha21'] = np.where(df['cond1'], -1,
                        np.where(df['cond2'], 1,
                            np.where(df['cond3'], 1, -1)))
    # 输出列
    base_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume'] if col in df.columns]
    calc_cols = ['close_mean_8', 'close_std_8', 'close_mean_2', 'adv20', 'volume_over_adv20', 'cond1', 'cond2', 'cond3', 'alpha21']
    out_cols = base_cols + [c for c in calc_cols if c not in base_cols]
    df_out = df[out_cols].copy()
    # 保留两位有效数字
    for col in ['close_mean_8', 'close_std_8', 'close_mean_2', 'adv20', 'volume_over_adv20', 'alpha21']:
        if col in df_out.columns:
            df_out[col] = df_out[col].apply(format_float_to_2_sig_figs)
    return df_out

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha21_results.csv"
    try:
        print(f"加载数据: {DATA_FILE_PATH}")
        input_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['date'])
        print("数据加载成功。")
    except Exception as e:
        print(f"数据加载失败: {e}")
        exit(1)
    try:
        alpha_df = calculate_alpha21(input_df)
        print("Alpha#21 计算完成。")
    except Exception as e:
        print(f"计算失败: {e}")
        exit(1)
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False)
        print(f"结果已保存到 {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"保存失败: {e}")
        exit(1) 