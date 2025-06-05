import pandas as pd
import numpy as np
from pathlib import Path

def calculate_alpha23(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算 Alpha#23: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)
    
    参数:
        df (pd.DataFrame): 包含必要数据的DataFrame，需要包含 'high' 列
        
    返回:
        pd.DataFrame: 包含原始数据和计算得到的Alpha#23值的DataFrame
    """
    # 按资产分组进行计算
    result_df = df.copy()
    
    # 计算20日高价移动平均
    result_df['high_ma_20'] = df.groupby('asset_id')['high'].transform(
        lambda x: x.rolling(window=20, min_periods=20).mean()
    )
    
    # 计算2日价格差分
    result_df['delta_high_2'] = df.groupby('asset_id')['high'].transform(
        lambda x: x.diff(2)
    )
    
    # 计算Alpha#23
    # 当high > high_ma_20时，返回-1 * delta_high_2；否则返回0
    result_df['alpha23'] = np.where(
        result_df['high'] > result_df['high_ma_20'],
        -1 * result_df['delta_high_2'],
        0
    )
    
    # 保留两位有效数字
    result_df['alpha23'] = result_df['alpha23'].round(2)
    
    return result_df

def main():
    # 读取数据
    data_path = Path('../../data/mock_data.csv')
    df = pd.read_csv(data_path)
    
    # 确保数据按日期和资产ID排序
    df = df.sort_values(['date', 'asset_id'])
    
    # 计算Alpha#23
    result_df = calculate_alpha23(df)
    
    # 保存结果
    output_path = Path('./alpha23_results.csv')
    result_df.to_csv(output_path, index=False)
    
    # 打印部分结果和统计信息
    print("\nAlpha#23 计算完成！")
    print("\n前5行结果:")
    print(result_df[['date', 'asset_id', 'high', 'high_ma_20', 'delta_high_2', 'alpha23']].head())
    print("\n后5行结果:")
    print(result_df[['date', 'asset_id', 'high', 'high_ma_20', 'delta_high_2', 'alpha23']].tail())
    print("\nAlpha#23统计信息:")
    print(result_df['alpha23'].describe())

if __name__ == '__main__':
    main() 