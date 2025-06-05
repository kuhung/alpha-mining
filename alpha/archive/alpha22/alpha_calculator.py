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

def calculate_alpha22(df):
    required_cols = ['high', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"数据缺少必要列: {col}")
    df = df.sort_values(['asset_id', 'date']).copy()
    # 5日相关性
    def rolling_corr(x):
        return x['high'].rolling(5, min_periods=5).corr(x['volume'])
    df['corr_high_vol_5'] = df.groupby('asset_id', group_keys=False).apply(rolling_corr).reset_index(level=0, drop=True)
    # 5日delta
    df['delta_corr_5'] = df.groupby('asset_id')['corr_high_vol_5'].diff(5)
    # 20日收盘价波动率
    df['stddev_close_20'] = df.groupby('asset_id')['close'].transform(lambda x: x.rolling(20, min_periods=20).std())
    # 截面排名
    df = df.sort_values(['date', 'asset_id'])
    df['rank_stddev_close_20'] = df.groupby('date')['stddev_close_20'].rank(method='average', pct=True)
    # 公式实现
    df['alpha22'] = -1 * (df['delta_corr_5'] * df['rank_stddev_close_20'])
    # 输出列
    base_cols = [col for col in ['date', 'asset_id', 'open', 'high', 'low', 'close', 'volume'] if col in df.columns]
    calc_cols = ['corr_high_vol_5', 'delta_corr_5', 'stddev_close_20', 'rank_stddev_close_20', 'alpha22']
    out_cols = base_cols + [c for c in calc_cols if c not in base_cols]
    df_out = df[out_cols].copy()
    # 保留两位有效数字
    for col in ['corr_high_vol_5', 'delta_corr_5', 'stddev_close_20', 'rank_stddev_close_20', 'alpha22']:
        if col in df_out.columns:
            df_out[col] = df_out[col].apply(format_float_to_2_sig_figs)
    return df_out

if __name__ == "__main__":
    DATA_FILE_PATH = "../../data/mock_data.csv"
    OUTPUT_FILE_PATH = "alpha22_results.csv"
    try:
        print(f"加载数据: {DATA_FILE_PATH}")
        input_df = pd.read_csv(DATA_FILE_PATH, parse_dates=['date'])
        print("数据加载成功。")
    except Exception as e:
        print(f"数据加载失败: {e}")
        exit(1)
    try:
        alpha_df = calculate_alpha22(input_df)
        print("Alpha#22 计算完成。")
    except Exception as e:
        print(f"计算失败: {e}")
        exit(1)
    try:
        alpha_df.to_csv(OUTPUT_FILE_PATH, index=False)
        print(f"结果已保存到 {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"保存失败: {e}")
        exit(1) 