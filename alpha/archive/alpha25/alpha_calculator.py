import pandas as pd
import numpy as np
from pathlib import Path

def calculate_alpha25(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算 Alpha#25: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))
    
    参数:
        df (pd.DataFrame): 包含必要数据的DataFrame，需要包含 returns, volume, vwap, high, close 列
        
    返回:
        pd.DataFrame: 包含原始数据和计算得到的Alpha#25值的DataFrame
    """
    # 按资产分组进行计算
    result_df = df.copy()
    
    # 计算20日平均成交量
    result_df['adv20'] = df.groupby('asset_id')['volume'].transform(
        lambda x: x.rolling(window=20, min_periods=20).mean()
    )
    
    # 计算日内价格差值
    result_df['high_close_diff'] = df['high'] - df['close']
    
    # 计算因子乘积
    result_df['factor'] = ((-1 * df['returns']) * 
                          result_df['adv20'] * 
                          df['vwap'] * 
                          result_df['high_close_diff'])
    
    # 按日期分组计算排名
    result_df['alpha25'] = result_df.groupby('date')['factor'].transform(
        lambda x: x.rank(pct=True)
    )
    
    # 保留两位有效数字
    result_df['alpha25'] = result_df['alpha25'].round(2)
    
    return result_df

def main():
    # 读取数据
    data_path = Path('../../data/mock_data.csv')
    df = pd.read_csv(data_path)
    
    # 确保数据按日期和资产ID排序
    df = df.sort_values(['date', 'asset_id'])
    
    # 如果returns列不存在，计算returns
    if 'returns' not in df.columns:
        df['returns'] = df.groupby('asset_id')['close'].pct_change()
    
    # 计算Alpha#25
    result_df = calculate_alpha25(df)
    
    # 保存结果
    output_path = Path('./alpha25_results.csv')
    result_df.to_csv(output_path, index=False)
    
    # 打印部分结果和统计信息
    print("\nAlpha#25 计算完成！")
    print("\n前5行结果:")
    print(result_df[['date', 'asset_id', 'returns', 'adv20', 'vwap', 'high_close_diff', 'factor', 'alpha25']].head())
    print("\n后5行结果:")
    print(result_df[['date', 'asset_id', 'returns', 'adv20', 'vwap', 'high_close_diff', 'factor', 'alpha25']].tail())
    print("\nAlpha#25统计信息:")
    print(result_df['alpha25'].describe())

if __name__ == '__main__':
    main() 