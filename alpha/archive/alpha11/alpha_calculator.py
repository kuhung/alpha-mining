import pandas as pd

# 读取数据
def load_data():
    data_path = '../../data/mock_data.csv'
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    # 确保数据包含所有需要的列
    required_columns = ['date', 'asset_id', 'close', 'vwap', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"错误：输入数据缺少必要列: {col}")
    return df

# 计算Alpha#11
def calculate_alpha11(df):
    # 确保数据按 asset_id 和 date 排序
    df = df.sort_values(by=['asset_id', 'date']).reset_index(drop=True)

    # 计算 vwap - close
    df['vwap_close_diff'] = (df['vwap'] - df['close']).round(4) # 保留更多小数位以提高中间计算精度

    # 按 asset_id 分组计算时间序列相关的指标
    # ts_max((vwap - close), 3)
    df['ts_max_diff_3'] = df.groupby('asset_id')['vwap_close_diff'].rolling(window=3, min_periods=3).max().reset_index(level=0, drop=True).round(4)
    
    # ts_min((vwap - close), 3)
    df['ts_min_diff_3'] = df.groupby('asset_id')['vwap_close_diff'].rolling(window=3, min_periods=3).min().reset_index(level=0, drop=True).round(4)
    
    # delta(volume, 3)
    df['delta_volume_3'] = df.groupby('asset_id')['volume'].transform(lambda x: x.diff(3)).round(4)

    # 按 date 分组进行截面排名 (pct=True 将排名转换为百分比形式 0-1)
    df['rank_ts_max_diff_3'] = df.groupby('date')['ts_max_diff_3'].rank(method='average', ascending=True, pct=True, na_option='keep')
    df['rank_ts_min_diff_3'] = df.groupby('date')['ts_min_diff_3'].rank(method='average', ascending=True, pct=True, na_option='keep')
    df['rank_delta_volume_3'] = df.groupby('date')['delta_volume_3'].rank(method='average', ascending=True, pct=True, na_option='keep')
    
    # 计算 Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))
    df['alpha11'] = ((df['rank_ts_max_diff_3'] + df['rank_ts_min_diff_3']) * df['rank_delta_volume_3']).round(2)
    
    # 选择输出列，包含原始数据和最终alpha值以及关键中间值
    output_columns = [
        'date', 'asset_id', 'close', 'vwap', 'volume', 
        'vwap_close_diff', 'ts_max_diff_3', 'ts_min_diff_3', 'delta_volume_3',
        'rank_ts_max_diff_3', 'rank_ts_min_diff_3', 'rank_delta_volume_3',
        'alpha11'
    ]
    return df[output_columns]

# 保存结果
def save_results(df):
    output_path = 'alpha11_results.csv'
    df.to_csv(output_path, index=False, float_format='%.2f') # 确保alpha11和其他浮点数按需格式化
    print(f"结果已保存到 {output_path}")

# 主函数
def main():
    # 加载数据
    df = load_data()
    
    # 计算Alpha#11
    df_alpha = calculate_alpha11(df)
    
    # 保存结果
    save_results(df_alpha)

if __name__ == "__main__":
    main() 