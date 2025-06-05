import pandas as pd
import numpy as np
from pathlib import Path

def calculate_alpha24(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算 Alpha#24:
    ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) ||
    ((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ?
    (-1 * (close - ts_min(close, 100))) : (-1 * delta(close, 3)))
    
    参数:
        df (pd.DataFrame): 包含必要数据的DataFrame，需要包含 'close' 列
        
    返回:
        pd.DataFrame: 包含原始数据和计算得到的Alpha#24值的DataFrame
    """
    # 按资产分组进行计算
    result_df = df.copy()
    
    # 对每个资产进行分组计算
    for asset_id in result_df['asset_id'].unique():
        asset_data = result_df[result_df['asset_id'] == asset_id].copy()
        
        # 计算100日移动平均
        ma_100 = asset_data['close'].rolling(window=100, min_periods=100).mean()
        
        # 计算移动平均的100日差分
        delta_ma_100 = ma_100 - ma_100.shift(100)
        
        # 计算100日前的收盘价
        delay_close_100 = asset_data['close'].shift(100)
        
        # 计算变化率
        change_rate = delta_ma_100 / delay_close_100
        
        # 计算100日最小值
        min_close_100 = asset_data['close'].rolling(window=100, min_periods=100).min()
        
        # 计算当前价格与最小值的差
        price_min_diff = asset_data['close'] - min_close_100
        
        # 计算3日价格差分
        delta_close_3 = asset_data['close'] - asset_data['close'].shift(3)
        
        # 根据条件计算Alpha#24
        alpha24 = np.where(
            (change_rate <= 0.05),
            -1 * price_min_diff,
            -1 * delta_close_3
        )
        
        # 更新结果DataFrame
        result_df.loc[result_df['asset_id'] == asset_id, 'ma_100'] = ma_100
        result_df.loc[result_df['asset_id'] == asset_id, 'delta_ma_100'] = delta_ma_100
        result_df.loc[result_df['asset_id'] == asset_id, 'change_rate'] = change_rate
        result_df.loc[result_df['asset_id'] == asset_id, 'min_close_100'] = min_close_100
        result_df.loc[result_df['asset_id'] == asset_id, 'delta_close_3'] = delta_close_3
        result_df.loc[result_df['asset_id'] == asset_id, 'alpha24'] = alpha24
    
    # 保留两位有效数字
    result_df['alpha24'] = result_df['alpha24'].round(2)
    
    return result_df

def main():
    # 读取数据
    data_path = Path('../../data/mock_data.csv')
    df = pd.read_csv(data_path)
    
    # 确保数据按日期和资产ID排序
    df = df.sort_values(['date', 'asset_id'])
    
    # 计算Alpha#24
    result_df = calculate_alpha24(df)
    
    # 保存结果
    output_path = Path('./alpha24_results.csv')
    result_df.to_csv(output_path, index=False)
    
    # 打印部分结果和统计信息
    print("\nAlpha#24 计算完成！")
    print("\n前5行结果:")
    print(result_df[['date', 'asset_id', 'close', 'change_rate', 'min_close_100', 'delta_close_3', 'alpha24']].head())
    print("\n后5行结果:")
    print(result_df[['date', 'asset_id', 'close', 'change_rate', 'min_close_100', 'delta_close_3', 'alpha24']].tail())
    print("\nAlpha#24统计信息:")
    print(result_df['alpha24'].describe())

if __name__ == '__main__':
    main() 